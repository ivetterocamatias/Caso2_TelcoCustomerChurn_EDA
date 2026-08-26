import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import io


st.set_page_config(
    page_title="Telco Customer Churn - EDA",
    page_icon="📊",
    layout="wide"
)

# Diccionarios de traducción

columnas_es = {
    "gender": "Género",
    "SeniorCitizen": "Cliente mayor de 65 años",
    "Partner": "Pareja",
    "Dependents": "Personas a cargo",
    "tenure": "Antigüedad (meses)",
    "PhoneService": "Servicio telefónico",
    "MultipleLines": "Múltiples líneas",
    "InternetService": "Servicio de Internet",
    "OnlineSecurity": "Seguridad en línea",
    "OnlineBackup": "Respaldo en línea",
    "DeviceProtection": "Protección del dispositivo",
    "TechSupport": "Soporte técnico",
    "StreamingTV": "Streaming de TV",
    "StreamingMovies": "Streaming de películas",
    "Contract": "Tipo de contrato",
    "PaperlessBilling": "Facturación electrónica",
    "PaymentMethod": "Método de pago",
    "MonthlyCharges": "Cargo mensual",
    "TotalCharges": "Cargo total",
    "Churn": "Abandono"
}


valores_es = {
    "Yes": "Abandonó",
    "No": "Permaneció",
    "Male": "Hombre",
    "Female": "Mujer",
    "Month-to-month": "Mensual",
    "One year": "Un año",
    "Two year": "Dos años",
    "Electronic check": "Cheque electrónico",
    "Mailed check": "Cheque por correo",
    "Bank transfer (automatic)": "Transferencia bancaria (automática)",
    "Credit card (automatic)": "Tarjeta de crédito (automática)",
    "DSL": "DSL",
    "Fiber optic": "Fibra óptica",
    "No internet service": "Sin servicio de Internet",
    0: "No",
    1: "Sí"
}

# Funciones de traducción

def traducir_variable(variable):
    return columnas_es.get(variable, variable)


def traducir_valores(serie):
    return serie.map(valores_es).fillna(serie)


# Clasificación de variables

def classify_variables(df):

    # Identificador costumerID

    # No usamos customerID para análisis estadístico porque
    # no representa una característica del cliente.
    
    id_vars = [
        "customerID"
    ]

    
    # Variables numéricas que utilizaremos en el análisis
    numeric_vars = [
        "tenure",
        "MonthlyCharges",
        "TotalCharges"
    ]

    # El resto de las variables se consideran categóricas
    categorical_vars = [
        col for col in df.columns
        if col not in numeric_vars
        and col not in id_vars
    ]

    return numeric_vars, categorical_vars


# CLASE DataAnalyzer

class DataAnalyzer:

    def __init__(self, df):

        # Guardamos el DataFrame dentro del objeto
        self.df = df

    def descriptive_statistics(self):

        return self.df.describe()

    def missing_values(self):

        return self.df.isnull().sum()

    def variable_types(self):

        return self.df.dtypes

    def duplicated_rows(self):

        return self.df.duplicated().sum()

# Ajustes de formato de título

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
      
    **Año:** 2026
    """)

    st.subheader("Sobre el dataset")

    st.write("""
    El dataset contiene información sobre clientes de una empresa
    de telecomunicaciones, incluyendo características demográficas,
    servicios contratados, permanencia y facturación.
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
        "Selecciona el archivo TelcoCustomerChurn.csv "
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

    # Conversión de TotalCharges a variable numérica

        df["TotalCharges"] = pd.to_numeric(
            df["TotalCharges"],
            errors="coerce"
        )

    # Guardamos el DataFrame en la memoria de Streamlit
    # para poder utilizarlo en los demás módulos.
    
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

        # Recuperamos el DataFrame almacenado
        df = st.session_state["df"]

        # Creamos un objeto de la clase DataAnalyzer
        analyzer = DataAnalyzer(df)

        # Clasificamos las variables mediante nuestra función
        numeric_vars, categorical_vars = classify_variables(df)

        # Creamos los 10 tabs del EDA
   
        tabs = st.tabs([
            "1. Información general",
            "2. Clasificación",
            "3. Estadísticas",
            "4. Valores faltantes",
            "5. Distribución numérica",
            "6. Variables categóricas",
            "7. Numérica vs abandono",
            "8. Categórica vs abandono",
            "9. Análisis dinámico",
            "10. Hallazgos"
        ])

      
        # ÍTEM 1 — Información general del dataset
 

        with tabs[0]:

            st.header("1. Información general del dataset")


            # Dimensiones

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Número de filas",
                    df.shape[0]
                )

            with col2:
                st.metric(
                    "Número de columnas",
                    df.shape[1]
                )

            with col3:
                st.metric(
                    "Filas duplicadas",
                    analyzer.duplicated_rows()
                )


            # Información general utilizando .info()


            st.subheader("Información general")

            buffer = io.StringIO()

            df.info(buf=buffer)

            info_text = buffer.getvalue()

            st.text(info_text)


            # Tipos de datos


            st.subheader("Tipos de datos")

            types_df = pd.DataFrame({
                "Variable": [
                    traducir_variable(col)
                    for col in df.columns
                ],
                "Tipo de dato": df.dtypes.astype(str).values
            })

            st.dataframe(
                types_df,
                use_container_width=True
            )


            # Conteo de valores nulos

            st.subheader("Conteo de valores nulos")

            null_df = pd.DataFrame({
                "Variable": [
                    traducir_variable(col)
                    for col in df.columns
                ],
                "Valores nulos": df.isnull().sum().values
            })

            st.dataframe(
                null_df,
                use_container_width=True
            )


        # ÍTEM 2 — Clasificación de variables
        
        with tabs[1]:

            st.header("2. Clasificación de variables")

            col1, col2 = st.columns(2)

            
            # Uso de función personalizada
            
            numeric_vars, categorical_vars = classify_variables(df)

            
            # Identificación de variables: Variables numéricas
            

            with col1:

                st.subheader("Variables numéricas")

                st.write(
                    f"Cantidad: {len(numeric_vars)}"
                )

                for variable in numeric_vars:
                    st.write(
                        f"• {traducir_variable(variable)}"
                    )
                
            # Identificación de variales: Variables categóricas
            

            with col2:

                st.subheader("Variables categóricas")

                st.write(
                    f"Cantidad: {len(categorical_vars)}"
                )

                for variable in categorical_vars:
                    st.write(
                        f"• {traducir_variable(variable)}"
                    )
        
        # ÍTEM 3 — Estadísticas descriptivas
        
        with tabs[2]:
        
            st.header("3. Estadísticas descriptivas")
        
            # Utilizamos .describe() sobre las variables numéricas
            descriptive_stats = df[numeric_vars].describe()
        
            # Traducimos los nombres de las variables al español
            descriptive_stats.columns = [
                traducir_variable(col)
                for col in descriptive_stats.columns
            ]
        
            # Traducimos también las medidas estadísticas
            descriptive_stats.index = [
                {
                    "count": "Cantidad",
                    "mean": "Media",
                    "std": "Desviación estándar",
                    "min": "Mínimo",
                    "25%": "Percentil 25%",
                    "50%": "Mediana",
                    "75%": "Percentil 75%",
                    "max": "Máximo"
                }.get(index, index)
                for index in descriptive_stats.index
            ]
        
            # Mostramos las estadísticas descriptivas
            st.dataframe(
                descriptive_stats,
                use_container_width=True
            )
        
            st.subheader("Medidas principales")
        
            # Selección de variable numérica
            selected_stat_var = st.selectbox(
                "Selecciona una variable numérica:",
                numeric_vars,
                format_func=traducir_variable,
                key="statistics_variable"
            )
        
            # Eliminamos valores faltantes
            stat_data = df[selected_stat_var].dropna()
        
            # Calculamos media utilizando NumPy
            mean_value = np.mean(stat_data)
        
            # Calculamos mediana utilizando NumPy
            median_value = np.median(stat_data)
        
            # Calculamos moda utilizando Pandas
            mode_value = df[selected_stat_var].mode()
        
            if not mode_value.empty:
                mode_value = mode_value.iloc[0]
            else:
                mode_value = "No disponible"
        
            # Mostramos los resultados
            col1, col2, col3 = st.columns(3)
        
            with col1:
                st.metric(
                    "Media",
                    f"{mean_value:.2f}"
                )
        
            with col2:
                st.metric(
                    "Mediana",
                    f"{median_value:.2f}"
                )
        
            with col3:
        
                if isinstance(mode_value, (int, float, np.integer, np.floating)):
                    mode_display = f"{mode_value:.2f}"
                else:
                    mode_display = str(mode_value)
        
                st.metric(
                    "Moda",
                    mode_display
                )
                
        # ÍTEM 4 — Análisis de valores faltantes

        with tabs[3]:

            st.header("4. Análisis de valores faltantes")

            # Conteo de valores faltantes

            missing_count = analyzer.missing_values()

            # Cálculo del porcentaje de valores faltantes

            missing_percentage = (
                missing_count / len(df) * 100
            )

            # Creación de tabla resumen

            missing_df = pd.DataFrame({
                "Variable": df.columns,
                "Valores faltantes": missing_count.values,
                "Porcentaje (%)": missing_percentage.values
            })

            # Selección de variables con valores faltantes
            # ----------------------------------------------------
            # Las variables con cero valores faltantes no se incluyen
            # en esta tabla
            
            missing_only = missing_df[
                missing_df["Valores faltantes"] > 0
            ]

    
            # Si no existen valores faltantes en ninguna variable,
            # mostramos un mensaje informativo.
            
            if missing_only.empty:

                st.success(
                    "✅ No se encontraron valores faltantes."
                )

            else:

                st.subheader("Conteo y porcentaje de valores faltantes")

                st.dataframe(
                    missing_only,
                    use_container_width=True
                )

                # Gráfico de valores faltantes

                fig, ax = plt.subplots()

                sns.barplot(
                    data=missing_only,
                    x="Valores faltantes",
                    y="Variable",
                    ax=ax
                )

                ax.set_title(
                    "Valores faltantes por variable"
                )

                ax.set_xlabel(
                    "Cantidad de valores faltantes"
                )
        
                ax.set_ylabel(
                    "Variable"
                )
                
                st.pyplot(fig)

                # Discusión breve

                st.subheader("Discusión")
        
                st.write(
                    "Los valores faltantes deben ser identificados y "
                    "evaluados antes de realizar análisis estadísticos "
                    "o visualizaciones, ya que pueden afectar la "
                    "interpretación de los resultados. La magnitud y "
                    "distribución de los datos faltantes determinará "
                    "si es necesario aplicar algún tratamiento." 
                )

        
        # ÍTEM 5 — Distribución de variables numéricas
        
        with tabs[4]:

            st.header(
                "5. Distribución de variables numéricas"
            )

            # Selección de variable con selectbox

            selected_numeric = st.selectbox(
                "Selecciona una variable numérica:",
                numeric_vars,
                format_func=traducir_variable,
                key="distribution_variable"
            )

            # Configuración del histograma

            bins = st.slider(
                "Número de intervalos del histograma:",
                min_value=5,
                max_value=50,
                value=20
            )

            # Crear gráfico
            fig, ax = plt.subplots()

            sns.histplot(
                data=df,
                x=selected_numeric,
                bins=bins,
                kde=True,
                ax=ax
            )

            # Configuración del gráfico
            
            nombre_numeric = traducir_variable(selected_numeric)
            
            ax.set_title(
                f"Distribución de {nombre_numeric}"
            )

            ax.set_xlabel(
                nombre_numeric
            )

            ax.set_ylabel(
                "Frecuencia"
            )


            st.pyplot(fig)

            # Interpretación visual -  breve descripción

            st.subheader("Interpretación")

            st.write(
                f"""
                El histograma muestra la distribución de
                los valores de ***{nombre_numeric}*** para
                identificar dónde se concentra la mayor parte
                de los valores, el grado de dispersión, posibles
                asimetrías y la presencia de valores extremos.
                """
            )

        
        # ÍTEM 6 — Análisis de variables categóricas
       
        with tabs[5]:

            st.header(
                "6. Análisis de variables categóricas"
            )

            selected_categorical = st.selectbox(
                "Selecciona una variable categórica:",
                categorical_vars,
                format_func=traducir_variable,
                key="categorical_variable"
            )

            # Conteos
            counts = (
                df[selected_categorical]
                .value_counts()
            )

            # Proporciones - Porcentajes
            percentages = (
                df[selected_categorical]
                .value_counts(normalize=True)
                * 100
            )

            categorical_summary = pd.DataFrame({
                "Conteo": counts,
                "Porcentaje (%)": percentages.round(2)
            })

            categorical_summary.index = [
                valores_es.get(valor, valor)
                for valor in categorical_summary.index
            ]

            st.subheader("Conteos y proporciones")

            st.dataframe(
                categorical_summary,
                use_container_width=True
            )

            # Creamos una copia solamente para el gráfico
            
            grafico_df = df.copy()
            
            # Traducimos los valores de la variable seleccionada

            grafico_df[selected_categorical] = traducir_valores(
                grafico_df[selected_categorical]
            )
            
            nombre_categorical = traducir_variable(
                selected_categorical
            )

            fig, ax = plt.subplots()

            sns.countplot(
                data=grafico_df,
                x=selected_categorical,
                ax=ax
            )

            ax.set_title(
                f"Distribución de {nombre_categorical}"
            )

            ax.set_xlabel(
                nombre_categorical
            )
            
            ax.set_ylabel(
                "Cantidad de clientes"
            )

            ax.tick_params(
                axis="x",
                rotation=45
            )

            st.pyplot(fig)


        # ÍTEM 7 — Análisis bivariado (numérico vs categórico)

        with tabs[6]:

            st.header(
                "7. Análisis bivariado: variable numérica vs abandono"
            )

            selected_numeric_churn = st.selectbox(
                "Selecciona una variable numérica:",
                numeric_vars,
                format_func=traducir_variable,
                key="numeric_churn_variable"
            )

            # Boxplot

            grafico_df = df.copy()

            grafico_df["Churn"] = traducir_valores(
                grafico_df["Churn"]
            )
            
            nombre_numeric_churn = traducir_variable(
                selected_numeric_churn
            )
            
            fig, ax = plt.subplots()

            sns.boxplot(
                data=df,
                x="Churn",
                y=selected_numeric_churn,
                ax=ax
            )

            ax.set_title(
                f"{nombre_numeric_churn} vs Abandono"
            )

            ax.set_xlabel(
                "Situación del cliente"
            )
            
            ax.set_ylabel(
                nombre_numeric_churn
            )

            st.pyplot(fig)

            # Tabla comparativa

            comparison = (
                df.groupby("Churn")[selected_numeric_churn]
                .agg(["mean", "median", "std"])
                .round(2)
            )

            comparison.index = [
                valores_es.get(valor, valor)
                for valor in comparison.index
            ]
            
            comparison.columns = [
                "Media",
                "Mediana",
                "Desviación estándar"
            ]

            st.subheader(
                "Comparación estadística entre grupos"
            )

            st.dataframe(
                comparison,
                use_container_width=True
            )


        # ÍTEM 8 — Análisis bivariado (categórico vs categórico)
        
        with tabs[7]:

            st.header(
                "8. Análisis bivariado: variable categórica vs abandono"
            )

            selected_categorical_churn = st.selectbox(
                "Selecciona una variable categórica:",
                categorical_vars,
                format_func=traducir_variable,
                key="categorical_churn_variable"
            )


            # Copia para visualización
            grafico_df = df.copy()
            
            # Traducción de valores
            grafico_df[selected_categorical_churn] = traducir_valores(
                grafico_df[selected_categorical_churn]
            )
            
            grafico_df["Churn"] = traducir_valores(
                grafico_df["Churn"]
            )
            
            nombre_categorical_churn = traducir_variable(
                selected_categorical_churn
            )
            
            fig, ax = plt.subplots()
            
            sns.countplot(
                data=grafico_df,
                x=selected_categorical_churn,
                hue="Churn",
                ax=ax
            )
            
            ax.set_title(
                f"{nombre_categorical_churn} vs. abandono"
            )
            
            ax.set_xlabel(
                nombre_categorical_churn
            )
            
            ax.set_ylabel(
                "Cantidad de clientes"
            )
            
            ax.legend(
                title="Situación del cliente"
            )
            
            ax.tick_params(
                axis="x",
                rotation=45
            )
            
            st.pyplot(fig)

            # Proporción de Churn dentro de cada categoría

            churn_rate = pd.crosstab(
                df[selected_categorical_churn],
                df["Churn"],
                normalize="index"
            ) * 100

            churn_rate = churn_rate.round(2)
            
            churn_rate.index = [
                valores_es.get(valor, valor)
                for valor in churn_rate.index
            ]
            
            churn_rate.columns = [
                valores_es.get(valor, valor)
                for valor in churn_rate.columns
            ]

            st.subheader(
                "Proporción de abandono por categoría (%)"
            )

            st.dataframe(
                churn_rate,
                use_container_width=True
            )


        # ÍTEM 9 — Análisis basado en parámetros seleccionados

        with tabs[8]:

            st.header(
                "9. Análisis basado en parámetros seleccionados"
            )

            st.write(
                "Utiliza los controles para explorar "
                "dinámicamente el dataset."
            )


            # Uso de selectox

            dynamic_variable = st.selectbox(
                "Selecciona una variable categórica:",
                categorical_vars,
                format_func=traducir_variable,
                key="dynamic_categorical"
            )


            # Uso de multiselect

            available_categories = sorted(
                df[dynamic_variable]
                .dropna()
                .unique()
                .tolist()
            )

            selected_categories = st.multiselect(
                "Selecciona una o más categorías:",
                available_categories,
                default=available_categories,
                format_func=lambda x: valores_es.get(x, x)
            )

            # SLIDER

            min_tenure = int(
                df["tenure"].min()
            )

            max_tenure = int(
                df["tenure"].max()
            )

            tenure_range = st.slider(
                "Rango de permanencia (tenure):",
                min_value=min_tenure,
                max_value=max_tenure,
                value=(min_tenure, max_tenure)
            )


            # CHECKBOX

            show_filtered_data = st.checkbox(
                "Mostrar datos filtrados"
            )

            # FILTRADO

            filtered_df = df[
                df[dynamic_variable]
                .isin(selected_categories)
                &
                df["tenure"].between(
                    tenure_range[0],
                    tenure_range[1]
                )
            ]

            # RESULTADOS

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Clientes seleccionados",
                    len(filtered_df)
                )

            with col2:

                churn_rate_dynamic = (
                    filtered_df["Churn"]
                    .eq("Yes")
                    .mean() * 100
                )

                st.metric(
                    "Churn (%)",
                    f"{churn_rate_dynamic:.2f}%"
                )

            # Mostrar tabla únicamente si se marca checkbox

            if show_filtered_data:

                st.subheader(
                    "Datos filtrados"
                )

                st.dataframe(
                    filtered_df,
                    use_container_width=True
                )


            # GRÁFICO DINÁMICO

            if not filtered_df.empty:

                # Crear copia de los datos filtrados
                grafico_df = filtered_df.copy()

                # Traducir los valores de la variable seleccionada
                grafico_df[dynamic_variable] = grafico_df[
                    dynamic_variable
                ].map(valores_es).fillna(
                    grafico_df[dynamic_variable]
                )

                # Traducir los valores de Churn
                grafico_df["Churn"] = grafico_df[
                    "Churn"
                ].map(valores_es).fillna(
                    grafico_df["Churn"]
                )

                # Obtener nombre de la variable en español
                nombre_variable = columnas_es.get(
                    dynamic_variable,
                    dynamic_variable
                )

                # Crear gráfico
                fig, ax = plt.subplots()

                sns.countplot(
                    data=grafico_df,
                    x=dynamic_variable,
                    hue="Churn",
                    ax=ax
                )

                # Título
                ax.set_title(
                    f"{nombre_variable} vs. situación del cliente"
                )

                # Etiquetas de los ejes
                ax.set_xlabel(
                    nombre_variable
                )

                ax.set_ylabel(
                    "Cantidad de clientes"
                )

                # Leyenda
                ax.legend(
                    title="Situación del cliente"
                )

                # Rotación de etiquetas
                ax.tick_params(
                    axis="x",
                    rotation=45
                )

                # Mostrar gráfico
                st.pyplot(fig)

        # ÍTEM 10 — Hallazgos clave

        with tabs[9]:

            st.header("10. Hallazgos clave")

            st.write(
                """
                Esta sección resume los principales patrones identificados durante
                el análisis exploratorio de datos (EDA), destacando el comportamiento
                del abandono de clientes y las variables que presentan diferencias
                relevantes entre quienes permanecen y quienes abandonan el servicio.
                """
            )

            # Resumen visual

            st.subheader("Resumen del dataset")
            
            # Cantidad total de clientes
            total_clientes = len(df)
        
            # Cantidad de clientes que abandonaron
            clientes_abandonaron = (
                df["Churn"]
                .eq("Yes")
                .sum()
            )
        
            # Cantidad de clientes que permanecieron
            clientes_permanecieron = (
                df["Churn"]
                .eq("No")
                .sum()
            )
        
            # Tasa de abandono
            tasa_abandono = (
                clientes_abandonaron / total_clientes * 100
            )
        
            # Antigüedad promedio
            tenure_promedio = df["tenure"].mean()
        
            # Cargo mensual promedio
            monthly_charges_promedio = df["MonthlyCharges"].mean()
                    
            # Mostrar KPIs
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Total de clientes",
                    f"{total_clientes:,}"
                )
            
            with col2:
                st.metric(
                    "Tasa de abandono",
                    f"{tasa_abandono:.1f} %"
                )
            
            with col3:
                st.metric(
                    "Antigüedad promedio",
                    f"{tenure_promedio:.1f} meses"
                )
            
            with col4:
                st.metric(
                    "Cargo mensual promedio",
                    f"${monthly_charges_promedio:.2f}"
                )
            
            
         
            # Distribución de clientes según abandono
                       
            st.subheader("Distribución de clientes según situación")
            
            churn_counts = (
                df["Churn"]
                .map({
                    "Yes": "Abandonó",
                    "No": "Permaneció"
                })
                .value_counts()
            )
        
            fig, ax = plt.subplots(figsize=(8, 4))
        
            sns.barplot(
                x=churn_counts.index,
                y=churn_counts.values,
                ax=ax
            )
        
            ax.set_xlabel(
                "Situación del cliente"
            )
        
            ax.set_ylabel(
                "Cantidad de clientes"
            )
        
            ax.set_title(
                "Distribución de clientes según situación"
            )
        
            st.pyplot(fig)
            
            
            # Principales insights
            
            st.subheader("Principales insights")
            

            # Insight 1: Abandono general
            
            st.markdown(
                f"""
                🔎 **Insight 1 — Abandono general**
            
                De un total de **{total_clientes:,} clientes**, 
                **{clientes_abandonaron:,}** abandonaron el servicio, lo que
                representa una tasa de abandono de aproximadamente
                **{tasa_abandono:.1f}%**.
        
                En contraste, **{clientes_permanecieron:,} clientes**
                permanecieron en el servicio.
                """
            )
            
            
            # Insight 2: Antigüedad
            
            if "tenure" in df.columns:
            
                tenure_churn = (
                    df.groupby("Churn")["tenure"]
                    .mean()
                )
        
                if (
                    "Yes" in tenure_churn.index
                    and "No" in tenure_churn.index
                ):
        
                    tenure_abandono = tenure_churn["Yes"]
                    tenure_permanencia = tenure_churn["No"]
        
                    diferencia_tenure = (
                        tenure_permanencia - tenure_abandono
                    )
        
                    if diferencia_tenure > 0:
        
                        st.markdown(
                            f"""
                            🔎 **Insight 2 — Antigüedad**
        
                            Los clientes que abandonaron el servicio presentan una
                            antigüedad promedio de **{tenure_abandono:.1f} meses**,
                            mientras que los clientes que permanecieron presentan
                            una antigüedad promedio de **{tenure_permanencia:.1f} meses**.
        
                            La diferencia es de aproximadamente
                            **{diferencia_tenure:.1f} meses**, lo que sugiere que
                            el abandono se concentra en mayor medida entre clientes
                            con menor antigüedad.
                            """
                        )
        
                    else:
        
                        st.markdown(
                            f"""
                            🔎 **Insight 2 — Antigüedad**
        
                            Los clientes que abandonaron el servicio presentan una
                            antigüedad promedio de **{tenure_abandono:.1f} meses**,
                            frente a **{tenure_permanencia:.1f} meses** entre quienes
                            permanecieron.
        
                            En este caso, la diferencia no indica una menor antigüedad
                            entre los clientes que abandonaron.
                            """
                        )
                    
            
            # Insight 3: Cargo mensual
            
            if "MonthlyCharges" in df.columns:
            
                charges_churn = (
                    df.groupby("Churn")["MonthlyCharges"]
                    .mean()
                )
        
                if (
                    "Yes" in charges_churn.index
                    and "No" in charges_churn.index
                ):
        
                    cargo_abandono = charges_churn["Yes"]
                    cargo_permanencia = charges_churn["No"]
        
                    diferencia_cargo = (
                        cargo_abandono - cargo_permanencia
                    )
        
                    if diferencia_cargo > 0:
        
                        st.markdown(
                            f"""
                            🔎 **Insight 3 — Cargo mensual**
        
                            El cargo mensual promedio de los clientes que abandonaron
                            el servicio es de **${cargo_abandono:.2f}**, frente a
                            **${cargo_permanencia:.2f}** entre quienes permanecieron.
        
                            Esto representa una diferencia de aproximadamente
                            **${diferencia_cargo:.2f}**, por lo que los clientes que
                            abandonaron presentan, en promedio, un cargo mensual mayor.
                            """
                        )
        
                    else:
        
                        diferencia_cargo_abs = abs(diferencia_cargo)
        
                        st.markdown(
                            f"""
                            🔎 **Insight 3 — Cargo mensual**
        
                            El cargo mensual promedio de los clientes que abandonaron
                            el servicio es de **${cargo_abandono:.2f}**, frente a
                            **${cargo_permanencia:.2f}** entre quienes permanecieron.
        
                            En este conjunto de datos, los clientes que permanecieron
                            presentan un cargo mensual promedio aproximadamente
                            **${diferencia_cargo_abs:.2f} mayor**.
                            """
                            """
                        )

                        
            # Insight 4: Tipo de contrato
            
            if "Contract" in df.columns:
            
                contract_churn = pd.crosstab(
                    df["Contract"],
                    df["Churn"],
                    normalize="index"
                ) * 100
        
                if "Yes" in contract_churn.columns:
        
                    contrato_mayor_abandono = (
                        contract_churn["Yes"]
                        .idxmax()
                    )
        
                    tasa_contrato_mayor = (
                        contract_churn["Yes"]
                        .max()
                    )
        
                    contrato_mayor_abandono_es = valores_es.get(
                        contrato_mayor_abandono,
                        contrato_mayor_abandono
                    )
        
                    st.markdown(
                        f"""
                        🔎 **Insight 4 — Tipo de contrato**
        
                        El tipo de contrato con mayor tasa de abandono es
                        **{contrato_mayor_abandono_es}**, con aproximadamente
                        **{tasa_contrato_mayor:.1f}%** de sus clientes abandonando
                        el servicio.
        
                        Este resultado indica que el tipo de contrato presenta una
                        asociación relevante con el comportamiento de abandono.
                        """
                    )

            
            # Insight 5: Método de pago
            
            if "PaymentMethod" in df.columns:
            
                payment_churn = pd.crosstab(
                    df["PaymentMethod"],
                    df["Churn"],
                    normalize="index"
                ) * 100

                if "Yes" in payment_churn.columns:
            
                    metodo_mayor_abandono = (
                        payment_churn["Yes"]
                        .idxmax()
                    )
        
                    tasa_metodo_mayor = (
                        payment_churn["Yes"]
                        .max()
                    )
        
                    metodo_mayor_abandono_es = valores_es.get(
                        metodo_mayor_abandono,
                        metodo_mayor_abandono
                    )
        
                    st.markdown(
                        f"""
                        🔎 **Insight 5 — Método de pago**
        
                        El método de pago asociado con la mayor tasa de abandono es
                        **{metodo_mayor_abandono_es}**, con aproximadamente
                        **{tasa_metodo_mayor:.1f}%** de sus clientes abandonando
                        el servicio.
        
                        Este resultado permite identificar un grupo que podría
                        requerir un análisis más detallado de sus características
                        y comportamiento.
                        """
                    )
            
            
            # Insight 6: Servicio de Internet
            
            if "InternetService" in df.columns:
            
                internet_churn = pd.crosstab(
                    df["InternetService"],
                    df["Churn"],
                    normalize="index"
                ) * 100
        
                if "Yes" in internet_churn.columns:
        
                    servicio_mayor_abandono = (
                        internet_churn["Yes"]
                        .idxmax()
                    )
        
                    tasa_servicio_mayor = (
                        internet_churn["Yes"]
                        .max()
                    )
        
                    servicio_mayor_abandono_es = valores_es.get(
                        servicio_mayor_abandono,
                        servicio_mayor_abandono
                    )
        
                    st.markdown(
                        f"""
                        🔎 **Insight 6 — Servicio de Internet**
        
                        Entre los tipos de servicio de Internet, **{servicio_mayor_abandono_es}**
                        presenta la mayor tasa de abandono, con aproximadamente
                        **{tasa_servicio_mayor:.1f}%** de sus clientes abandonando
                        el servicio.
        
                        Este resultado señala una posible relación entre el tipo de
                        servicio de Internet contratado y el comportamiento de abandono.
                        """
                    )
            
            

# CONCLUSIONES

elif opcion == "📝 Conclusiones":

            st.subheader("Conclusiones finales")

            # ----------------------------------------------------------
            # CONCLUSIÓN 1
            # ----------------------------------------------------------

            st.markdown(
                f"""
                ### 1. El abandono de clientes representa un problema relevante

                Del total de **{total_clientes:,} clientes analizados**, 
                **{churn_count:,} abandonaron el servicio**, lo que representa
                una tasa de abandono de aproximadamente **{churn_rate:.1f}%**.

                **Implicación para la toma de decisiones:**  
                La empresa debería considerar la retención de clientes como un
                aspecto prioritario de gestión, destinando acciones de
                seguimiento y fidelización a los segmentos donde se concentra
                una mayor proporción de abandonos.
                """
            )

            # ----------------------------------------------------------
            # CONCLUSIÓN 2
            # ----------------------------------------------------------

            st.markdown(
                f"""
                ### 2. Los clientes con menor antigüedad presentan mayor abandono

                La antigüedad promedio de los clientes que abandonaron el servicio
                fue de **{tenure_yes:.1f} meses**, mientras que entre quienes
                permanecieron fue de **{tenure_no:.1f} meses**.

                **Implicación para la toma de decisiones:**  
                La empresa debería reforzar las estrategias de incorporación,
                acompañamiento y fidelización durante los primeros meses de
                relación con el cliente, ya que esta etapa representa una
                oportunidad importante para fortalecer la permanencia.
                """
            )

            # ----------------------------------------------------------
            # CONCLUSIÓN 3
            # ----------------------------------------------------------

            if diferencia_cargo > 0:

                texto_cargo = (
                    f"Los clientes que abandonaron presentaron un cargo mensual "
                    f"promedio de **${charges_yes:.2f}**, frente a **${charges_no:.2f}** "
                    f"entre quienes permanecieron. La diferencia promedio fue de "
                    f"**${diferencia_cargo:.2f}**."
                )

            else:

                texto_cargo = (
                    f"Los clientes que abandonaron presentaron un cargo mensual "
                    f"promedio de **${charges_yes:.2f}**, frente a **${charges_no:.2f}** "
                    f"entre quienes permanecieron."
                )

            st.markdown(
                f"""
                ### 3. El cargo mensual presenta diferencias entre los grupos

                {texto_cargo}

                **Implicación para la toma de decisiones:**  
                La empresa debería revisar la estructura de precios y los servicios
                asociados a los planes con cargos mensuales elevados, procurando
                que el valor percibido por el cliente sea consistente con el costo
                del servicio.
                """
            )

            # ----------------------------------------------------------
            # CONCLUSIÓN 4
            # ----------------------------------------------------------

            st.markdown(
                f"""
                ### 4. El tipo de contrato está asociado con diferencias importantes en el abandono

                El tipo de contrato con mayor tasa de abandono fue
                **{contrato_mayor_churn_es}**, con aproximadamente
                **{tasa_contrato:.1f}%** de clientes que abandonaron el servicio.

                **Implicación para la toma de decisiones:**  
                La empresa debería revisar las condiciones comerciales de este
                tipo de contrato y evaluar estrategias de fidelización que
                incentiven relaciones contractuales de mayor duración.
                """
            )

            # ----------------------------------------------------------
            # CONCLUSIÓN 5
            # ----------------------------------------------------------

            st.markdown(
                f"""
                ### 5. El método de pago y el servicio contratado permiten identificar segmentos de atención prioritaria

                El método de pago con mayor tasa de abandono fue
                **{metodo_mayor_churn_es}**, con aproximadamente
                **{tasa_metodo:.1f}%** de churn.

                Asimismo, entre los servicios de Internet analizados,
                **{servicio_mayor_churn_es}** presentó la mayor tasa de abandono,
                con aproximadamente **{tasa_servicio:.1f}%**.

                **Implicación para la toma de decisiones:**  
                Estos segmentos deberían ser analizados con mayor profundidad
                para identificar posibles problemas relacionados con la
                experiencia del cliente, el servicio contratado o el proceso
                de pago, y así orientar acciones específicas de retención.
                """
            )

            # ==========================================================
            # CIERRE
            # ==========================================================

            st.info(
                """
                **Conclusión general del EDA:**  
                Los resultados muestran que el abandono de clientes no se distribuye
                de manera uniforme. Las diferencias observadas según antigüedad,
                cargo mensual, tipo de contrato, método de pago y servicio de
                Internet permiten identificar segmentos que requieren una mayor
                atención. Estos hallazgos pueden utilizarse como base para diseñar
                estrategias de fidelización y mejora de la experiencia del cliente.
                """
            )
