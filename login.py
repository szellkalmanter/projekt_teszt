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

# Session state inicializálás
if 'bejelentkezve' not in st.session_state:
    st.session_state['bejelentkezve'] = False

# --- 1. FÁZIS: Ha nincs bejelentkezve (Login ablak + CSS elrejtés) ---
if not st.session_state['bejelentkezve']:
    # Sima CSS trükk, ami megpróbálja elrejteni a menüt
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {display: none !important;}
        </style>
        """,
        unsafe_allow_html=True
    )
    
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

# --- 2. FÁZIS: Ha sikeresen bejelentkezett (A Főoldal) ---
else:
    st.title("Főoldal")
    st.sidebar.write("Bejelentkezve: **Sikeres!**")
    
    if st.sidebar.button("Kijelentkezés"):
        st.session_state['bejelentkezve'] = False
        st.rerun()

    st.info("Sikeresen bent vagy a rendszerben!")
    
    # Visszaállítva a régi működő gomb a pages mappára
    if st.button("Kattints ide a Menüválasztó megnyitásához ➡️"):
        st.switch_page("pages/menuvalaszto.py")
        
    st.divider()

    tab1, tab2, tab3 = st.tabs(["📊 Adatok megtekintése", "⚙️ Excel Riport export", "🛡️ Biztonsági Napló (Logok)"])

    if 'adatok' not in st.session_state:
        st.session_state['adatok'] = generalj_teszt_adatokat()

    with tab1:
        st.header("Ügyfél és Ügylet adatok")
        st.dataframe(st.session_state['adatok'], use_container_width=True)

    with tab2:
        st.header("Rendszerfunkciók")
        if st.button("🔄 Új tesztadatok generálása"):
            st.session_state['adatok'] = generalj_teszt_adatokat()
            st.success("Adatbázis frissítve!")
            st.rerun()
        
        st.write("---")
        df = st.session_state['adatok']
        st.download_button(
            label="📥 Excel jelentés letöltése",
            data=df.to_csv(index=False).encode('utf-8-sig'),
            file_name='backoffice_ugylet_riport.csv',
            mime='text/csv',
        )

    with tab3:
        st.header("🛡️ Rendszer-hozzáférési napló")
        try:
            with open("log.txt", "r", encoding="utf-8") as f:
                logok = f.read()
            st.text(logok)
        except FileNotFoundError:
            st.info("Még nem történt bejelentkezés (a napló üres).")