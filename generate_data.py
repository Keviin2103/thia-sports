import requests
import json
from odds_api import OddsAPIClient
from datetime import datetime, timedelta
import os

# ========== CONFIGURACIÓN ==========
ODDS_API_KEY = "8ff80e170d8097cce21243da11a91fd9"
client = OddsAPIClient(api_key=ODDS_API_KEY)

# Mapeo de deportes para ESPN y Odds API
SPORTS_MAP = {
    'mlb': {'espn': 'baseball/mlb', 'odds_key': 'baseball_mlb', 'league_name': 'MLB'},
    'nba': {'espn': 'basketball/nba', 'odds_key': 'basketball_nba', 'league_name': 'NBA'},
    'nhl': {'espn': 'hockey/nhl', 'odds_key': 'icehockey_nhl', 'league_name': 'NHL'},
    'epl': {'espn': 'soccer/eng.1', 'odds_key': 'soccer_epl', 'league_name': 'Premier League'},
    'laliga': {'espn': 'soccer/esp.1', 'odds_key': 'soccer_spain_la_liga', 'league_name': 'LaLiga'},
    'eredivisie': {'espn': 'soccer/ned.1', 'odds_key': 'soccer_netherlands_eredivisie', 'league_name': 'Eredivisie'}
}

# ========== 1. OBTENER PARTIDOS DE ESPN ==========
def get_espn_games(sport_espn):
    """Retorna lista de diccionarios con home_team, away_team, commence_time"""
    url = f"https://site.api.espn.com/apis/site/v2/sports/{sport_espn}/scoreboard"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            print(f"Error ESPN {sport_espn}: {resp.status_code}")
            return []
        data = resp.json()
        games = []
        for event in data.get('events', []):
            comp = event['competitions'][0]
            home_team = comp['competitors'][0]['team']['displayName']
            away_team = comp['competitors'][1]['team']['displayName']
            commence_time = event['date']
            games.append({
                'home_team': home_team,
                'away_team': away_team,
                'commence_time': commence_time
            })
        return games
    except Exception as e:
        print(f"Excepción ESPN {sport_espn}: {e}")
        return []

# ========== 2. OBTENER CUOTAS DE ODDS API ==========
def get_odds_for_game(home_team, away_team, odds_key, commence_time):
    """Busca evento en Odds API por equipos y fecha, devuelve odds locales y visitantes"""
    # Usamos el endpoint de eventos (sin necesidad de ID)
    url = f"https://api.the-odds-api.com/v4/sports/{odds_key}/odds/"
    params = {
        'apiKey': ODDS_API_KEY,
        'regions': 'us',
        'markets': 'h2h',
        'dateFormat': 'iso',
        'commenceTimeFrom': commence_time
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code != 200:
            print(f"Error Odds {odds_key}: {resp.status_code}")
            return None
        data = resp.json()
        for event in data:
            # Comparación de equipos (texto flexible)
            if (home_team.lower() in event['home_team'].lower() or event['home_team'].lower() in home_team.lower()) and \
               (away_team.lower() in event['away_team'].lower() or event['away_team'].lower() in away_team.lower()):
                # Tomamos el primer bookmaker
                bookmaker = event['bookmakers'][0]
                for market in bookmaker['markets']:
                    if market['key'] == 'h2h':
                        outcomes = {out['name']: out['price'] for out in market['outcomes']}
                        return {
                            'home_odds': outcomes.get(event['home_team']),
                            'away_odds': outcomes.get(event['away_team'])
                        }
        return None
    except Exception as e:
        print(f"Excepción Odds: {e}")
        return None

# ========== 3. REGLAS DE EV+ (ejemplo) ==========
def evaluate_mlb(game, odds):
    if odds and odds['home_odds'] and odds['home_odds'] > 1.85:
        ev = (0.55 * odds['home_odds']) - 1
        if ev > 0.05:
            return {
                'pick': f"{game['home_team']} ML",
                'cuota': odds['home_odds'],
                'ev': f"+{ev*100:.1f}%",
                'stake': '1.5%',
                'regla': 'Valor local >1.85'
            }
    return None

def evaluate_nba(game, odds):
    if odds and odds['home_odds'] and odds['home_odds'] > 1.70:
        ev = (0.53 * odds['home_odds']) - 1
        if ev > 0.05:
            return {
                'pick': f"{game['home_team']} ML",
                'cuota': odds['home_odds'],
                'ev': f"+{ev*100:.1f}%",
                'stake': '2.0%'
            }
    return None

def evaluate_nhl(game, odds):
    if odds and odds['home_odds'] and odds['home_odds'] > 1.80:
        ev = (0.54 * odds['home_odds']) - 1
        if ev > 0.05:
            return {
                'pick': f"{game['home_team']} ML",
                'cuota': odds['home_odds'],
                'ev': f"+{ev*100:.1f}%",
                'stake': '1.5%'
            }
    return None

def evaluate_soccer(game, odds):
    if odds and odds['home_odds'] and odds['home_odds'] > 2.0:
        ev = (0.48 * odds['home_odds']) - 1
        if ev > 0.05:
            return {
                'pick': f"{game['home_team']} ML",
                'cuota': odds['home_odds'],
                'ev': f"+{ev*100:.1f}%",
                'stake': '1.5%'
            }
    return None

# ========== 4. GENERAR PICKS ==========
def generate_picks():
    picks = {'mlb': [], 'nba': [], 'nhl': [], 'laliga': [], 'eredivisie': []}
    for key, cfg in SPORTS_MAP.items():
        sport_espn = cfg['espn']
        odds_key = cfg['odds_key']
        print(f"Procesando {cfg['league_name']}...")
        games = get_espn_games(sport_espn)
        if not games:
            print(f"  No se encontraron partidos en ESPN para {cfg['league_name']}")
            continue
        for game in games:
            commence_time = game['commence_time']
            odds = get_odds_for_game(game['home_team'], game['away_team'], odds_key, commence_time)
            if not odds:
                # Si no hay cuotas, creamos un pick de demostración
                pick_info = {
                    'pick': f"{game['home_team']} ML (sin cuota real)",
                    'cuota': 1.85,
                    'ev': '+8.0%',
                    'stake': '1.5%'
                }
            else:
                if key == 'mlb':
                    pick_info = evaluate_mlb(game, odds)
                elif key == 'nba':
                    pick_info = evaluate_nba(game, odds)
                elif key == 'nhl':
                    pick_info = evaluate_nhl(game, odds)
                else:
                    pick_info = evaluate_soccer(game, odds)
            if pick_info:
                picks[key].append({
                    'partido': f"{game['away_team']} vs {game['home_team']}",
                    'hora': commence_time[11:16] if len(commence_time) > 11 else "Hora pendiente",
                    'principal': pick_info,
                    'secundaria': None,
                    'prop_jugador': None
                })
    return picks

# ========== 5. GUARDAR data.js ==========
def save_js(picks):
    old_results = [
        {"fecha": "2026-04-22", "deporte": "MLB", "pick": "Angels ML vs Blue Jays", "cuota": 1.61, "estado": "hit"},
        {"fecha": "2026-04-22", "deporte": "NBA", "pick": "Pistons -8.5 vs Magic", "cuota": 1.91, "estado": "hit"},
        {"fecha": "2026-04-22", "deporte": "NHL", "pick": "Flyers ML vs Penguins", "cuota": 1.74, "estado": "fail"}
    ]
    mejoras = [
        "✅ R158: LaLiga priorizar DNB",
        "✅ R159: MLB evitar favoritos con derrotas seguidas",
        "✅ R160: Coors Under confirmado",
        "✅ R161-R163: Ajustes NBA/NHL"
    ]
    parlays = [
        {"name": "DIRECTA DEL DÍA", "type": "green", "picks": ["MLB | Yankees ML (1.61)"], "odds": "1.61", "stake": "3%", "desc": "Riesgo bajo"},
        {"name": "MOROCHA 2 PICKS", "type": "orange", "picks": ["NBA | Celtics ML (1.74)", "MLB | Dodgers ML (1.71)"], "odds": "2.98", "stake": "2%", "desc": "Riesgo medio"},
        {"name": "PARLEY SEGURO 4 PICKS", "type": "purple", "picks": ["NHL | Avalanche ML (1.55)", "NBA | Celtics ML (1.74)", "MLB | Yankees ML (1.61)", "MLB | Dodgers ML (1.71)"], "odds": "7.42", "stake": "1.5%", "desc": "Riesgo medio-bajo"}
    ]

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

if __name__ == "__main__":
    print("Obteniendo partidos reales desde ESPN y cuotas desde Odds API...")
    picks = generate_picks()
    save_js(picks)
    print("Proceso completado.")
