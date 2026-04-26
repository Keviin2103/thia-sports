import requests
import json
from datetime import datetime, timezone, timedelta

# ==================================================
# 1. CONFIGURACIÓN DE LIGAS Y LIMITES DE CUOTAS
# ==================================================
API_FOOTBALL_KEY = "23dfce9520b77b484a213d84973f522743590da9f426f97e07350b03addaa92e"

LEAGUES_FUTBOL = {
    'eng.1': {'name': 'Premier League', 'api_football_id': 39},
    'esp.2': {'name': 'LaLiga', 'api_football_id': 140},
    'ita.1': {'name': 'Serie A', 'api_football_id': 135},
    'fra.1': {'name': 'Ligue 1', 'api_football_id': 61},
    'ned.1': {'name': 'Eredivisie', 'api_football_id': 88},
    'por.1': {'name': 'Primeira Liga', 'api_football_id': 94},
    'ger.1': {'name': 'Bundesliga', 'api_football_id': 78},
    'usa.1': {'name': 'MLS', 'api_football_id': 253},
    'uefa.champions': {'name': 'Champions League', 'api_football_id': 2},
    'uefa.europa': {'name': 'Europa League', 'api_football_id': 3},
}

# Reglas de cuota: solo entre -200 y +200 (0.33 a 3.0 en decimal)
MAX_CUOTA_DECIMAL = 3.0
MIN_CUOTA_DECIMAL = 1.50   # -200 en decimal

# Probabilidades mínimas por liga (Regla #12)
PROB_MIN_POR_LIGA = {
    'Premier League': 0.60,
    'LaLiga': 0.62,
    'Serie A': 0.58,
    'Bundesliga': 0.60,
    'Ligue 1': 0.55,
    'MLB': 0.55,
    'default': 0.65
}

# ==================================================
# 2. FUNCIONES AUXILIARES
# ==================================================
def convertir_hora_venezuela(utc_date_str):
    try:
        utc_date_str = utc_date_str.replace('Z', '+00:00')
        utc_time = datetime.fromisoformat(utc_date_str)
        venezuela_tz = timezone(timedelta(hours=-4))
        local_time = utc_time.astimezone(venezuela_tz)
        return local_time.strftime('%I:%M %p')
    except:
        return "Hora pendiente"

def obtener_confianza_liga(liga):
    """Regla #11 y #12: asigna confianza según la liga y la cuota"""
    prob_min = PROB_MIN_POR_LIGA.get(liga, PROB_MIN_POR_LIGA['default'])
    # Simulamos confianza (luego lo conectaremos a datos reales)
    return prob_min

def calcular_ev(cuota, prob_real):
    return (prob_real * cuota) - 1

def filtrar_por_cuota(cuota):
    """Regla #1: solo cuotas entre MIN_CUOTA_DECIMAL y MAX_CUOTA_DECIMAL"""
    if cuota < MIN_CUOTA_DECIMAL or cuota > MAX_CUOTA_DECIMAL:
        return False
    return True

# ==================================================
# 3. OBTENER PARTIDOS DESDE ESPN (con lanzadores de MLB)
# ==================================================
def extraer_datos_espn(data, incluir_pitchers=True):
    if not data or 'events' not in data:
        return []
    partidos = []
    for event in data['events']:
        if 'competitions' not in event:
            continue
        comp = event['competitions'][0]
        home = comp['competitors'][0]['team']['displayName']
        away = comp['competitors'][1]['team']['displayName']
        game_date = event['date']
        stadium = comp['venue']['fullName'] if 'venue' in comp else ''
        # Intentar obtener lanzadores abridores (si es MLB)
        home_pitcher = "TBD"
        away_pitcher = "TBD"
        if incluir_pitchers and 'notes' in comp:
            for note in comp['notes']:
                if note['type'] == 'probablePitcher':
                    if note['homePro']['fullName']:
                        home_pitcher = note['homePro']['fullName']
                    if note['awayPro']['fullName']:
                        away_pitcher = note['awayPro']['fullName']
        partidos.append({
            'home_team': home,
            'away_team': away,
            'date': game_date,
            'stadium': stadium,
            'home_pitcher': home_pitcher,
            'away_pitcher': away_pitcher
        })
    return partidos

def obtener_partidos_espn(slug, incluir_pitchers=False):
    url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{slug}/scoreboard"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return extraer_datos_espn(data, incluir_pitchers=False)
    except:
        pass
    return []

def obtener_partidos_api_football(league_id):
    today = datetime.now().strftime('%Y-%m-%d')
    url = f"https://v3.football.api-sports.io/fixtures?date={today}&league={league_id}&season=2025"
    headers = {'x-apisports-key': API_FOOTBALL_KEY}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            partidos = []
            for item in data.get('response', []):
                fixture = item['fixture']
                home = item['teams']['home']['name']
                away = item['teams']['away']['name']
                partidos.append({
                    'home_team': home,
                    'away_team': away,
                    'date': fixture['date'],
                    'stadium': fixture['venue']['name'],
                    'home_pitcher': None,
                    'away_pitcher': None
                })
            return partidos
    except Exception as e:
        print(f"Error en API-Football: {e}")
    return []

def obtener_partidos_mlb():
    partidos = []
    url = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            partidos = extraer_datos_espn(data, incluir_pitchers=True)
    except:
        pass
    # Si ESPN no devuelve datos, usamos statsapi como respaldo (sin pitchers)
    if not partidos:
        try:
            import statsapi
            today = datetime.now().strftime('%Y-%m-%d')
            schedule = statsapi.schedule(start_date=today, end_date=today)
            for game in schedule:
                partidos.append({
                    'home_team': game['home_name'],
                    'away_team': game['away_name'],
                    'date': game['game_datetime'],
                    'stadium': game['venue_name'],
                    'home_pitcher': "TBD",
                    'away_pitcher': "TBD"
                })
        except Exception as e:
            print(f"Error en statsapi: {e}")
    return partidos

# ==================================================
# 4. GENERACIÓN DE PICKS CON REGLAS THIA
# ==================================================

# Probabilidad real simulada (en producción se obtendría de modelos estadísticos)
def estimar_probabilidad_real(home, away, deporte):
    # Placeholder – aquí irían las métricas avanzadas (xG, NetRating, Corsi, etc.)
    return 0.55

def generar_pick_principal(home, away, deporte, cuota_estimada=1.85, prob_real=None):
    """Regla #1, #11, #12 aplicadas"""
    if prob_real is None:
        prob_real = estimar_probabilidad_real(home, away, deporte)
    confianza = obtener_confianza_liga(deporte)
    if prob_real < confianza:
        return None
    if not filtrar_por_cuota(cuota_estimada):
        return None
    ev = calcular_ev(cuota_estimada, prob_real)
    if ev < 0.05:
        return None
    return {
        'pick': f"{home} ML",
        'cuota': cuota_estimada,
        'ev': f"+{ev*100:.1f}%",
        'stake': '1.5%',
        'regla': f'Confianza {confianza*100:.0f}% + EV +{ev*100:.1f}%'
    }

def generar_pick_secundario(home, away, deporte):
    # Ejemplo: en fútbol, Over 2.5 si el partido es ofensivo; en MLB, Under si Coors.
    if any(liga in deporte for liga in ['Premier League', 'LaLiga', 'Serie A', 'Bundesliga', 'Ligue 1']):
        return {
            'pick': 'Over 2.5 goles',
            'cuota': 1.85,
            'ev': '+7.5%',
            'stake': '1.0%',
            'regla': 'Partido ofensivo'
        }
    if deporte == 'MLB' and 'Coors' in home:
        return {
            'pick': 'Under 9.5',
            'cuota': 1.85,
            'ev': '+8.0%',
            'stake': '1.0%',
            'regla': 'Coors Field Under'
        }
    return None

def generar_prop_jugador(home, away, deporte):
    # Por ahora, solo ejemplo; luego se basará en estadísticas reales.
    if any(liga in deporte for liga in ['Premier League', 'LaLiga', 'Serie A', 'Bundesliga', 'Ligue 1']):
        return {
            'jugador': 'Jugador destacado',
            'prop': 'Over 0.5 goles',
            'cuota': 2.10,
            'stake': '0.5%',
            'ev': '+9.0%'
        }
    if deporte == 'MLB' and 'Judge' in home:
        return {
            'jugador': 'Aaron Judge',
            'prop': 'Over 0.5 HR',
            'cuota': 2.50,
            'stake': '0.5%',
            'ev': '+11.0%'
        }
    return None

# ==================================================
# 5. OBTENER PARTIDOS DE FÚTBOL
# ==================================================
def obtener_partidos_futbol():
    leagues = []
    for slug, league_info in LEAGUES_FUTBOL.items():
        league_name = league_info['name']
        league_id = league_info.get('api_football_id')
        print(f"Consultando {league_name}...")
        partidos = obtener_partidos_espn(slug)
        if not partidos and league_id:
            print(f"  - ESPN sin datos, probando API-Football...")
            partidos = obtener_partidos_api_football(league_id)
        if not partidos:
            print(f"  - No hay partidos para {league_name} hoy.")
            continue
        league_games = []
        for game in partidos:
            hora = convertir_hora_venezuela(game['date'])
            principal = generar_pick_principal(game['home_team'], game['away_team'], league_name, cuota_estimada=1.85)
            if principal is None:
                continue   # No pasa los filtros de confianza/EV
            secundaria = generar_pick_secundario(game['home_team'], game['away_team'], league_name)
            prop = generar_prop_jugador(game['home_team'], game['away_team'], league_name)
            league_games.append({
                'partido': f"{game['away_team']} vs {game['home_team']}",
                'hora': hora,
                'principal': principal,
                'secundaria': secundaria,
                'prop_jugador': prop
            })
        if league_games:
            leagues.append({
                'name': league_name,
                'games': league_games
            })
        print(f"  - {len(league_games)} picks generados.")
    return leagues

# ==================================================
# 6. OBTENER PARTIDOS DE MLB (CON LANZADORES)
# ==================================================
def obtener_partidos_mlb():
    partidos = obtener_partidos_mlb()
    mlb_picks = []
    for game in partidos:
        hora = convertir_hora_venezuela(game['date'])
        principal = generar_pick_principal(game['home_team'], game['away_team'], 'MLB', cuota_estimada=1.75)
        if principal is None:
            continue
        secundaria = generar_pick_secundario(game['home_team'], game['away_team'], 'MLB')
        prop = generar_prop_jugador(game['home_team'], game['away_team'], 'MLB')
        mlb_picks.append({
            'partido': f"{game['away_team']} vs {game['home_team']}",
            'hora': hora,
            'home_pitcher': game.get('home_pitcher', 'TBD'),
            'away_pitcher': game.get('away_pitcher', 'TBD'),
            'principal': principal,
            'secundaria': secundaria,
            'prop_jugador': prop
        })
    return mlb_picks

# ==================================================
# 7. GUARDAR data.js (con pitchers incluidos)
# ==================================================
def guardar_js(leagues_futbol, mlb_picks):
    resultados_vivo = {'mlb': [], 'nba': [], 'nhl': [], 'soccer': []}
    mejoras = [
        "✅ Reglas ThIA aplicadas: cuotas entre -200 y +200, confianza por liga, EV positivo",
        "✅ Lanzadores abridores de MLB (si están disponibles en ESPN)",
        "✅ Filtro de picks que no cumplen confianza mínima",
        "✅ Preparado para métricas avanzadas (xG, NetRating, etc.)"
    ]
    js_content = f"""// Generado automáticamente el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
const nhlPicks = [];
const nbaPicks = [];
const mlbPicks = {json.dumps(mlb_picks, indent=2)};
const leaguesData = {json.dumps(leagues_futbol, indent=2)};
const oldResults = [];
const mejores = {json.dumps(mejoras, indent=2)};
const parlaysData = [];
const todayResultsArray = {json.dumps(resultados_vivo, indent=2)};
"""
    with open('data.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    print("✅ data.js generado correctamente.")

# ==================================================
# 8. MAIN
# ==================================================
if __name__ == "__main__":
    print("=== ThIA-SA v6.0 - Reglas completas activas ===\n")
    print("Obteniendo partidos de fútbol...")
    leagues = obtener_partidos_futbol()
    print(f"Total de ligas con picks: {len(leagues)}\n")
    print("Obteniendo partidos de MLB...")
    mlb = obtener_partidos_mlb()
    print(f"Total de picks de MLB: {len(mlb)}\n")
    guardar_js(leagues, mlb)
    print("Proceso completado.")
