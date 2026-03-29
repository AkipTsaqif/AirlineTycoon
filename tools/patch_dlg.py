import sys, os, subprocess, re

SRC = r"D:\Games\Steam\steamapps\common\Airline Tycoon Deluxe\misc\dlg_ger.res"
SCRIPT = os.path.join(os.path.dirname(__file__), "xtrle_decode.py")

# Decode
result = subprocess.run([sys.executable, SCRIPT, SRC], capture_output=True)
content = result.stdout.decode("latin-1")
print(f"Loaded {len(content.splitlines())} lines")

# Encoding constants (Windows-1252 read as latin-1)
EUR = "\x80"   # euro sign
U   = "\xfc"   # u-umlaut
O   = "\xf6"   # o-umlaut
SZ  = "\xdf"   # eszett
A_T = "\xe3"   # a-tilde (Portuguese a~)
O_T = "\xf5"   # o-tilde (Portuguese o~)
NL  = "\r\n"   # CRLF

# ── 1. Insert strings 696, 697, 698 after 695 ────────────────────────────────
anchor_695 = f"  D::[[P1\\MA\\145]]10 St{U}ck (=%s {EUR}){NL}{NL}>>0000700"

new_696_698 = (
f"{NL}>>0000696{NL}"
f"  B::Preciso de 25 ($ =%s ){NL}"
f"  E::I need 25 ($ =%s ){NL}"
f"  F::Il m'en faut 25 (=%s {EUR}){NL}"
f"  I::Ne voglio 25 (= %s $){NL}"
f"  N::Ik heb er 25 nodig (=%s $){NL}"
f"  O::Preciso de 25 (=%s $){NL}"
f"  S::25 unidades (Pts =%s ){NL}"
f"  D::25 St{U}ck (=%s {EUR}){NL}"
f"{NL}>>0000697{NL}"
f"  B::Preciso de 50 ($ =%s ){NL}"
f"  E::I need 50 ($ =%s ){NL}"
f"  F::Il m'en faut 50 (=%s {EUR}){NL}"
f"  I::Ne voglio 50 (= %s $){NL}"
f"  N::Ik heb er 50 nodig (=%s $){NL}"
f"  O::Preciso de 50 (=%s $){NL}"
f"  S::50 unidades (Pts =%s ){NL}"
f"  D::50 St{U}ck (=%s {EUR}){NL}"
f"{NL}>>0000698{NL}"
f"  B::Preciso de 100 ($ =%s ){NL}"
f"  E::I need 100 ($ =%s ){NL}"
f"  F::Il m'en faut 100 (=%s {EUR}){NL}"
f"  I::Ne voglio 100 (= %s $){NL}"
f"  N::Ik heb er 100 nodig (=%s $){NL}"
f"  O::Preciso de 100 (=%s $){NL}"
f"  S::100 unidades (Pts =%s ){NL}"
f"  D::100 St{U}ck (=%s {EUR}){NL}"
)

assert anchor_695 in content, f"FAIL: 695 anchor not found\nGot: {repr(content[content.find('>>0000695'):content.find('>>0000695')+300])}"
content = content.replace(
    anchor_695,
    f"  D::[[P1\\MA\\145]]10 St{U}ck (=%s {EUR}){NL}" + new_696_698 + f"{NL}>>0000700",
    1)
print("1. 696-698 inserted OK")

# ── 2. String 800 English ─────────────────────────────────────────────────────
old_800_E = ("  E::[[AA\\800]]I have storage tanks in all shapes, colors and sizes. "
             "10000 gallons for $ 10000, 30000 gallons for $ 20000, "
             "50000 gallons for $ 40000 and 100000 gallons for $ 60000!")
new_800_E = ("  E::[[AA\\800]]I have storage tanks in all shapes, colors and sizes. "
             "10000 gallons for $ 10000, 30000 gallons for $ 20000, "
             "50000 gallons for $ 40000, 100000 gallons for $ 60000, "
             "300000 gallons for $ 150000 and 1000000 gallons for $ 400000!")
assert old_800_E in content, "FAIL: 800 E not found"
content = content.replace(old_800_E, new_800_E, 1)
print("2. 800 English OK")

# ── 3. String 800 German ──────────────────────────────────────────────────────
m = re.search(r"  D::\[\[AA\\800\]\][^\r\n]+", content)
if m:
    old_800_D = m.group(0)
    # Strip trailing ! and append new sizes
    new_800_D = (old_800_D.rstrip("!") +
                 f", 300000l f{U}r {EUR} 150000 und 1000000l f{U}r {EUR} 400000!")
    content = content.replace(old_800_D, new_800_D, 1)
    print("3. 800 German OK")
else:
    print("WARN: 800 German not found, skipping")

# ── 4. Replace string 904; add 905, 906 ───────────────────────────────────────
m = re.search(r">>0000904\r\n(?:  [BEFINOSD]::[^\r\n]*\r\n)+  D::[^\r\n]*", content)
assert m, "FAIL: 904 block not found"
old_904 = m.group(0)

new_904_906 = (
f">>0000904{NL}"
f"  B::Vou levar o de 300000 gal{O_T}es ($ 150000).{NL}"
f"  E::I will take the one with 300000 gallons ($ 150000).{NL}"
f"  F::Je prendrai celui qui fait 300000 litres (150000 {EUR}).{NL}"
f"  I::Prendo quello da 300.000 litri (150.000 $).{NL}"
f"  N::Ik neem de tank van 300000l (150000 $).{NL}"
f"  O::Levo o de 300000 litros (150000$).{NL}"
f"  S::Me quedo con el de 300.000 l (15.000.000 Pts).{NL}"
f"  D::Ich nehme den mit 300000l (150000 {EUR}).{NL}"
f"{NL}>>0000905{NL}"
f"  B::Vou levar o de 1000000 gal{O_T}es ($ 400000).{NL}"
f"  E::I will take the one with 1000000 gallons ($ 400000).{NL}"
f"  F::Je prendrai celui qui fait 1000000 litres (400000 {EUR}).{NL}"
f"  I::Prendo quello da 1.000.000 litri (400.000 $).{NL}"
f"  N::Ik neem de tank van 1000000l (400000 $).{NL}"
f"  O::Levo o de 1000000 litros (400000$).{NL}"
f"  S::Me quedo con el de 1.000.000 l (40.000.000 Pts).{NL}"
f"  D::Ich nehme den mit 1000000l (400000 {EUR}).{NL}"
f"{NL}>>0000906{NL}"
f"  B::[[P1\\AA\\904]]N{A_T}o vou levar nenhum deles. Tchau.{NL}"
f"  E::[[P1\\AA\\904]]I don't want any of them. Bye.{NL}"
f"  F::[[P1\\AA\\904]]Je n'en prendrai aucun. Ciao.{NL}"
f"  I::[[P1\\AA\\904]]Non prendo nulla. Arrivederci.{NL}"
f"  N::[[P1\\AA\\904]]Ik neem er geen. Tot ziens.{NL}"
f"  O::[[P1\\AA\\904]]N{A_T}o levo nenhum. Adeus.{NL}"
f"  S::[[P1\\AA\\904]]No quiero ninguno. Hasta luego.{NL}"
f"  D::[[P1\\AA\\904]]Ich nehme gar keinen. Ciao."
)

content = content.replace(old_904, new_904_906, 1)
print("4. 904/905/906 OK")

# ── 5. Insert string 20280 after 20264 (grace period warning for morning briefing) ──
E_ACUTE = "\xe9"   # e-acute  (é)
A_ACUTE = "\xe1"   # a-acute  (á)
I_ACUTE = "\xed"   # i-acute  (í)
N_TILDE = "\xf1"   # n-tilde  (ñ)

anchor_20264_D = "  D::[[BO\\20264]]Perfekt. Einfach nur perfekt. Sie beherrschen Ihr Handwerk."
if ">>0020280" in content:
    print("5. 20280 already present, skipping")
else:
    assert anchor_20264_D in content, "FAIL: 20264 German anchor not found"

new_20280 = (
f"{NL}>>0020280{NL}"
f"  B::Faltam %s dia(s) para melhorar a imagem, ou ser{A_T}o removidos do aeroporto.{NL}"
f"  E::%s day(s) left to fix your image or you will be removed from the airport.{NL}"
f"  F::Il vous reste %s jour(s) pour am{E_ACUTE}liorer votre image, sinon vous serez renvoy{E_ACUTE}.{NL}"
f"  I::Restano %s giorno/i per migliorare la sua reputazione, altrimenti verr\xe0 rimosso.{NL}"
f"  N::Nog %s dag(en) om uw imago te verbeteren, anders wordt u verwijderd.{NL}"
f"  O::Faltam %s dia(s) para melhorar a imagem, caso contr{A_ACUTE}rio ser{A_ACUTE} removido.{NL}"
f"  S::Quedan %s d{I_ACUTE}a(s) para mejorar su imagen o ser{A_ACUTE}n expulsados del aeropuerto.{NL}"
f"  D::Noch %s Tag(e) zur Verbesserung des Images, sonst wird die Fluglinie ausgeschlossen.{NL}"
)

    content = content.replace(
        anchor_20264_D,
        anchor_20264_D + new_20280,
        1)
    print("5. 20280 grace period warning inserted OK")

# ── Write result ──────────────────────────────────────────────────────────────
with open(SRC, "w", encoding="latin-1", newline="") as f:
    f.write(content)
print(f"Written to {SRC} ({content.count(NL)} lines)")
