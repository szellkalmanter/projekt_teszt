import streamlit as st

st.title("🎛️ Menüválasztó Oldal")
st.write("Vállalati hitel nyilvántartás")
st.write("Faktor nyilvántartás")
# Visszalépés gomb a főoldalra (URL-váltással)
if st.button("⬅️ Vissza a Belépőre"):
    st.switch_page("login.py")
