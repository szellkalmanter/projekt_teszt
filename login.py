import streamlit as st
import pandas as pd
from faker import Faker
import random
from datetime import datetime

# --- BIZTONSÁGI NAPLÓZÓ FUNKCIÓ ---
def log_bejelentezes(felhasznalonev):
    # Lekérjük az időpontot
    most = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Megpróbáljuk kiolvasni a böngésző adatait (Eszköz/Böngésző)
    eszkosz_info = "Ismeretlen eszköz"
    if "X-Forwarded-For" in st.context.headers:
        # Streamlit Cloud környezetben látja a böngészőt
        eszkosz_info = st.context.headers.get("User-Agent", "Ismeretlen eszköz")
    
    # Beírjuk a log.txt fájlba a háttérben
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(f"{most} | Felhasználó: {felhasznalonev} | Eszköz: {eszkosz_info}\n")

# --- 1. Tesztadat generátor funkció ---
def generalj_teszt_adatokat():
    fake = Faker('hu_HU')
    ugyfelek = []
    for i in range(1, 21):
        ugyfel_id = f"UGY-{1000+i}"
        ugylet_id = f"UGL-{5000+i}"
        ugyfelek.append({
            "Ügyfél ID": ugyfel_id,
            "Ügyfél Neve": fake.name(),
            "Ügylet ID": ugylet_id,
            "Ügylet Összeg (HUF)": random.randint(500000, 15000000),
            "Fedezet Típusa": random.choice(["Ingatlan", "Készpénz", "Gépjármű", "Nincs"]),
            "Számlaszám": fake.bank_account_number(),
            "Státusz": random.choice(["Aktív", "Bírálat alatt", "Lezárt"])
        })
    return pd.DataFrame(ugyfelek)

# --- 2. Bejelentkező képernyő fázis ---
if 'bejelentkezve' not in st.session_state:
    st.session_state['bejelentkezve'] = False

if not st.session_state['bejelentkezve']:
    st.title("🔒 Back Office Rendszer - Belépés")
    st.subheader("Kérjük, adja meg a biztonságos belépési adatokat")
    
    felhasznalonev = st.text_input("Felhasználónév")
    jelszo = st.text_input("Jelszó", type="password")
    
    if st.button("Belépés"):
        # ERŐS JELSZAVAK: Ezt írjátok be majd a belépéshez!
        if felhasznalonev == "Ricsi" and jelszo == "^ZazX^{K697|":
            st.session_state['bejelentkezve'] = True
            log_bejelentezes("admin") # NAPLÓZÁS INDÍTÁSA
            st.rerun()
        elif felhasznalonev == "Boti" and jelszo == "8k=8Q4Lk>|6+":
            st.session_state['bejelentkezve'] = True
            log_bejelentezes("barat") # NAPLÓZÁS INDÍTÁSA
            st.rerun()
        else:
            st.error("Hibás felhasználónév vagy jelszó!")

# --- 3. Fő alkalmazás fázis (Sikeres belépés után) ---

        except FileNotFoundError:
            st.info("Még nem történt bejelentkezés (a napló üres).")

st.set_page_config(
    page_title="Menüválasztó", 
    layout="centered"
st.title("Menüválasztó")
st.divider()
st.page_link("vallalatihitel.py", label="Vállalati Hitelezés",)
st.divider()
st.page_link("Faktorálás.py", label=("Faktorálás",)
st.divider()
st.page_link("login.py", label=("Kilépés",)
