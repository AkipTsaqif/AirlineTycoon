#!/usr/bin/env python3
"""
add_workers.py  -  Expand piloten.csv with more diverse staff entries

- Reads  tools/decoded/piloten.csv
- Adds pilots (Art=10), stewardesses (Art=11), and consultants (Art=1-9)
- Skips entries whose Name already exists
- Writes back to tools/decoded/piloten.csv

Run from the repo root:
    python tools/add_workers.py

Worker Art types (from defines.h):
    1 = BERATERTYP_PERSONAL    (HR consultant)
    2 = BERATERTYP_KEROSIN     (fuel consultant)
    3 = BERATERTYP_ROUTE       (route consultant)
    4 = BERATERTYP_AUFTRAG     (contracts consultant)
    5 = BERATERTYP_GELD        (finance consultant)
    6 = BERATERTYP_INFO        (info consultant)
    7 = BERATERTYP_FLUGZEUG    (aircraft consultant)
    8 = BERATERTYP_FITNESS     (maintenance consultant)
    9 = BERATERTYP_SICHERHEIT  (security consultant)
   10 = WORKER_PILOT
   11 = WORKER_STEWARDESS

Geschlecht: 0=female, 1=male
"""

import os, sys

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
DECODED_CSV = os.path.join(SCRIPT_DIR, "decoded", "piloten.csv")

MAX_WORKERS = 2000  # must match defines.h

# ---------------------------------------------------------------------------
# New worker definitions
# (name, geschlecht, art, gehalt, talent, alter, kommentar)
# ---------------------------------------------------------------------------
NEW_WORKERS = [

    # =========================================================================
    # PILOTS (Art=10)
    # =========================================================================
    ("James Thornton",    1, 10, 8200,  85, 38, "Former RAF pilot with 12 years of commercial flying experience. Rated on wide-body jets."),
    ("Maria Santos",      0, 10, 7800,  80, 34, "Experienced Airbus captain, previously with a major South American carrier."),
    ("Erik Lindqvist",    1, 10, 9000,  90, 45, "Scandinavian Airlines veteran with over 15,000 flight hours. Wide-body certified."),
    ("Yuki Tanaka",       0, 10, 7500,  75, 31, "First officer seeking upgrade to captain. Strong technical background."),
    ("Carlos Mendez",     1, 10, 8500,  88, 42, "Former military transport pilot. Excellent instrument rating record."),
    ("Sophie Lambert",    0, 10, 8000,  82, 36, "French airline captain. Specialized in long-haul transatlantic operations."),
    ("Ivan Petrov",       1, 10, 7200,  72, 29, "Young co-pilot with 3 years commercial experience. Quick learner."),
    ("Rachel Morgan",     0, 10, 8800,  91, 40, "British Airways veteran. Former training captain with impeccable safety record."),
    ("Hiroshi Yamamoto",  1, 10, 9200,  93, 48, "JAL senior captain. Expert in Pacific long-haul operations."),
    ("Fatima Al-Rashid",  0, 10, 8100,  84, 37, "Gulf carrier captain. Experienced in extreme weather operations."),
    ("Stefan Bauer",      1, 10, 8600,  87, 43, "Lufthansa line captain. Qualified on A320 and B737 family."),
    ("Lisa Chen",         0, 10, 7600,  78, 33, "Taiwanese captain. Multi-type rated with strong Asia-Pacific network knowledge."),
    ("Tom Bradley",       1, 10, 7000,  70, 27, "Recently qualified commercial pilot. Eager and disciplined."),
    ("Nadia Dupont",      0, 10, 8300,  86, 39, "Air France first officer with wide-body endorsement. Ready for command upgrade."),
    ("Rajesh Kumar",      1, 10, 7900,  81, 35, "IndiGo captain. Experienced in high-frequency short-haul operations."),
    ("Anna Kowalski",     0, 10, 8700,  89, 41, "LOT Polish Airlines senior captain. ATPL with multiple type ratings."),
    ("David Okafor",      1, 10, 7400,  74, 30, "Nigerian Eagle captain. Strong knowledge of African routes."),
    ("Elena Volkov",      0, 10, 8400,  85, 38, "Aeroflot captain with Siberian route experience. Cold weather specialist."),
    ("Marco Ricci",       1, 10, 8100,  83, 37, "Alitalia veteran. Experienced in busy Mediterranean operations."),
    ("Grace Osei",        0, 10, 7300,  73, 29, "African Airlines first officer with international ambitions."),
    ("Klaus Richter",     1, 10, 9500,  96, 52, "Retired Lufthansa check captain. Comes out of retirement for passion of flying."),
    ("Priya Sharma",      0, 10, 7700,  79, 32, "Air India captain. Excellent monsoon and tropical weather experience."),
    ("Jack O'Brien",      1, 10, 8200,  84, 39, "Aer Lingus captain. North Atlantic specialist with MNPS qualification."),
    ("Mei Lin",           0, 10, 7800,  80, 34, "China Southern first officer. High-density route expert."),
    ("Ahmed Mansour",     1, 10, 8900,  91, 46, "EgyptAir veteran captain. Middle East and African route specialist."),
    ("Ingrid Sorensen",   0, 10, 8500,  87, 40, "SAS captain. Expert in northern European and Arctic operations."),
    ("Paul Tremblay",     1, 10, 7500,  76, 31, "Air Canada junior captain. ETOPS qualified. Good attitude."),
    ("Akiko Watanabe",    0, 10, 8100,  83, 36, "ANA captain. Renowned for precise landings in difficult conditions."),
    ("Mohammed Al-Farsi", 1, 10, 9100,  92, 47, "Emirates senior captain. Ultra-long-haul specialist with A380 type rating."),
    ("Laura Hoffmann",    0, 10, 8700,  88, 42, "Austrian Airlines captain. Alpine airport specialist."),
    ("Samuel Diallo",     1, 10, 7100,  71, 28, "Air Senegal first officer. Building international experience."),
    ("Olga Petersen",     0, 10, 8000,  82, 36, "Scandinavian first officer. Known for smooth operations in Nordic weather."),
    ("Vincent Moreau",    1, 10, 8300,  85, 40, "Corsair International captain. Charter and scheduled long-haul experience."),
    ("Sunita Verma",      0, 10, 7600,  77, 33, "Jet Airways captain. Sub-continent route specialist."),
    ("Lars Eriksson",     1, 10, 8800,  90, 44, "Finnair captain. Polar route certified. Extremely reliable."),
    ("Diane Foster",      0, 10, 8200,  84, 38, "Delta Air Lines first officer. Hub-and-spoke expert."),
    ("Takashi Ito",       1, 10, 9000,  92, 49, "ANA check captain. Simulator instructor in his spare time."),
    ("Valentina Cruz",    0, 10, 7900,  81, 35, "LATAM captain. South American continent route specialist."),
    ("Georg Brunner",     1, 10, 8600,  88, 43, "Swiss International captain. Mountain and alpine approach certified."),
    ("Joy Mensah",        0, 10, 7400,  75, 30, "Ghana International first officer. Passionate advocate for African aviation."),
    ("Alexei Sokolov",    1, 10, 7800,  80, 34, "S7 Airlines captain. Experienced in Siberian regional operations."),
    ("Caroline Bell",     0, 10, 8500,  87, 41, "Virgin Atlantic captain. Transatlantic entertainment route specialist."),
    ("Wei Zhang",         1, 10, 8100,  83, 37, "Air China captain. Pacific and European long-haul routes."),
    ("Monika Gruber",     0, 10, 7700,  79, 32, "Austrian regional captain. Excellent Alps approach skills."),
    ("Patrick Flynn",     1, 10, 8900,  91, 47, "Ryanair captain. High-frequency short-haul operations master."),
    ("Yuna Kim",          0, 10, 8000,  82, 36, "Korean Air first officer ready for command. Diligent and precise."),
    ("Henri Rousseau",    1, 10, 8400,  86, 41, "Air France cargo captain transitioning to passenger. Excellent logistician."),
    ("Deepa Nair",        0, 10, 7500,  76, 31, "IndiGo co-pilot with 5 years experience. Night-stop route specialist."),
    ("Johan Andersson",   1, 10, 9200,  93, 50, "Scandinavian veteran. One of the most experienced Nordic pilots available."),
    ("Amara Diallo",      0, 10, 7200,  73, 29, "Air Burkina first officer. Eager to gain international experience."),
    ("Nikolai Fedorov",   1, 10, 8300,  85, 39, "Aeroflot captain. CIS route specialist with Central Asia experience."),
    ("Soo-Yeon Park",     0, 10, 8100,  83, 37, "Asiana Airlines captain. Korean Peninsula short-haul expert."),
    ("Bruno Castro",      1, 10, 7900,  81, 35, "TAP Air Portugal captain. Lusophone world route expert."),
    ("Elsa Gustafsson",   0, 10, 8600,  88, 42, "SAS senior captain. Exceptional cold weather and deicing expertise."),
    ("Kwame Asante",      1, 10, 7300,  74, 30, "Africa World Airlines pilot. Growing regional African route network."),
    ("Isabel Ferreira",   0, 10, 7800,  80, 34, "TAP first officer. Atlantic island specialist including Azores."),
    ("Dmitri Volkov",     1, 10, 8500,  87, 43, "Pobeda captain. Low-cost carrier efficiency expert."),
    ("Hana Nakamura",     0, 10, 8200,  84, 38, "JAL first officer. Customer service oriented approach to flying."),
    ("Andrei Popescu",    1, 10, 7600,  78, 33, "Tarom captain. Eastern European route specialist."),
    ("Fatou Camara",      0, 10, 7100,  72, 28, "Air Mali pilot. West African domestic and regional routes."),
    ("Max Zimmermann",    1, 10, 9000,  92, 48, "Condor veteran. Holiday charter specialist with Mediterranean expertise."),
    ("Chiara Romano",     0, 10, 8000,  82, 36, "ITA Airways captain. Mediterranean and North African routes."),
    ("Omar Khalil",       1, 10, 8700,  89, 44, "Royal Jordanian captain. Middle East hub specialist."),
    ("Freya Nilsson",     0, 10, 7700,  79, 32, "Norwegian Air captain. Low-cost transatlantic pioneer."),
    ("Tunde Adeyemi",     1, 10, 7400,  75, 30, "Air Nigeria first officer. Lagos hub operations."),
    ("Katerina Novak",    0, 10, 8400,  86, 40, "Czech Airlines captain. Central European specialist."),
    ("Ravi Patel",        1, 10, 8100,  83, 37, "Air India Express captain. Indian subcontinent short-haul expert."),
    ("Astrid Bergstrom",  0, 10, 8800,  90, 45, "SAS check captain. Exceptional simulator evaluator."),
    ("Seun Okonkwo",      1, 10, 7200,  73, 29, "Dana Air first officer. Building hours on Nigerian domestic routes."),
    ("Camille Dubois",    0, 10, 8300,  85, 39, "Air Tahiti Nui captain. Pacific island and ultra-long-haul expert."),
    ("Viktor Kovalev",    1, 10, 7800,  80, 34, "Ukraine International captain. Eastern Europe and CIS routes."),
    ("Lena Becker",       0, 10, 8100,  83, 37, "Eurowings captain. European low-cost short-haul operations."),
    ("Moussa Toure",      1, 10, 7000,  71, 27, "Air Senegal first officer. Committed to growing his career."),
    ("Rosa Gomez",        0, 10, 7900,  81, 35, "Iberia captain. Spanish domestic and Latin American routes."),
    ("Einar Thorvaldsen", 1, 10, 8600,  88, 43, "Icelandair captain. North Atlantic crossing and Iceland stopover specialist."),
    ("Ji-Young Choi",     0, 10, 8000,  82, 36, "Jeju Air captain. Korean low-cost carrier short-haul master."),
    ("Luca Esposito",     1, 10, 8500,  87, 41, "Neos captain. Italian charter holiday route specialist."),
    ("Nia Mensah",        0, 10, 7300,  74, 30, "Precision Air first officer. East African regional routes."),
    ("Andrzej Wozniak",   1, 10, 8200,  84, 38, "LOT captain. Central and Eastern European hub specialist."),
    ("Yoko Hashimoto",    0, 10, 8700,  89, 44, "ANA senior captain. Domestic Japanese high-frequency service expert."),
    ("Bilal Nasser",      1, 10, 7700,  79, 32, "Air Arabia captain. Middle East and North Africa low-cost specialist."),

    # =========================================================================
    # STEWARDESSES / CABIN CREW (Art=11)
    # =========================================================================
    ("Claire Beaumont",   0, 11, 3800,  78, 26, "Former hotel concierge. Excellent multilingual customer service skills."),
    ("Jason Park",        1, 11, 3600,  72, 24, "Trained in hospitality management. Calm and efficient under pressure."),
    ("Lucia Fernandez",   0, 11, 4200,  85, 29, "5 years cabin crew experience. Senior purser qualified."),
    ("Ahmed Hassan",      1, 11, 3500,  70, 23, "Completed cabin crew training with distinction. First aviation role."),
    ("Yuki Sato",         0, 11, 4000,  80, 27, "JAL trained crew. Bilingual Japanese-English. Excellent service scores."),
    ("Emma Wilson",       0, 11, 3900,  79, 26, "Virgin trained. Known for exceptional passenger rapport."),
    ("Fabio Lanza",       1, 11, 3700,  74, 25, "Alitalia background. Fluent in Italian, English, and French."),
    ("Priya Nair",        0, 11, 4100,  83, 28, "Air India senior crew. Expert in long-haul passenger care."),
    ("Lars Madsen",       1, 11, 3600,  71, 24, "Scandinavian background. Excellent in northern European service standards."),
    ("Sofia Reyes",       0, 11, 4300,  87, 30, "LATAM purser. South American route specialist with 6 years experience."),
    ("Mohammed Al-Amin",  1, 11, 3800,  76, 25, "Gulf carrier trained. Excellent Arabic and English language skills."),
    ("Hana Kim",          0, 11, 4000,  80, 27, "Korean Air cabin crew. Professional and calm in all situations."),
    ("Thomas Muller",     1, 11, 3500,  70, 23, "Recently qualified. Eager to build international flying hours."),
    ("Valentina Moreno",  0, 11, 4200,  84, 29, "Avianca trained purser. Expert South American passenger service."),
    ("Kevin Osei",        1, 11, 3600,  72, 24, "African Airlines crew. First aviation job, excellent attitude."),
    ("Astrid Lindgren",   0, 11, 4100,  83, 28, "SAS veteran. Scandinavian service standards ambassador."),
    ("Marco Bianchi",     1, 11, 3700,  75, 25, "EasyJet trained. Expert in quick turnaround cabin procedures."),
    ("Aisha Ibrahim",     0, 11, 3900,  79, 26, "Emirates trained. Multi-lingual Arabic-English-French service expert."),
    ("William Bennett",   1, 11, 3500,  70, 23, "British Airways graduate trainee. Excellent grooming and presentation."),
    ("Mei Zhao",          0, 11, 4400,  88, 31, "China Airlines senior purser. Mandarin, English, and Cantonese speaker."),
    ("Carlos Vega",       1, 11, 3800,  76, 25, "Aeromexico trained. Strong Spanish-English bilingual skills."),
    ("Natasha Popova",    0, 11, 4000,  80, 27, "Aeroflot senior crew. Expert in long-haul passenger management."),
    ("Daniel Okafor",     1, 11, 3600,  72, 24, "African World Airlines crew. West African route specialist."),
    ("Julie Marchand",    0, 11, 4200,  85, 29, "Air France senior cabin crew. Parisian elegance in passenger service."),
    ("Ryota Ito",         1, 11, 3700,  74, 25, "ANA trained. Japanese service precision and attention to detail."),
    ("Fatima Diallo",     0, 11, 3800,  77, 26, "Air Senegal crew. French-English-Wolof trilingual."),
    ("James Cooper",      1, 11, 3500,  70, 23, "Delta trainee. Sports background gives excellent stamina for long flights."),
    ("Elena Petrov",      0, 11, 4100,  82, 28, "S7 Airlines crew. Expert in Russian domestic and international service."),
    ("Gabriel Silva",     1, 11, 3600,  73, 24, "TAM Brasil trained. Portuguese-English-Spanish service skills."),
    ("Charlotte King",    0, 11, 4300,  86, 30, "Qantas purser. Expert Australian and Pacific route cabin management."),
    ("Kwame Mensah",      1, 11, 3700,  75, 25, "Ghana International crew. West Africa specialist."),
    ("Nadia Blanc",       0, 11, 4000,  80, 27, "Swiss International trained. Renowned Swiss precision and discretion."),
    ("Patrick Nguyen",    1, 11, 3600,  72, 24, "Vietnam Airlines background. South-East Asia specialist."),
    ("Ana Rodrigues",     0, 11, 4200,  84, 29, "TAP Air Portugal crew. Atlantic island route specialist."),
    ("Tobias Weiss",      1, 11, 3500,  70, 23, "Condor trainee. Holiday charter specialist in training."),
    ("Soo-Jin Lee",       0, 11, 4100,  83, 28, "Asiana trained purser. Korean hospitality standards master."),
    ("Ibrahim Traore",    1, 11, 3600,  72, 24, "Air Mali crew. West African hospitality focus."),
    ("Marta Kowalczyk",   0, 11, 3900,  79, 26, "LOT trained. Eastern European and transatlantic route crew."),
    ("Samir Khalil",      1, 11, 3800,  76, 25, "Royal Jordanian trained. Arabic and English customer service."),
    ("Ingrid Dahl",       0, 11, 4200,  85, 30, "Norwegian Air crew. Transatlantic low-cost cabin standards."),
    ("Diego Herrera",     1, 11, 3600,  72, 24, "Avianca trainee. Latin American domestic route specialist."),
    ("Lena Schmidt",      0, 11, 4000,  80, 27, "Eurowings crew. European short-haul efficiency expert."),
    ("Ji-Ho Nam",         1, 11, 3700,  74, 25, "Jeju Air trained. Korean low-cost carrier efficiency."),
    ("Amara Diallo",      0, 11, 3800,  77, 26, "Air Cote d'Ivoire crew. French-English bilingual West African specialist."),
    ("Ethan Brooks",      1, 11, 3500,  70, 23, "American Airlines trainee. US domestic routes."),
    ("Vera Horvatova",    0, 11, 4100,  83, 28, "Czech Airlines crew. Central European route specialist."),
    ("Boubacar Bah",      1, 11, 3600,  72, 24, "Guinée Air crew. West African route specialist."),
    ("Rosa Esposito",     0, 11, 4300,  87, 30, "ITA Airways purser. Mediterranean route passenger service."),
    ("Ade Williams",      1, 11, 3700,  75, 25, "Air Nigeria crew. Lagos hub hospitality specialist."),
    ("Freya Andersen",    0, 11, 4000,  80, 27, "SAS cabin crew. Expert in Scandinavian service culture."),

    # =========================================================================
    # CONSULTANTS — Art=1 (HR)
    # =========================================================================
    ("Patricia Voss",     0, 1, 8000,  82, 38, "Former HR director at a major European airline. Specialises in pilot recruitment and retention."),
    ("James Harrington",  1, 1, 9000,  90, 45, "20 years in aviation HR. Has restructured staff departments at three major carriers."),
    ("Lena Braun",        0, 1, 6500,  65, 28, "Fresh HR graduate with internship at a regional carrier. Ambitious and data-driven."),
    ("Kofi Asante",       1, 1, 7500,  75, 35, "African aviation HR specialist. Experienced in multicultural workforce management."),
    ("Isabelle Renaud",   0, 1, 8500,  88, 42, "Air France HR veteran. Expert in union negotiations and collective agreements."),

    # =========================================================================
    # CONSULTANTS — Art=2 (Fuel)
    # =========================================================================
    ("Werner Kohl",       1, 2, 7000,  72, 40, "Former fuel logistics manager at a major German airport. Knows every fuel supplier in Europe."),
    ("Sandra Liu",        0, 2, 8000,  83, 36, "Petroleum engineer turned aviation fuel consultant. Excellent cost reduction track record."),
    ("Tariq Nasser",      1, 2, 7500,  78, 38, "Gulf fuel broker with contacts across Middle Eastern suppliers."),
    ("Helen Burke",       0, 2, 6500,  65, 30, "Young fuel analyst with strong quantitative skills."),
    ("Gerhard Mayer",     1, 2, 9000,  91, 50, "Retired oil company executive. Reduced fuel costs by 18% at his last airline posting."),

    # =========================================================================
    # CONSULTANTS — Art=3 (Routes)
    # =========================================================================
    ("Nicolas Faure",     1, 3, 8500,  87, 43, "Route planning expert from a major European hub carrier. Optimised dozens of route networks."),
    ("Akosua Mensah",     0, 3, 7500,  76, 34, "African route specialist. Deep knowledge of bilateral agreements across the continent."),
    ("Jens Holst",        1, 3, 7000,  72, 37, "Former Scandinavian route planner. Expert in thin markets and seasonal demand."),
    ("Beatriz Campos",    0, 3, 8000,  82, 40, "Latin American route consultant. Unlocked new high-demand corridors for three carriers."),
    ("Eun-Ji Baek",       0, 3, 8200,  84, 38, "Asian route economist. Specialises in yield optimisation across Pacific routes."),

    # =========================================================================
    # CONSULTANTS — Art=4 (Contracts)
    # =========================================================================
    ("Frederick Holt",    1, 4, 11000, 95, 52, "Aviation contract lawyer turned consultant. Negotiated bilateral agreements at ministerial level."),
    ("Amelia Russo",      0, 4, 9500,  92, 46, "Alitalia contract director. Expert in EU Open Skies agreements."),
    ("Rashid Aziz",       1, 4, 8000,  82, 38, "Middle East contract specialist. Excellent government relations."),
    ("Ingeborg Hansen",   0, 4, 7500,  76, 34, "Nordic contract analyst. Strong EU aviation law background."),
    ("Eduardo Lopes",     1, 4, 8500,  87, 43, "LATAM contracts veteran. South American regulatory expert."),

    # =========================================================================
    # CONSULTANTS — Art=5 (Finance)
    # =========================================================================
    ("Wilhelm Stern",     1, 5, 12000, 96, 55, "Former CFO of a European airline. Restructured three near-bankrupt carriers."),
    ("Christine Dao",     0, 5, 10000, 92, 47, "Investment banker turned airline finance consultant. Cost reduction specialist."),
    ("Marcus Goldberg",   1, 5, 8500,  87, 40, "Aviation financial analyst. Expert in aircraft leasing and capital structure."),
    ("Yolanda Ferreira",  0, 5, 7500,  76, 33, "Young finance consultant. Strong airline revenue management background."),
    ("Pavel Horák",       1, 5, 9000,  90, 45, "Eastern European finance expert. Navigated currency risk for regional carriers."),

    # =========================================================================
    # CONSULTANTS — Art=6 (Info)
    # =========================================================================
    ("Sebastian Vogel",   1, 6, 7000,  73, 36, "Aviation data analyst. Expert in market intelligence and competitor analysis."),
    ("Miriam Schulte",    0, 6, 8000,  83, 40, "Former aviation journalist turned industry consultant. Excellent market insight."),
    ("Takuo Ishida",      1, 6, 8500,  88, 44, "Japanese aviation market specialist. Deep contacts in Asia-Pacific industry."),
    ("Florence Osei",     0, 6, 6500,  67, 29, "Young analyst specialising in emerging market aviation data."),
    ("Anton Rabe",        1, 6, 7500,  78, 38, "Aviation economist. Published researcher on hub efficiency and passenger behaviour."),

    # =========================================================================
    # CONSULTANTS — Art=7 (Aircraft)
    # =========================================================================
    ("Reinhard Kessler",  1, 7, 11000, 95, 53, "Former Boeing technical representative. Expert in wide-body fleet transition."),
    ("Isabelle Monet",    0, 7, 9500,  91, 47, "Airbus fleet planning consultant. Helped four carriers upgrade from classic to neo."),
    ("Kenji Fujii",       1, 7, 8500,  87, 42, "Aircraft leasing specialist. Strong ACMI and dry-lease market contacts."),
    ("Sandra Hartmann",   0, 7, 7500,  76, 35, "Aircraft acquisition analyst. Excellent knowledge of used aircraft market values."),
    ("Thomas Novak",      1, 7, 9000,  91, 48, "Airframe engineer turned consultant. Expert in airworthiness directives and cost impact."),

    # =========================================================================
    # CONSULTANTS — Art=8 (Maintenance)
    # =========================================================================
    ("Dietrich Sauer",    1, 8, 9500,  92, 50, "Former Lufthansa Technik director. Reduced maintenance costs by 22% at his last airline."),
    ("Yuki Ishikawa",     0, 8, 8500,  87, 43, "ANA maintenance planning veteran. Expert in predictive maintenance scheduling."),
    ("Brian Walsh",       1, 8, 7500,  77, 37, "Boeing certified maintenance consultant. Engine overhaul specialist."),
    ("Nathalie Girard",   0, 8, 8000,  82, 40, "Air France Industries alumni. Expert in heavy maintenance outsourcing deals."),
    ("Georgi Ivanov",     1, 8, 7000,  72, 34, "Eastern European MRO specialist. Low-cost maintenance solutions network."),

    # =========================================================================
    # CONSULTANTS — Art=9 (Security)
    # =========================================================================
    ("Klaus Herrmann",    1, 9, 9000,  91, 48, "Former Bundespolizei aviation security chief. Expert in airport vulnerability assessment."),
    ("Amina Okafor",      0, 9, 8000,  83, 40, "African Union aviation security specialist. Excellent threat assessment skills."),
    ("Richard Lawson",    1, 9, 10000, 94, 52, "Ex-TSA senior official. Comprehensive knowledge of North American security protocols."),
    ("Isabeau Clement",   0, 9, 7500,  77, 35, "Interpol aviation liaison. International security intelligence background."),
    ("Hamid Rahimi",      1, 9, 8500,  87, 45, "Middle East aviation security consultant. Expert in regional threat landscapes."),
]

# ---------------------------------------------------------------------------
# Read existing piloten.csv
# ---------------------------------------------------------------------------
def read_existing(path):
    with open(path, "r", encoding="cp1252", errors="replace") as f:
        lines = f.readlines()
    header = lines[0].rstrip("\n")
    workers = {}  # name -> raw line
    for line in lines[1:]:
        line = line.rstrip("\n")
        if not line:
            continue
        parts = line.split(";")
        name = parts[0] if parts else ""
        workers[name] = line
    return header, workers

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    if not os.path.exists(DECODED_CSV):
        print(f"ERROR: cannot find {DECODED_CSV}", file=sys.stderr)
        sys.exit(1)

    header, existing = read_existing(DECODED_CSV)

    new_rows = {}
    for entry in NEW_WORKERS:
        name, geschlecht, art, gehalt, talent, alter, kommentar = entry
        row = f"{name};{geschlecht};{art};{gehalt};{talent};{alter};{kommentar}"
        new_rows[name] = row

    collisions = set(existing.keys()) & set(new_rows.keys())
    if collisions:
        print(f"WARNING: {len(collisions)} worker(s) already exist and will be SKIPPED:")
        for c in sorted(collisions):
            print(f"  - {c}")

    merged = dict(existing)
    added = 0
    for name, row in new_rows.items():
        if name not in merged:
            merged[name] = row
            added += 1

    with open(DECODED_CSV, "w", encoding="cp1252", errors="replace", newline="\r\n") as f:
        f.write(header + "\n")
        for row in merged.values():
            f.write(row + "\n")

    total = len(merged)
    print(f"Done.  {added} new workers added.  Total: {total} workers.")
    print(f"Output: {DECODED_CSV}")

    if total > MAX_WORKERS:
        print(f"WARNING: {total} workers exceeds MAX_WORKERS={MAX_WORKERS} — bump defines.h!")

if __name__ == "__main__":
    main()
