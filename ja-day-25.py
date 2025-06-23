import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.set_page_config(page_title="Descubra o seu tema!")

st.title("🔮 Descubra o seu tema!")

# Define the options
male_options = ["Futebol ⚽\n\nEm clima de Copa do Mundo de Clubes, você pode vir com a camisa de um time de futebol e, se quiser ir além, pode vir com chuteira e tudo.",
                "Números 🔢\n\nTodo mundo sabe que eu gosto um pouquinho de números. Então vamos trazer isso como um tema também. Sua roupa tem que ter algum número. Qualquer um, em qualquer lugar. Na frente, nas costas, o importante é ter um número pra gente admirar.",
                "Joãozinho 🤓\n\nJá que é JA Day, que seja pra valer! Você deve vir vestido de Joãozinho (no caso eu). Qualquer coisa que eu usaria vale, monte seu visual mais engraçado de Joãozinho para esse dia.",
                "Ops! Lugar errado! 😅\n\nVista-se para ir para qualquer outro lugar que não o meu aniversário. Pode se vestir como se estivesse indo para o escritório, para a academia, para a praia ou qualquer outro lugar. Não uso o tal do TikTok, mas ouvi falar que lá dá pra encontrar várias ideias.",
                "Monocromático 🕴\n\nTem que combinar tudo. A roupa de cima, a roupa de baixo, o calçado, tudo no mesmo tom. Pode ir de branco como se fosse jogar Wimbledon, pode meter um all black ou pode lançar uma cor inesperada. O importante é manter o visual todo na mesma cor!",
                "Personagem 🎭\n\nPouco importa como. Pode ser cosplay, cospobre, máscara, algum trocadilho com a roupa. O importante é que você tem que representar algum personagem, seja histórico ou ficcional."]
female_options = ["Números 🔢\n\nTodo mundo sabe que eu gosto um pouquinho de números. Então vamos trazer isso como um tema também. Sua roupa tem que ter algum número. Qualquer um, em qualquer lugar. Na frente, nas costas, o importante é ter um número pra gente admirar.",
                "Joãozinho 🤓\n\nJá que é JA Day, que seja pra valer! Você deve vir vestida de Joãozinho (no caso eu). Qualquer coisa que eu usaria vale, monte seu visual mais engraçado de Joãozinho para esse dia.",
                "Ops! Lugar errado! 😅\n\nVista-se para ir para qualquer outro lugar que não o meu aniversário. Pode se vestir como se estivesse indo para o escritório, para a academia, para a praia ou qualquer outro lugar. Não uso o tal do TikTok, mas ouvi falar que lá dá pra encontrar várias ideias.",
                "Monocromático 🕴\n\nTem que combinar tudo. A roupa de cima, a roupa de baixo, o calçado, tudo no mesmo tom. Pode ir de branco como se fosse jogar Wimbledon, pode meter um all black ou pode lançar uma cor inesperada. O importante é manter o visual todo na mesma cor!",
                "Personagem 🎭\n\nPouco importa como. Pode ser cosplay, cospobre, máscara, algum trocadilho com a roupa. O importante é que você tem que representar algum personagem, seja histórico ou ficcional."]
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
    gender = st.selectbox("Qual é o seu gênero?", ["Masculino", "Feminino", "Outro"])

    submitted = st.form_submit_button("Enviar")

if submitted:
    # Verificar se nome já foi usado (normalizando espaços e maiúsculas/minúsculas)
    name_check = name.lower()

    if name_check in df["Name"].str.strip().str.lower().values:
        st.error("🚫 Este nome já foi utilizado. Você já preencheu antes!")
    else:
        # Escolher resultado baseado no gênero
        if gender == "Masculino":
            result = random.choice(male_options)
        elif gender == "Feminino":
            result = random.choice(female_options)
        else:
            result = random.choice(other_options)

        st.success(f"🎉 {name}, o seu tema será... **{result}!**")

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
