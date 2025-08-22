import streamlit as st
import pandas as pd
import gspread
import random
from datetime import datetime
from gspread_dataframe import get_as_dataframe, set_with_dataframe

st.set_page_config(page_title="Pesquisa do Joãozinho")
st.title("Uma pesquisa do vosso amigo Joãozinho")

# ✅ Conectar ao Google Sheets
gc = gspread.service_account_from_dict(st.secrets["google_service_account"])
sh = gc.open("JA-Day-25")
worksheet = sh.sheet1

# ✅ Tentar ler os dados
try:
    df = get_as_dataframe(worksheet).dropna(how="all")

    # Se dataframe está vazio ou não tem as colunas, cria a estrutura
    if df.empty or not set(["Timestamp", "Salary", "Contract"]).issubset(df.columns):
        df = pd.DataFrame(columns=["Timestamp", "Salary", "Contract"])

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    df = pd.DataFrame(columns=["Timestamp", "Salary", "Contract"])
    
# ✅ Formulário
with st.form("user_form"):
    salary = st.text_input("Qual é o seu salário médio bruto (R$)?").strip()
    salary = st.text_input("Qual é o seu salário médio líquido, incluindo benefícios (R$)?").strip()
    contract = st.selectbox("Qual é o seu regime de trabalho?", ["CLT", "PJ"])

    submitted = st.form_submit_button("Enviar")

    st.success(f"📌 Você informou salário de R$ {salary} e regime {contract}.")

    # 📝 Salvar os dados
    user_data = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Salary": salary,
        "Contract": contract,
    }

    df = pd.concat([df, pd.DataFrame([user_data])], ignore_index=True)
    set_with_dataframe(worksheet, df)

    st.info("✅ Essa informação foi salva com sucesso. Valeu demais, Marciers!")
