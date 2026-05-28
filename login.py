import streamlit as st
import pandas as pd
from faker import Faker
import random
from datetime import datetime

# --- BIZTONSÁGI NAPLÓZÓ FUNKCIÓ ---
def log_bejelentezes(felhasznalonev):
    most = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    eszkosz_info = "Ismeretlen eszköz"
    if "X-Forwarded-For" in st.context.headers:
        eszkosz_info = st.context.headers.get("User-Agent", "Ismeretlen eszköz")
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(f"{most} | Felhasználó: {felhasznalonev} | Eszköz: {eszkosz_info}\n")

# --- Tesztadat generátor funkció ---
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

# --- 1. OLDALAK DEFINIÁLÁSA (A RENDSER EZ ALAPJÁN ÉPÍTI AZ URL-EKET) ---
login_page = st.Page("login.py", title="Bejelentkezés", icon="🔒")
menu_page = st.Page("pages/menuvalaszto.py", title="Menüválasztó", icon="🎛️")
partner_page = st.Page("pages/partner_adatok.py", title="Partner Adatok", icon="🤝")

# Session state inicializálás
if 'bejelentkezve' not in st.session_state:
    st.session_state['bejelentkezve'] = False

# --- 2. DINAMIKUS NAVIGÁCIÓS LOGIKA ---
if not st.session_state['bejelentkezve']:
    # HA NINCS BEJELENTKEZVE: Csak a login oldalt adjuk át a navigációnak, a menüt elrejtjük
    pg = st.navigation([login_page], position="hidden")
else:
    # HA BEJELENTKEZETT: Elérhetővé tesszük a menüt és a partner oldalt, normál oldalsávval
    pg = st.navigation([menu_page, partner_page], position="sidebar")

# Ez a parancs futtatja le a kiválasztott oldalt
pg.run()

# --- 3. RENDERSPECIFIKUS TARTALOM (Kizárólag akkor fut le, ha a login_page aktív) ---
if not st.session_state['bejelentkezve']:
    st.title("🔒 Back Office Rendszer - Belépés")
    st.subheader("Kérjük, adja meg a biztonságos belépési adatokat")
    
    felhasznalonev = st.text_input("Felhasználónév")
    jelszo = st.text_input("Jelszó", type="password")
    
    if st.button("Belépés"):
        if felhasznalonev == "Ricsi" and jelszo == "^ZazX^{K697|":
            st.session_state['bejelentkezve'] = True
            log_bejelentezes("admin")
            st.rerun()
        elif felhasznalonev == "Boti" and jelszo == "8k=8Q4Lk>|6+":
            st.session_state['bejelentkezve'] = True
            log_bejelentezes("barat")
            st.rerun()
        else:
            st.error("Hibás felhasználónév vagy jelszó!")