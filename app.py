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

st.title("Telco Customer Churn — Análisis Exploratorio de Datos")
col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.image("Telco_logo.png", width=600)

# Menú lateral

col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.sidebar.image("Teleco.png", width=600)
    
modulo = st.sidebar.selectbox(
    "Menú",
    ("Home", "Ejercicio 1", "Ejercicio 2", "Ejercicio 3", "Ejercicio 4")
)

# Información en sección Home
