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
                games.append({'home_team': home, 'away_team': away, 'date': event['date']})
            return games
        else:
            return []
    except:
        return []

def apply_rules(home, away):
    # Regla de ejemplo: siempre apostar al local (solo para tener picks)
    # Aquí después pondrás tus reglas reales (R144, R159, etc.)
    return {
        'pick': f"{home} ML",
        'cuota': 1.85,
        'ev': '+8.5%',
        'stake': '1.5%',
        'regla': 'Ejemplo'
    }

def generate_picks():
    picks = {'mlb': [], 'nba': [], 'nhl': [], 'laliga': [], 'eredivisie': []}
    for espn_sport, key in [('mlb','mlb'), ('nba','nba'), ('nhl','nhl'), ('soccer','laliga')]:
        games = fetch_espn_games(espn_sport)
        for game in games:
            principal = apply_rules(game['home_team'], game['away_team'])
            picks[key].append({
                'partido': f"{game['away_team']} vs {game['home_team']}",
                'hora': game['date'][11:16] + " VEN",
                'principal': principal,
                'secundaria': None,
                'prop_jugador': None
            })
    return picks

def save_js(picks):
    old_results = []
    mejoras = ["✅ Sistema ThIA-SA v5.8 activo"]
    parlays = []
    js = f"""// Generado el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
const nhlPicks = {json.dumps(picks['nhl'])};
const nbaPicks = {json.dumps(picks['nba'])};
const mlbPicks = {json.dumps(picks['mlb'])};
const laligaPicks = {json.dumps(picks['laliga'])};
const eredivisiePicks = {json.dumps(picks['eredivisie'])};
const oldResults = {json.dumps(old_results)};
const mejores = {json.dumps(mejoras)};
const parlaysData = {json.dumps(parlays)};
const todayResultsArray = [];
"""
    with open('data.js', 'w') as f:
        f.write(js)
    print("✅ data.js generado")

if __name__ == "__main__":
    picks = generate_picks()
    save_js(picks)
