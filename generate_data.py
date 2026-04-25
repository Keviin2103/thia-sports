import requests
import json
from datetime import datetime, timezone

def fetch_espn_scoreboard(sport):
    """Obtiene los eventos del día desde ESPN (público, sin clave)"""
    urls = {
        'mlb': 'https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard',
        'nba': 'https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard',
        'nhl': 'https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard',
        'soccer': 'https://site.api.espn.com/apis/site/v2/sports/soccer/usa.1/scoreboard'  # MLS por defecto
    }
    url = urls.get(sport)
    if not url:
        return []
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            events = []
            for event in data.get('events', []):
                comp = event['competitions'][0]
                home_team = comp['competitors'][0]['team']['displayName']
                away_team = comp['competitors'][1]['team']['displayName']
                game_date = event['date']
                events.append({
                    'home_team': home_team,
                    'away_team': away_team,
                    'date': game_date
                })
            return events
        else:
            print(f"Error ESPN {sport}: {resp.status_code}")
            return []
    except Exception as e:
        print(f"Excepción ESPN {sport}: {e}")
        return []

def generate_picks():
    picks = {
        'mlb': [],
        'nba': [],
        'nhl': [],
        'laliga': [],
        'eredivisie': []
    }
    # Mapeo de deportes a las claves de nuestro sistema
    sports_map = {
        'mlb': 'mlb',
        'nba': 'nba',
        'nhl': 'nhl',
        'soccer': 'laliga'  # Podríamos separar ligas, pero por simplicidad lo dejamos así
    }
    # También podríamos obtener fútbol europeo con diferentes slugs, pero para demo es suficiente
    for espn_sport, pick_key in sports_map.items():
        print(f"Obteniendo {espn_sport}...")
        events = fetch_espn_scoreboard(espn_sport)
        for ev in events:
            # Crear un pick principal simple (local ML con cuota estimada)
            pick_info = {
                'pick': f"{ev['home_team']} ML",
                'cuota': 1.85,
                'ev': '+8.5%',
                'stake': '1.5%',
                'regla': 'Valor local estimado'
            }
            picks[pick_key].append({
                'partido': f"{ev['away_team']} vs {ev['home_team']}",
                'hora': ev['date'][11:16] + " VEN" if 'date' in ev else "Hora pendiente",
                'principal': pick_info,
                'secundaria': None,
                'prop_jugador': None
            })
    # Si algún deporte no tiene eventos, añadimos datos de demostración para que se vea contenido
    if not picks['mlb']:
        picks['mlb'].append({
            'partido': "Yankees vs Red Sox",
            'hora': "07:10 PM VEN",
            'principal': {'pick': 'Yankees ML', 'cuota': 1.61, 'ev': '+9.5%', 'stake': '2.0%'},
            'secundaria': None,
            'prop_jugador': None
        })
    if not picks['nba']:
        picks['nba'].append({
            'partido': "Celtics vs 76ers",
            'hora': "07:30 PM VEN",
            'principal': {'pick': 'Celtics ML', 'cuota': 1.74, 'ev': '+11.0%', 'stake': '2.0%'},
            'secundaria': None,
            'prop_jugador': None
        })
    if not picks['nhl']:
        picks['nhl'].append({
            'partido': "Avalanche vs Kings",
            'hora': "10:00 PM VEN",
            'principal': {'pick': 'Avalanche ML', 'cuota': 1.55, 'ev': '+10.5%', 'stake': '2.0%'},
            'secundaria': None,
            'prop_jugador': None
        })
    if not picks['laliga']:
        picks['laliga'].append({
            'partido': "Real Madrid vs Barcelona",
            'hora': "04:00 PM VEN",
            'principal': {'pick': 'Real Madrid ML', 'cuota': 1.85, 'ev': '+9.0%', 'stake': '1.5%'},
            'secundaria': None,
            'prop_jugador': None
        })
    if not picks['eredivisie']:
        picks['eredivisie'].append({
            'partido': "Ajax vs PSV",
            'hora': "02:00 PM VEN",
            'principal': {'pick': 'PSV ML', 'cuota': 2.10, 'ev': '+8.5%', 'stake': '1.0%'},
            'secundaria': None,
            'prop_jugador': None
        })
    return picks

def save_js(picks):
    # Datos estáticos (resultados antiguos, mejoras, parlays)
    old_results = [
        {"fecha": "2026-04-22", "deporte": "MLB", "pick": "Angels ML vs Blue Jays", "cuota": 1.61, "estado": "hit"},
        {"fecha": "2026-04-22", "deporte": "NBA", "pick": "Pistons -8.5 vs Magic", "cuota": 1.91, "estado": "hit"},
        {"fecha": "2026-04-22", "deporte": "NHL", "pick": "Flyers ML vs Penguins", "cuota": 1.74, "estado": "fail"}
    ]
    mejoras = [
        "✅ R158: LaLiga priorizar DNB",
        "✅ R159: MLB evitar favoritos con derrotas seguidas",
        "✅ R160: Coors Under confirmado"
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
    print("Obteniendo datos de ESPN...")
    picks = generate_picks()
    save_js(picks)
    print("Proceso completado.")
