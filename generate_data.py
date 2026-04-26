import requests
import json
from datetime import datetime, timezone, timedelta

# ========== 1. CONFIGURACIÓN ==========
SOCCER_LEAGUES = {
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

# ========== 2. FUNCIONES ==========
def obtener_fecha_actual_venezuela():
    venezuela_tz = timezone(timedelta(hours=-4))
    return datetime.now(venezuela_tz).strftime('%Y-%m-%d')

def fetch_espn_games(league_slug):
    url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{league_slug}/scoreboard"
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
                    game_date = event['date']
                    games.append({'home': home, 'away': away, 'date': game_date})
            return games
    except:
        return []
    return []

def convertir_hora_venezuela(utc_date_str):
    try:
        utc_date_str = utc_date_str.replace('Z', '+00:00')
        utc_time = datetime.fromisoformat(utc_date_str)
        venezuela_tz = timezone(timedelta(hours=-4))
        local_time = utc_time.astimezone(venezuela_tz)
        return local_time.strftime('%I:%M %p')
    except:
        return "Hora pendiente"

def generar_principal(home, away):
    return {
        'pick': f"{home} ML",
        'cuota': 1.85,
        'ev': '+8.5%',
        'stake': '1.5%',
        'regla': 'Ejemplo'
    }

def generar_todos_los_picks():
    picks = {'laliga': [], 'eredivisie': []}
    for slug, league_name in SOCCER_LEAGUES.items():
        juegos = fetch_espn_games(slug)
        for juego in juegos:
            hora_local = convertir_hora_venezuela(juego['date'])
            principal = generar_principal(juego['home'], juego['away'])
            item = {
                'partido': f"{juego['away']} vs {juego['home']}",
                'hora': hora_local,
                'principal': principal,
                'secundaria': None,
                'prop_jugador': None
            }
            if league_name in ['LaLiga', 'Serie A', 'Bundesliga', 'Ligue 1',
                               'Premier League', 'Eredivisie', 'Primeira Liga',
                               'Champions League', 'Europa League']:
                picks['laliga'].append(item)
            else:
                picks['eredivisie'].append(item)
    return picks

def guardar_js(picks):
    mejora = ["✅ Sistema ThIA-SA - Datos ESPN", "✅ Ligas europeas completas", "✅ Horario Venezuela"]
    js = f"""// Generado el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
const nhlPicks = [];
const nbaPicks = [];
const mlbPicks = [];
const laligaPicks = {json.dumps(picks['laliga'], indent=2)};
const eredivisiePicks = {json.dumps(picks['eredivisie'], indent=2)};
const oldResults = [];
const mejores = {json.dumps(mejora, indent=2)};
const parlaysData = [];
const todayResultsArray = {{}};
"""
    with open('data.js', 'w') as f:
        f.write(js)
    print("✅ data.js generado correctamente.")

if __name__ == "__main__":
    print("Obteniendo datos de ESPN...")
    picks = generar_todos_los_picks()
    guardar_js(picks)
    print("Proceso completado.")
