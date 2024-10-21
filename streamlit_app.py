import streamlit as st
import pandas as pd
import requests
import openai
import os

# Configuración
FASTAPI_URL = "http://localhost:8000"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

def get_data_from_api():
    try:

        #response = requests.get(f"{FASTAPI_URL}/get_data")
        response = requests.get(f"{FASTAPI_URL}/get_data", timeout=30)
        st.write(f"Status code: {response.status_code}")
        st.write(f"Response content: {response.text[:1000]}")  # Mostrar los primeros 1000 caracteres
            
        if response.status_code == 200:
            data = response.json()
            return pd.DataFrame(data['data'], columns=data['columns'])
        else:
            st.error(f"Error al obtener datos: {response.text}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error en la solicitud: {str(e)}")
        return pd.DataFrame()
    

def get_ai_response(prompt, data):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Cambiado de "gpt-4o" a "gpt-4"
        messages=[
            {"role": "system", "content": "Eres un asistente de datos que ayuda a analizar tablas."},
            {"role": "user", "content": f"Basado en los siguientes datos:\n{data.head().to_string()}\n\nResponde a la pregunta: {prompt}"}
        ],
        max_tokens=150
    )
    return response['choices'][0]['message']['content'].strip()

st.title("Analizador de Datos de Emails")

# Obtener los resultados guardados
try:
    df = get_data_from_api()
    if not df.empty:
        st.success("Datos cargados exitosamente.")
    else:
        st.warning("No se obtuvieron datos.")
except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
    df = pd.DataFrame()

# Interfaz para preguntas al usuario
user_question = st.text_input("Haz una pregunta sobre los datos:")

if st.button("Obtener respuesta"):
    if not df.empty and user_question:
        with st.spinner("Generando respuesta..."):
            ai_response = get_ai_response(user_question, df)
        st.write("Respuesta:", ai_response)
    elif df.empty:
        st.warning("No hay datos disponibles.")
    else:
        st.warning("Por favor, introduce una pregunta.")

# Opción para mostrar los datos brutos (opcional)
if st.checkbox("Mostrar datos brutos"):
    st.write(df)
