import requests
import json
from datetime import datetime

def fetch_espn_games(sport):
    urls = {
        'mlb': 'https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard',
        'nba': 'https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard',
        'nhl': 'https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard',
        'soccer': 'https://site.api.espn.com/apis/site/v2/sports/soccer/esp.1/scoreboard'
    }
    url = urls.get(sport)
    if not url:
        print(f"Deporte {sport} no soportado")
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
            print(f"  {len(games)} partidos encontrados en {sport}")
            return games
        else:
            print(f"  Error HTTP {resp.status_code} en {sport}")
            return []
    except Exception as e:
        print(f"  Excepción en {sport}: {e}")
        return []

def apply_rules(home_team, away_team):
    """
    Aquí aplicas TUS reglas (R144, R159, etc.)
    Por ahora es un ejemplo: siempre apuesta al local.
    Tú luego lo reemplazarás con tu lógica real.
    """
    # Ejemplo: pick principal (local ML)
    principal = {
        'pick': f"{home_team} ML",
        'cuota': 1.85,
        'ev': '+8.5%',
        'stake': '1.5%',
        'regla': 'Ejemplo: local favorito'
    }
    secundaria = None    # Aquí puedes poner otra apuesta
    prop_jugador = None  # Aquí puedes poner un prop
    return principal, secundaria, prop_jugador

def generate_picks():
    picks = {
        'mlb': [],
        'nba': [],
        'nhl': [],
        'laliga': [],
        'eredivisie': []
    }
    # Mapeo: (deporte_espn, clave_destino)
    sports_map = [
        ('mlb', 'mlb'),
        ('nba', 'nba'),
        ('nhl', 'nhl'),
        ('soccer', 'laliga')   # soccer -> laliga, pero puedes cambiarlo
    ]
    for espn_sport, key in sports_map:
        print(f"Obteniendo {espn_sport}...")
        games = fetch_espn_games(espn_sport)
        for game in games:
            principal, secundaria, prop = apply_rules(game['home_team'], game['away_team'])
            picks[key].append({
                'partido': f"{game['away_team']} vs {game['home_team']}",
                'hora': game['date'][11:16] + " VEN",
                'principal': principal,
                'secundaria': secundaria,
                'prop_jugador': prop
            })
    return picks

def save_js(picks):
    # Datos estáticos (puedes mantenerlos así o cargarlos desde otro lado)
    old_results = [
        {"fecha": "2026-04-22", "deporte": "MLB", "pick": "Angels ML vs Blue Jays", "cuota": 1.61, "estado": "hit"}
    ]
    mejoras = [
        "✅ Sistema ThIA-SA v5.8 activo",
        "✅ Picks generados con datos reales de ESPN"
    ]
    parlays = [
        {"name": "DIRECTA DEL DÍA", "type": "green", "picks": ["MLB | Yankees ML (1.61)"], "odds": "1.61", "stake": "3%", "desc": "Riesgo bajo"}
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
    print("✅ data.js generado correctamente")

if __name__ == "__main__":
    print("Obteniendo datos reales de ESPN...")
    picks = generate_picks()
    save_js(picks)
    print("Proceso completado.")
