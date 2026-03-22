#!/usr/bin/env python3
"""
add_routes.py  -  Add ~475 realistic hub-and-spoke routes to routen.csv

- Reads  tools/decoded/routen.csv  (CR-only line endings)
- Merges new routes, skipping exact duplicates
- Validates every city name against the current city.csv
- Writes result back to tools/decoded/routen.csv  (CR-only, matching original)

Run from the repo root:
    python tools/add_routes.py
"""

import os, sys

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
ROUTES_CSV  = os.path.join(SCRIPT_DIR, "decoded", "routen.csv")
CITIES_CSV  = os.path.join(SCRIPT_DIR, "decoded", "city.csv")

# ---------------------------------------------------------------------------
# New routes  (ebene, city_a, city_b, miete, faktor)
# Each entry is ONE direction — the game engine automatically creates both.
# Ebene 1 = regional / medium-haul
# Ebene 2 = long-haul intercontinental
# ---------------------------------------------------------------------------
NEW_ROUTES = [

    # ════════════════════════════════════════════════════════════════════════
    # TIER 1 MEGAHUBS — connections to existing game hubs
    # ════════════════════════════════════════════════════════════════════════

    # Dubai → existing hubs
    (2, "Dubai", "London",           900000, 1.8),
    (2, "Dubai", "Frankfurt",        850000, 1.5),
    (2, "Dubai", "New York",         950000, 1.6),
    (2, "Dubai", "Singapore",        700000, 1.5),
    (2, "Dubai", "Sydney",           850000, 1.4),
    (1, "Dubai", "Riyadh",           300000, 1.3),
    (1, "Dubai", "Delhi",            400000, 1.5),
    (1, "Dubai", "Nairobi",          500000, 1.2),
    (1, "Dubai", "Cairo",            450000, 1.2),
    (2, "Dubai", "Paris",            870000, 1.4),
    (2, "Dubai", "Bangkok",          650000, 1.3),
    (2, "Dubai", "Tokyo",            950000, 1.2),

    # Istanbul → existing hubs
    (2, "Istanbul", "London",        800000, 1.5),
    (2, "Istanbul", "Frankfurt",     700000, 1.4),
    (1, "Istanbul", "Moscow",        500000, 1.2),
    (1, "Istanbul", "Cairo",         400000, 1.3),
    (2, "Istanbul", "New York",      900000, 1.4),
    (1, "Istanbul", "Athens",        300000, 1.2),
    (1, "Istanbul", "Vienna",        400000, 1.1),
    (1, "Istanbul", "Warsaw",        400000, 1.0),
    (1, "Istanbul", "Kiev",          400000, 1.0),
    (2, "Istanbul", "Bangkok",       700000, 1.1),
    (2, "Istanbul", "Singapore",     800000, 1.0),

    # Shanghai → existing hubs
    (1, "Shanghai", "Tokyo",         600000, 1.5),
    (1, "Shanghai", "Seoul",         500000, 1.4),
    (1, "Shanghai", "Hong Kong",     400000, 1.3),
    (1, "Shanghai", "Peking",        300000, 1.8),
    (2, "Shanghai", "Singapore",     700000, 1.3),
    (2, "Shanghai", "London",       1000000, 1.3),
    (2, "Shanghai", "Frankfurt",     950000, 1.2),
    (2, "Shanghai", "Los Angeles",   900000, 1.2),
    (2, "Shanghai", "Sydney",        850000, 1.1),
    (1, "Shanghai", "Osaka",         400000, 1.2),

    # Mumbai → existing hubs
    (2, "Mumbai", "London",          850000, 1.5),
    (2, "Mumbai", "Frankfurt",       800000, 1.3),
    (1, "Mumbai", "Singapore",       600000, 1.3),
    (1, "Mumbai", "Delhi",           300000, 1.8),
    (1, "Mumbai", "Bangkok",         500000, 1.2),
    (2, "Mumbai", "New York",        900000, 1.2),

    # Sao Paulo → existing hubs
    (2, "Sao Paulo", "London",      1000000, 1.4),
    (2, "Sao Paulo", "Frankfurt",   1000000, 1.3),
    (2, "Sao Paulo", "New York",     900000, 1.4),
    (2, "Sao Paulo", "Miami",        800000, 1.5),
    (1, "Sao Paulo", "Rio de Janeiro", 200000, 2.0),
    (1, "Sao Paulo", "Buenos Aires", 300000, 1.5),
    (1, "Sao Paulo", "Lima",         400000, 1.2),
    (1, "Sao Paulo", "Santiago de Chile", 350000, 1.3),
    (1, "Sao Paulo", "Caracas",      400000, 1.1),

    # Kuala Lumpur → existing hubs
    (1, "Kuala Lumpur", "Singapore", 200000, 1.5),
    (1, "Kuala Lumpur", "Bangkok",   300000, 1.3),
    (2, "Kuala Lumpur", "Sydney",    700000, 1.2),
    (2, "Kuala Lumpur", "London",    900000, 1.2),
    (2, "Kuala Lumpur", "Delhi",     600000, 1.1),
    (1, "Kuala Lumpur", "Manila",    400000, 1.1),
    (2, "Kuala Lumpur", "Tokyo",     800000, 1.0),

    # Addis Ababa → existing hubs
    (2, "Addis Ababa", "London",     750000, 1.2),
    (2, "Addis Ababa", "Frankfurt",  700000, 1.1),
    (1, "Addis Ababa", "Cairo",      400000, 1.2),
    (1, "Addis Ababa", "Nairobi",    250000, 1.3),
    (1, "Addis Ababa", "Johannesburg", 500000, 1.1),
    (2, "Addis Ababa", "Delhi",      600000, 0.9),

    # Lagos → existing hubs
    (2, "Lagos", "London",           750000, 1.3),
    (2, "Lagos", "Paris",            700000, 1.2),
    (1, "Lagos", "Johannesburg",     500000, 1.1),
    (1, "Lagos", "Nairobi",          500000, 1.0),
    (1, "Lagos", "Cairo",            500000, 1.0),
    (1, "Lagos", "Dakar",            300000, 1.0),

    # Casablanca → existing hubs
    (1, "Casablanca", "Paris",       500000, 1.3),
    (2, "Casablanca", "London",      600000, 1.1),
    (1, "Casablanca", "Madrid",      350000, 1.2),
    (1, "Casablanca", "Dakar",       350000, 1.0),
    (1, "Casablanca", "Cairo",       450000, 1.0),
    (2, "Casablanca", "New York",    800000, 1.0),

    # Doha → existing hubs
    (2, "Doha", "London",            850000, 1.5),
    (2, "Doha", "Frankfurt",         800000, 1.3),
    (2, "Doha", "New York",          900000, 1.4),
    (2, "Doha", "Singapore",         700000, 1.3),
    (2, "Doha", "Sydney",            850000, 1.2),
    (1, "Doha", "Riyadh",            250000, 1.1),
    (1, "Doha", "Cairo",             400000, 1.2),
    (2, "Doha", "Bangkok",           650000, 1.1),

    # Jakarta → existing hubs
    (1, "Jakarta", "Singapore",      300000, 1.4),
    (1, "Jakarta", "Bangkok",        500000, 1.2),
    (2, "Jakarta", "Sydney",         600000, 1.2),
    (2, "Jakarta", "Tokyo",          700000, 1.1),
    (2, "Jakarta", "Seoul",          750000, 1.0),

    # ════════════════════════════════════════════════════════════════════════
    # TIER 1 CROSS-HUB & T1→T2 SPOKES
    # ════════════════════════════════════════════════════════════════════════

    (1, "Dubai", "Istanbul",         600000, 1.4),
    (1, "Dubai", "Mumbai",           400000, 1.5),
    (1, "Dubai", "Doha",             200000, 1.0),
    (1, "Dubai", "Abu Dhabi",        150000, 1.0),
    (1, "Dubai", "Muscat",           250000, 0.9),
    (1, "Dubai", "Kuwait City",      300000, 1.0),
    (1, "Dubai", "Manama",           250000, 0.9),
    (1, "Dubai", "Amman",            350000, 1.0),
    (1, "Dubai", "Tehran",           350000, 1.0),
    (1, "Dubai", "Karachi",          400000, 1.0),
    (1, "Dubai", "Addis Ababa",      500000, 1.2),
    (1, "Dubai", "Colombo",          550000, 0.9),
    (1, "Dubai", "Islamabad",        600000, 0.9),
    (1, "Dubai", "Kabul",            600000, 0.7),
    (1, "Dubai", "Djibouti",         500000, 0.7),
    (1, "Dubai", "Khartoum",         600000, 0.7),
    (1, "Dubai", "Bangalore",        500000, 1.0),
    (1, "Dubai", "Dhaka",            500000, 0.9),

    (1, "Istanbul", "Amman",         350000, 1.1),
    (1, "Istanbul", "Baghdad",       400000, 1.0),
    (1, "Istanbul", "Tehran",        350000, 1.0),
    (1, "Istanbul", "Baku",          300000, 0.9),
    (1, "Istanbul", "Tbilisi",       300000, 0.9),
    (1, "Istanbul", "Tashkent",      500000, 0.8),
    (1, "Istanbul", "Beirut",        400000, 1.0),
    (1, "Istanbul", "Damascus",      500000, 0.8),
    (1, "Istanbul", "Yerevan",       400000, 0.8),
    (1, "Istanbul", "Astana",        700000, 0.7),
    (1, "Istanbul", "Bucharest",     400000, 1.1),
    (1, "Istanbul", "Belgrade",      500000, 1.0),
    (1, "Istanbul", "Sofia",         400000, 1.0),

    (1, "Shanghai", "Taipei",        300000, 1.3),
    (1, "Shanghai", "Guangzhou",     250000, 1.5),
    (1, "Shanghai", "Chengdu",       300000, 1.3),
    (1, "Shanghai", "Nagoya",        400000, 1.0),

    (1, "Mumbai", "Karachi",         350000, 1.1),
    (1, "Mumbai", "Colombo",         350000, 1.0),
    (1, "Mumbai", "Bangalore",       200000, 1.6),
    (1, "Mumbai", "Dhaka",           400000, 1.0),
    (1, "Mumbai", "Kathmandu",       350000, 0.9),
    (1, "Mumbai", "Muscat",          350000, 1.1),
    (1, "Mumbai", "Dubai",           400000, 1.5),

    (1, "Sao Paulo", "Bogota",       500000, 1.3),
    (1, "Sao Paulo", "Brasilia",     250000, 1.5),
    (1, "Sao Paulo", "Asuncion",     250000, 0.9),
    (1, "Sao Paulo", "Montevideo",   300000, 1.0),
    (1, "Sao Paulo", "Quito",        450000, 1.0),

    (1, "Kuala Lumpur", "Jakarta",   350000, 1.4),
    (1, "Kuala Lumpur", "Ho Chi Minh City", 400000, 1.2),
    (1, "Kuala Lumpur", "Bali",      350000, 1.2),
    (1, "Kuala Lumpur", "Colombo",   400000, 1.0),
    (1, "Kuala Lumpur", "Phnom Penh", 350000, 0.9),
    (1, "Kuala Lumpur", "Phuket",    250000, 1.1),
    (1, "Kuala Lumpur", "Bandar Seri Begawan", 200000, 0.7),
    (2, "Kuala Lumpur", "Dubai",     700000, 1.2),
    (1, "Kuala Lumpur", "Hanoi",     600000, 0.9),
    (1, "Kuala Lumpur", "Chiang Mai", 500000, 0.7),
    (1, "Kuala Lumpur", "Dhaka",     600000, 0.8),

    (1, "Addis Ababa", "Dubai",      500000, 1.2),
    (1, "Addis Ababa", "Dar es Salaam", 300000, 1.0),
    (1, "Addis Ababa", "Khartoum",   250000, 0.8),
    (1, "Addis Ababa", "Kampala",    250000, 0.9),
    (1, "Addis Ababa", "Kigali",     300000, 0.9),
    (1, "Addis Ababa", "Djibouti",   200000, 0.7),
    (1, "Addis Ababa", "Mogadishu",  250000, 0.6),
    (1, "Addis Ababa", "Asmara",     200000, 0.6),
    (2, "Addis Ababa", "Paris",      800000, 1.0),

    (1, "Lagos", "Accra",            200000, 1.2),
    (1, "Lagos", "Abuja",            150000, 1.3),
    (1, "Lagos", "Casablanca",       400000, 1.0),
    (1, "Lagos", "Addis Ababa",      500000, 0.9),
    (1, "Lagos", "Kinshasa",         350000, 0.8),
    (1, "Lagos", "Libreville",       250000, 0.7),
    (1, "Lagos", "Lome",             150000, 0.8),
    (1, "Lagos", "Cotonou",          150000, 0.7),
    (1, "Lagos", "Yamoussoukro",     400000, 0.6),
    (1, "Lagos", "Ouagadougou",      500000, 0.6),
    (1, "Lagos", "NDjamena",         600000, 0.5),
    (1, "Lagos", "Bangui",           600000, 0.4),

    (1, "Casablanca", "Rabat",       100000, 0.8),
    (1, "Casablanca", "Algiers",     300000, 1.0),
    (1, "Casablanca", "Tripoli",     350000, 0.8),
    (1, "Casablanca", "Accra",       350000, 0.9),
    (1, "Casablanca", "Bamako",      350000, 0.7),
    (1, "Casablanca", "Marrakech",   150000, 1.2),
    (1, "Casablanca", "Nouakchott",  500000, 0.5),

    (1, "Doha", "Dubai",             200000, 1.0),
    (1, "Doha", "Mumbai",            450000, 1.3),
    (1, "Doha", "Karachi",           450000, 1.0),
    (1, "Doha", "Addis Ababa",       500000, 1.0),
    (1, "Doha", "Istanbul",          500000, 1.1),

    (1, "Jakarta", "Kuala Lumpur",   350000, 1.4),
    (1, "Jakarta", "Bali",           200000, 1.5),
    (1, "Jakarta", "Dili",           250000, 0.5),

    # ════════════════════════════════════════════════════════════════════════
    # TIER 2 — EUROPE
    # ════════════════════════════════════════════════════════════════════════

    # Lisbon
    (1, "Lisbon", "London",          500000, 1.2),
    (1, "Lisbon", "Madrid",          300000, 1.3),
    (1, "Lisbon", "Paris",           500000, 1.2),
    (1, "Lisbon", "Casablanca",      350000, 1.0),
    (1, "Lisbon", "Porto",           150000, 0.9),
    (2, "Lisbon", "New York",        800000, 1.1),
    (2, "Lisbon", "Sao Paulo",       900000, 1.0),

    # Milan
    (1, "Milan", "Rome",             300000, 1.2),
    (1, "Milan", "Frankfurt",        500000, 1.2),
    (1, "Milan", "Paris",            450000, 1.2),
    (1, "Milan", "London",           600000, 1.1),
    (1, "Milan", "Istanbul",         500000, 1.1),
    (2, "Milan", "New York",         800000, 1.1),
    (1, "Milan", "Cairo",            600000, 0.9),

    # Prague
    (1, "Prague", "Frankfurt",       400000, 1.0),
    (1, "Prague", "Vienna",          300000, 1.1),
    (1, "Prague", "London",          500000, 1.0),
    (1, "Prague", "Warsaw",          300000, 1.0),
    (1, "Prague", "Amsterdam",       400000, 1.0),

    # Budapest
    (1, "Budapest", "Vienna",        200000, 1.1),
    (1, "Budapest", "Frankfurt",     450000, 1.0),
    (1, "Budapest", "Warsaw",        350000, 0.9),
    (1, "Budapest", "Istanbul",      500000, 1.0),
    (1, "Budapest", "London",        600000, 1.0),

    # Bucharest
    (1, "Bucharest", "Vienna",       500000, 1.0),
    (1, "Bucharest", "Frankfurt",    600000, 0.9),
    (1, "Bucharest", "Warsaw",       500000, 0.9),
    (1, "Bucharest", "Kiev",         350000, 1.0),

    # Edinburgh
    (1, "Edinburgh", "London",       200000, 1.1),
    (1, "Edinburgh", "Amsterdam",    400000, 1.0),
    (1, "Edinburgh", "Reykjavik",    400000, 0.8),
    (1, "Edinburgh", "Dublin",       300000, 1.0),

    # Hamburg
    (1, "Hamburg", "Frankfurt",      300000, 1.0),
    (1, "Hamburg", "London",         400000, 1.0),
    (1, "Hamburg", "Amsterdam",      250000, 1.1),
    (1, "Hamburg", "Copenhagen",     200000, 1.1),

    # Manchester
    (1, "Manchester", "London",      200000, 1.1),
    (1, "Manchester", "Amsterdam",   350000, 1.0),
    (1, "Manchester", "Dublin",      250000, 1.1),
    (2, "Manchester", "New York",    700000, 1.1),

    # Tier-3 European capitals — each 2-3 connections
    (1, "Belgrade",     "Vienna",    500000, 0.9),
    (1, "Belgrade",     "Budapest",  300000, 0.9),

    (1, "Zagreb",       "Vienna",    400000, 0.9),
    (1, "Zagreb",       "Frankfurt", 600000, 0.8),
    (1, "Zagreb",       "Munich",    400000, 0.9),

    (1, "Bratislava",   "Vienna",    100000, 0.8),
    (1, "Bratislava",   "Prague",    200000, 0.8),
    (1, "Bratislava",   "Budapest",  100000, 0.8),

    (1, "Sofia",        "Athens",    400000, 0.9),
    (1, "Sofia",        "Vienna",    600000, 0.8),

    (1, "Sarajevo",     "Vienna",    600000, 0.8),
    (1, "Sarajevo",     "Belgrade",  300000, 0.8),

    (1, "Skopje",       "Athens",    400000, 0.8),
    (1, "Skopje",       "Belgrade",  300000, 0.8),

    (1, "Vilnius",      "Warsaw",    400000, 0.9),
    (1, "Vilnius",      "Stockholm", 500000, 0.8),
    (1, "Vilnius",      "Riga",      200000, 0.8),

    (1, "Riga",         "Warsaw",    450000, 0.9),
    (1, "Riga",         "Stockholm", 500000, 0.9),
    (1, "Riga",         "Tallinn",   200000, 0.8),

    (1, "Tallinn",      "Helsinki",  200000, 0.9),
    (1, "Tallinn",      "Stockholm", 400000, 0.8),

    (1, "Minsk",        "Moscow",    500000, 0.9),
    (1, "Minsk",        "Warsaw",    400000, 0.9),
    (1, "Minsk",        "Kiev",      300000, 0.9),

    (1, "Tirana",       "Rome",      500000, 0.8),
    (1, "Tirana",       "Athens",    400000, 0.9),

    (1, "Podgorica",    "Rome",      500000, 0.7),
    (1, "Podgorica",    "Belgrade",  200000, 0.7),

    (1, "Nicosia",      "Athens",    400000, 0.8),
    (1, "Nicosia",      "Beirut",    300000, 0.8),

    (1, "Valletta",     "Rome",      300000, 0.8),
    (1, "Valletta",     "Frankfurt", 600000, 0.7),
    (1, "Valletta",     "Tunisia",   250000, 0.7),

    (1, "Luxembourg City", "Frankfurt", 200000, 0.8),
    (1, "Luxembourg City", "Paris",  300000, 0.8),
    (1, "Luxembourg City", "Brussels", 200000, 0.8),

    (1, "Porto",        "Madrid",    300000, 0.8),
    (1, "Porto",        "London",    500000, 0.8),

    (1, "Seville",      "Madrid",    300000, 0.9),
    (1, "Seville",      "Lisbon",    200000, 0.9),
    (1, "Seville",      "Casablanca", 350000, 0.9),

    (1, "Cologne",      "Frankfurt", 150000, 0.9),
    (1, "Cologne",      "Amsterdam", 200000, 0.9),
    (1, "Cologne",      "London",    400000, 0.9),

    (1, "Dusseldorf",   "Frankfurt", 150000, 0.9),
    (1, "Dusseldorf",   "Amsterdam", 150000, 1.0),
    (1, "Dusseldorf",   "London",    400000, 1.0),

    (1, "Lyon",         "Paris",     200000, 0.9),
    (1, "Lyon",         "Frankfurt", 400000, 0.8),
    (1, "Lyon",         "Rome",      400000, 0.8),

    (1, "Nice",         "Paris",     300000, 0.9),
    (1, "Nice",         "Rome",      300000, 0.9),
    (1, "Nice",         "Barcelona", 300000, 0.9),

    (1, "Venice",       "Rome",      300000, 0.8),
    (1, "Venice",       "Frankfurt", 500000, 0.8),
    (1, "Venice",       "Munich",    400000, 0.8),

    (1, "Florence",     "Rome",      200000, 0.8),
    (1, "Florence",     "Milan",     200000, 0.9),

    (1, "Naples",       "Rome",      200000, 0.9),
    (1, "Naples",       "Tunisia",   250000, 0.7),

    # ════════════════════════════════════════════════════════════════════════
    # TIER 2 — CAUCASUS & EASTERN EUROPE
    # ════════════════════════════════════════════════════════════════════════

    (1, "Tbilisi",      "Moscow",    700000, 0.9),
    (1, "Tbilisi",      "Warsaw",    700000, 0.8),
    (1, "Tbilisi",      "Yerevan",   200000, 0.8),
    (1, "Tbilisi",      "Baku",      200000, 0.8),
    (1, "Tbilisi",      "Dubai",     500000, 0.9),

    (1, "Baku",         "Moscow",    700000, 0.9),
    (1, "Baku",         "Tehran",    400000, 0.8),
    (1, "Baku",         "Dubai",     500000, 0.8),

    (1, "Yerevan",      "Moscow",    700000, 0.9),
    (1, "Yerevan",      "Dubai",     500000, 0.8),

    # ════════════════════════════════════════════════════════════════════════
    # TIER 2 — MIDDLE EAST
    # ════════════════════════════════════════════════════════════════════════

    (1, "Amman",        "Cairo",     350000, 1.1),
    (1, "Amman",        "Riyadh",    350000, 1.0),
    (1, "Amman",        "Beirut",    200000, 1.0),

    (1, "Tehran",       "Moscow",    700000, 0.9),
    (1, "Tehran",       "Tashkent",  450000, 0.8),
    (1, "Tehran",       "Baghdad",   400000, 1.0),
    (1, "Tehran",       "Kabul",     500000, 0.7),

    (1, "Baghdad",      "Amman",     400000, 0.9),

    (1, "Beirut",       "Cairo",     350000, 1.0),
    (1, "Beirut",       "Amman",     200000, 1.0),

    (1, "Kuwait City",  "Riyadh",    300000, 1.0),
    (1, "Kuwait City",  "Cairo",     500000, 0.9),
    (2, "Kuwait City",  "London",    800000, 0.9),

    (1, "Abu Dhabi",    "Riyadh",    300000, 1.0),
    (1, "Manama",       "Riyadh",    250000, 0.9),
    (1, "Muscat",       "Karachi",   400000, 0.8),
    (1, "Muscat",       "Riyadh",    450000, 0.8),

    (1, "Damascus",     "Beirut",    200000, 0.8),
    (1, "Damascus",     "Amman",     200000, 0.8),

    (1, "Jerusalem",    "Amman",     200000, 0.8),
    (1, "Jerusalem",    "Cairo",     400000, 0.8),

    # ════════════════════════════════════════════════════════════════════════
    # TIER 2 — SOUTH & CENTRAL ASIA
    # ════════════════════════════════════════════════════════════════════════

    (1, "Karachi",      "Islamabad", 200000, 1.1),
    (1, "Karachi",      "Riyadh",    400000, 1.0),
    (1, "Karachi",      "Delhi",     500000, 1.0),

    (1, "Islamabad",    "Kabul",     300000, 0.9),
    (1, "Islamabad",    "Delhi",     400000, 1.0),
    (1, "Islamabad",    "Tashkent",  500000, 0.7),

    (1, "Bangalore",    "Delhi",     300000, 1.3),
    (1, "Bangalore",    "Singapore", 500000, 1.0),

    (1, "Colombo",      "Male",      300000, 0.9),
    (1, "Colombo",      "Singapore", 500000, 1.0),

    (1, "Dhaka",        "Delhi",     400000, 1.0),
    (1, "Dhaka",        "Bangkok",   500000, 0.9),

    (1, "Kathmandu",    "Delhi",     350000, 0.9),
    (1, "Kathmandu",    "Bangkok",   500000, 0.8),
    (1, "Kathmandu",    "Chengdu",   450000, 0.7),

    (1, "Kabul",        "Dubai",     600000, 0.7),

    (1, "Tashkent",     "Moscow",    700000, 0.9),
    (1, "Tashkent",     "Bishkek",   200000, 0.7),

    (1, "Astana",       "Moscow",    700000, 0.9),
    (2, "Astana",       "Frankfurt", 1000000, 0.7),
    (1, "Astana",       "Tashkent",  400000, 0.7),
    (1, "Astana",       "Peking",    800000, 0.7),

    (1, "Bishkek",      "Astana",    400000, 0.7),
    (1, "Bishkek",      "Moscow",    700000, 0.7),

    (1, "Ashgabat",     "Tashkent",  400000, 0.7),
    (1, "Ashgabat",     "Tehran",    400000, 0.7),

    (1, "Dushanbe",     "Tashkent",  300000, 0.7),
    (1, "Dushanbe",     "Moscow",    800000, 0.6),
    (1, "Dushanbe",     "Islamabad", 400000, 0.6),

    (1, "Thimphu",      "Delhi",     500000, 0.5),
    (1, "Thimphu",      "Kathmandu", 300000, 0.5),

    # ════════════════════════════════════════════════════════════════════════
    # TIER 2 — EAST & SOUTHEAST ASIA
    # ════════════════════════════════════════════════════════════════════════

    (1, "Hanoi",        "Bangkok",   500000, 1.1),
    (1, "Hanoi",        "Singapore", 600000, 1.0),
    (1, "Hanoi",        "Ho Chi Minh City", 300000, 1.2),
    (1, "Hanoi",        "Seoul",     700000, 1.0),
    (1, "Hanoi",        "Peking",    600000, 1.0),

    (1, "Ho Chi Minh City", "Singapore", 400000, 1.2),
    (1, "Ho Chi Minh City", "Bangkok",   350000, 1.2),
    (1, "Ho Chi Minh City", "Tokyo",     700000, 1.0),
    (1, "Ho Chi Minh City", "Seoul",     700000, 1.0),

    (1, "Taipei",       "Tokyo",     500000, 1.3),
    (1, "Taipei",       "Hong Kong", 350000, 1.2),
    (1, "Taipei",       "Seoul",     500000, 1.1),
    (1, "Taipei",       "Singapore", 600000, 1.0),

    (1, "Guangzhou",    "Peking",    400000, 1.3),
    (1, "Guangzhou",    "Hong Kong", 200000, 1.5),
    (1, "Guangzhou",    "Singapore", 500000, 1.1),
    (1, "Guangzhou",    "Bangkok",   500000, 1.0),

    (1, "Chengdu",      "Peking",    500000, 1.1),
    (1, "Chengdu",      "Bangkok",   500000, 0.9),

    (1, "Busan",        "Seoul",     200000, 1.0),
    (1, "Busan",        "Tokyo",     400000, 1.1),
    (1, "Busan",        "Osaka",     300000, 1.0),

    (1, "Nagoya",       "Tokyo",     200000, 1.2),
    (1, "Nagoya",       "Seoul",     500000, 1.0),

    (1, "Naypyidaw",    "Bangkok",   600000, 0.6),
    (1, "Naypyidaw",    "Kuala Lumpur", 700000, 0.5),

    (1, "Vientiane",    "Bangkok",   400000, 0.7),
    (1, "Vientiane",    "Hanoi",     300000, 0.7),

    (1, "Phnom Penh",   "Bangkok",   400000, 0.7),
    (1, "Phnom Penh",   "Ho Chi Minh City", 200000, 0.8),
    (1, "Phnom Penh",   "Singapore", 600000, 0.7),

    (1, "Chiang Mai",   "Bangkok",   200000, 0.9),

    (1, "Phuket",       "Bangkok",   300000, 1.0),
    (1, "Phuket",       "Singapore", 500000, 1.0),

    (1, "Bali",         "Singapore", 400000, 1.2),
    (1, "Bali",         "Sydney",    500000, 0.9),
    (1, "Bali",         "Perth",     300000, 1.0),

    (1, "Bandar Seri Begawan", "Singapore", 500000, 0.6),

    (1, "Ulaanbaatar",  "Peking",    700000, 0.6),
    (1, "Ulaanbaatar",  "Moscow",    700000, 0.6),

    (1, "Pyongyang",    "Peking",    700000, 0.4),
    (1, "Pyongyang",    "Moscow",   1000000, 0.4),

    # ════════════════════════════════════════════════════════════════════════
    # TIER 2 — AFRICA
    # ════════════════════════════════════════════════════════════════════════

    (1, "Accra",        "London",    700000, 1.1),
    (1, "Accra",        "Dakar",     350000, 0.9),
    (1, "Accra",        "Addis Ababa", 600000, 0.8),
    (1, "Accra",        "Abuja",     200000, 1.0),

    (1, "Abuja",        "Addis Ababa", 600000, 0.7),
    (1, "Abuja",        "Casablanca", 500000, 0.8),

    (1, "Kinshasa",     "Nairobi",   600000, 0.7),
    (1, "Kinshasa",     "Johannesburg", 500000, 0.8),
    (1, "Kinshasa",     "Luanda",    250000, 0.7),
    (2, "Kinshasa",     "Paris",     900000, 0.7),
    (1, "Kinshasa",     "Brazzaville", 100000, 0.6),

    (1, "Luanda",       "Johannesburg", 600000, 0.8),
    (1, "Luanda",       "Lisbon",    800000, 0.8),
    (1, "Luanda",       "Addis Ababa", 600000, 0.6),

    (1, "Algiers",      "Tunisia",   300000, 1.0),
    (1, "Algiers",      "Paris",     500000, 1.1),
    (1, "Algiers",      "Madrid",    500000, 0.9),
    (1, "Algiers",      "Cairo",     600000, 0.8),

    (1, "Kampala",      "Nairobi",   300000, 0.9),
    (1, "Kampala",      "Kigali",    200000, 0.8),
    (1, "Kampala",      "Dar es Salaam", 350000, 0.8),

    (1, "Kigali",       "Nairobi",   300000, 0.9),
    (1, "Kigali",       "Johannesburg", 700000, 0.8),

    (1, "Dar es Salaam","Nairobi",   300000, 1.0),
    (1, "Dar es Salaam","Johannesburg", 600000, 0.9),
    (1, "Dar es Salaam","Mombasa",   200000, 0.9),
    (1, "Dar es Salaam","Dubai",     500000, 0.9),

    (1, "Mombasa",      "Nairobi",   150000, 0.9),
    (1, "Mombasa",      "Dubai",     500000, 0.9),

    (1, "Harare",       "Johannesburg", 400000, 1.0),
    (1, "Harare",       "Nairobi",   500000, 0.8),
    (1, "Harare",       "Lusaka",    250000, 0.8),

    (1, "Lusaka",       "Johannesburg", 450000, 0.9),
    (1, "Lusaka",       "Nairobi",   500000, 0.8),

    (1, "Maputo",       "Johannesburg", 400000, 0.8),
    (1, "Maputo",       "Dar es Salaam", 400000, 0.7),

    (1, "Gaborone",     "Johannesburg", 300000, 0.8),
    (1, "Gaborone",     "Cape Town", 400000, 0.7),
    (1, "Gaborone",     "Harare",    350000, 0.7),

    (1, "Windhoek",     "Johannesburg", 500000, 0.7),
    (1, "Windhoek",     "Cape Town", 400000, 0.7),

    (1, "Brazzaville",  "Lagos",     500000, 0.6),
    (1, "Brazzaville",  "Addis Ababa", 600000, 0.5),

    (1, "Rabat",        "Madrid",    400000, 0.8),
    (1, "Rabat",        "Paris",     500000, 0.8),

    (1, "Tripoli",      "Tunisia",   300000, 0.7),
    (1, "Tripoli",      "Cairo",     600000, 0.7),

    (1, "Khartoum",     "Cairo",     600000, 0.7),
    (1, "Khartoum",     "Dubai",     600000, 0.7),

    (1, "Bamako",       "Dakar",     400000, 0.7),
    (1, "Bamako",       "Lagos",     600000, 0.6),

    (1, "Marrakech",    "Paris",     600000, 1.0),
    (1, "Marrakech",    "Madrid",    500000, 0.9),

    (1, "Sharm el-Sheikh", "Cairo",  200000, 1.1),
    (1, "Sharm el-Sheikh", "Riyadh", 300000, 0.8),
    (1, "Sharm el-Sheikh", "Amman",  300000, 0.8),

    (1, "Lilongwe",     "Nairobi",   500000, 0.7),
    (1, "Lilongwe",     "Johannesburg", 400000, 0.7),

    (1, "Asmara",       "Cairo",     600000, 0.6),

    (1, "Maseru",       "Johannesburg", 300000, 0.6),
    (1, "Mbabane",      "Johannesburg", 200000, 0.6),

    (1, "Djibouti",     "Dubai",     500000, 0.7),

    (1, "Yamoussoukro", "Accra",     250000, 0.7),
    (1, "Yamoussoukro", "Casablanca", 500000, 0.6),

    (1, "Ouagadougou",  "Dakar",     500000, 0.6),
    (1, "Ouagadougou",  "Casablanca", 600000, 0.5),

    (1, "NDjamena",     "Addis Ababa", 700000, 0.5),
    (1, "NDjamena",     "Cairo",     700000, 0.5),

    (1, "Libreville",   "Kinshasa",  350000, 0.5),
    (1, "Libreville",   "Casablanca", 600000, 0.5),

    (1, "Bangui",       "Kinshasa",  400000, 0.4),

    (1, "Lome",         "Accra",     150000, 0.8),
    (1, "Cotonou",      "Accra",     200000, 0.7),

    (1, "Banjul",       "Dakar",     200000, 0.5),
    (1, "Banjul",       "Casablanca", 500000, 0.5),

    (1, "Bissau",       "Dakar",     200000, 0.5),

    (1, "Conakry",      "Dakar",     300000, 0.5),
    (1, "Conakry",      "Lagos",     500000, 0.5),

    (1, "Freetown",     "Dakar",     350000, 0.5),
    (1, "Freetown",     "Accra",     400000, 0.5),

    (1, "Monrovia",     "Dakar",     400000, 0.5),
    (1, "Monrovia",     "Accra",     400000, 0.5),

    (1, "Niamey",       "Lagos",     500000, 0.5),
    (1, "Niamey",       "Bamako",    300000, 0.5),

    (1, "Nouakchott",   "Dakar",     300000, 0.5),

    (1, "Gitega",       "Nairobi",   400000, 0.5),
    (1, "Gitega",       "Kigali",    150000, 0.5),

    (1, "Moroni",       "Nairobi",   500000, 0.5),
    (1, "Moroni",       "Antananarivo", 300000, 0.5),

    (1, "Victoria",     "Nairobi",   500000, 0.5),
    (1, "Victoria",     "Antananarivo", 400000, 0.5),

    (1, "Sao Tome",     "Lagos",     400000, 0.4),
    (1, "Sao Tome",     "Libreville", 300000, 0.4),

    (1, "Malabo",       "Lagos",     350000, 0.4),
    (1, "Malabo",       "Libreville", 200000, 0.4),

    # ════════════════════════════════════════════════════════════════════════
    # TIER 2 — AMERICAS
    # ════════════════════════════════════════════════════════════════════════

    (1, "Bogota",       "Miami",     600000, 1.2),
    (2, "Bogota",       "New York",  700000, 1.1),
    (1, "Bogota",       "Lima",      500000, 1.1),
    (1, "Bogota",       "Medellin",  150000, 1.1),
    (1, "Bogota",       "Panama City", 400000, 1.0),
    (1, "Bogota",       "Quito",     300000, 1.0),
    (1, "Bogota",       "Caracas",   400000, 1.0),
    (2, "Bogota",       "Madrid",    900000, 0.9),

    (1, "Panama City",  "Miami",     600000, 1.1),
    (1, "Panama City",  "Mexico City", 700000, 1.0),
    (1, "Panama City",  "San Jose",  300000, 1.0),
    (1, "Panama City",  "Lima",      700000, 0.9),
    (2, "Panama City",  "New York",  700000, 1.0),

    (1, "Havana",       "Miami",     400000, 1.2),
    (1, "Havana",       "New York",  600000, 1.1),
    (1, "Havana",       "Mexico City", 500000, 1.0),
    (1, "Havana",       "Santo Domingo", 400000, 0.9),
    (2, "Havana",       "Madrid",    800000, 0.9),

    (1, "Santo Domingo","Miami",     500000, 1.1),
    (1, "Santo Domingo","New York",  600000, 1.1),

    (1, "Cancun",       "Mexico City", 400000, 1.3),
    (1, "Cancun",       "Miami",     500000, 1.3),
    (1, "Cancun",       "New York",  700000, 1.1),
    (1, "Cancun",       "Los Angeles", 700000, 1.0),

    (1, "Brasilia",     "Rio de Janeiro", 400000, 1.2),
    (1, "Brasilia",     "Bogota",    700000, 0.7),

    (1, "Quito",        "Lima",      500000, 0.8),

    (1, "Asuncion",     "Buenos Aires", 400000, 0.8),

    (1, "Montevideo",   "Buenos Aires", 200000, 0.9),

    (1, "Medellin",     "Caracas",   400000, 0.8),
    (1, "Medellin",     "Panama City", 400000, 0.8),

    (1, "Cali",         "Lima",      500000, 0.7),

    (1, "Guatemala City","Mexico City", 600000, 0.8),
    (1, "Guatemala City","Miami",    700000, 0.8),
    (1, "Guatemala City","San Salvador", 150000, 0.8),
    (1, "Guatemala City","Panama City", 600000, 0.7),

    (1, "San Salvador", "Mexico City", 700000, 0.7),
    (1, "San Salvador", "Miami",     700000, 0.7),

    (1, "Tegucigalpa",  "Mexico City", 700000, 0.7),
    (1, "Tegucigalpa",  "Miami",     700000, 0.7),
    (1, "Tegucigalpa",  "Guatemala City", 200000, 0.7),

    (1, "Managua",      "Mexico City", 700000, 0.7),
    (1, "Managua",      "Miami",     700000, 0.7),
    (1, "Managua",      "San Jose",  300000, 0.8),

    (1, "Port au Prince","Miami",    500000, 0.9),
    (1, "Port au Prince","Havana",   400000, 0.8),
    (1, "Port au Prince","Santo Domingo", 200000, 0.8),

    (1, "Port of Spain","Miami",     700000, 0.8),
    (1, "Port of Spain","Bogota",    500000, 0.7),
    (1, "Port of Spain","Caracas",   300000, 0.8),

    (1, "Georgetown",   "Miami",     700000, 0.7),
    (1, "Georgetown",   "Sao Paulo", 700000, 0.6),
    (1, "Georgetown",   "Port of Spain", 300000, 0.6),

    (1, "Paramaribo",   "Miami",     700000, 0.6),
    (1, "Paramaribo",   "Georgetown", 200000, 0.6),
    (1, "Paramaribo",   "Sao Paulo", 600000, 0.6),

    (1, "Bridgetown",   "Miami",     600000, 0.7),
    (1, "Bridgetown",   "New York",  700000, 0.7),

    (1, "Nassau",       "Miami",     300000, 0.8),
    (1, "Nassau",       "New York",  700000, 0.7),

    (1, "Belmopan",     "Mexico City", 600000, 0.4),
    (1, "Belmopan",     "Cancun",    300000, 0.5),

    # ════════════════════════════════════════════════════════════════════════
    # TIER 2/3 — OCEANIA & PACIFIC
    # ════════════════════════════════════════════════════════════════════════

    (1, "Auckland",     "Sydney",    400000, 1.3),
    (1, "Auckland",     "Melbourne", 500000, 1.1),
    (2, "Auckland",     "Los Angeles", 900000, 1.1),
    (2, "Auckland",     "Singapore", 800000, 1.0),
    (1, "Auckland",     "Honolulu",  700000, 0.9),
    (1, "Auckland",     "Brisbane",  400000, 1.1),
    (1, "Auckland",     "Suva",      500000, 0.6),
    (1, "Auckland",     "Apia",      500000, 0.5),
    (1, "Auckland",     "Nukualofa", 500000, 0.5),
    (1, "Auckland",     "Papeete",   600000, 0.7),

    (1, "Brisbane",     "Sydney",    300000, 1.3),
    (1, "Brisbane",     "Melbourne", 400000, 1.1),
    (1, "Brisbane",     "Port Moresby", 300000, 0.7),
    (2, "Brisbane",     "Singapore", 700000, 1.0),
    (1, "Brisbane",     "Cairns",    300000, 0.9),
    (1, "Brisbane",     "Honiara",   600000, 0.5),
    (1, "Brisbane",     "Port Vila", 600000, 0.5),

    (1, "Cairns",       "Sydney",    500000, 0.8),
    (1, "Cairns",       "Port Moresby", 300000, 0.6),

    (1, "Canberra",     "Sydney",    200000, 0.7),
    (1, "Canberra",     "Melbourne", 200000, 0.7),

    (1, "Port Moresby", "Sydney",    700000, 0.6),

    (1, "Suva",         "Sydney",    600000, 0.6),
    (1, "Apia",         "Honolulu",  600000, 0.5),
    (1, "Nukualofa",    "Suva",      300000, 0.5),

    (2, "Papeete",      "Los Angeles", 800000, 0.7),
]

# ---------------------------------------------------------------------------
# Load all valid city names from city.csv
# ---------------------------------------------------------------------------
def load_city_names(path):
    names = set()
    with open(path, "r", encoding="cp1252", errors="replace") as f:
        for i, line in enumerate(f):
            if i == 0:
                continue
            line = line.strip("\r\n")
            parts = line.split(";")
            if len(parts) > 1:
                names.add(parts[1])
    return names

# ---------------------------------------------------------------------------
# Read existing routes — handles CR-only line endings
# ---------------------------------------------------------------------------
def read_existing_routes(path):
    with open(path, "rb") as f:
        raw = f.read()
    text  = raw.decode("cp1252", errors="replace")
    lines = text.split("\r")
    header = lines[0]
    existing = set()
    rows = []
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        rows.append(line)
        parts = line.split(";")
        if len(parts) >= 3:
            # Store canonical (lower-case, sorted pair) for dedup
            a, b = parts[1].strip(), parts[2].strip()
            existing.add((a.lower(), b.lower()))
            existing.add((b.lower(), a.lower()))
    return header, rows, existing

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    if not os.path.exists(ROUTES_CSV):
        print(f"ERROR: cannot find {ROUTES_CSV}", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(CITIES_CSV):
        print(f"ERROR: cannot find {CITIES_CSV}", file=sys.stderr)
        sys.exit(1)

    valid_cities  = load_city_names(CITIES_CSV)
    header, existing_rows, existing_pairs = read_existing_routes(ROUTES_CSV)

    added   = 0
    skipped_dup   = 0
    skipped_city  = 0
    new_rows = []

    for ebene, von, nach, miete, faktor in NEW_ROUTES:
        # Validate city names
        if von not in valid_cities:
            print(f"  UNKNOWN city: '{von}'  (route {von}->{nach})")
            skipped_city += 1
            continue
        if nach not in valid_cities:
            print(f"  UNKNOWN city: '{nach}'  (route {von}->{nach})")
            skipped_city += 1
            continue

        # Skip if pair already exists (either direction)
        key = (von.lower(), nach.lower())
        if key in existing_pairs:
            skipped_dup += 1
            continue

        row = f"{ebene};{von};{nach};{miete};{faktor}"
        new_rows.append(row)
        existing_pairs.add(key)
        existing_pairs.add((nach.lower(), von.lower()))
        added += 1

    # Write output — CR-only line endings to match original
    all_rows = existing_rows + new_rows
    with open(ROUTES_CSV, "wb") as f:
        f.write((header + "\r").encode("cp1252"))
        for row in all_rows:
            f.write((row + "\r").encode("cp1252"))

    total = len(all_rows)
    print(f"Done.")
    print(f"  {added} new routes added")
    print(f"  {skipped_dup} skipped (already exist)")
    print(f"  {skipped_city} skipped (unknown city name)")
    print(f"  Total routes in file: {total}")
    if total > 1500:
        print(f"WARNING: {total} routes exceeds MAX_ROUTES=1500 — bump defines.h further!")

if __name__ == "__main__":
    main()
