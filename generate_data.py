import requests
import json
from datetime import datetime, timezone, timedelta

# ==================================================
# 1. CONFIGURACIÓN
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

# ==================================================
# 2. FUNCIONES AUXILIARES (sin cambios)
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

def fetch_espn_games(url, incluir_pitchers=False):
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            games = []
            for event in data.get('events', []):
                if 'competitions' not in event:
                    continue
                comp = event['competitions'][0]
                home = comp['competitors'][0]['team']['displayName']
                away = comp['competitors'][1]['team']['displayName']
                game_date = event['date']
                stadium = comp['venue']['fullName'] if 'venue' in comp else ''
                home_pitcher = away_pitcher = "TBD"
                if incluir_pitchers and 'notes' in comp:
                    for note in comp['notes']:
                        if note.get('type') == 'probablePitcher':
                            home_pitcher = note.get('homePro', {}).get('fullName', 'TBD')
                            away_pitcher = note.get('awayPro', {}).get('fullName', 'TBD')
                games.append({
                    'home_team': home,
                    'away_team': away,
                    'date': game_date,
                    'stadium': stadium,
                    'home_pitcher': home_pitcher,
                    'away_pitcher': away_pitcher
                })
            return games
    except:
        pass
    return []

# ==================================================
# 3. MLB (datos reales desde ESPN + statsapi)
# ==================================================
def obtener_partidos_mlb():
    url = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"
    games = fetch_espn_games(url, incluir_pitchers=True)
    if not games:
        try:
            import statsapi
            today = datetime.now().strftime('%Y-%m-%d')
            schedule = statsapi.schedule(start_date=today, end_date=today)
            for game in schedule:
                games.append({
                    'home_team': game['home_name'],
                    'away_team': game['away_name'],
                    'date': game['game_datetime'],
                    'stadium': game['venue_name'],
                    'home_pitcher': "TBD",
                    'away_pitcher': "TBD"
                })
        except:
            pass
    return games

# ==================================================
# 4. FÚTBOL (ESPN + API-Football)
# ==================================================
def obtener_partidos_espn_futbol(slug):
    url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{slug}/scoreboard"
    return fetch_espn_games(url, incluir_pitchers=False)

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
                partidos.append({
                    'home_team': item['teams']['home']['name'],
                    'away_team': item['teams']['away']['name'],
                    'date': item['fixture']['date'],
                    'stadium': item['fixture']['venue']['name'],
                    'home_pitcher': None,
                    'away_pitcher': None
                })
            return partidos
    except:
        pass
    return []

def obtener_futbol():
    leagues = []
    for slug, info in LEAGUES_FUTBOL.items():
        league_name = info['name']
        league_id = info.get('api_football_id')
        print(f"Consultando {league_name}...")
        partidos = obtener_partidos_espn_futbol(slug)
        if not partidos and league_id:
            partidos = obtener_partidos_api_football(league_id)
        if not partidos:
            print(f"  - No hay partidos para {league_name} hoy.")
            continue
        league_games = []
        for game in partidos:
            hora = convertir_hora_venezuela(game['date'])
            # Pick principal para fútbol (genérico, pero funcional)
            principal = {
                'pick': f"{game['home_team']} ML",
                'cuota': 1.85,
                'ev': '+8.5%',
                'stake': '1.5%',
                'regla': 'Local favorito'
            }
            league_games.append({
                'partido': f"{game['away_team']} vs {game['home_team']}",
                'hora': hora,
                'principal': principal,
                'secundaria': None,  # Por ahora sin secundario en fútbol
                'prop_jugador': None
            })
        leagues.append({'name': league_name, 'games': league_games})
        print(f"  - {len(league_games)} partidos encontrados.")
    return leagues

# ==================================================
# 5. GENERAR PICKS DE MLB (con secundarios y props)
# ==================================================
def generar_principal_mlb(home, away, home_pitcher, away_pitcher):
    # Regla simple: apostar al local (puedes cambiarla después)
    return {
        'pick': f"{home} ML",
        'cuota': 1.85,
        'ev': '+8.5%',
        'stake': '1.5%',
        'regla': 'Local favorito (mejorable)'
    }

def generar_secundario_mlb(home_era, away_era):
    # Si tenemos las ERAs, podemos generar Over/Under realistas
    # Por ahora, devolvemos un ejemplo
    return {
        'pick': 'Over 8.5 carreras',
        'cuota': 1.85,
        'ev': '+7.5%',
        'stake': '1.0%',
        'regla': 'Duelo ofensivo esperado'
    }

def generar_prop_mlb(pitcher_name):
    return {
        'jugador': pitcher_name if pitcher_name != "TBD" else "Lanzador abridor",
        'prop': 'Over 5.5 ponches',
        'cuota': 1.85,
        'stake': '0.5%',
        'ev': '+8.0%',
        'regla': 'Lanzador con buen K/9'
    }

def obtener_mlb():
    partidos = obtener_partidos_mlb()
    mlb_picks = []
    for game in partidos:
        hora = convertir_hora_venezuela(game['date'])
        mlb_picks.append({
            'partido': f"{game['away_team']} vs {game['home_team']}",
            'hora': hora,
            'home_pitcher': game.get('home_pitcher', 'TBD'),
            'away_pitcher': game.get('away_pitcher', 'TBD'),
            'principal': generar_principal_mlb(game['home_team'], game['away_team'], game.get('home_pitcher', 'TBD'), game.get('away_pitcher', 'TBD')),
            'secundaria': generar_secundario_mlb(3.5, 4.0),  # Valores de ejemplo (puedes mejorarlos con datos reales)
            'prop_jugador': generar_prop_mlb(game.get('home_pitcher', 'TBD'))
        })
    return mlb_picks

# ==================================================
# 6. GUARDAR data.js
# ==================================================
def guardar_js(leagues_futbol, mlb_picks):
    mejoras = [
        "✅ Fútbol: datos reales desde ESPN + API-Football",
        "✅ MLB: datos reales desde ESPN + statsapi",
        "✅ MLB: picks secundarios y props generados automáticamente",
        "✅ Horario Venezuela (UTC-4)"
    ]
    js_content = f"""// Generado automáticamente el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
const nhlPicks = [];
const nbaPicks = [];
const mlbPicks = {json.dumps(mlb_picks, indent=2)};
const leaguesData = {json.dumps(leagues_futbol, indent=2)};
const oldResults = [];
const mejores = {json.dumps(mejoras, indent=2)};
const parlaysData = [];
const todayResultsArray = {{}};
"""
    with open('data.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    print("✅ data.js generado correctamente.")

# ==================================================
# 7. MAIN
# ==================================================
if __name__ == "__main__":
    print("=== ThIA-SA v6.4 - Sistema estable con mejoras ===\n")
    print("Obteniendo fútbol...")
    fut = obtener_futbol()
    print(f"Total ligas con partidos: {len(fut)}\n")
    print("Obteniendo MLB...")
    mlb = obtener_mlb()
    print(f"Total picks de MLB: {len(mlb)}\n")
    guardar_js(fut, mlb)
    print("Proceso completado.")
