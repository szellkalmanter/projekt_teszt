Python
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
        # ERŐS JELSZAVAK
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

# --- 3. Fő alkalmazás fázis (Sikeres belépés után) ---
else:
    st.title("Főoldal")
    st.sidebar.write("Bejelentkezve: **Sikeres!**")
    
    if st.sidebar.button("Kijelentkezés"):
        st.session_state['bejelentkezve'] = False
        st.rerun()

    st.info("Sikeresen bent vagy a rendszerben!")
    
    # Modern, kőbiztos átirányítás a menüválasztóra
    if st.button("Kattints ide a Menüválasztó megnyitásához ➡️"):
        st.switch_page("pages/menuvalaszto.py")
        
    st.divider()

    # Három fül: Adatok, Riportok és a Biztonsági Napló
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
        st.write("Itt láthatjátok, ki és mikor lépett be a rendszerbe.")
        try:
            with open("log.txt", "r", encoding="utf-8") as f:
                logok = f.read()
            st.text(logok)
        except FileNotFoundError:
            st.info("Még nem történt bejelentkezés (a napló üres).")
