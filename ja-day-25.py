import streamlit as st
import pandas as pd
import gspread
import random
from datetime import datetime
from gspread_dataframe import get_as_dataframe, set_with_dataframe

st.set_page_config(page_title="Descubra o seu tema!")
st.title("🔮 Descubra o seu tema!")

# ✅ Conectar ao Google Sheets
gc = gspread.service_account_from_dict(st.secrets["google_service_account"])
sh = gc.open("JA-Day-25")
worksheet = sh.sheet1

# ✅ Tentar ler os dados
try:
    df = get_as_dataframe(worksheet).dropna(how="all")

    # Se dataframe está vazio ou não tem as colunas, cria a estrutura
    if df.empty or not set(["Timestamp", "Name", "Age", "Gender", "Result"]).issubset(df.columns):
        df = pd.DataFrame(columns=["Timestamp", "Name", "Age", "Gender", "Result"])

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    df = pd.DataFrame(columns=["Timestamp", "Name", "Age", "Gender", "Result"])

# ✅ Opções de temas
male_options = [
    "**Futebol! ⚽**\n\nEm clima de Copa do Mundo de Clubes, você pode vir com a camisa de um time de futebol e, se quiser ir além, pode vir com chuteira e tudo.",
    "**Personagem! 🎭**\n\nPouco importa como. Pode ser cosplay, cospobre, máscara ou algum trocadilho. O importante é que você tem que representar algum personagem, seja histórico ou ficcional."
]

female_options = [
    "**Personagem! 🎭**\n\nPouco importa como. Pode ser cosplay, cospobre, máscara ou algum trocadilho. O importante é que você tem que representar algum personagem."
]

other_options = male_options  # Mesmos temas do masculino para 'outro'

# ✅ Formulário
with st.form("user_form"):
    name = st.text_input("Qual é o seu nome completo?").strip()
    age = st.text_input("Qual é a sua idade?").strip()
    gender = st.selectbox("Qual é o seu gênero?", ["Masculino", "Feminino", "Outro"])

    submitted = st.form_submit_button("Enviar")

if submitted:
    name_check = name.lower()

    # 🔍 Verificar se nome já existe
    if name_check in df["Name"].astype(str).str.strip().str.lower().values:
        st.error("🚫 Este nome já foi utilizado. Você já preencheu antes!")
    else:
        # 🎲 Escolher o tema
        if gender == "Masculino":
            result = random.choice(male_options)
        elif gender == "Feminino":
            result = random.choice(female_options)
        else:
            result = random.choice(other_options)

        st.success(f"🎉 {name}, o seu tema será... {result}")

        # 📝 Salvar os dados
        user_data = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Name": name,
            "Age": age,
            "Gender": gender,
            "Result": result
        }

        df = pd.concat([df, pd.DataFrame([user_data])], ignore_index=True)
        set_with_dataframe(worksheet, df)

        st.info("Seu tema foi salvo com sucesso. Obrigado!")
