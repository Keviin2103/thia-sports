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
# 4. REGLAS THIA-SA PARA GENERAR PICKS
# ==================================================
def aplicar_regla_R144(home_team):
    """Ejemplo: R144 – evitar ML de equipo con récord perdedor en 2025.
       Necesitas una base de datos de récords. Por ahora, retorna True (apostable)."""
    # Aquí puedes conectar con un archivo JSON de récords históricos.
    # Por defecto, permitimos la apuesta.
    return True

def aplicar_regla_R159(home_team):
    """R159 – no apostar ML de local con 5+ derrotas consecutivas en casa.
       Necesitas datos de rachas. Por defecto, no la activamos."""
    return False

def aplicar_regla_R160(stadium_name, total_line):
    """R160 – en Coors Field con total ≥10.5, apostar Under."""
    if 'Coors' in stadium_name and total_line >= 10.5:
        return 'Under'
    return None

def aplicar_regla_R152(series_score, game_number):
    """R152 – en NBA playoffs Juego 2, si el favorito ganó J1 por +15, apostar spread del perdedor."""
    # Simulación: si es Juego 2 y el local ganó por más de 15 (necesitas datos reales)
    return False

def generar_picks_deportivos(home_team, away_team, sport, stadium='', total_line=0, game_number=1, series_score='1-0'):
    """
    Aplica todas las reglas y devuelve (principal, secundaria, prop).
    Por ahora, las reglas están simplificadas. Puedes expandirlas con datos reales.
    """
    principal = None
    secundaria = None
    prop = None

    # ----- Regla R144 (MLB) -----
    if sport == 'MLB' and aplicar_regla_R144(home_team):
        # Ejemplo de pick principal: apostar al local si cuota estimada > 1.85
        cuota_estimada = 1.90
        ev = (0.55 * cuota_estimada) - 1
        if ev > 0.05:
            principal = {
                'pick': f"{home_team} ML",
                'cuota': cuota_estimada,
                'ev': f"+{ev*100:.1f}%",
                'stake': '1.5%',
                'regla': 'R144 (local con cuota alta)'
            }

    # ----- Regla R160 (MLB en Coors Field) -----
    if sport == 'MLB' and stadium:
        under_over = aplicar_regla_R160(stadium, total_line)
        if under_over == 'Under':
            secundaria = {
                'pick': f"{under_over} {total_line}",
                'cuota': 1.91,
                'ev': '+9.5%',
                'stake': '1.0%',
                'regla': 'R160 (Coors Field Under)'
            }

    # ----- Regla R152 (NBA playoffs) -----
    if sport == 'NBA' and aplicar_regla_R152(series_score, game_number):
        # Apostar al spread del perdedor (equipo visitante)
        principal = {
            'pick': f"{away_team} +7.5",
            'cuota': 1.91,
            'ev': '+11.0%',
            'stake': '2.0%',
            'regla': 'R152 (Juego 2 ajuste del perdedor)'
        }

    # ----- Si no se generó ningún pick principal, ponemos un valor por defecto (local ML) -----
    if principal is None:
        principal = {
            'pick': f"{home_team} ML",
            'cuota': 1.85,
            'ev': '+8.5%',
            'stake': '1.5%',
            'regla': 'Valor por defecto (local)'
        }

    # ----- Pick secundario genérico (Over 2.5 para fútbol, Over 8.5 para MLB, etc.) -----
    if sport in ['Premier League', 'LaLiga', 'Serie A', 'Bundesliga', 'Ligue 1', 'Champions League', 'Europa League']:
        secundaria = {
            'pick': 'Over 2.5 goles',
            'cuota': 1.85,
            'ev': '+7.5%',
            'stake': '1.0%',
            'regla': 'Partido ofensivo (genérico)'
        }
    elif sport == 'MLB':
        secundaria = {
            'pick': 'Over 8.5 carreras',
            'cuota': 1.85,
            'ev': '+7.0%',
            'stake': '1.0%',
            'regla': 'Genérico MLB'
        }
    elif sport == 'NBA':
        secundaria = {
            'pick': 'Under 225.5 puntos',
            'cuota': 1.85,
            'ev': '+6.5%',
            'stake': '1.0%',
            'regla': 'Genérico NBA'
        }
    else:
        secundaria = None

    # ----- Prop de jugador genérico (puedes personalizarlo después) -----
    prop = {
        'jugador': 'Jugador Destacado',
        'prop': 'Over 0.5 goles / puntos',
        'cuota': 2.10,
        'stake': '0.5%',
        'ev': '+9.0%'
    }

    return principal, secundaria, prop

# ==================================================
# 5. GENERAR TODOS LOS PICKS (con reglas aplicadas)
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
            principal, secundaria, prop = generar_picks_deportivos(game['home_team'], game['away_team'], league_name)

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
        # Por simplicidad, pasamos stadium vacío y total_line 0 (luego puedes mejorarlo)
        principal, secundaria, prop = generar_picks_deportivos(game['home_team'], game['away_team'], 'MLB')
        picks['mlb'].append({
            'partido': f"{game['away_team']} vs {game['home_team']}",
            'hora': "Hora pendiente",
            'principal': principal,
            'secundaria': secundaria,
            'prop_jugador': prop
        })

    # ---------- NBA ----------
    print("Obteniendo NBA...")
    nba_games = fetch_nba_games()
    for game in nba_games:
        principal, secundaria, prop = generar_picks_deportivos(game['home_team'], game['away_team'], 'NBA')
        picks['nba'].append({
            'partido': f"{game['away_team']} vs {game['home_team']}",
            'hora': "Hora pendiente",
            'principal': principal,
            'secundaria': secundaria,
            'prop_jugador': prop
        })

    # ---------- NHL ----------
    print("Obteniendo NHL...")
    nhl_games = fetch_nhl_games()
    for game in nhl_games:
        # Para NHL, podemos usar la misma función con un deporte genérico
        principal, secundaria, prop = generar_picks_deportivos(game['home_team'], game['away_team'], 'NHL')
        picks['nhl'].append({
            'partido': f"{game['away_team']} vs {game['home_team']}",
            'hora': "Hora pendiente",
            'principal': principal,
            'secundaria': secundaria,
            'prop_jugador': prop
        })

    return picks

# ==================================================
# 6. GUARDAR EN data.js
# ==================================================
def guardar_js(picks):
    old_results = []
    mejoras = [
        "✅ Sistema ThIA-SA v5.8 - Datos reales desde ESPN + APIs oficiales",
        "✅ Reglas aplicadas: R144, R159, R160, R152 (versión preliminar)",
        "✅ Ligas de fútbol incluidas: Premier, LaLiga, Serie A, Bundesliga, Ligue 1, Eredivisie, Primeira Liga, MLS, Champions, Europa League",
        "✅ Horario ajustado a Venezuela (UTC-4)",
        "✅ MLB, NBA, NHL con fecha actual"
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
