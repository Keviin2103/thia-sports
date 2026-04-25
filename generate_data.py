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
# 2. FUNCIÓN PARA OBTENER PARTIDOS DESDE ESPN
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

# ==================================================
# 3. CONVERSIÓN DE FECHA UTC A HORA DE VENEZUELA (UTC-4)
# ==================================================
def convertir_hora_venezuela(utc_date_str):
    try:
        utc_date_str = utc_date_str.replace('Z', '+00:00')
        utc_time = datetime.fromisoformat(utc_date_str)
        venezuela_tz = timezone(timedelta(hours=-4))
        local_time = utc_time.astimezone(venezuela_tz)
        return local_time.strftime('%I:%M %p')  # Ejemplo: "03:00 PM"
    except:
        return "Hora pendiente"

# ==================================================
# 4. FUNCIONES PARA GENERAR PICKS (ejemplos)
# ==================================================
def generar_principal(home_team, away_team):
    # Aquí puedes poner tus reglas reales (R144, R159, etc.)
    # Ejemplo: apostar al local con cuota fija 1.85
    return {
        'pick': f"{home_team} ML",
        'cuota': 1.85,
        'ev': '+8.5%',
        'stake': '1.5%',
        'regla': 'Ejemplo: local favorito'
    }

def generar_secundaria(home_team, away_team):
    # Ejemplo de pick secundario (Over 2.5 goles)
    return {
        'pick': 'Over 2.5 goles',
        'cuota': 1.85,
        'ev': '+7.5%',
        'stake': '1.0%',
        'regla': 'Ejemplo: partido ofensivo'
    }

def generar_prop(home_team, away_team):
    # Ejemplo de prop de jugador
    return {
        'jugador': 'Jugador Destacado',
        'prop': 'Over 0.5 goles',
        'cuota': 2.10,
        'stake': '0.5%',
        'ev': '+9.0%'
    }

# ==================================================
# 5. GENERAR TODOS LOS PICKS (FÚTBOL + MLB/NBA/NHL)
# ==================================================
def generar_todos_los_picks():
    # Estructura completa que espera tu index.html
    picks = {
        'mlb': [],          # Aquí irán partidos de MLB (puedes añadirlos después)
        'nba': [],          # Aquí irán partidos de NBA
        'nhl': [],          # Aquí irán partidos de NHL
        'laliga': [],       # Para LaLiga y otras ligas europeas
        'eredivisie': []    # Para el resto de ligas (puedes renombrar)
    }

    # ---------- FÚTBOL (todas las ligas) ----------
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
            # Clasificación según el nombre de la liga (ajústalo a tu dashboard)
            if 'LaLiga' in league_name or 'Serie A' in league_name or 'Bundesliga' in league_name:
                picks['laliga'].append(pick_info)
            else:
                picks['eredivisie'].append(pick_info)

    # ---------- MLB (béisbol) ----------
    # Puedes ampliar con statsapi después. Por ahora queda vacío.
    # ---------- NBA ----------
    # Puedes ampliar con nba_api después.
    # ---------- NHL ----------
    # Puedes ampliar con nhl-api-py después.

    return picks

# ==================================================
# 6. GUARDAR EN data.js
# ==================================================
def guardar_js(picks):
    old_results = []
    mejoras = [
        "✅ Sistema ThIA-SA v5.8 - Datos reales desde ESPN",
        "✅ Ligas incluidas: Premier, LaLiga, Serie A, Bundesliga, Ligue 1, Eredivisie, Primeira Liga, MLS, Champions, Europa League",
        "✅ Horario ajustado a Venezuela (UTC-4)",
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
    print("Obteniendo datos reales de ESPN...")
    todos_los_picks = generar_todos_los_picks()
    guardar_js(todos_los_picks)
    print("Proceso completado.")
