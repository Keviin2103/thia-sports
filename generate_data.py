import requests
import json
from datetime import datetime, timezone, timedelta

# ==================================================
# 1. CONFIGURACIÓN
# ==================================================
# Tu clave de API-Football (ya insertada)
API_FOOTBALL_KEY = "23dfce9520b77b484a213d84973f522743590da9f426f97e07350b03addaa92e"

# Endpoint de MLB (ESPN y respaldo con statsapi)
MLB_URL = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"

# Ligas de fútbol (slugs de ESPN y también IDs para API-Football)
# Para API-Football he mapeado los slugs a los IDs de liga más comunes (puedes ampliarlos)
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

def generar_pick_principal(home_team, away_team, deporte):
    # Aquí es donde meterás después tus reglas ThIA.
    # Por ahora, es solo un ejemplo.
    return {
        'pick': f"{home_team} ML",
        'cuota': 1.85,
        'ev': '+8.5%',
        'stake': '1.5%',
        'regla': 'Valor por defecto (hook para reglas reales)'
    }

def generar_pick_secundario(home_team, away_team, deporte):
    # Igual, luego lo personalizas con tus criterios.
    if any(liga in deporte for liga in ['Premier League', 'LaLiga', 'Serie A', 'Bundesliga', 'Ligue 1']):
        return {
            'pick': 'Over 2.5 goles',
            'cuota': 1.85,
            'ev': '+7.5%',
            'stake': '1.0%',
            'regla': 'Partido ofensivo'
        }
    return None

def generar_prop_jugador(home_team, away_team, deporte):
    # Similar a los picks, lo personalizarás luego.
    if any(liga in deporte for liga in ['Premier League', 'LaLiga', 'Serie A', 'Bundesliga', 'Ligue 1']):
        return {
            'jugador': 'Jugador destacado',
            'prop': 'Over 0.5 goles',
            'cuota': 2.10,
            'stake': '0.5%',
            'ev': '+9.0%'
        }
    return None

# ==================================================
# 3. OBTENER PARTIDOS DESDE ESPN (FUENTE PRIMARIA)
# ==================================================
def extraer_datos_espn(data):
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
        partidos.append({
            'home_team': home,
            'away_team': away,
            'date': game_date,
            'stadium': stadium
        })
    return partidos

def obtener_partidos_espn(slug):
    url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{slug}/scoreboard"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return extraer_datos_espn(data)
    except:
        pass
    return []

# ==================================================
# 4. OBTENER PARTIDOS DESDE API-FOOTBALL (FUENTE SECUNDARIA)
# ==================================================
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
                    'stadium': fixture['venue']['name']
                })
            return partidos
    except Exception as e:
        print(f"Error en API-Football: {e}")
    return []

# ==================================================
# 5. OBTENER PARTIDOS DE MLB (ESPN + statsapi)
# ==================================================
def obtener_partidos_mlb():
    partidos = []
    # Fuente primaria: ESPN
    try:
        resp = requests.get(MLB_URL, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            partidos = extraer_datos_espn(data)
    except:
        pass

    # Fuente secundaria: statsapi (si ESPN no devolvió nada)
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
                    'stadium': game['venue_name']
                })
        except Exception as e:
            print(f"Error en statsapi: {e}")

    mlb_picks = []
    for game in partidos:
        hora = convertir_hora_venezuela(game['date'])
        mlb_picks.append({
            'partido': f"{game['away_team']} vs {game['home_team']}",
            'hora': hora,
            'principal': generar_pick_principal(game['home_team'], game['away_team'], 'MLB'),
            'secundaria': None,
            'prop_jugador': None
        })
    return mlb_picks

# ==================================================
# 6. OBTENER TODAS LAS LIGAS DE FÚTBOL (CON FALLBACK)
# ==================================================
def obtener_partidos_futbol():
    leagues = []
    for slug, league_info in LEAGUES_FUTBOL.items():
        league_name = league_info['name']
        league_id = league_info.get('api_football_id')
        print(f"Consultando {league_name}...")

        # Intentar ESPN primero
        partidos = obtener_partidos_espn(slug)
        if not partidos and league_id:
            # Si ESPN no tiene partidos, intentar API-Football
            print(f"  - ESPN sin datos, probando API-Football para {league_name}...")
            partidos = obtener_partidos_api_football(league_id)

        if not partidos:
            print(f"  - No hay partidos para {league_name} hoy.")
            continue

        league_games = []
        for game in partidos:
            hora = convertir_hora_venezuela(game['date'])
            league_games.append({
                'partido': f"{game['away_team']} vs {game['home_team']}",
                'hora': hora,
                'principal': generar_pick_principal(game['home_team'], game['away_team'], league_name),
                'secundaria': generar_pick_secundario(game['home_team'], game['away_team'], league_name),
                'prop_jugador': generar_prop_jugador(game['home_team'], game['away_team'], league_name)
            })
        leagues.append({
            'name': league_name,
            'games': league_games
        })
        print(f"  - {len(league_games)} partidos encontrados.")
    return leagues

# ==================================================
# 7. GUARDAR data.js
# ==================================================
def guardar_js(leagues_futbol, mlb_picks):
    resultados_vivo = {'mlb': [], 'nba': [], 'nhl': [], 'soccer': []}
    mejoras = [
        "✅ Sistema ThIA-SA v6.0 - Profesional",
        "✅ Fuentes: ESPN + API-Football (fútbol) | ESPN + statsapi (MLB)",
        "✅ Horario Venezuela (UTC-4)",
        "✅ Preparado para reglas reales de apuestas"
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
    print("=== ThIA-SA - Obteniendo datos reales (con API-Football activada) ===")
    print("Obteniendo partidos de fútbol...")
    leagues = obtener_partidos_futbol()
    print(f"Total de ligas con partidos: {len(leagues)}\n")
    print("Obteniendo partidos de MLB...")
    mlb = obtener_partidos_mlb()
    print(f"Total de partidos de MLB: {len(mlb)}\n")
    guardar_js(leagues, mlb)
    print("Proceso completado.")
