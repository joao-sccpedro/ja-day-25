import streamlit as st
import pandas as pd
import gspread
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
    expected_cols = ["Timestamp", "SalaryBruto", "SalaryLiquido", "Contract", "WorkMode", "Seniority", "Observations"]
    if df.empty or not set(expected_cols).issubset(df.columns):
        df = pd.DataFrame(columns=expected_cols)

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    df = pd.DataFrame(columns=["Timestamp", "SalaryBruto", "SalaryLiquido", "Contract", "WorkMode", "Seniority", "Observations"])
    
# ✅ Formulário
with st.form("user_form"):
    salary_bruto = st.text_input("Qual é o seu salário médio bruto (R$)?").strip()
    salary_liquido = st.text_input("Qual é o seu salário médio líquido, incluindo benefícios (R$)?").strip()
    contract = st.selectbox("Qual é o seu regime de trabalho?", ["CLT", "PJ"])
    work_mode = st.selectbox("Qual é o seu modelo de trabalho?", ["Remoto", "Híbrido", "Presencial"])
    seniority = st.selectbox("Qual é o seu nível de carreira?", ["Júnior", "Pleno", "Sênior"])
    observations = st.text_area("Alguma observação adicional? (opcional)").strip()

    submitted = st.form_submit_button("Enviar")

if submitted:
    st.success(
        f"📌 Você informou:\n\n"
        f"- Salário bruto: R$ {salary_bruto}\n"
        f"- Salário líquido: R$ {salary_liquido}\n"
        f"- Regime: {contract}\n"
        f"- Modelo de trabalho: {work_mode}\n"
        f"- Senioridade: {seniority}"
    )

    # 📝 Salvar os dados
    user_data = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "SalaryBruto": salary_bruto,
        "SalaryLiquido": salary_liquido,
        "Contract": contract,
        "WorkMode": work_mode,
        "Seniority": seniority,
        "Observations": observations
    }

    df = pd.concat([df, pd.DataFrame([user_data])], ignore_index=True)
    set_with_dataframe(worksheet, df)

    st.info("✅ Essa informação foi salva com sucesso. Valeu demais, Marciers!")
