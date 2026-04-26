import requests
import json
from datetime import datetime, timezone, timedelta
import pandas as pd

# ========== 1. OBTENER FECHA ACTUAL VENEZUELA ==========
def obtener_fecha_actual_venezuela():
    venezuela_tz = timezone(timedelta(hours=-4))
    return datetime.now(venezuela_tz).strftime('%Y-%m-%d')

# ========== 2. OBTENER PARTIDOS DE ESPN ==========
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
                    date = event['date']
                    games.append({'home': home, 'away': away, 'date': date})
            return games
    except:
        return []
    return []

# ========== 3. GENERAR ESTRUCTURA DE PICKS ==========
def generar_picks():
    picks = {'laliga': [], 'eredivisie': []}
    ligas = {'eng.1':'Premier League','esp.2':'LaLiga','ita.1':'Serie A',
             'fra.1':'Ligue 1','ned.1':'Eredivisie','por.1':'Primeira Liga',
             'ger.1':'Bundesliga','usa.1':'MLS'}
    for slug, nombre in ligas.items():
        juegos = fetch_espn_games(slug)
        for juego in juegos:
            item = {
                'partido': f"{juego['away']} vs {juego['home']}",
                'hora': juego['date'][11:16],
                'principal': {'pick':f"{juego['home']} ML", 'cuota':1.85, 'ev':'+8.5%', 'stake':'1.5%', 'regla':'Ejemplo'},
                'secundaria': None,
                'prop_jugador': None
            }
            if nombre == 'LaLiga':
                picks['laliga'].append(item)
            else:
                picks['eredivisie'].append(item)
    return picks

# ========== 4. GUARDAR data.js ==========
def guardar_js(picks):
    mejora = ["✅ Sistema ThIA-SA - Modo seguro", "✅ Se cargan datos de ESPN"]
    data = f"""// Generado el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
const nhlPicks = [];
const nbaPicks = [];
const mlbPicks = [];
const laligaPicks = {json.dumps(picks['laliga'], indent=2)};
const eredivisiePicks = {json.dumps(picks['eredivisie'], indent=2)};
const oldResults = [];
const mejores = {json.dumps(mejora, indent=2)};
const parlaysData = [];
const todayResultsArray = {{}};
"""
    with open('data.js', 'w') as f:
        f.write(data)
    print("✅ data.js generado correctamente.")

if __name__ == "__main__":
    print("Cargando datos de ESPN...")
    picks = generar_picks()
    guardar_js(picks)
    print("¡Proceso completado!")
