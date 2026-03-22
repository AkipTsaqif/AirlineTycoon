#!/usr/bin/env python3
"""
add_cities.py  -  Add ~165 new world capitals and prominent cities to city.csv

- Reads  tools/decoded/city.csv
- Merges in new cities (Wave=-, NOCITY, AnzPhotos=0, AnzTexts=0  -> zero new assets needed)
- Sorts the entire list alphabetically by city name
- Writes the merged result back to tools/decoded/city.csv

Run from the repo root:
    python tools/add_cities.py
"""

import os, sys

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
DECODED_CSV = os.path.join(SCRIPT_DIR, "decoded", "city.csv")

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------
def fc(val):
    """Format a float/int as a coordinate string using comma decimal (European)."""
    if val == int(val):
        return str(int(val))
    return f"{val:.1f}".replace(".", ",")

def city_row(cid, name, region, areacode, abbr, iata,
             pop, lon, lat, rent, new_in_addon=1):
    """
    Build a city.csv row.
    lat  = geographic latitude (positive=N, negative=S)
    GlobY/MapY in the game = -lat  (northern hemisphere stored as negative Y)
    """
    glob_x = fc(lon)
    glob_y = fc(-lat)          # negate: game stores latitude sign-flipped
    return (
        f"{cid};{name};{region};{areacode};"
        f"{abbr};{iata};-;"      # Wave = "-"
        f"0;0;NOCITY;0;"         # TextResBaseId=0 AnzTexts=0 NOCITY AnzPhotos=0
        f"{pop};"
        f"{glob_x};{glob_y};"
        f"{glob_x};{glob_y};"    # MapX/MapY identical to GlobX/GlobY
        f"{rent};{new_in_addon}"
    )

# ---------------------------------------------------------------------------
# New city definitions
# (id, name, region, areacode, abbr3, iata, population, lon, lat, rent)
#
# Areacode:  1=Europe   2=Americas   3=Africa/Middle East/South+Central Asia
#            4=East Asia / SE Asia / Pacific
# lat sign:  positive = North,  negative = South
# ---------------------------------------------------------------------------
NEW_CITIES_RAW = [

    # ── EUROPE (areacode=1) ──────────────────────────────────────────────
    (200, "Algiers",            "North Africa",     3, "ALG", "ALG",  3700000,   3.1,  36.7, 14000),
    (201, "Lisbon",             "West Europe",      1, "LIS", "LIS",  2900000,  -9.1,  38.7, 15000),
    (202, "Prague",             "Mid Europa",       1, "PRG", "PRG",  1300000,  14.4,  50.1, 15000),
    (203, "Budapest",           "Mid Europa",       1, "BUD", "BUD",  1750000,  19.0,  47.5, 15000),
    (204, "Bucharest",          "East Europe",      1, "BUH", "OTP",  1800000,  26.1,  44.4, 12000),
    (205, "Belgrade",           "East Europe",      1, "BEG", "BEG",  1700000,  20.5,  44.8, 10000),
    (206, "Zagreb",             "Mid Europa",       1, "ZAG", "ZAG",   800000,  16.0,  45.8,  9000),
    (207, "Sarajevo",           "East Europe",      1, "SJJ", "SJJ",   275000,  18.4,  43.9,  7000),
    (208, "Bratislava",         "Mid Europa",       1, "BTS", "BTS",   475000,  17.1,  48.2,  9000),
    (209, "Vilnius",            "North Europe",     1, "VNO", "VNO",   580000,  25.3,  54.7,  8000),
    (210, "Riga",               "North Europe",     1, "RIX", "RIX",   615000,  24.1,  56.9,  8000),
    (211, "Tallinn",            "North Europe",     1, "TLL", "TLL",   440000,  24.8,  59.4,  8000),
    (212, "Minsk",              "East Europe",      1, "MSQ", "MSQ",  1980000,  27.6,  53.9, 10000),
    (213, "Sofia",              "South-East Europe",1, "SOF", "SOF",  1260000,  23.3,  42.7,  9000),
    (214, "Tirana",             "South-East Europe",1, "TIA", "TIA",   800000,  19.8,  41.3,  7000),
    (215, "Skopje",             "South-East Europe",1, "SKP", "SKP",   540000,  21.4,  42.0,  7000),
    (216, "Podgorica",          "South-East Europe",1, "TGD", "TGD",   190000,  19.3,  42.4,  6000),
    (217, "Nicosia",            "South-East Europe",1, "NIC", "NIC",   330000,  33.4,  35.2,  9000),
    (218, "Valletta",           "South Europe",     1, "MLA", "MLA",   213000,  14.5,  35.9,  9000),
    (219, "Tbilisi",            "East Europe",      1, "TBS", "TBS",  1120000,  44.8,  41.7,  8000),
    (220, "Baku",               "East Europe",      1, "GYD", "GYD",  2300000,  49.9,  40.4,  9000),
    (221, "Yerevan",            "East Europe",      1, "EVN", "EVN",  1090000,  44.5,  40.2,  8000),
    (222, "Luxembourg City",    "West Europe",      1, "LUX", "LUX",   130000,   6.1,  49.6, 18000),
    (223, "Edinburgh",          "North Europe",     1, "EDI", "EDI",   540000,  -3.2,  55.9, 12000),
    (224, "Manchester",         "West Europe",      1, "MAN", "MAN",  2800000,  -2.2,  53.5, 13000),
    (225, "Milan",              "South Europe",     1, "MXP", "MXP",  1380000,   9.2,  45.5, 16000),
    (226, "Venice",             "South Europe",     1, "VCE", "VCE",   260000,  12.3,  45.4, 14000),
    (227, "Florence",           "South Europe",     1, "FLR", "FLR",   380000,  11.3,  43.8, 12000),
    (228, "Naples",             "South Europe",     1, "NAP", "NAP",   960000,  14.3,  40.9,  9000),
    (229, "Lyon",               "West Europe",      1, "LYS", "LYS",   520000,   4.8,  45.7, 12000),
    (230, "Nice",               "South Europe",     1, "NCE", "NCE",   340000,   7.3,  43.7, 14000),
    (231, "Hamburg",            "North Europe",     1, "HAM", "HAM",  1850000,  10.0,  53.6, 14000),
    (232, "Cologne",            "West Europe",      1, "CGN", "CGN",  1080000,   7.0,  50.9, 13000),
    (233, "Dusseldorf",         "West Europe",      1, "DUS", "DUS",   620000,   6.8,  51.2, 14000),
    (234, "Porto",              "West Europe",      1, "OPO", "OPO",   240000,  -8.6,  41.2, 10000),
    (235, "Seville",            "South Europe",     1, "SVQ", "SVQ",   700000,  -6.0,  37.4, 10000),
    (236, "Istanbul",           "Europe",           1, "IST", "IST", 15460000,  28.9,  41.0, 18000),

    # ── AFRICA (areacode=3) ──────────────────────────────────────────────
    (237, "Rabat",              "North Africa",     3, "RBA", "RBA",   580000,  -6.8,  34.0,  9000),
    (238, "Casablanca",         "North Africa",     3, "CMN", "CMN",  3752000,  -7.6,  33.6, 12000),
    (239, "Tripoli",            "North Africa",     3, "TIP", "TIP",  1126000,  13.2,  32.9, 10000),
    (240, "Addis Ababa",        "East Africa",      3, "ADD", "ADD",  3600000,  38.7,   9.0, 10000),
    (241, "Khartoum",           "North Africa",     3, "KRT", "KRT",  5000000,  32.5,  15.6,  8000),
    (242, "Accra",              "West Africa",      3, "ACC", "ACC",  2270000,  -0.2,   5.6,  9000),
    (243, "Abuja",              "West Africa",      3, "ABV", "ABV",  3000000,   7.4,   9.1, 10000),
    (244, "Lagos",              "West Africa",      3, "LOS", "LOS", 14800000,   3.4,   6.5, 14000),
    (245, "Kinshasa",           "Central Africa",   3, "FIH", "FIH", 14000000,  15.3,  -4.3,  8000),
    (246, "Luanda",             "Central Africa",   3, "LAD", "LAD",  8300000,  13.2,  -8.8, 11000),
    (247, "Harare",             "East Africa",      3, "HRE", "HRE",  1500000,  31.1, -17.8,  8000),
    (248, "Lusaka",             "East Africa",      3, "LUN", "LUN",  2400000,  28.3, -15.4,  8000),
    (249, "Maputo",             "East Africa",      3, "MPM", "MPM",  1100000,  32.6, -26.0,  7000),
    (250, "Gaborone",           "Southern Africa",  3, "GBE", "GBE",   270000,  25.9, -24.7,  7000),
    (251, "Windhoek",           "Southern Africa",  3, "WDH", "WDH",   430000,  17.1, -22.6,  7000),
    (252, "Kampala",            "East Africa",      3, "EBB", "EBB",  3200000,  32.6,   0.3,  8000),
    (253, "Kigali",             "East Africa",      3, "KGL", "KGL",  1130000,  30.1,  -1.9,  8000),
    (254, "Bamako",             "West Africa",      3, "BKO", "BKO",  2700000,  -8.0,  12.6,  7000),
    (255, "Conakry",            "West Africa",      3, "CKY", "CKY",  1600000, -13.7,   9.5,  6000),
    (256, "Freetown",           "West Africa",      3, "FNA", "FNA",  1055000, -13.2,   8.5,  6000),
    (257, "Monrovia",           "West Africa",      3, "ROB", "ROB",  1010000, -10.8,   6.3,  5000),
    (258, "Ouagadougou",        "West Africa",      3, "OUA", "OUA",  2400000,  -1.5,  12.4,  6000),
    (259, "Niamey",             "West Africa",      3, "NIM", "NIM",  1260000,   2.1,  13.5,  5000),
    (260, "Brazzaville",        "Central Africa",   3, "BZV", "BZV",  1827000,  15.2,  -4.3,  7000),
    (261, "NDjamena",           "Central Africa",   3, "NDJ", "NDJ",  1300000,  15.0,  12.1,  6000),
    (262, "Mogadishu",          "East Africa",      3, "MGQ", "MGQ",  2587000,  45.3,   2.1,  5000),
    (263, "Djibouti",           "East Africa",      3, "JIB", "JIB",   620000,  43.1,  11.6,  7000),
    (264, "Moroni",             "East Africa",      3, "HAH", "HAH",    62000,  43.3, -11.7,  5000),
    (265, "Libreville",         "Central Africa",   3, "LBV", "LBV",   800000,   9.5,   0.4,  9000),
    (266, "Bangui",             "Central Africa",   3, "BGF", "BGF",   889000,  18.6,   4.4,  5000),
    (267, "Lome",               "West Africa",      3, "LFW", "LFW",   837000,   1.2,   6.1,  6000),
    (268, "Cotonou",            "West Africa",      3, "COO", "COO",   800000,   2.4,   6.4,  6000),
    (269, "Banjul",             "West Africa",      3, "BJL", "BJL",   413000, -16.7,  13.5,  5000),
    (270, "Bissau",             "West Africa",      3, "OXB", "OXB",   395000, -15.6,  11.9,  5000),
    (271, "Lilongwe",           "East Africa",      3, "LLW", "LLW",  1077000,  33.8, -14.0,  6000),
    (272, "Asmara",             "East Africa",      3, "ASM", "ASM",   963000,  38.9,  15.3,  6000),
    (273, "Maseru",             "Southern Africa",  3, "MSU", "MSU",   330000,  27.5, -29.3,  5000),
    (274, "Mbabane",            "Southern Africa",  3, "MTS", "MTS",    95000,  31.1, -26.3,  5000),
    (275, "Sao Tome",           "Central Africa",   3, "TMS", "TMS",    90000,   6.7,   0.3,  6000),
    (276, "Victoria",           "East Africa",      3, "SEZ", "SEZ",    28000,  55.5,  -4.6,  8000),
    (277, "Malabo",             "Central Africa",   3, "SSG", "SSG",   187000,   8.8,   3.8,  7000),
    (278, "Gitega",             "East Africa",      3, "GID", "GID",   133000,  29.9,  -3.4,  5000),
    (279, "Nouakchott",         "West Africa",      3, "NKC", "NKC",  1030000, -16.0,  18.1,  5000),
    (280, "Yamoussoukro",       "West Africa",      3, "ASK", "ASK",   280000,  -5.3,   6.8,  7000),
    (281, "Mombasa",            "East Africa",      3, "MBA", "MBA",  1200000,  39.7,  -4.0,  9000),
    (282, "Marrakech",          "North Africa",     3, "RAK", "RAK",   928000, -8.0,   31.6, 10000),
    (283, "Sharm el-Sheikh",    "North Africa",     3, "SSH", "SSH",    35000,  34.3,  27.9, 12000),
    (284, "Dar es Salaam",      "East Africa",      3, "DAR", "DAR",  4364000,  39.3,  -6.8, 10000),

    # ── MIDDLE EAST (areacode=3) ─────────────────────────────────────────
    (285, "Tehran",             "Middle East",      3, "THR", "THR",  8700000,  51.4,  35.7, 14000),
    (286, "Baghdad",            "Middle East",      3, "BGW", "BGW",  7144000,  44.4,  33.3, 10000),
    (287, "Amman",              "Middle East",      3, "AMM", "AMM",  2182000,  35.9,  31.9, 11000),
    (288, "Beirut",             "Middle East",      3, "BEY", "BEY",  2385000,  35.5,  33.9, 14000),
    (289, "Damascus",           "Middle East",      3, "DAM", "DAM",  1800000,  36.3,  33.5,  9000),
    (290, "Jerusalem",          "Middle East",      3, "JRS", "JRS",   919000,  35.2,  31.8, 12000),
    (291, "Kuwait City",        "Middle East",      3, "KWI", "KWI",  2380000,  48.0,  29.4, 14000),
    (292, "Manama",             "Middle East",      3, "BAH", "BAH",   617000,  50.6,  26.2, 14000),
    (293, "Doha",               "Middle East",      3, "DOH", "DOH",  2382000,  51.5,  25.3, 16000),
    (294, "Abu Dhabi",          "Middle East",      3, "AUH", "AUH",  1483000,  54.4,  24.5, 16000),
    (295, "Dubai",              "Middle East",      3, "DXB", "DXB",  3331000,  55.3,  25.2, 18000),
    (296, "Muscat",             "Middle East",      3, "MCT", "MCT",  1421000,  58.6,  23.6, 12000),

    # ── SOUTH ASIA (areacode=3) ──────────────────────────────────────────
    (297, "Islamabad",          "South Asia",       3, "ISB", "ISB",  1014000,  73.1,  33.7,  8000),
    (298, "Karachi",            "South Asia",       3, "KHI", "KHI", 14910000,  67.0,  24.9, 10000),
    (299, "Dhaka",              "South Asia",       3, "DAC", "DAC", 14399000,  90.4,  23.8,  9000),
    (300, "Colombo",            "South Asia",       3, "CMB", "CMB",   752000,  79.9,   6.9,  9000),
    (301, "Kathmandu",          "South Asia",       3, "KTM", "KTM",  1029000,  85.3,  27.7,  8000),
    (302, "Kabul",              "South Asia",       3, "KBL", "KBL",  4601000,  69.2,  34.5,  7000),
    (303, "Bangalore",          "South Asia",       3, "BLR", "BLR",  8443000,  77.6,  13.0, 11000),

    # ── CENTRAL ASIA (areacode=3) ────────────────────────────────────────
    (304, "Tashkent",           "Central Asia",     3, "TAS", "TAS",  2371000,  69.3,  41.3,  9000),
    (305, "Astana",             "Central Asia",     3, "TSE", "NQZ",  1200000,  71.5,  51.2, 10000),
    (306, "Bishkek",            "Central Asia",     3, "FRU", "FRU",  1012000,  74.6,  42.9,  7000),
    (307, "Ashgabat",           "Central Asia",     3, "ASB", "ASB",  1032000,  58.4,  38.0,  8000),
    (308, "Dushanbe",           "Central Asia",     3, "DYU", "DYU",   863000,  68.8,  38.6,  7000),

    # ── EAST & SOUTHEAST ASIA (areacode=4) ──────────────────────────────
    (309, "Hanoi",              "Far East",         4, "HAN", "HAN",  8053000, 105.8,  21.0,  9000),
    (310, "Ho Chi Minh City",   "Far East",         4, "SGN", "SGN",  8993000, 106.6,  10.8, 10000),
    (311, "Phnom Penh",         "Far East",         4, "PNH", "PNH",  1501000, 104.9,  11.6,  7000),
    (312, "Vientiane",          "Far East",         4, "VTE", "VTE",   820000, 102.6,  18.0,  6000),
    (313, "Naypyidaw",          "Far East",         4, "NYT", "NYT",   924000,  96.1,  19.8,  6000),
    (314, "Jakarta",            "Far East",         4, "CGK", "CGK", 10562000, 106.9,  -6.2, 11000),
    (315, "Kuala Lumpur",       "Far East",         4, "KUL", "KUL",  1768000, 101.7,   3.1, 12000),
    (316, "Bali",               "Far East",         4, "DPS", "DPS",  1234000, 115.1,  -8.3, 12000),
    (317, "Bandar Seri Begawan","Far East",         4, "BWN", "BWN",   100700, 114.9,   4.9, 10000),
    (318, "Dili",               "Australia",        4, "DIL", "DIL",   222000, 125.6,  -8.6,  5000),
    (319, "Pyongyang",          "Far East",         4, "FNJ", "FNJ",  3255000, 125.7,  39.0,  6000),
    (320, "Ulaanbaatar",        "Far East",         4, "ULN", "ULN",  1466000, 106.9,  47.9,  7000),
    (321, "Thimphu",            "South Asia",       3, "PBH", "PBH",   115000,  89.6,  27.5,  6000),
    (322, "Taipei",             "Far East",         4, "TPE", "TPE",  2646000, 121.6,  25.1, 12000),
    (323, "Phuket",             "Far East",         4, "HKT", "HKT",    76000,  98.4,   7.9, 12000),
    (324, "Chiang Mai",         "Far East",         4, "CNX", "CNX",   127000,  99.0,  18.8,  9000),
    (325, "Shanghai",           "Far East",         4, "PVG", "PVG", 24152000, 121.5,  31.2, 16000),
    (326, "Mumbai",             "South Asia",       3, "BOM", "BOM", 20667000,  72.9,  19.1, 14000),
    (327, "Guangzhou",          "Far East",         4, "CAN", "CAN", 13501000, 113.3,  23.1, 13000),
    (328, "Chengdu",            "Far East",         4, "CTU", "CTU", 16044000, 104.1,  30.6, 11000),
    (329, "Busan",              "Far East",         4, "PUS", "PUS",  3404000, 129.1,  35.2,  9000),
    (330, "Nagoya",             "Far East",         4, "NGO", "NGO",  2283000, 136.9,  35.2, 11000),

    # ── AMERICAS (areacode=2) ────────────────────────────────────────────
    (331, "Sao Paulo",          "South America",    2, "GRU", "GRU", 12325000, -46.6, -23.5, 14000),
    (332, "Brasilia",           "South America",    2, "BSB", "BSB",  3055000, -47.9, -15.8, 12000),
    (333, "Bogota",             "South America",    2, "BOG", "BOG",  7412000, -74.1,   4.7, 12000),
    (334, "Medellin",           "South America",    2, "MDE", "MDE",  2569000, -75.6,   6.3,  9000),
    (335, "Cali",               "South America",    2, "CLO", "CLO",  2401000, -76.5,   3.4,  8000),
    (336, "Quito",              "South America",    2, "UIO", "UIO",  2011000, -78.5,  -0.2,  9000),
    (337, "Asuncion",           "South America",    2, "ASU", "ASU",  2200000, -57.6, -25.3,  8000),
    (338, "Montevideo",         "South America",    2, "MVD", "MVD",  1380000, -56.2, -34.9, 10000),
    (339, "Havana",             "Middle America",   2, "HAV", "HAV",  2106000, -82.4,  23.1,  8000),
    (340, "Santo Domingo",      "Middle America",   2, "SDQ", "SDQ",  2201000, -69.9,  18.5,  8000),
    (341, "Port au Prince",     "Middle America",   2, "PAP", "PAP",   987000, -72.3,  18.5,  5000),
    (342, "Guatemala City",     "Middle America",   2, "GUA", "GUA",  2450000, -90.5,  14.6,  8000),
    (343, "San Salvador",       "Middle America",   2, "SAL", "SAL",   567000, -89.2,  13.7,  7000),
    (344, "Tegucigalpa",        "Middle America",   2, "TGU", "TGU",   850000, -87.2,  14.1,  6000),
    (345, "Managua",            "Middle America",   2, "MGA", "MGA",  1100000, -86.3,  12.1,  6000),
    (346, "Panama City",        "Middle America",   2, "PTY", "PTY",   880000, -79.5,   9.0, 10000),
    (347, "Nassau",             "Middle America",   2, "NAS", "NAS",   280000, -77.4,  25.0, 12000),
    (348, "Georgetown",         "South America",    2, "GEO", "GEO",   235000, -58.2,   6.8,  7000),
    (349, "Paramaribo",         "South America",    2, "PBM", "PBM",   240000, -55.2,   5.9,  7000),
    (350, "Port of Spain",      "Middle America",   2, "POS", "POS",   534000, -61.5,  10.7,  9000),
    (351, "Bridgetown",         "Middle America",   2, "BGI", "BGI",   110000, -59.6,  13.1, 10000),
    (352, "Belmopan",           "Middle America",   2, "BZE", "BZE",    13000, -88.8,  17.3,  5000),
    (353, "Cancun",             "Middle America",   2, "CUN", "CUN",   888000, -86.9,  21.2, 14000),

    # ── OCEANIA / PACIFIC (areacode=4) ───────────────────────────────────
    (354, "Canberra",           "Australia",        4, "CBR", "CBR",   395000, 149.1, -35.3, 11000),
    (355, "Auckland",           "Australia",        4, "AKL", "AKL",  1628000, 174.8, -36.9, 12000),
    (356, "Brisbane",           "Australia",        4, "BNE", "BNE",  2360000, 153.0, -27.5, 11000),
    (357, "Cairns",             "Australia",        4, "CNS", "CNS",   150000, 145.8, -16.9,  9000),
    (358, "Port Moresby",       "Australia",        4, "POM", "POM",   364000, 147.2,  -9.4,  7000),
    (359, "Suva",               "Pacific",          4, "SUV", "SUV",    77000, 178.4, -18.1,  7000),
    (360, "Honiara",            "Pacific",          4, "HIR", "HIR",    84000, 160.0,  -9.4,  6000),
    (361, "Port Vila",          "Pacific",          4, "VLI", "VLI",    51000, 168.3, -17.7,  6000),
    (362, "Apia",               "Pacific",          4, "APW", "APW",    37000,-171.8, -13.8,  6000),
    (363, "Nukualofa",          "Pacific",          4, "TBU", "TBU",    23000,-175.2, -21.1,  5000),
    (364, "Papeete",            "Pacific",          4, "PPT", "PPT",    26000,-149.6, -17.5,  9000),
]

# ---------------------------------------------------------------------------
# Build the new rows
# ---------------------------------------------------------------------------
def build_new_rows():
    rows = {}
    for entry in NEW_CITIES_RAW:
        cid, name, region, areacode, abbr, iata, pop, lon, lat, rent = entry
        rows[name] = city_row(cid, name, region, areacode, abbr, iata,
                              pop, lon, lat, rent, new_in_addon=1)
    return rows

# ---------------------------------------------------------------------------
# Read existing city.csv  (skip header row)
# ---------------------------------------------------------------------------
def read_existing(path):
    with open(path, "r", encoding="cp1252", errors="replace") as f:
        lines = f.readlines()
    header = lines[0].rstrip("\n")
    cities = {}  # name -> raw line
    for line in lines[1:]:
        line = line.rstrip("\n")
        if not line:
            continue
        parts = line.split(";")
        name = parts[1] if len(parts) > 1 else ""
        cities[name] = line
    return header, cities

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    if not os.path.exists(DECODED_CSV):
        print(f"ERROR: cannot find {DECODED_CSV}", file=sys.stderr)
        sys.exit(1)

    header, existing = read_existing(DECODED_CSV)
    new_rows = build_new_rows()

    # Check for name collisions
    collisions = set(existing.keys()) & set(new_rows.keys())
    if collisions:
        print(f"WARNING: {len(collisions)} name(s) already exist and will be SKIPPED:")
        for c in sorted(collisions):
            print(f"  - {c}")

    # Merge  (existing cities take priority over new ones with same name)
    merged = dict(existing)
    added = 0
    for name, row in new_rows.items():
        if name not in merged:
            merged[name] = row
            added += 1

    # Sort alphabetically by city name (case-insensitive)
    sorted_names = sorted(merged.keys(), key=lambda n: n.lower())

    # Write output
    out_path = DECODED_CSV
    with open(out_path, "w", encoding="cp1252", newline="\r\n") as f:
        f.write(header + "\n")
        for name in sorted_names:
            f.write(merged[name] + "\n")

    total = len(sorted_names)
    print(f"Done.  {added} new cities added.  Total: {total} cities.")
    print(f"Output: {out_path}")

    if total > 320:
        print(f"WARNING: {total} cities exceeds MAX_CITIES=320 — bump defines.h further!")

if __name__ == "__main__":
    main()
