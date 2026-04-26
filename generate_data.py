import requests
import json
from datetime import datetime, timezone, timedelta

# ==================================================
# 1. CONFIGURACIÓN DE LIGAS
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

def convertir_hora_venezuela(utc_date_str):
    try:
        utc_date_str = utc_date_str.replace('Z', '+00:00')
        utc_time = datetime.fromisoformat(utc_date_str)
        venezuela_tz = timezone(timedelta(hours=-4))
        local_time = utc_time.astimezone(venezuela_tz)
        return local_time.strftime('%I:%M %p')
    except:
        return "Hora pendiente"

def fetch_espn_json(url):
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            return resp.json()
        else:
            print(f"Error {url}: {resp.status_code}")
            return None
    except Exception as e:
        print(f"Excepción en {url}: {e}")
        return None

def obtener_partidos_desde_espn(url):
    data = fetch_espn_json(url)
    if not data:
        return []
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

def generar_principal(home_team, away_team, sport):
    return {
        'pick': f"{home_team} ML",
        'cuota': 1.85,
        'ev': '+8.5%',
        'stake': '1.5%',
        'regla': 'Valor por defecto'
    }

def generar_secundaria(home_team, away_team, sport):
    if 'Premier' in sport or 'LaLiga' in sport or 'Serie A' in sport:
        return {
            'pick': 'Over 2.5 goles',
            'cuota': 1.85,
            'ev': '+7.5%',
            'stake': '1.0%',
            'regla': 'Partido ofensivo'
        }
    return None

def generar_prop(home_team, away_team, sport):
    if 'Premier' in sport or 'LaLiga' in sport or 'Serie A' in sport:
        return {
            'jugador': 'Jugador destacado',
            'prop': 'Over 0.5 goles',
            'cuota': 2.10,
            'stake': '0.5%',
            'ev': '+9.0%'
        }
    return None

def obtener_futbol_por_ligas():
    leagues = []
    for slug, league_name in LEAGUE_NAMES.items():
        url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{slug}/scoreboard"
        games = obtener_partidos_desde_espn(url)
        print(f"{league_name}: {len(games)} partidos")
        if not games:
            continue
        league_games = []
        for game in games:
            hora = convertir_hora_venezuela(game['date'])
            league_games.append({
                'partido': f"{game['away_team']} vs {game['home_team']}",
                'hora': hora,
                'principal': generar_principal(game['home_team'], game['away_team'], league_name),
                'secundaria': generar_secundaria(game['home_team'], game['away_team'], league_name),
                'prop_jugador': generar_prop(game['home_team'], game['away_team'], league_name)
            })
        leagues.append({'name': league_name, 'games': league_games})
    return leagues

def obtener_mlb():
    url = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"
    games = obtener_partidos_desde_espn(url)
    result = []
    for game in games:
        hora = convertir_hora_venezuela(game['date'])
        result.append({
            'partido': f"{game['away_team']} vs {game['home_team']}",
            'hora': hora,
            'principal': generar_principal(game['home_team'], game['away_team'], 'MLB'),
            'secundaria': None,
            'prop_jugador': None
        })
    return result

def obtener_nba():
    url = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"
    games = obtener_partidos_desde_espn(url)
    result = []
    for game in games:
        hora = convertir_hora_venezuela(game['date'])
        result.append({
            'partido': f"{game['away_team']} vs {game['home_team']}",
            'hora': hora,
            'principal': generar_principal(game['home_team'], game['away_team'], 'NBA'),
            'secundaria': None,
            'prop_jugador': None
        })
    return result

def obtener_nhl():
    url = "https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard"
    games = obtener_partidos_desde_espn(url)
    result = []
    for game in games:
        hora = convertir_hora_venezuela(game['date'])
        result.append({
            'partido': f"{game['away_team']} vs {game['home_team']}",
            'hora': hora,
            'principal': generar_principal(game['home_team'], game['away_team'], 'NHL'),
            'secundaria': None,
            'prop_jugador': None
        })
    return result

def obtener_resultados_en_vivo():
    return {'mlb': [], 'nba': [], 'nhl': [], 'soccer': []}

def guardar_js(leagues, mlb, nba, nhl, resultados_vivo):
    mejoras = [
        "✅ Datos desde ESPN (con fallback a vacío si no hay partidos)",
        "✅ Ligas de fútbol organizadas por nombre",
        "✅ Horario Venezuela (UTC-4)"
    ]
    js_content = f"""// Generado el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
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

if __name__ == "__main__":
    print("Iniciando obtención de datos...")
    leagues = obtener_futbol_por_ligas()
    mlb = obtener_mlb()
    nba = obtener_nba()
    nhl = obtener_nhl()
    resultados_vivo = obtener_resultados_en_vivo()
    guardar_js(leagues, mlb, nba, nhl, resultados_vivo)
    print("Proceso completado.")
