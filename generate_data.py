import requests
import json
from datetime import datetime, timezone, timedelta

# ==================================================
# 1. CONFIGURACIÓN: Ligas de fútbol (ESPN slugs)
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
# 2. FUNCIONES PARA OBTENER PARTIDOS (FECHA ACTUAL)
# ==================================================
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
                    games.append({
                        'home_team': home,
                        'away_team': away,
                        'date': game_date
                    })
            return games
        else:
            print(f"Error ESPN {league_slug}: {resp.status_code}")
            return []
    except Exception as e:
        print(f"Excepción ESPN {league_slug}: {e}")
        return []

def fetch_mlb_games():
    try:
        import statsapi
        today_str = obtener_fecha_actual_venezuela()
        schedule = statsapi.schedule(start_date=today_str, end_date=today_str)
        games = []
        for game in schedule:
            games.append({
                'home_team': game['home_id'],
                'away_team': game['away_id'],
                'date': game['game_datetime']
            })
        return games
    except Exception as e:
        print(f"Error MLB: {e}")
        return []

def fetch_nba_games():
    try:
        from nba_api.stats.endpoints import leaguegamefinder
        import pandas as pd
        today_str = obtener_fecha_actual_venezuela()
        gamefinder = leaguegamefinder.LeagueGameFinder(season_nullable='2025-26')
        games_df = gamefinder.get_data_frames()[0]
        games_df['GAME_DATE'] = pd.to_datetime(games_df['GAME_DATE']).dt.strftime('%Y-%m-%d')
        day_games = games_df[games_df['GAME_DATE'] == today_str]
        games = []
        for _, row in day_games.iterrows():
            games.append({
                'home_team': row['HOME_TEAM_ID'],
                'away_team': row['VISITOR_TEAM_ID'],
                'date': today_str
            })
        return games
    except Exception as e:
        print(f"Error NBA: {e}")
        return []

def fetch_nhl_games():
    try:
        import nhl_api_py as nhl
        today_str = obtener_fecha_actual_venezuela()
        client = nhl.NHLClient()
        daily_schedule = client.schedule.daily_schedule(date=today_str)
        games = []
        for game in daily_schedule.get('games', []):
            games.append({
                'home_team': game['teams']['home']['team']['name'],
                'away_team': game['teams']['away']['team']['name'],
                'date': game['gameDate']
            })
        return games
    except Exception as e:
        print(f"Error NHL: {e}")
        return []

# ==================================================
# 3. CONVERSIÓN DE FECHA UTC A HORA DE VENEZUELA
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

# ==================================================
# 4. GENERACIÓN DE PICKS (puedes personalizar después)
# ==================================================
def generar_principal(home_team, away_team):
    return {
        'pick': f"{home_team} ML",
        'cuota': 1.85,
        'ev': '+8.5%',
        'stake': '1.5%',
        'regla': 'Ejemplo'
    }

def generar_secundaria(home_team, away_team):
    return {
        'pick': 'Over 2.5 goles',
        'cuota': 1.85,
        'ev': '+7.5%',
        'stake': '1.0%',
        'regla': 'Ejemplo'
    }

def generar_prop(home_team, away_team):
    return {
        'jugador': 'Jugador Destacado',
        'prop': 'Over 0.5 goles',
        'cuota': 2.10,
        'stake': '0.5%',
        'ev': '+9.0%'
    }

# ==================================================
# 5. GENERAR TODOS LOS PICKS
# ==================================================
def generar_todos_los_picks():
    picks = {
        'mlb': [], 'nba': [], 'nhl': [], 'laliga': [], 'eredivisie': []
    }

    # ---------- FÚTBOL ----------
    for slug, league_name in SOCCER_LEAGUES.items():
        print(f"Obteniendo {league_name}...")
        games = fetch_espn_games(slug)
        for game in games:
            hora_local = convertir_hora_venezuela(game['date'])
            principal = generar_principal(game['home_team'], game['away_team'])
            secundaria = generar_secundaria(game['home_team'], game['away_team'])
            prop = generar_prop(game['home_team'], game['away_team'])

            pick_info = {
                'partido': f"{game['away_team']} vs {game['home_team']}",
                'hora': hora_local,
                'principal': principal,
                'secundaria': secundaria,
                'prop_jugador': prop
            }
            # Clasificación para que aparezcan en la web
            if league_name in ['LaLiga', 'Serie A', 'Bundesliga', 'Ligue 1', 'Premier League',
                               'Eredivisie', 'Primeira Liga', 'Champions League', 'Europa League']:
                picks['laliga'].append(pick_info)
            else:
                picks['eredivisie'].append(pick_info)

    # ---------- MLB ----------
    print("Obteniendo MLB...")
    mlb_games = fetch_mlb_games()
    for game in mlb_games:
        picks['mlb'].append({
            'partido': f"{game['away_team']} vs {game['home_team']}",
            'hora': "Hora pendiente",
            'principal': generar_principal(game['home_team'], game['away_team']),
            'secundaria': generar_secundaria(game['home_team'], game['away_team']),
            'prop_jugador': generar_prop(game['home_team'], game['away_team'])
        })

    # ---------- NBA ----------
    print("Obteniendo NBA...")
    nba_games = fetch_nba_games()
    for game in nba_games:
        picks['nba'].append({
            'partido': f"{game['away_team']} vs {game['home_team']}",
            'hora': "Hora pendiente",
            'principal': generar_principal(game['home_team'], game['away_team']),
            'secundaria': generar_secundaria(game['home_team'], game['away_team']),
            'prop_jugador': generar_prop(game['home_team'], game['away_team'])
        })

    # ---------- NHL ----------
    print("Obteniendo NHL...")
    nhl_games = fetch_nhl_games()
    for game in nhl_games:
        picks['nhl'].append({
            'partido': f"{game['away_team']} vs {game['home_team']}",
            'hora': "Hora pendiente",
            'principal': generar_principal(game['home_team'], game['away_team']),
            'secundaria': generar_secundaria(game['home_team'], game['away_team']),
            'prop_jugador': generar_prop(game['home_team'], game['away_team'])
        })

    return picks

# ==================================================
# 6. GUARDAR EN data.js
# ==================================================
def guardar_js(picks):
    old_results = []
    mejoras = [
        "✅ Sistema ThIA-SA v5.8 - Datos reales desde ESPN + APIs oficiales",
        "✅ Ligas de fútbol incluidas: Premier, LaLiga, Serie A, Bundesliga, Ligue 1, Eredivisie, Primeira Liga, MLS, Champions, Europa League",
        "✅ Horario ajustado a Venezuela (UTC-4)",
        "✅ MLB, NBA, NHL con fecha actual",
        "✅ Picks secundarios y props de ejemplo (personalizables)"
    ]
    parlays = []

    js_content = f"""// Generado automáticamente el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
const nhlPicks = {json.dumps(picks['nhl'], indent=2)};
const nbaPicks = {json.dumps(picks['nba'], indent=2)};
const mlbPicks = {json.dumps(picks['mlb'], indent=2)};
const laligaPicks = {json.dumps(picks['laliga'], indent=2)};
const eredivisiePicks = {json.dumps(picks['eredivisie'], indent=2)};
const oldResults = {json.dumps(old_results, indent=2)};
const mejores = {json.dumps(mejoras, indent=2)};
const parlaysData = {json.dumps(parlays, indent=2)};
const todayResultsArray = [];
"""
    with open('data.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    print("✅ data.js generado correctamente.")

# ==================================================
# 7. MAIN
# ==================================================
if __name__ == "__main__":
    print("Obteniendo datos reales de ESPN y APIs...")
    todos_los_picks = generar_todos_los_picks()
    guardar_js(todos_los_picks)
    print("Proceso completado.")
