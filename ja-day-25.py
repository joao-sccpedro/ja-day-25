import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.set_page_config(page_title="Descubra o seu tema")

st.title("🔮 Your Future Awaits!")

# Define the options
male_options = ["Astronaut", "Chef", "Engineer", "Firefighter", "Pilot"]
female_options = ["Astronaut", "Chef", "Engineer", "Firefighter", "Pilot", "Ballerina", "Fashion Designer"]
other_options = female_options  # You can decide how to handle other genders

# Create the form
with st.form("user_form"):
    name = st.text_input("Qual é o seu nome completo?")
    age = st.text_input("Qual é a sua idade?")
    gender = st.selectbox("Qual é o seu gênero?", ["Male", "Female", "Other/Prefer not to say"])

    submitted = st.form_submit_button("Submit")

if submitted:
    # Determine options based on gender
    if gender == "Male":
        result = random.choice(male_options)
    elif gender == "Female":
        result = random.choice(female_options)
    else:
        result = random.choice(other_options)

    st.success(f"🎉 {name}, you are going to be... **{result}!**")

    # Save the data
    user_data = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Name": name,
        "Age": age,
        "Gender": gender,
        "Result": result
    }

    try:
        df = pd.read_csv("user_data.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Timestamp", "Name", "Age", "Gender", "Result"])
    
    # Verificar se o nome já existe
    if name in df["Name"].values:
        st.error("🚫 Este nome já foi utilizado. Você já preencheu antes!")
    else:
        # Continua normalmente
       st.success(f"🎉 {name}, você vai ser... **{result}!**")
    
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
        
    df.to_csv("user_data.csv", index=False)

    st.info("Your path has been saved. Thank you!")
