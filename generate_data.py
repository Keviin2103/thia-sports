import requests
import json
from datetime import datetime, timezone, timedelta

# ==================================================
# CONFIGURACIÓN DE LIGAS DE FÚTBOL (ESPN)
# ==================================================
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

# ==================================================
# FUNCIONES AUXILIARES GENERALES
# ==================================================
def obtener_fecha_actual_venezuela():
    venezuela_tz = timezone(timedelta(hours=-4))
    return datetime.now(venezuela_tz).strftime('%Y-%m-%d')

def convertir_hora_venezuela(utc_date_str):
    try:
        utc_date_str = utc_date_str.replace('Z', '+00:00')
        utc_time = datetime.fromisoformat(utc_date_str)
        venezuela_tz = timezone(timedelta(hours=-4))
        local_time = utc_time.astimezone(venezuela_tz)
        return local_time.strftime('%I:%M %p')
    except:
        return "Hora pendiente"

# ==================================================
# 1. OBTENER PARTIDOS DE FÚTBOL (ESPN)
# ==================================================
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
                    games.append({
                        'home': home,
                        'away': away,
                        'date': game_date
                    })
            return games
        else:
            return []
    except Exception as e:
        print(f"Error fútbol {league_slug}: {e}")
        return []

def generar_principal_futbol(home, away):
    return {
        'pick': f"{home} ML",
        'cuota': 1.85,
        'ev': '+8.5%',
        'stake': '1.5%',
        'regla': 'Ejemplo (local favorito)'
    }

# ==================================================
# 2. OBTENER PARTIDOS DE MLB (ESPN) – CON LANZADORES PROBABLES
# ==================================================
def fetch_mlb_games_espn():
    """Obtiene juegos de MLB del día actual, incluyendo lanzadores probables"""
    url = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"
    juegos = []
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            for event in data.get('events', []):
                comp = event['competitions'][0]
                home_team = comp['competitors'][0]['team']['displayName']
                away_team = comp['competitors'][1]['team']['displayName']
                game_date = event['date']
                status = event['status']['type']['description']

                # Lanzadores probables (pueden venir o no)
                home_pitcher = "No disponible"
                away_pitcher = "No disponible"
                if 'probable' in comp['competitors'][0]:
                    home_pitcher = comp['competitors'][0]['probable']['displayName']
                if 'probable' in comp['competitors'][1]:
                    away_pitcher = comp['competitors'][1]['probable']['displayName']

                juegos.append({
                    'home': home_team,
                    'away': away_team,
                    'home_pitcher': home_pitcher,
                    'away_pitcher': away_pitcher,
                    'date': game_date,
                    'status': status
                })
            return juegos
        else:
            print(f"Error MLB ESPN: {resp.status_code}")
            return []
    except Exception as e:
        print(f"Excepción MLB: {e}")
        return []

def generar_principal_mlb(home, away, home_pitcher, away_pitcher):
    # Aquí puedes meter tus reglas reales (R144, R160, etc.)
    # Por ahora, dejamos un pick de ejemplo con la información de los lanzadores
    return {
        'pick': f"{home} ML",
        'cuota': 1.85,
        'ev': '+8.5%',
        'stake': '1.5%',
        'regla': f'Local favorito (Lan. {home_pitcher} vs {away_pitcher})',
        'home_pitcher': home_pitcher,
        'away_pitcher': away_pitcher
    }

# ==================================================
# 3. FUNCIÓN PRINCIPAL: GENERAR TODOS LOS PICKS
# ==================================================
def generar_todos_los_picks():
    picks = {
        'mlb': [],
        'nba': [],
        'nhl': [],
        'laliga': [],
        'eredivisie': []
    }

    # ----- FÚTBOL (sin cambios) -----
    for slug, league_name in SOCCER_LEAGUES.items():
        games = fetch_espn_games(slug)
        for game in games:
            hora_local = convertir_hora_venezuela(game['date'])
            principal = generar_principal_futbol(game['home'], game['away'])
            item = {
                'partido': f"{game['away']} vs {game['home']}",
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

    # ----- MLB (nuevo con datos reales) -----
    mlb_games = fetch_mlb_games_espn()
    for game in mlb_games:
        hora_local = convertir_hora_venezuela(game['date'])
        principal = generar_principal_mlb(
            game['home'], game['away'],
            game['home_pitcher'], game['away_pitcher']
        )
        picks['mlb'].append({
            'partido': f"{game['away']} vs {game['home']}",
            'hora': hora_local,
            'principal': principal,
            'secundaria': None,
            'prop_jugador': None
        })

    # ----- NBA y NHL (de momento vacíos; tú puedes añadirlos después con el mismo patrón) -----
    return picks

# ==================================================
# 4. GUARDAR data.js
# ==================================================
def guardar_js(picks):
    mejoras = [
        "✅ Sistema ThIA-SA v5.9 - Datos reales desde ESPN",
        "✅ Ligas de fútbol europeas completas",
        "✅ MLB integrada (lanzadores incluidos)",
        "✅ Horario ajustado a Venezuela (UTC-4)"
    ]
    js_content = f"""// Generado automáticamente el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
const nhlPicks = {json.dumps(picks['nhl'], indent=2)};
const nbaPicks = {json.dumps(picks['nba'], indent=2)};
const mlbPicks = {json.dumps(picks['mlb'], indent=2)};
const laligaPicks = {json.dumps(picks['laliga'], indent=2)};
const eredivisiePicks = {json.dumps(picks['eredivisie'], indent=2)};
const oldResults = [];
const mejores = {json.dumps(mejoras, indent=2)};
const parlaysData = [];
const todayResultsArray = {{}};
"""
    with open('data.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    print("✅ data.js generado correctamente.")

if __name__ == "__main__":
    print("Obteniendo datos de ESPN (fútbol + MLB)...")
    todos = generar_todos_los_picks()
    guardar_js(todos)
    print("Proceso completado.")
