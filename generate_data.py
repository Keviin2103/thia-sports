import requests
import json
from datetime import datetime, timezone, timedelta

# ==================================================
# 1. CONFIGURACIÓN DE LIGAS (slug ESPN -> nombre real)
# ==================================================
LEAGUE_NAMES = {
    'eng.1': 'Premier League',
    'esp.2': 'LaLiga',
    'ita.1': 'Serie A',
    'fra.1': 'Ligue 1',
    'ned.1': 'Eredivisie',
    'por.1': 'Primeira Liga',
    'ger.1': 'Bundesliga',
    'usa.1': 'MLS',
    'uefa.champions': 'Champions League',
    'uefa.europa': 'Europa League',
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

def fetch_espn_general(url):
    """Obtiene partidos desde cualquier endpoint de ESPN (fútbol, MLB, NBA, NHL)"""
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            games = []
            for event in data.get('events', []):
                if 'competitions' in event:
                    comp = event['competitions'][0]
                    home = comp['competitors'][0]['team']['displayName']
                    away = comp['competitors'][1]['team']['displayName']
                    date_str = event['date']
                    stadium = comp['venue']['fullName'] if 'venue' in comp else ''
                    games.append({
                        'home_team': home,
                        'away_team': away,
                        'date': date_str,
                        'stadium': stadium
                    })
            return games
    except Exception as e:
        print(f"Error en {url}: {e}")
    return []

# ==================================================
# 3. GENERAR PICKS (estructura simple, después personalizas)
# ==================================================
def generar_picks_deportivos(home_team, away_team, sport, stadium=''):
    principal = {
        'pick': f"{home_team} ML",
        'cuota': 1.85,
        'ev': '+8.5%',
        'stake': '1.5%',
        'regla': 'Valor por defecto'
    }
    secundaria = None
    prop = None
    if 'Premier' in sport or 'LaLiga' in sport or 'Serie A' in sport:
        secundaria = {
            'pick': 'Over 2.5 goles',
            'cuota': 1.85,
            'ev': '+7.5%',
            'stake': '1.0%',
            'regla': 'Partido ofensivo'
        }
        prop = {
            'jugador': 'Jugador destacado',
            'prop': 'Over 0.5 goles',
            'cuota': 2.10,
            'stake': '0.5%',
            'ev': '+9.0%'
        }
    return principal, secundaria, prop

# ==================================================
# 4. OBTENER PARTIDOS DE TODOS LOS DEPORTES
# ==================================================
def obtener_futbol_por_ligas():
    leagues = []
    for slug, league_name in LEAGUE_NAMES.items():
        url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{slug}/scoreboard"
        games = fetch_espn_general(url)
        if not games:
            continue
        league_games = []
        for game in games:
            hora = convertir_hora_venezuela(game['date'])
            principal, sec, prop = generar_picks_deportivos(game['home_team'], game['away_team'], league_name, game.get('stadium',''))
            league_games.append({
                'partido': f"{game['away_team']} vs {game['home_team']}",
                'hora': hora,
                'principal': principal,
                'secundaria': sec,
                'prop_jugador': prop
            })
        leagues.append({
            'name': league_name,
            'games': league_games
        })
    return leagues

def obtener_mlb():
    url = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"
    games = fetch_espn_general(url)
    result = []
    for game in games:
        hora = convertir_hora_venezuela(game['date'])
        principal, sec, prop = generar_picks_deportivos(game['home_team'], game['away_team'], 'MLB', game.get('stadium',''))
        result.append({
            'partido': f"{game['away_team']} vs {game['home_team']}",
            'hora': hora,
            'principal': principal,
            'secundaria': sec,
            'prop_jugador': prop
        })
    return result

def obtener_nba():
    url = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"
    games = fetch_espn_general(url)
    result = []
    for game in games:
        hora = convertir_hora_venezuela(game['date'])
        principal, sec, prop = generar_picks_deportivos(game['home_team'], game['away_team'], 'NBA', game.get('stadium',''))
        result.append({
            'partido': f"{game['away_team']} vs {game['home_team']}",
            'hora': hora,
            'principal': principal,
            'secundaria': sec,
            'prop_jugador': prop
        })
    return result

def obtener_nhl():
    url = "https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard"
    games = fetch_espn_general(url)
    result = []
    for game in games:
        hora = convertir_hora_venezuela(game['date'])
        principal, sec, prop = generar_picks_deportivos(game['home_team'], game['away_team'], 'NHL', game.get('stadium',''))
        result.append({
            'partido': f"{game['away_team']} vs {game['home_team']}",
            'hora': hora,
            'principal': principal,
            'secundaria': sec,
            'prop_jugador': prop
        })
    return result

# ==================================================
# 5. RESULTADOS EN VIVO (opcional, por ahora vacío)
# ==================================================
def obtener_resultados_en_vivo():
    return {'mlb': [], 'nba': [], 'nhl': [], 'soccer': []}

# ==================================================
# 6. GUARDAR data.js
# ==================================================
def guardar_js(leagues, mlb, nba, nhl, resultados_vivo):
    mejoras = [
        "✅ Datos en tiempo real desde ESPN sin dependencias externas",
        "✅ Ligas de fútbol separadas por nombre real",
        "✅ Horario ajustado a Venezuela (UTC-4)",
        "✅ MLB, NBA, NHL también desde ESPN"
    ]
    js_content = f"""// Generado automáticamente el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
const nhlPicks = {json.dumps(nhl, indent=2)};
const nbaPicks = {json.dumps(nba, indent=2)};
const mlbPicks = {json.dumps(mlb, indent=2)};
const leaguesData = {json.dumps(leagues, indent=2)};
const oldResults = [];
const mejores = {json.dumps(mejoras, indent=2)};
const parlaysData = [];
const todayResultsArray = {json.dumps(resultados_vivo, indent=2)};
"""
    with open('data.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    print("✅ data.js generado correctamente.")

# ==================================================
# 7. MAIN
# ==================================================
if __name__ == "__main__":
    print("Obteniendo datos deportivos desde ESPN...")
    leagues = obtener_futbol_por_ligas()
    mlb = obtener_mlb()
    nba = obtener_nba()
    nhl = obtener_nhl()
    resultados_vivo = obtener_resultados_en_vivo()
    guardar_js(leagues, mlb, nba, nhl, resultados_vivo)
    print("Proceso completado.")
