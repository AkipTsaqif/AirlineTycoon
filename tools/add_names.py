#!/usr/bin/env python3
"""
add_names.py  -  Expand Names.csv with diverse international names

- Reads  tools/decoded/Names.csv
- Adds female (Art=0), male (Art=1), last names (Art=2)
- Skips duplicates
- Preserves non-name rows (copy-protection numeric entries)
- Writes back to tools/decoded/Names.csv

Run from the repo root:
    python tools/add_names.py
"""

import os, sys

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
DECODED_CSV = os.path.join(SCRIPT_DIR, "decoded", "Names.csv")

MAX_PNAMES1 = 1000  # must match defines.h (FNames + MNames each)
MAX_PNAMES2 = 500   # must match defines.h (LNames)

# ---------------------------------------------------------------------------
# New names — diverse international pool
# Art=0: female first names
# Art=1: male first names
# Art=2: last names
# ---------------------------------------------------------------------------

NEW_FEMALE = [
    # European
    "Sofia", "Isabella", "Emma", "Olivia", "Mia", "Lea", "Laura", "Julia",
    "Hannah", "Lena", "Maria", "Elena", "Nina", "Lisa", "Clara", "Sara",
    "Eva", "Ida", "Iris", "Nora", "Rosa", "Vera", "Ines", "Katja",
    "Monika", "Renate", "Sabine", "Ursula", "Helga", "Ingrid", "Astrid",
    "Sigrid", "Hilde", "Gerda", "Ilse", "Erika", "Greta", "Else",
    "Theresa", "Magdalena", "Veronika", "Stefanie", "Claudia", "Kerstin",
    "Nadine", "Nicole", "Silvia", "Susanne", "Birgit", "Cornelia",
    "Dorothea", "Elisabeth", "Friederike", "Gabriele", "Heike",
    # British/American
    "Charlotte", "Amelia", "Ava", "Sophia", "Abigail", "Madison",
    "Harper", "Evelyn", "Elizabeth", "Scarlett", "Grace", "Chloe",
    "Victoria", "Penelope", "Riley", "Zoey", "Nora", "Lily", "Eleanor",
    "Hannah", "Lillian", "Addison", "Aubrey", "Ellie", "Stella",
    "Natalie", "Zoe", "Leah", "Hazel", "Violet", "Aurora", "Savannah",
    "Audrey", "Brooklyn", "Bella", "Claire", "Skylar", "Lucy",
    "Paisley", "Everly", "Anna", "Caroline", "Nova", "Genesis", "Emilia",
    "Kennedy", "Samantha", "Maya", "Willow", "Kinsley", "Naomi",
    # French
    "Camille", "Manon", "Chloe", "Lucie", "Mathilde", "Pauline",
    "Marie", "Julie", "Aurelie", "Celine", "Valerie", "Nathalie",
    "Isabelle", "Veronique", "Sandrine", "Laetitia", "Elodie", "Amandine",
    # Spanish/Latin
    "Valentina", "Lucia", "Catalina", "Gabriela", "Natalia", "Daniela",
    "Alejandra", "Valeria", "Camila", "Mariana", "Fernanda", "Paola",
    "Andrea", "Monica", "Diana", "Lorena", "Adriana", "Claudia",
    # Asian
    "Yuki", "Akiko", "Keiko", "Yoko", "Hanako", "Naoko", "Sachiko",
    "Aiko", "Emi", "Hana", "Mei", "Lin", "Wei", "Xiu", "Fang",
    "Priya", "Anita", "Sunita", "Kavita", "Nisha", "Pooja", "Deepa",
    "Soo", "Ji-Young", "Hyun", "Yuna", "Min-Ji", "So-Yeon",
    # Arabic/Middle Eastern
    "Fatima", "Aisha", "Zainab", "Maryam", "Nadia", "Layla", "Rania",
    "Dina", "Hana", "Yasmin", "Leila", "Salma", "Sara", "Samira",
    # African
    "Amara", "Imani", "Zara", "Nia", "Adaeze", "Chioma", "Ngozi",
    "Amirah", "Fatou", "Mariama", "Kadiatou", "Aminata",
    # Eastern European
    "Anastasia", "Natasha", "Tatiana", "Irina", "Svetlana", "Olga",
    "Ekaterina", "Darya", "Alina", "Oksana", "Yulia", "Galina",
    "Ludmila", "Natalya", "Larisa", "Valentina", "Yelena", "Marina",
    "Zuzanna", "Agnieszka", "Malgorzata", "Katarzyna", "Monika",
    "Magdalena", "Joanna", "Anna", "Barbara", "Beata", "Dorota",
    # Scandinavian
    "Freya", "Maja", "Elsa", "Elin", "Lovisa", "Klara", "Fanny",
    "Ebba", "Tilda", "Agnes", "Hedvig", "Birgitte", "Ragnhild",
    "Solveig", "Signe", "Inga", "Bodil", "Turid",
]

NEW_MALE = [
    # European
    "Luca", "Marco", "Matteo", "Lorenzo", "Davide", "Federico",
    "Alessandro", "Stefano", "Andrea", "Massimo", "Roberto", "Antonio",
    "Francesco", "Giovanni", "Paolo", "Giuseppe", "Enzo", "Carlo",
    "Giorgio", "Sergio", "Mauro", "Claudio", "Fabio", "Simone",
    "Klaus", "Dieter", "Werner", "Günter", "Wolfgang", "Horst",
    "Gerhard", "Manfred", "Heinz", "Jürgen", "Rainer", "Stefan",
    "Matthias", "Markus", "Florian", "Sebastian", "Christoph",
    "Dominik", "Fabian", "Jan", "Lukas", "Maximilian", "Niklas",
    "Felix", "Leon", "Jonas", "Noah", "Paul", "Jakob",
    # British/American
    "James", "Oliver", "William", "Benjamin", "Elijah", "Lucas",
    "Mason", "Ethan", "Aiden", "Logan", "Jackson", "Sebastian",
    "Mateo", "Jack", "Owen", "Theodore", "Liam", "Noah",
    "Ryan", "Nathan", "Aaron", "Isaac", "Caleb", "Connor",
    "Dylan", "Evan", "Hunter", "Jordan", "Tyler", "Zachary",
    "Brandon", "Austin", "Justin", "Nicholas", "Eric", "Sean",
    "Kyle", "Jason", "Brian", "Scott", "Donald", "Gary",
    "Edward", "Ronald", "Timothy", "Kenneth", "Steven", "Joseph",
    # French
    "Antoine", "Mathieu", "Julien", "Nicolas", "Romain", "Maxime",
    "Pierre", "Guillaume", "Baptiste", "Alexandre", "Sebastien",
    "Christophe", "Laurent", "Frederic", "Vincent", "Benoit",
    "Thierry", "Xavier", "Philippe", "Bruno", "Stephane",
    # Spanish/Latin
    "Santiago", "Matias", "Sebastian", "Emiliano", "Tomas",
    "Juan", "Carlos", "Miguel", "Jose", "Luis", "Jorge",
    "Fernando", "Ricardo", "Pablo", "Eduardo", "Francisco",
    "Alejandro", "Diego", "Andres", "Rodrigo", "Gabriel",
    # Asian
    "Kenji", "Takashi", "Hiroshi", "Yoshio", "Makoto", "Daisuke",
    "Kazuki", "Ryota", "Shota", "Yuto", "Wei", "Ming", "Jian",
    "Hao", "Feng", "Raj", "Vikram", "Arjun", "Suresh", "Ramesh",
    "Min-Jun", "Ji-Ho", "Sung", "Hyun-Soo", "Jae-Won",
    # Arabic/Middle Eastern
    "Mohammed", "Ahmed", "Ali", "Omar", "Hassan", "Ibrahim",
    "Yusuf", "Khalid", "Tariq", "Samir", "Karim", "Nasser",
    "Faisal", "Hamid", "Walid", "Ziad", "Rami", "Bilal",
    # African
    "Kwame", "Kofi", "Ade", "Chukwu", "Emeka", "Tunde",
    "Seun", "Babatunde", "Oluwaseun", "Ibrahim", "Mamadou",
    "Moussa", "Oumar", "Amadou", "Boubacar",
    # Eastern European
    "Dmitri", "Sergei", "Alexei", "Nikolai", "Vladimir", "Andrei",
    "Igor", "Pavel", "Roman", "Viktor", "Maxim", "Artem",
    "Mikhail", "Konstantin", "Stanislav", "Bogdan", "Ruslan",
    "Piotr", "Krzysztof", "Tomasz", "Marek", "Pawel", "Lukasz",
    "Rafal", "Michal", "Marcin", "Jacek", "Grzegorz", "Adam",
    # Scandinavian
    "Erik", "Lars", "Bjorn", "Sven", "Magnus", "Gunnar", "Olaf",
    "Torbjorn", "Eirik", "Leif", "Sigurd", "Ragnar", "Vidar",
    "Henning", "Rolf", "Knut", "Dag", "Arne", "Einar",
]

NEW_LAST = [
    # German
    "Weber", "Meyer", "Wagner", "Becker", "Schulz", "Hoffmann",
    "Schäfer", "Koch", "Bauer", "Richter", "Klein", "Wolf",
    "Schröder", "Neumann", "Schwarz", "Zimmermann", "Braun",
    "Krüger", "Hofmann", "Lange", "Hildebrandt", "Lehmann",
    "Maurer", "Brandt", "Vogt", "König", "Walter", "Mayer",
    "Huber", "Steiner", "Gruber", "Wimmer", "Winkler", "Pichler",
    "Moser", "Berger", "Auer", "Brunner", "Fuchs", "Hahn",
    "Hermann", "Kaiser", "Keller", "Krause", "Kunze", "Lenz",
    "Ludwig", "Martens", "Naumann", "Otto", "Ritter", "Roth",
    # British/American
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia",
    "Miller", "Davis", "Wilson", "Anderson", "Taylor", "Thomas",
    "Jackson", "White", "Harris", "Martin", "Thompson", "Robinson",
    "Lewis", "Walker", "Hall", "Allen", "Young", "King",
    "Wright", "Scott", "Green", "Baker", "Adams", "Nelson",
    "Hill", "Ramirez", "Campbell", "Mitchell", "Roberts", "Carter",
    "Phillips", "Evans", "Turner", "Torres", "Parker", "Collins",
    "Edwards", "Stewart", "Flores", "Morris", "Nguyen", "Murphy",
    "Rivera", "Cook", "Rogers", "Morgan", "Peterson", "Cooper",
    "Reed", "Bailey", "Bell", "Gomez", "Kelly", "Howard",
    # French
    "Dupont", "Durand", "Lefebvre", "Moreau", "Laurent", "Simon",
    "Michel", "Leroy", "Roux", "David", "Bertrand", "Morel",
    "Girard", "Bonnet", "Dupuis", "Lambert", "Fontaine", "Rousseau",
    "Vincent", "Muller", "Garnier", "Chevalier", "Faure", "Gauthier",
    # Spanish/Italian
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Perez", "Sanchez", "Ramirez", "Flores", "Cruz", "Reyes",
    "Ferrari", "Rossi", "Russo", "Romano", "Ricci", "Marino",
    "Greco", "Bruno", "Gallo", "Conti", "Esposito", "Bianchi",
    # Eastern European
    "Novak", "Kovac", "Horvat", "Babic", "Kovacevic", "Petrovic",
    "Jovanovic", "Nikolic", "Markovic", "Stojanovic", "Ilic",
    "Popov", "Ivanov", "Petrov", "Smirnov", "Kuznetsov", "Sokolov",
    "Volkov", "Morozov", "Kozlov", "Pavlov", "Lebedev", "Fedorov",
    "Kowalski", "Wojcik", "Kowalczyk", "Kaminski", "Lewandowski",
    "Zielinski", "Szymanski", "Wozniak", "Dabrowski", "Kozlowski",
    # Scandinavian
    "Andersen", "Nielsen", "Hansen", "Pedersen", "Jensen", "Larsen",
    "Sorensen", "Christensen", "Poulsen", "Madsen", "Kristensen",
    "Lindqvist", "Bergstrom", "Lundgren", "Eriksson", "Lindberg",
    "Johansson", "Nilsson", "Karlsson", "Persson", "Olsson",
    "Gustafsson", "Pettersson", "Andersson", "Magnusson",
    # Asian
    "Yamamoto", "Tanaka", "Watanabe", "Ito", "Kobayashi", "Nakamura",
    "Matsumoto", "Inoue", "Kimura", "Hayashi", "Shimizu", "Yamazaki",
    "Wang", "Li", "Zhang", "Liu", "Chen", "Yang", "Huang", "Zhao",
    "Kim", "Lee", "Park", "Choi", "Jung", "Kang", "Cho", "Yoon",
    "Patel", "Sharma", "Singh", "Kumar", "Verma", "Gupta",
    # Arabic/African
    "Al-Rashid", "Al-Hassan", "Al-Farsi", "Mansour", "Khalil",
    "Nasser", "Badawi", "Aziz", "Rahim", "Osman", "Diallo",
    "Traore", "Coulibaly", "Camara", "Bah", "Toure", "Keita",
    # Misc international
    "O'Brien", "O'Connor", "Murphy", "Walsh", "Burke", "Fitzgerald",
    "Kennedy", "McCarthy", "Flynn", "Brennan", "Doyle", "Sullivan",
    "Van der Berg", "Van Dijk", "De Groot", "De Vries", "Bakker",
    "Visser", "Smit", "Meijer", "De Jong", "Janssen",
]

# ---------------------------------------------------------------------------
# Read existing Names.csv
# ---------------------------------------------------------------------------
def read_existing(path):
    with open(path, "r", encoding="cp1252", errors="replace") as f:
        lines = f.readlines()

    header = lines[0].rstrip("\n")
    female, male, last = set(), set(), set()
    other_rows = []   # non-name rows (copy-protection data etc.)
    name_rows  = []   # (art, name) tuples in original order

    for line in lines[1:]:
        line = line.rstrip("\n")
        if not line:
            continue
        parts = line.split(";")
        try:
            art = int(parts[0])
        except ValueError:
            other_rows.append(line)
            continue

        if art == 0:
            female.add(parts[1])
            name_rows.append((0, parts[1]))
        elif art == 1:
            male.add(parts[1])
            name_rows.append((1, parts[1]))
        elif art == 2:
            last.add(parts[1])
            name_rows.append((2, parts[1]))
        else:
            other_rows.append(line)

    return header, female, male, last, name_rows, other_rows

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    if not os.path.exists(DECODED_CSV):
        print(f"ERROR: cannot find {DECODED_CSV}", file=sys.stderr)
        sys.exit(1)

    header, existing_f, existing_m, existing_l, name_rows, other_rows = read_existing(DECODED_CSV)

    added_f = added_m = added_l = 0

    for name in NEW_FEMALE:
        if name not in existing_f:
            name_rows.append((0, name))
            existing_f.add(name)
            added_f += 1

    for name in NEW_MALE:
        if name not in existing_m:
            name_rows.append((1, name))
            existing_m.add(name)
            added_m += 1

    for name in NEW_LAST:
        if name not in existing_l:
            name_rows.append((2, name))
            existing_l.add(name)
            added_l += 1

    total_f = len(existing_f)
    total_m = len(existing_m)
    total_l = len(existing_l)

    with open(DECODED_CSV, "w", encoding="cp1252", errors="replace", newline="\r\n") as f:
        f.write(header + "\n")
        for art, name in name_rows:
            f.write(f"{art};{name}\n")
        for row in other_rows:
            f.write(row + "\n")

    print(f"Done.")
    print(f"  Female names: +{added_f} new  (total {total_f})")
    print(f"  Male names:   +{added_m} new  (total {total_m})")
    print(f"  Last names:   +{added_l} new  (total {total_l})")
    print(f"Output: {DECODED_CSV}")

    if total_f > MAX_PNAMES1: print(f"WARNING: {total_f} female names exceeds MAX_PNAMES1={MAX_PNAMES1}!")
    if total_m > MAX_PNAMES1: print(f"WARNING: {total_m} male names exceeds MAX_PNAMES1={MAX_PNAMES1}!")
    if total_l > MAX_PNAMES2: print(f"WARNING: {total_l} last names exceeds MAX_PNAMES2={MAX_PNAMES2}!")

if __name__ == "__main__":
    main()
