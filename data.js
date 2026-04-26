// Generado automáticamente el 2026-04-26 15:53:57
const nhlPicks = [];
const nbaPicks = [];
const mlbPicks = [
  {
    "partido": "Red Sox vs Orioles",
    "hora": "1:35 PM",
    "home_pitcher": "K. Bradish",
    "away_pitcher": "C. Early",
    "principal": {
      "pick": "Red Sox ML",
      "cuota": 1.85,
      "ev": "+8.5%",
      "stake": "1.5%",
      "regla": "Mejor ERA visitante (2.88 vs 3.96)"
    },
    "secundaria": {
      "pick": "Over 8.0",
      "cuota": 1.85,
      "ev": "+7.5%",
      "stake": "1.0%",
      "regla": "Suma de ERAs media (6.84)"
    },
    "prop_jugador": {
      "jugador": "C. Early",
      "prop": "Over 5.5 ponches",
      "cuota": 1.85,
      "stake": "0.5%",
      "ev": "+8.0%",
      "regla": "Mejor ERA visitante (2.88)"
    }
  },
  {
    "partido": "Phillies vs Braves",
    "hora": "1:35 PM",
    "home_pitcher": "C. Sale",
    "away_pitcher": "A. Nola",
    "principal": {
      "pick": "Braves ML",
      "cuota": 1.85,
      "ev": "+8.5%",
      "stake": "1.5%",
      "regla": "Mejor ERA local (2.79 vs 5.06)"
    },
    "secundaria": {
      "pick": "Over 8.5",
      "cuota": 1.85,
      "ev": "+7.5%",
      "stake": "1.0%",
      "regla": "Suma de ERAs alta (7.85)"
    },
    "prop_jugador": {
      "jugador": "C. Sale",
      "prop": "Over 5.5 ponches",
      "cuota": 1.85,
      "stake": "0.5%",
      "ev": "+8.0%",
      "regla": "Mejor ERA local (2.79)"
    }
  },
  {
    "partido": "Guardians vs Blue Jays",
    "hora": "1:37 PM",
    "home_pitcher": "P. Corbin",
    "away_pitcher": "S. Cecconi",
    "principal": {
      "pick": "Blue Jays ML",
      "cuota": 1.85,
      "ev": "+8.5%",
      "stake": "1.5%",
      "regla": "Mejor ERA local (3.68 vs 6.20)"
    },
    "secundaria": {
      "pick": "Over 8.5",
      "cuota": 1.85,
      "ev": "+7.5%",
      "stake": "1.0%",
      "regla": "Suma de ERAs alta (9.88)"
    },
    "prop_jugador": {
      "jugador": "P. Corbin",
      "prop": "Over 5.5 ponches",
      "cuota": 1.85,
      "stake": "0.5%",
      "ev": "+8.0%",
      "regla": "Mejor ERA local (3.68)"
    }
  },
  {
    "partido": "Rockies (G1) vs Mets",
    "hora": "1:40 PM",
    "home_pitcher": "N. McLean",
    "away_pitcher": "J. Quintana",
    "principal": {
      "pick": "Mets ML",
      "cuota": 1.85,
      "ev": "+8.5%",
      "stake": "1.5%",
      "regla": "Mejor ERA local (2.67 vs 6.23)"
    },
    "secundaria": {
      "pick": "Over 8.5",
      "cuota": 1.85,
      "ev": "+7.5%",
      "stake": "1.0%",
      "regla": "Suma de ERAs alta (8.90)"
    },
    "prop_jugador": {
      "jugador": "N. McLean",
      "prop": "Over 5.5 ponches",
      "cuota": 1.85,
      "stake": "0.5%",
      "ev": "+8.0%",
      "regla": "Mejor ERA local (2.67)"
    }
  },
  {
    "partido": "Tigers vs Reds",
    "hora": "1:40 PM",
    "home_pitcher": "R. Lowder",
    "away_pitcher": "K. Montero",
    "principal": {
      "pick": "Reds ML",
      "cuota": 1.85,
      "ev": "+8.5%",
      "stake": "1.5%",
      "regla": "Mejor ERA local (3.10 vs 3.68)"
    },
    "secundaria": {
      "pick": "Over 8.0",
      "cuota": 1.85,
      "ev": "+7.5%",
      "stake": "1.0%",
      "regla": "Suma de ERAs media (6.78)"
    },
    "prop_jugador": {
      "jugador": "R. Lowder",
      "prop": "Over 5.5 ponches",
      "cuota": 1.85,
      "stake": "0.5%",
      "ev": "+8.0%",
      "regla": "Mejor ERA local (3.10)"
    }
  },
  {
    "partido": "Twins vs Rays",
    "hora": "1:40 PM",
    "home_pitcher": "J. Scholtens",
    "away_pitcher": "S. Woods Richardson",
    "principal": {
      "pick": "Rays ML",
      "cuota": 1.85,
      "ev": "+8.5%",
      "stake": "1.5%",
      "regla": "Mejor ERA local (2.93 vs 5.96)"
    },
    "secundaria": {
      "pick": "Over 8.5",
      "cuota": 1.85,
      "ev": "+7.5%",
      "stake": "1.0%",
      "regla": "Suma de ERAs alta (8.89)"
    },
    "prop_jugador": {
      "jugador": "J. Scholtens",
      "prop": "Over 5.5 ponches",
      "cuota": 1.85,
      "stake": "0.5%",
      "ev": "+8.0%",
      "regla": "Mejor ERA local (2.93)"
    }
  },
  {
    "partido": "Yankees vs Astros",
    "hora": "2:10 PM",
    "home_pitcher": "S. Arrighetti",
    "away_pitcher": "L. Gil",
    "principal": {
      "pick": "Astros ML",
      "cuota": 1.85,
      "ev": "+8.5%",
      "stake": "1.5%",
      "regla": "Mejor ERA local (2.45 vs 4.11)"
    },
    "secundaria": {
      "pick": "Over 8.0",
      "cuota": 1.85,
      "ev": "+7.5%",
      "stake": "1.0%",
      "regla": "Suma de ERAs media (6.56)"
    },
    "prop_jugador": {
      "jugador": "S. Arrighetti",
      "prop": "Over 5.5 ponches",
      "cuota": 1.85,
      "stake": "0.5%",
      "ev": "+8.0%",
      "regla": "Mejor ERA local (2.45)"
    }
  },
  {
    "partido": "Pirates vs Brewers",
    "hora": "2:10 PM",
    "home_pitcher": "K. Harrison",
    "away_pitcher": "C. Mlodzinski",
    "principal": {
      "pick": "Brewers ML",
      "cuota": 1.85,
      "ev": "+8.5%",
      "stake": "1.5%",
      "regla": "Mejor ERA local (3.06 vs 3.28)"
    },
    "secundaria": {
      "pick": "Over 8.0",
      "cuota": 1.85,
      "ev": "+7.5%",
      "stake": "1.0%",
      "regla": "Suma de ERAs media (6.34)"
    },
    "prop_jugador": {
      "jugador": "K. Harrison",
      "prop": "Over 5.5 ponches",
      "cuota": 1.85,
      "stake": "0.5%",
      "ev": "+8.0%",
      "regla": "Mejor ERA local (3.06)"
    }
  },
  {
    "partido": "Nationals vs White Sox",
    "hora": "2:10 PM",
    "home_pitcher": "B. Hudson",
    "away_pitcher": "F. Griffin",
    "principal": {
      "pick": "White Sox ML",
      "cuota": 1.85,
      "ev": "+8.5%",
      "stake": "1.5%",
      "regla": "Mejor ERA local (1.54 vs 3.38)"
    },
    "secundaria": {
      "pick": "Under 7.5",
      "cuota": 1.85,
      "ev": "+7.5%",
      "stake": "1.0%",
      "regla": "Suma de ERAs baja (4.92)"
    },
    "prop_jugador": {
      "jugador": "B. Hudson",
      "prop": "Over 5.5 ponches",
      "cuota": 1.85,
      "stake": "0.5%",
      "ev": "+8.0%",
      "regla": "Mejor ERA local (1.54)"
    }
  },
  {
    "partido": "Mariners vs Cardinals",
    "hora": "2:15 PM",
    "home_pitcher": "M. McGreevy",
    "away_pitcher": "E. Hancock",
    "principal": {
      "pick": "Mariners ML",
      "cuota": 1.85,
      "ev": "+8.5%",
      "stake": "1.5%",
      "regla": "Mejor ERA visitante (2.83 vs 3.29)"
    },
    "secundaria": {
      "pick": "Over 8.0",
      "cuota": 1.85,
      "ev": "+7.5%",
      "stake": "1.0%",
      "regla": "Suma de ERAs media (6.12)"
    },
    "prop_jugador": {
      "jugador": "E. Hancock",
      "prop": "Over 5.5 ponches",
      "cuota": 1.85,
      "stake": "0.5%",
      "ev": "+8.0%",
      "regla": "Mejor ERA visitante (2.83)"
    }
  },
  {
    "partido": "Athletics vs Rangers",
    "hora": "2:35 PM",
    "home_pitcher": "K. Rocker",
    "away_pitcher": "J.T. Ginn",
    "principal": {
      "pick": "Rangers ML",
      "cuota": 1.85,
      "ev": "+8.5%",
      "stake": "1.5%",
      "regla": "Mejor ERA local (3.48 vs 3.74)"
    },
    "secundaria": {
      "pick": "Over 8.5",
      "cuota": 1.85,
      "ev": "+7.5%",
      "stake": "1.0%",
      "regla": "Suma de ERAs alta (7.22)"
    },
    "prop_jugador": {
      "jugador": "K. Rocker",
      "prop": "Over 5.5 ponches",
      "cuota": 1.85,
      "stake": "0.5%",
      "ev": "+8.0%",
      "regla": "Mejor ERA local (3.48)"
    }
  },
  {
    "partido": "Marlins vs Giants",
    "hora": "4:05 PM",
    "home_pitcher": "L. Roupp",
    "away_pitcher": "M. Meyer",
    "principal": {
      "pick": "Giants ML",
      "cuota": 1.85,
      "ev": "+8.5%",
      "stake": "1.5%",
      "regla": "Mejor ERA local (2.28 vs 3.96)"
    },
    "secundaria": {
      "pick": "Over 8.0",
      "cuota": 1.85,
      "ev": "+7.5%",
      "stake": "1.0%",
      "regla": "Suma de ERAs media (6.24)"
    },
    "prop_jugador": {
      "jugador": "L. Roupp",
      "prop": "Over 5.5 ponches",
      "cuota": 1.85,
      "stake": "0.5%",
      "ev": "+8.0%",
      "regla": "Mejor ERA local (2.28)"
    }
  },
  {
    "partido": "Padres vs Diamondbacks",
    "hora": "4:05 PM",
    "home_pitcher": "R. Nelson",
    "away_pitcher": "M. King",
    "principal": {
      "pick": "Padres ML",
      "cuota": 1.85,
      "ev": "+8.5%",
      "stake": "1.5%",
      "regla": "Mejor ERA visitante (2.28 vs 6.97)"
    },
    "secundaria": {
      "pick": "Over 8.5",
      "cuota": 1.85,
      "ev": "+7.5%",
      "stake": "1.0%",
      "regla": "Suma de ERAs alta (9.25)"
    },
    "prop_jugador": {
      "jugador": "M. King",
      "prop": "Over 5.5 ponches",
      "cuota": 1.85,
      "stake": "0.5%",
      "ev": "+8.0%",
      "regla": "Mejor ERA visitante (2.28)"
    }
  },
  {
    "partido": "Cubs vs Dodgers",
    "hora": "4:10 PM",
    "home_pitcher": "J. Wrobleski",
    "away_pitcher": "S. Imanaga",
    "principal": {
      "pick": "Dodgers ML",
      "cuota": 1.85,
      "ev": "+8.5%",
      "stake": "1.5%",
      "regla": "Mejor ERA local (1.88 vs 2.17)"
    },
    "secundaria": {
      "pick": "Under 7.5",
      "cuota": 1.85,
      "ev": "+7.5%",
      "stake": "1.0%",
      "regla": "Suma de ERAs baja (4.05)"
    },
    "prop_jugador": {
      "jugador": "J. Wrobleski",
      "prop": "Over 5.5 ponches",
      "cuota": 1.85,
      "stake": "0.5%",
      "ev": "+8.0%",
      "regla": "Mejor ERA local (1.88)"
    }
  },
  {
    "partido": "Rockies vs Mets (G2)",
    "hora": "5:10 PM",
    "home_pitcher": "K. Senga",
    "away_pitcher": "TBD",
    "principal": {
      "pick": "Mets (G2) ML",
      "cuota": 1.85,
      "ev": "+8.5%",
      "stake": "1.5%",
      "regla": "Mejor ERA local (8.83 vs 99.00)"
    },
    "secundaria": {
      "pick": "Over 8.5",
      "cuota": 1.85,
      "ev": "+7.5%",
      "stake": "1.0%",
      "regla": "Suma de ERAs alta (107.83)"
    },
    "prop_jugador": {
      "jugador": "K. Senga",
      "prop": "Over 5.5 ponches",
      "cuota": 1.85,
      "stake": "0.5%",
      "ev": "+8.0%",
      "regla": "Mejor ERA local (8.83)"
    }
  },
  {
    "partido": "Angels vs Royals",
    "hora": "7:20 PM",
    "home_pitcher": "S. Lugo",
    "away_pitcher": "R. Detmers",
    "principal": {
      "pick": "Royals ML",
      "cuota": 1.85,
      "ev": "+8.5%",
      "stake": "1.5%",
      "regla": "Mejor ERA local (1.15 vs 4.08)"
    },
    "secundaria": {
      "pick": "Over 8.0",
      "cuota": 1.85,
      "ev": "+7.5%",
      "stake": "1.0%",
      "regla": "Suma de ERAs media (5.23)"
    },
    "prop_jugador": {
      "jugador": "S. Lugo",
      "prop": "Over 5.5 ponches",
      "cuota": 1.85,
      "stake": "0.5%",
      "ev": "+8.0%",
      "regla": "Mejor ERA local (1.15)"
    }
  }
];
const leaguesData = [
  {
    "name": "Premier League",
    "games": [
      {
        "partido": "Brentford vs Manchester United",
        "hora": "03:00 PM",
        "principal": {
          "pick": "Manchester United ML",
          "cuota": 1.85,
          "ev": "+8.5%",
          "stake": "1.5%",
          "regla": "Local favorito (valor por defecto)"
        },
        "secundaria": {
          "pick": "Over 2.5 goles",
          "cuota": 1.85,
          "ev": "+7.5%",
          "stake": "1.0%",
          "regla": "Partido ofensivo"
        },
        "prop_jugador": {
          "jugador": "Jugador destacado",
          "prop": "Over 0.5 goles",
          "cuota": 2.1,
          "stake": "0.5%",
          "ev": "+9.0%"
        }
      }
    ]
  },
  {
    "name": "LaLiga",
    "games": [
      {
        "partido": "Sporting Gij\u00f3n vs C\u00f3rdoba",
        "hora": "08:00 AM",
        "principal": {
          "pick": "C\u00f3rdoba ML",
          "cuota": 1.85,
          "ev": "+8.5%",
          "stake": "1.5%",
          "regla": "Local favorito (valor por defecto)"
        },
        "secundaria": {
          "pick": "Over 2.5 goles",
          "cuota": 1.85,
          "ev": "+7.5%",
          "stake": "1.0%",
          "regla": "Partido ofensivo"
        },
        "prop_jugador": {
          "jugador": "Jugador destacado",
          "prop": "Over 0.5 goles",
          "cuota": 2.1,
          "stake": "0.5%",
          "ev": "+9.0%"
        }
      },
      {
        "partido": "Almer\u00eda vs Granada",
        "hora": "10:15 AM",
        "principal": {
          "pick": "Granada ML",
          "cuota": 1.85,
          "ev": "+8.5%",
          "stake": "1.5%",
          "regla": "Local favorito (valor por defecto)"
        },
        "secundaria": {
          "pick": "Over 2.5 goles",
          "cuota": 1.85,
          "ev": "+7.5%",
          "stake": "1.0%",
          "regla": "Partido ofensivo"
        },
        "prop_jugador": {
          "jugador": "Jugador destacado",
          "prop": "Over 0.5 goles",
          "cuota": 2.1,
          "stake": "0.5%",
          "ev": "+9.0%"
        }
      },
      {
        "partido": "Cultural Leonesa vs Mirand\u00e9s",
        "hora": "10:15 AM",
        "principal": {
          "pick": "Mirand\u00e9s ML",
          "cuota": 1.85,
          "ev": "+8.5%",
          "stake": "1.5%",
          "regla": "Local favorito (valor por defecto)"
        },
        "secundaria": {
          "pick": "Over 2.5 goles",
          "cuota": 1.85,
          "ev": "+7.5%",
          "stake": "1.0%",
          "regla": "Partido ofensivo"
        },
        "prop_jugador": {
          "jugador": "Jugador destacado",
          "prop": "Over 0.5 goles",
          "cuota": 2.1,
          "stake": "0.5%",
          "ev": "+9.0%"
        }
      },
      {
        "partido": "Real Zaragoza vs Huesca",
        "hora": "12:30 PM",
        "principal": {
          "pick": "Huesca ML",
          "cuota": 1.85,
          "ev": "+8.5%",
          "stake": "1.5%",
          "regla": "Local favorito (valor por defecto)"
        },
        "secundaria": {
          "pick": "Over 2.5 goles",
          "cuota": 1.85,
          "ev": "+7.5%",
          "stake": "1.0%",
          "regla": "Partido ofensivo"
        },
        "prop_jugador": {
          "jugador": "Jugador destacado",
          "prop": "Over 0.5 goles",
          "cuota": 2.1,
          "stake": "0.5%",
          "ev": "+9.0%"
        }
      },
      {
        "partido": "FC Andorra vs Legan\u00e9s",
        "hora": "12:30 PM",
        "principal": {
          "pick": "Legan\u00e9s ML",
          "cuota": 1.85,
          "ev": "+8.5%",
          "stake": "1.5%",
          "regla": "Local favorito (valor por defecto)"
        },
        "secundaria": {
          "pick": "Over 2.5 goles",
          "cuota": 1.85,
          "ev": "+7.5%",
          "stake": "1.0%",
          "regla": "Partido ofensivo"
        },
        "prop_jugador": {
          "jugador": "Jugador destacado",
          "prop": "Over 0.5 goles",
          "cuota": 2.1,
          "stake": "0.5%",
          "ev": "+9.0%"
        }
      },
      {
        "partido": "Racing Santander vs Ceuta",
        "hora": "03:00 PM",
        "principal": {
          "pick": "Ceuta ML",
          "cuota": 1.85,
          "ev": "+8.5%",
          "stake": "1.5%",
          "regla": "Local favorito (valor por defecto)"
        },
        "secundaria": {
          "pick": "Over 2.5 goles",
          "cuota": 1.85,
          "ev": "+7.5%",
          "stake": "1.0%",
          "regla": "Partido ofensivo"
        },
        "prop_jugador": {
          "jugador": "Jugador destacado",
          "prop": "Over 0.5 goles",
          "cuota": 2.1,
          "stake": "0.5%",
          "ev": "+9.0%"
        }
      }
    ]
  },
  {
    "name": "Serie A",
    "games": [
      {
        "partido": "Sassuolo vs Fiorentina",
        "hora": "06:30 AM",
        "principal": {
          "pick": "Fiorentina ML",
          "cuota": 1.85,
          "ev": "+8.5%",
          "stake": "1.5%",
          "regla": "Local favorito (valor por defecto)"
        },
        "secundaria": {
          "pick": "Over 2.5 goles",
          "cuota": 1.85,
          "ev": "+7.5%",
          "stake": "1.0%",
          "regla": "Partido ofensivo"
        },
        "prop_jugador": {
          "jugador": "Jugador destacado",
          "prop": "Over 0.5 goles",
          "cuota": 2.1,
          "stake": "0.5%",
          "ev": "+9.0%"
        }
      },
      {
        "partido": "Como vs Genoa",
        "hora": "09:00 AM",
        "principal": {
          "pick": "Genoa ML",
          "cuota": 1.85,
          "ev": "+8.5%",
          "stake": "1.5%",
          "regla": "Local favorito (valor por defecto)"
        },
        "secundaria": {
          "pick": "Over 2.5 goles",
          "cuota": 1.85,
          "ev": "+7.5%",
          "stake": "1.0%",
          "regla": "Partido ofensivo"
        },
        "prop_jugador": {
          "jugador": "Jugador destacado",
          "prop": "Over 0.5 goles",
          "cuota": 2.1,
          "stake": "0.5%",
          "ev": "+9.0%"
        }
      },
      {
        "partido": "Internazionale vs Torino",
        "hora": "12:00 PM",
        "principal": {
          "pick": "Torino ML",
          "cuota": 1.85,
          "ev": "+8.5%",
          "stake": "1.5%",
          "regla": "Local favorito (valor por defecto)"
        },
        "secundaria": {
          "pick": "Over 2.5 goles",
          "cuota": 1.85,
          "ev": "+7.5%",
          "stake": "1.0%",
          "regla": "Partido ofensivo"
        },
        "prop_jugador": {
          "jugador": "Jugador destacado",
          "prop": "Over 0.5 goles",
          "cuota": 2.1,
          "stake": "0.5%",
          "ev": "+9.0%"
        }
      },
      {
        "partido": "Juventus vs AC Milan",
        "hora": "02:45 PM",
        "principal": {
          "pick": "AC Milan ML",
          "cuota": 1.85,
          "ev": "+8.5%",
          "stake": "1.5%",
          "regla": "Local favorito (valor por defecto)"
        },
        "secundaria": {
          "pick": "Over 2.5 goles",
          "cuota": 1.85,
          "ev": "+7.5%",
          "stake": "1.0%",
          "regla": "Partido ofensivo"
        },
        "prop_jugador": {
          "jugador": "Jugador destacado",
          "prop": "Over 0.5 goles",
          "cuota": 2.1,
          "stake": "0.5%",
          "ev": "+9.0%"
        }
      }
    ]
  },
  {
    "name": "Ligue 1",
    "games": [
      {
        "partido": "Strasbourg vs Lorient",
        "hora": "09:00 AM",
        "principal": {
          "pick": "Lorient ML",
          "cuota": 1.85,
          "ev": "+8.5%",
          "stake": "1.5%",
          "regla": "Local favorito (valor por defecto)"
        },
        "secundaria": {
          "pick": "Over 2.5 goles",
          "cuota": 1.85,
          "ev": "+7.5%",
          "stake": "1.0%",
          "regla": "Partido ofensivo"
        },
        "prop_jugador": {
          "jugador": "Jugador destacado",
          "prop": "Over 0.5 goles",
          "cuota": 2.1,
          "stake": "0.5%",
          "ev": "+9.0%"
        }
      },
      {
        "partido": "Metz vs Le Havre AC",
        "hora": "11:15 AM",
        "principal": {
          "pick": "Le Havre AC ML",
          "cuota": 1.85,
          "ev": "+8.5%",
          "stake": "1.5%",
          "regla": "Local favorito (valor por defecto)"
        },
        "secundaria": {
          "pick": "Over 2.5 goles",
          "cuota": 1.85,
          "ev": "+7.5%",
          "stake": "1.0%",
          "regla": "Partido ofensivo"
        },
        "prop_jugador": {
          "jugador": "Jugador destacado",
          "prop": "Over 0.5 goles",
          "cuota": 2.1,
          "stake": "0.5%",
          "ev": "+9.0%"
        }
      },
      {
        "partido": "Lille vs Paris FC",
        "hora": "11:15 AM",
        "principal": {
          "pick": "Paris FC ML",
          "cuota": 1.85,
          "ev": "+8.5%",
          "stake": "1.5%",
          "regla": "Local favorito (valor por defecto)"
        },
        "secundaria": {
          "pick": "Over 2.5 goles",
          "cuota": 1.85,
          "ev": "+7.5%",
          "stake": "1.0%",
          "regla": "Partido ofensivo"
        },
        "prop_jugador": {
          "jugador": "Jugador destacado",
          "prop": "Over 0.5 goles",
          "cuota": 2.1,
          "stake": "0.5%",
          "ev": "+9.0%"
        }
      },
      {
        "partido": "Nantes vs Stade Rennais",
        "hora": "11:15 AM",
        "principal": {
          "pick": "Stade Rennais ML",
          "cuota": 1.85,
          "ev": "+8.5%",
          "stake": "1.5%",
          "regla": "Local favorito (valor por defecto)"
        },
        "secundaria": {
          "pick": "Over 2.5 goles",
          "cuota": 1.85,
          "ev": "+7.5%",
          "stake": "1.0%",
          "regla": "Partido ofensivo"
        },
        "prop_jugador": {
          "jugador": "Jugador destacado",
          "prop": "Over 0.5 goles",
          "cuota": 2.1,
          "stake": "0.5%",
          "ev": "+9.0%"
        }
      },
      {
        "partido": "Nice vs Marseille",
        "hora": "02:45 PM",
        "principal": {
          "pick": "Marseille ML",
          "cuota": 1.85,
          "ev": "+8.5%",
          "stake": "1.5%",
          "regla": "Local favorito (valor por defecto)"
        },
        "secundaria": {
          "pick": "Over 2.5 goles",
          "cuota": 1.85,
          "ev": "+7.5%",
          "stake": "1.0%",
          "regla": "Partido ofensivo"
        },
        "prop_jugador": {
          "jugador": "Jugador destacado",
          "prop": "Over 0.5 goles",
          "cuota": 2.1,
          "stake": "0.5%",
          "ev": "+9.0%"
        }
      }
    ]
  },
  {
    "name": "Eredivisie",
    "games": [
      {
        "partido": "FC Utrecht vs Excelsior",
        "hora": "06:15 AM",
        "principal": {
          "pick": "Excelsior ML",
          "cuota": 1.85,
          "ev": "+8.5%",
          "stake": "1.5%",
          "regla": "Local favorito (valor por defecto)"
        },
        "secundaria": {
          "pick": "Over 2.5 goles",
          "cuota": 1.85,
          "ev": "+7.5%",
          "stake": "1.0%",
          "regla": "Partido ofensivo"
        },
        "prop_jugador": {
          "jugador": "Jugador destacado",
          "prop": "Over 0.5 goles",
          "cuota": 2.1,
          "stake": "0.5%",
          "ev": "+9.0%"
        }
      },
      {
        "partido": "FC Volendam vs Heracles Almelo",
        "hora": "08:30 AM",
        "principal": {
          "pick": "Heracles Almelo ML",
          "cuota": 1.85,
          "ev": "+8.5%",
          "stake": "1.5%",
          "regla": "Local favorito (valor por defecto)"
        },
        "secundaria": {
          "pick": "Over 2.5 goles",
          "cuota": 1.85,
          "ev": "+7.5%",
          "stake": "1.0%",
          "regla": "Partido ofensivo"
        },
        "prop_jugador": {
          "jugador": "Jugador destacado",
          "prop": "Over 0.5 goles",
          "cuota": 2.1,
          "stake": "0.5%",
          "ev": "+9.0%"
        }
      }
    ]
  },
  {
    "name": "Primeira Liga",
    "games": [
      {
        "partido": "FC Famalicao vs Estoril",
        "hora": "10:30 AM",
        "principal": {
          "pick": "Estoril ML",
          "cuota": 1.85,
          "ev": "+8.5%",
          "stake": "1.5%",
          "regla": "Local favorito (valor por defecto)"
        },
        "secundaria": {
          "pick": "Over 2.5 goles",
          "cuota": 1.85,
          "ev": "+7.5%",
          "stake": "1.0%",
          "regla": "Partido ofensivo"
        },
        "prop_jugador": {
          "jugador": "Jugador destacado",
          "prop": "Over 0.5 goles",
          "cuota": 2.1,
          "stake": "0.5%",
          "ev": "+9.0%"
        }
      },
      {
        "partido": "FC Porto vs Estrela",
        "hora": "01:00 PM",
        "principal": {
          "pick": "Estrela ML",
          "cuota": 1.85,
          "ev": "+8.5%",
          "stake": "1.5%",
          "regla": "Local favorito (valor por defecto)"
        },
        "secundaria": {
          "pick": "Over 2.5 goles",
          "cuota": 1.85,
          "ev": "+7.5%",
          "stake": "1.0%",
          "regla": "Partido ofensivo"
        },
        "prop_jugador": {
          "jugador": "Jugador destacado",
          "prop": "Over 0.5 goles",
          "cuota": 2.1,
          "stake": "0.5%",
          "ev": "+9.0%"
        }
      },
      {
        "partido": "Braga vs Santa Clara",
        "hora": "01:00 PM",
        "principal": {
          "pick": "Santa Clara ML",
          "cuota": 1.85,
          "ev": "+8.5%",
          "stake": "1.5%",
          "regla": "Local favorito (valor por defecto)"
        },
        "secundaria": {
          "pick": "Over 2.5 goles",
          "cuota": 1.85,
          "ev": "+7.5%",
          "stake": "1.0%",
          "regla": "Partido ofensivo"
        },
        "prop_jugador": {
          "jugador": "Jugador destacado",
          "prop": "Over 0.5 goles",
          "cuota": 2.1,
          "stake": "0.5%",
          "ev": "+9.0%"
        }
      },
      {
        "partido": "Sporting CP vs AVS",
        "hora": "03:30 PM",
        "principal": {
          "pick": "AVS ML",
          "cuota": 1.85,
          "ev": "+8.5%",
          "stake": "1.5%",
          "regla": "Local favorito (valor por defecto)"
        },
        "secundaria": {
          "pick": "Over 2.5 goles",
          "cuota": 1.85,
          "ev": "+7.5%",
          "stake": "1.0%",
          "regla": "Partido ofensivo"
        },
        "prop_jugador": {
          "jugador": "Jugador destacado",
          "prop": "Over 0.5 goles",
          "cuota": 2.1,
          "stake": "0.5%",
          "ev": "+9.0%"
        }
      }
    ]
  },
  {
    "name": "Bundesliga",
    "games": [
      {
        "partido": "Werder Bremen vs VfB Stuttgart",
        "hora": "09:30 AM",
        "principal": {
          "pick": "VfB Stuttgart ML",
          "cuota": 1.85,
          "ev": "+8.5%",
          "stake": "1.5%",
          "regla": "Local favorito (valor por defecto)"
        },
        "secundaria": {
          "pick": "Over 2.5 goles",
          "cuota": 1.85,
          "ev": "+7.5%",
          "stake": "1.0%",
          "regla": "Partido ofensivo"
        },
        "prop_jugador": {
          "jugador": "Jugador destacado",
          "prop": "Over 0.5 goles",
          "cuota": 2.1,
          "stake": "0.5%",
          "ev": "+9.0%"
        }
      },
      {
        "partido": "SC Freiburg vs Borussia Dortmund",
        "hora": "11:30 AM",
        "principal": {
          "pick": "Borussia Dortmund ML",
          "cuota": 1.85,
          "ev": "+8.5%",
          "stake": "1.5%",
          "regla": "Local favorito (valor por defecto)"
        },
        "secundaria": {
          "pick": "Over 2.5 goles",
          "cuota": 1.85,
          "ev": "+7.5%",
          "stake": "1.0%",
          "regla": "Partido ofensivo"
        },
        "prop_jugador": {
          "jugador": "Jugador destacado",
          "prop": "Over 0.5 goles",
          "cuota": 2.1,
          "stake": "0.5%",
          "ev": "+9.0%"
        }
      }
    ]
  },
  {
    "name": "MLS",
    "games": [
      {
        "partido": "Real Salt Lake vs LA Galaxy",
        "hora": "07:00 PM",
        "principal": {
          "pick": "LA Galaxy ML",
          "cuota": 1.85,
          "ev": "+8.5%",
          "stake": "1.5%",
          "regla": "Local favorito (valor por defecto)"
        },
        "secundaria": {
          "pick": "Over 2.5 goles",
          "cuota": 1.85,
          "ev": "+7.5%",
          "stake": "1.0%",
          "regla": "Partido ofensivo"
        },
        "prop_jugador": {
          "jugador": "Jugador destacado",
          "prop": "Over 0.5 goles",
          "cuota": 2.1,
          "stake": "0.5%",
          "ev": "+9.0%"
        }
      }
    ]
  },
  {
    "name": "Champions League",
    "games": [
      {
        "partido": "Bayern Munich vs Paris Saint-Germain",
        "hora": "03:00 PM",
        "principal": {
          "pick": "Paris Saint-Germain ML",
          "cuota": 1.85,
          "ev": "+8.5%",
          "stake": "1.5%",
          "regla": "Local favorito (valor por defecto)"
        },
        "secundaria": {
          "pick": "Over 2.5 goles",
          "cuota": 1.85,
          "ev": "+7.5%",
          "stake": "1.0%",
          "regla": "Partido ofensivo"
        },
        "prop_jugador": {
          "jugador": "Jugador destacado",
          "prop": "Over 0.5 goles",
          "cuota": 2.1,
          "stake": "0.5%",
          "ev": "+9.0%"
        }
      }
    ]
  },
  {
    "name": "Europa League",
    "games": [
      {
        "partido": "SC Freiburg vs Braga",
        "hora": "03:00 PM",
        "principal": {
          "pick": "Braga ML",
          "cuota": 1.85,
          "ev": "+8.5%",
          "stake": "1.5%",
          "regla": "Local favorito (valor por defecto)"
        },
        "secundaria": {
          "pick": "Over 2.5 goles",
          "cuota": 1.85,
          "ev": "+7.5%",
          "stake": "1.0%",
          "regla": "Partido ofensivo"
        },
        "prop_jugador": {
          "jugador": "Jugador destacado",
          "prop": "Over 0.5 goles",
          "cuota": 2.1,
          "stake": "0.5%",
          "ev": "+9.0%"
        }
      },
      {
        "partido": "Aston Villa vs Nottingham Forest",
        "hora": "03:00 PM",
        "principal": {
          "pick": "Nottingham Forest ML",
          "cuota": 1.85,
          "ev": "+8.5%",
          "stake": "1.5%",
          "regla": "Local favorito (valor por defecto)"
        },
        "secundaria": {
          "pick": "Over 2.5 goles",
          "cuota": 1.85,
          "ev": "+7.5%",
          "stake": "1.0%",
          "regla": "Partido ofensivo"
        },
        "prop_jugador": {
          "jugador": "Jugador destacado",
          "prop": "Over 0.5 goles",
          "cuota": 2.1,
          "stake": "0.5%",
          "ev": "+9.0%"
        }
      }
    ]
  }
];
const oldResults = [];
const mejores = [
  "\u2705 MLB con datos reales (lanzadores y ERAs del 26/04)",
  "\u2705 Picks principales basados en comparaci\u00f3n de ERAs",
  "\u2705 Picks secundarios (Over/Under) seg\u00fan suma de ERAs",
  "\u2705 Props de jugador: lanzador con mejor ERA para Over 5.5 Ks",
  "\u2705 F\u00fatbol con ESPN + API-Football (todas las ligas europeas)"
];
const parlaysData = [];
const todayResultsArray = {};
