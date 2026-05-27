import streamlit as st

st.title("🎛️ Menüválasztó Oldal")
st.write("Sikeresen átléptél a másik URL-re!")

# Visszalépés gomb a főoldalra (URL-váltással)
if st.button("⬅️ Vissza a Belépőre"):
    st.switch_page("login.py")
