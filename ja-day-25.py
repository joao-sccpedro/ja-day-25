import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.set_page_config(page_title="Descubra o seu tema")

st.title("🔮 Descubra o seu destino!")

# Define the options
male_options = ["Astronaut", "Chef", "Engineer", "Firefighter", "Pilot"]
female_options = ["Astronaut", "Chef", "Engineer", "Firefighter", "Pilot", "Ballerina", "Fashion Designer"]
other_options = female_options  # Ou defina outro grupo se quiser

# Carregar dados existentes
try:
    df = pd.read_csv("user_data.csv")
except FileNotFoundError:
    df = pd.DataFrame(columns=["Timestamp", "Name", "Age", "Gender", "Result"])

# Formulário
with st.form("user_form"):
    name = st.text_input("Qual é o seu nome completo?").strip()
    age = st.text_input("Qual é a sua idade?").strip()
    gender = st.selectbox("Qual é o seu gênero?", ["Male", "Female", "Other/Prefer not to say"])

    submitted = st.form_submit_button("Enviar")

if submitted:
    # Verificar se nome já foi usado (normalizando espaços e maiúsculas/minúsculas)
    name_check = name.lower()

    if name_check in df["Name"].str.strip().str.lower().values:
        st.error("🚫 Este nome já foi utilizado. Você já preencheu antes!")
    else:
        # Escolher resultado baseado no gênero
        if gender == "Male":
            result = random.choice(male_options)
        elif gender == "Female":
            result = random.choice(female_options)
        else:
            result = random.choice(other_options)

        st.success(f"🎉 {name}, você vai ser... **{result}!**")

        # Salvar os dados
        user_data = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Name": name,
            "Age": age,
            "Gender": gender,
            "Result": result
        }

        df = pd.concat([df, pd.DataFrame([user_data])], ignore_index=True)
        df.to_csv("user_data.csv", index=False)

        st.info("Seu destino foi salvo. Obrigado!")
