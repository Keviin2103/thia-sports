import requests
import json
import os
from datetime import datetime, timezone

# ========== CONFIGURACIÓN ==========
ODDS_API_KEY = os.environ.get('ODDS_API_KEY')  # Tu clave secreta de GitHub
if not ODDS_API_KEY:
    print("⚠️ ODDS_API_KEY no encontrada. Las cuotas serán nulas.")

# ========== 1. OBTENER PARTIDOS REALES DESDE ESPN ==========
def fetch_espn_games(sport):
    """Devuelve lista de partidos del día con equipos y fecha"""
    urls = {
        'mlb': 'https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard',
        'nba': 'https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard',
        'nhl': 'https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard',
        'soccer': 'https://site.api.espn.com/apis/site/v2/sports/soccer/esp.1/scoreboard'  # Premier League
    }
    url = urls.get(sport)
    if not url:
        return []
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            games = []
            for event in data.get('events', []):
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
            print(f"Error ESPN {sport}: {resp.status_code}")
            return []
    except Exception as e:
        print(f"Excepción ESPN {sport}: {e}")
        return []

# ========== 2. OBTENER CUOTAS REALES DESDE THE ODDS API ==========
def fetch_odds(sport_key, home_team, away_team):
    """Busca cuotas para un partido específico (usando nombres de equipos)"""
    if not ODDS_API_KEY:
        return None
    url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds/"
    params = {
        'apiKey': ODDS_API_KEY,
        'regions': 'us',
        'markets': 'h2h',
        'dateFormat': 'iso'
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            for event in data:
                # Comparar nombres de equipos (ignorando mayúsculas/minúsculas)
                if (home_team.lower() in event['home_team'].lower() and
                    away_team.lower() in event['away_team'].lower()):
                    # Tomar el primer bookmaker (por ejemplo, DraftKings)
                    outcomes = event['bookmakers'][0]['markets'][0]['outcomes']
                    home_odds = None
                    away_odds = None
                    for out in outcomes:
                        if out['name'].lower() == event['home_team'].lower():
                            home_odds = out['price']
                        elif out['name'].lower() == event['away_team'].lower():
                            away_odds = out['price']
                    return {'home_odds': home_odds, 'away_odds': away_odds}
            return None
        else:
            print(f"Error Odds API: {resp.status_code}")
            return None
    except Exception as e:
        print(f"Excepción Odds API: {e}")
        return None

# ========== 3. APLICAR TUS REGLAS (ejemplos) ==========
def apply_rules(home_team, away_team, odds):
    """
    Aquí implementas TUS reglas (R139, R142, R144, etc.)
    Debe retornar: (pick_principal, pick_secundario, prop_jugador)
    """
    # EJEMPLO DE REGLA SIMPLE (R144: solo apostar ML local si cuota > 1.85)
    principal = None
    secundaria = None
    prop_jugador = None

    if odds and odds['home_odds'] and odds['home_odds'] > 1.85:
        ev = (0.55 * odds['home_odds']) - 1
        if ev > 0.05:
            principal = {
                'pick': f"{home_team} ML",
                'cuota': odds['home_odds'],
                'ev': f"+{ev*100:.1f}%",
                'stake': '1.5%',
                'regla': 'R144 (local con cuota alta)'
            }
    # Aquí puedes añadir más reglas (R159, R160, etc.)
    # Para props, puedes usar estadísticas predefinidas (ej. "Jugador X Over 1.5 bases")
    # Por ahora, los dejamos vacíos para que luego los llenes con tu lógica.

    return principal, secundaria, prop_jugador

# ========== 4. GENERAR PICKS ÚNICAMENTE CON DATOS REALES ==========
def generate_real_picks():
    picks = {
        'mlb': [], 'nba': [], 'nhl': [], 'laliga': [], 'eredivisie': []
    }
    # Mapeo deporte ESPN -> clave de nuestro sistema
    espn_to_key = {
        'mlb': 'mlb',
        'nba': 'nba',
        'nhl': 'nhl',
        'soccer': 'laliga'  # Para fútbol, tomamos Premier League como ejemplo
    }
    # Mapeo deporte -> sport_key para Odds API
    odds_sport_key = {
        'mlb': 'baseball_mlb',
        'nba': 'basketball_nba',
        'nhl': 'icehockey_nhl',
        'soccer': 'soccer_epl'
    }

    for espn_sport, key in espn_to_key.items():
        print(f"Obteniendo {espn_sport}...")
        games = fetch_espn_games(espn_sport)
        for game in games:
            # Obtener cuotas reales
            sport_key = odds_sport_key.get(espn_sport)
            odds = fetch_odds(sport_key, game['home_team'], game['away_team']) if sport_key else None
            # Aplicar reglas
            principal, secundaria, prop = apply_rules(game['home_team'], game['away_team'], odds)
            if principal:  # Solo agregar si hay un pick válido según las reglas
                picks[key].append({
                    'partido': f"{game['away_team']} vs {game['home_team']}",
                    'hora': game['date'][11:16] + " VEN",
                    'principal': principal,
                    'secundaria': secundaria,
                    'prop_jugador': prop
                })
    return picks

# ========== 5. GUARDAR EN data.js (sin demostración) ==========
def save_js(picks):
    # Datos estáticos (resultados antiguos, mejoras, parlays) – los puedes mantener
    old_results = [
        {"fecha": "2026-04-22", "deporte": "MLB", "pick": "Angels ML vs Blue Jays", "cuota": 1.61, "estado": "hit"},
        # Puedes ir agregando más resultados reales a medida que se jueguen
    ]
    mejoras = [
        "✅ R144: ML local con cuota > 1.85",
        "✅ R159: Evitar favoritos con derrotas seguidas",
        "✅ R160: Coors Under"
        # Añade aquí tus otras reglas
    ]
    parlays = [
        {"name": "DIRECTA DEL DÍA", "type": "green", "picks": [], "odds": "0.00", "stake": "0%", "desc": "Sin parlays aún"}
    ]

    js_content = f"""// Generado automáticamente el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - SIN DEMOSTRACIÓN
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
    print("✅ data.js generado con datos REALES (sin demo)")

# ========== 6. MAIN ==========
if __name__ == "__main__":
    print("Obteniendo datos reales de ESPN y cuotas de Odds API...")
    picks = generate_real_picks()
    save_js(picks)
    print("Proceso completado.")
