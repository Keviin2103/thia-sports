import requests
import json
from odds_api import OddsAPIClient
from datetime import datetime, timedelta

# Configuración
ODDS_API_KEY = "8ff80e170d8097cce21243da11a91fd9"
client = OddsAPIClient(api_key=ODDS_API_KEY)

def get_espn_games(sport, league):
    # ... (código de arriba, adaptado para retornar lista de dicts con home/away)
    pass

def get_odds_for_game(home_team, away_team, sport_key):
    # Buscar evento por nombre de equipo (aproximado)
    events = client.get_events(sport=sport_key)
    for ev in events:
        if (home_team in ev.home_team or ev.home_team in home_team) and \
           (away_team in ev.away_team or ev.away_team in away_team):
            odds = client.get_event_odds(sport=sport_key, event_id=ev.id)
            # extraer cuotas del primer bookmaker
            return odds.bookmakers[0].markets[0].outcomes
    return None

# ... reglas de evaluación ...

def main():
    all_picks = {'mlb': [], 'nba': [], ...}
    # Para cada deporte:
    games = get_espn_games('baseball', 'mlb')
    for game in games:
        odds = get_odds_for_game(game['home_team'], game['away_team'], 'baseball_mlb')
        if odds:
            pick = evaluate_mlb(game, odds)
            if pick:
                all_picks['mlb'].append(pick)
    # Guardar data.js
    with open('data.js', 'w') as f:
        f.write(f"const mlbPicks = {json.dumps(all_picks['mlb'])}; ...")