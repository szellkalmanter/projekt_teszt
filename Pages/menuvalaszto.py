import streamlit as st

st.title("🎛️ Menüválasztó Oldal")
if st.button("Vállalati hitel nyilvántartás"):
    st.switch_page("partner_adatok.py")
st.write("Faktor nyilvántartás")
# Visszalépés gomb a főoldalra (URL-váltással)
if st.button("⬅️ Vissza a Belépőre"):
    st.switch_page("login.py")
