import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


st.set_page_config(
    page_title="Telco Customer Churn - EDA",
    page_icon="📊",
    layout="wide"
)

st.title("<h1 style='text-align: center;'>"
    "Telco Customer Churn: Análisis Exploratorio de Datos"
    "</h1>",
    unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.image("Telco_logo.png", width=600)

# Menú lateral

col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.sidebar.image("Teleco.png", width=600)

st.sidebar.title("Menú principal")

opcion = st.sidebar.radio(
    "Selecciona una sección:",
    [
        "🏠 Home",
        "📂 Carga del dataset",
        "📊 Análisis Exploratorio",
        "📝 Conclusiones"
    ]
)

# Información en sección Home

if opcion == "🏠 Home":

       
    st.subheader("""
    
    Breve descripción del objetivo del análisis

    Esta aplicación tiene como objetivo realizar un Análisis
    Exploratorio de Datos (EDA) del dataset Telco Customer Churn,
    con el propósito de identificar patrones asociados a la fuga
    de clientes.
    """)

    st.subheader("Datos generales de autora")

    st.write("""
    **Nombre completo:** Ivette Isaura Roca Matias
    
    **Especialización:** Especialización en Python for Analytics
    
    **Información general de la estudiante:** Ingeniera pesquera cursando una maestría en Ciencia y Tecnología de Alimentos
    
    **Año:** 2026
    """)

    st.subheader("Sobre el dataset")

    st.write("""
    El dataset contiene información sobre clientes de una empresa
    de telecomunicaciones, incluyendo características demográficas,
    servicios contratados, permanencia, facturación y estado de churn."
    """)
    
    st.markdown("""
    ### Tecnologías utilizadas

    - 🐍 Python
    - 👑 Streamlit
    - 📊 NumPy
    - 🐼 Pandas
    """)
