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

st.markdown(
    "<h1 style='text-align: center;'>"
    "Telco Customer Churn: Análisis Exploratorio de Datos"
    "</h1>",
    unsafe_allow_html=True
)

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

# Módulo 1: Información en sección Home

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

# Módulo 2: Carga del dataset

elif opcion == "📂 Carga del dataset":

    st.header("Carga del dataset")

    st.write(
        "Selecciona el archivo TelcoCustomerChurn.csv"
        "para comenzar el análisis."
    )

# Uso de st.file_uploader() para cargar el archivo .csv
    
    archivo = st.file_uploader(
        "Cargar archivo CSV",
        type=["csv"]
    )

    # Validación del archivo cargado correctamente
    
    if archivo is not None:

        df = pd.read_csv(archivo)
    
        st.session_state["df"] = df
    
        st.success("✅ Dataset cargado correctamente.")

# Mostrar una vista previa del dataset (head)
    
        st.subheader("Vista previa del dataset")
    
        st.dataframe(df.head())

# Mostrar dimensiones del dataset (filas y columnas)
        
        st.subheader("Dimensiones del dataset")
    
        col1, col2 = st.columns(2)
    
        with col1:
            st.metric("Número de filas", df.shape[0])
    
        with col2:
            st.metric("Número de columnas", df.shape[1])

# Análisis Exploratorio de Datos (EDA)
        
elif opcion == "📊 Análisis Exploratorio":

    st.header("Análisis Exploratorio de Datos")

    if "df" not in st.session_state:

        st.warning(
            "⚠️ Primero debes cargar el dataset. "
            )

    else:

        df = st.session_state["df"]

        st.success("✅ Dataset disponible para el análisis.")
