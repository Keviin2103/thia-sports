import requests
import json
import os
from datetime import datetime, timezone, timedelta

# ========== CONFIGURACIÓN ==========
ODDS_API_KEY = os.environ.get('ODDS_API_KEY')  # Se usará después para cuotas reales

# Lista de ligas de fútbol con sus slugs de ESPN
FOOTBALL_LEAGUES = {
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

# ========== 1. OBTENER PARTIDOS DE ESPN ==========
def fetch_espn_soccer_games(league_slug):
    """Obtiene los partidos del día para una liga específica de ESPN"""
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
            return []
    except Exception as e:
        print(f"Error ESPN {league_slug}: {e}")
        return []

# ========== 2. FUNCIÓN AUXILIAR DE HORARIO ==========
def convert_to_venezuela_time(utc_date_str):
    """Convierte una fecha UTC a hora local de Venezuela (UTC-4)"""
    if not utc_date_str:
        return "Hora pendiente"
    try:
        # Limpiar el formato
        utc_date_str = utc_date_str.replace('Z', '+00:00')
        utc_time = datetime.fromisoformat(utc_date_str)
        venezuela_tz = timezone(timedelta(hours=-4))
        local_time = utc_time.astimezone(venezuela_tz)
        return local_time.strftime('%I:%M %p')  # Formato 12h (ej. "03:00 PM")
    except:
        return "Hora pendiente"

# ========== 3. APLICAR REGLAS (ejemplo) ==========
def apply_rules(home_team, away_team):
    """Genera picks principal, secundario y prop de jugador (ejemplo)"""
    # Pick principal: Apostar al local con cuota 1.85
    principal = {
        'pick': f"{home_team} ML",
        'cuota': 1.85,
        'ev': '+8.5%',
        'stake': '1.5%',
        'regla': 'Ejemplo: local favorito'
    }
    
    # Pick secundario: Over 2.5 goles (cuota 1.85)
    secundario = {
        'pick': 'Over 2.5 goles',
        'cuota': 1.85,
        'ev': '+7.5%',
        'stake': '1.0%',
        'regla': 'Ejemplo: partido ofensivo'
    }
    
    # Prop de jugador: Jugador destacado (genérico)
    prop = {
        'jugador': 'Jugador Destacado',
        'prop': 'Over 0.5 goles',
        'cuota': 2.10,
        'stake': '0.5%',
        'ev': '+9.0%'
    }
    
    return principal, secundario, prop

# ========== 4. GENERAR PICKS ==========
def generate_picks():
    picks = {}
    # Inicializamos las listas para cada liga
    for league_name in FOOTBALL_LEAGUES.values():
        # Convertir nombre a clave segura (sin espacios, en minúsculas)
        key = league_name.lower().replace(' ', '_')
        picks[key] = []
    
    for slug, league_name in FOOTBALL_LEAGUES.items():
        print(f"Obteniendo {league_name}...")
        games = fetch_espn_soccer_games(slug)
        for game in games:
            principal, secundario, prop = apply_rules(game['home_team'], game['away_team'])
            hora_local = convert_to_venezuela_time(game['date'])
            
            pick_info = {
                'partido': f"{game['away_team']} vs {game['home_team']}",
                'hora': hora_local,
                'principal': principal,
                'secundaria': secundario,
                'prop_jugador': prop
            }
            key = league_name.lower().replace(' ', '_')
            picks[key].append(pick_info)
    
    return picks

# ========== 5. GUARDAR EN data.js ==========
def save_js(picks):
    # Datos estáticos (resultados antiguos, mejoras, parlays)
    old_results = []
    mejoras = ["✅ Sistema ThIA-SA v5.8 activo", "✅ Integradas todas las ligas de fútbol", "✅ Horario corregido a Venezuela"]
    parlays = []
    
    js_content = f"""// Generado automáticamente el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
// Datos de fútbol
const premier_league = {json.dumps(picks.get('premier_league', []), indent=2)};
const laliga = {json.dumps(picks.get('laliga', []), indent=2)};
const serie_a = {json.dumps(picks.get('serie_a', []), indent=2)};
const ligue_1 = {json.dumps(picks.get('ligue_1', []), indent=2)};
const eredivisie = {json.dumps(picks.get('eredivisie', []), indent=2)};
const primeira_liga = {json.dumps(picks.get('primeira_liga', []), indent=2)};
const bundesliga = {json.dumps(picks.get('bundesliga', []), indent=2)};
const mls = {json.dumps(picks.get('mls', []), indent=2)};
const champions_league = {json.dumps(picks.get('champions_league', []), indent=2)};
const europa_league = {json.dumps(picks.get('europa_league', []), indent=2)};

// Datos de otros deportes (se pueden añadir después)
const nhlPicks = [];
const nbaPicks = [];
const mlbPicks = [];
const oldResults = {json.dumps(old_results, indent=2)};
const mejores = {json.dumps(mejoras, indent=2)};
const parlaysData = {json.dumps(parlays, indent=2)};
const todayResultsArray = [];
"""
    with open('data.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    print("✅ data.js generado correctamente.")

# ========== 6. MAIN ==========
if __name__ == "__main__":
    print("Obteniendo partidos de fútbol desde ESPN...")
    picks = generate_picks()
    save_js(picks)
    print("Proceso completado.")
