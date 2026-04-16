"""Constants for the Andorra Meteo integration."""

DOMAIN = "andorra_meteo"

# Config entry types
ENTRY_TYPE_STATION = "station"
ENTRY_TYPE_AVALANCHE = "avalanche"

CONF_ENTRY_TYPE = "entry_type"
CONF_STATION_CODE = "station_code"
CONF_STATION_NAME = "station_name"
CONF_PARISH = "parish"

# Update intervals (seconds)
SCAN_INTERVAL_STATION = 1800   # 30 minutes
SCAN_INTERVAL_AVALANCHE = 3600  # 60 minutes

# Meteoclimatic RSS feed base URL
METEOCLIMATIC_FEED_URL = "https://www.meteoclimatic.net/feed/rss/{}"

# Meteo.ad avalanche bulletin URL
AVALANCHE_URL = "https://www.meteo.ad/en/snowstate"

# Avalanche danger level names (European scale, index 0 unused)
AVALANCHE_LEVEL_NAMES = {
    1: "Feble",
    2: "Limitat",
    3: "Marcat",
    4: "Fort",
    5: "Molt fort",
}

AVALANCHE_LEVEL_NAMES_EN = {
    1: "Low",
    2: "Moderate",
    3: "Considerable",
    4: "High",
    5: "Very High",
}

# Danger level at which binary_sensor triggers (≥ WARN_LEVEL → True)
AVALANCHE_WARN_LEVEL = 3

# -----------------------------------------------------------------------
# Andorra parishes and their verified Meteoclimatic stations
# Structure: { parish_key: { "name": <catalan name>, "stations": [ {...} ] } }
# Codes verified from meteoclimatic.net/perfil/<code> URLs provided by user.
# Stations NOT listed here simply do not exist in Meteoclimatic for that parish.
# -----------------------------------------------------------------------
PARISHES = {
    "canillo": {
        "name": "Canillo",
        "stations": [
            {
                "code": "ADAND9000000100000A",
                "name": "Els Plans de Canillo",
                "location": "Els Plans de Canillo, 1.780 m",
            },
        ],
    },
    "encamp": {
        "name": "Encamp",
        "stations": [
            {
                "code": "ADAND9000000200000A",
                "name": "Encamp",
                "location": "Encamp, 1.270 m",
            },
        ],
    },
    "ordino": {
        "name": "Ordino",
        "stations": [
            {
                "code": "ADAND9000000300000A",
                "name": "La Cortinada",
                "location": "La Cortinada, 1.330 m",
            },
        ],
    },
    # La Massana: no verified station found — omitted until confirmed
    "sant_julia": {
        "name": "Sant Julià de Lòria",
        "stations": [
            {
                "code": "ADAND9000000600000A",
                "name": "Certés",
                "location": "Certés, 1.350 m",
            },
        ],
    },
    "escaldes": {
        "name": "Escaldes-Engordany",
        "stations": [
            {
                "code": "ADAND9000000700000B",
                "name": "Escaldes-Engordany — Centre",
                "location": "Escaldes-Engordany, 1.050 m",
            },
            {
                "code": "ADAND9000000700000D",
                "name": "Escaldes-Engordany — Sa Calma",
                "location": "Sa Calma, 1.180 m",
            },
        ],
    },
}

# Flat lookup: code → station info (includes parish name and location)
STATION_BY_CODE: dict[str, dict] = {}
for _parish_key, _parish in PARISHES.items():
    for _st in _parish["stations"]:
        STATION_BY_CODE[_st["code"]] = {
            "code": _st["code"],
            "name": _st["name"],
            "location": _st["location"],
            "parish": _parish["name"],
        }
        