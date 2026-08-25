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


# Clasificación de variables

def classify_variables(df):

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
            "7. Numérica vs Churn",
            "8. Categórica vs Churn",
            "9. Análisis dinámico",
            "10. Hallazgos"
        ])

      
        # ÍTEM 1 — Iformación general del dataset
 

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
                "Variable": df.columns,
                "Tipo de dato": df.dtypes.astype(str).values
            })

            st.dataframe(
                types_df,
                use_container_width=True
            )


            # Conteo de valores nulos

            st.subheader("Conteo de valores nulos")

            null_df = pd.DataFrame({
                "Variable": df.columns,
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
                    st.write(f"• {variable}")

            
            # Identificación de variales: Variables categóricas
            

            with col2:

                st.subheader("Variables categóricas")

                st.write(
                    f"Cantidad: {len(categorical_vars)}"
                )

                for variable in categorical_vars:
                    st.write(f"• {variable}")

        
        # ÍTEM 3 — Estadísticas descriptivas

        with tabs[2]:

            st.header("3. Estadísticas descriptivas")

            # Utilizamos .describe()

            descriptive_stats = df[numeric_vars].describe()

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
                key="statistics_variable"
            )

            # Calculamos media utilizando NumPy
            mean_value = np.mean(
                df[selected_stat_var].dropna()
            )

            # Calculamos mediana utilizando NumPy
            median_value = np.median(
                df[selected_stat_var].dropna()
            )

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

            ax.set_title(
                f"Distribución de {selected_numeric}"
            )

            ax.set_xlabel(
                selected_numeric
            )

            ax.set_ylabel(
                "Frecuencia"
            )


            st.pyplot(fig)

            # Interpretación visual -  breve descripción

            st.subheader("Interperetación")

            st.write(
                f"El histograma muestra la distribución de "
                "los valores de {selected_numeric} para "
                "identificar dónde se concentra la mayor parte "
                "de los valores, el grado de dispersión, posibles "
                "asimetrías y la presencia de valores extremos."
            )

        
        # ÍTEM 6 — Análisis de variables categóricas
       
        with tabs[5]:

            st.header(
                "6. Análisis de variables categóricas"
            )

            selected_categorical = st.selectbox(
                "Selecciona una variable categórica:",
                categorical_vars,
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

            st.subheader("Conteos y proporciones")

            st.dataframe(
                categorical_summary,
                use_container_width=True
            )

            # Gráfico de barras

            fig, ax = plt.subplots()

            sns.countplot(
                data=df,
                x=selected_categorical,
                ax=ax
            )

            ax.set_title(
                f"Distribución de {selected_categorical}"
            )

            ax.tick_params(
                axis="x",
                rotation=45
            )

            st.pyplot(fig)


        # ÍTEM 7 — Análisis bivariado (numérico vs categórico)

        with tabs[6]:

            st.header(
                "7. Análisis bivariado: variable numérica vs Churn"
            )

            selected_numeric_churn = st.selectbox(
                "Selecciona una variable numérica:",
                numeric_vars,
                key="numeric_churn_variable"
            )

            # Boxplot
            fig, ax = plt.subplots()

            sns.boxplot(
                data=df,
                x="Churn",
                y=selected_numeric_churn,
                ax=ax
            )

            ax.set_title(
                f"{selected_numeric_churn} vs Churn"
            )

            st.pyplot(fig)

            # Tabla comparativa

            comparison = (
                df.groupby("Churn")[selected_numeric_churn]
                .agg(["mean", "median", "std"])
                .round(2)
            )

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
                "8. Análisis bivariado: variable categórica vs Churn"
            )

            selected_categorical_churn = st.selectbox(
                "Selecciona una variable categórica:",
                categorical_vars,
                key="categorical_churn_variable"
            )

            # Gráfico de conteos

            fig, ax = plt.subplots()

            sns.countplot(
                data=df,
                x=selected_categorical_churn,
                hue="Churn",
                ax=ax
            )

            ax.set_title(
                f"{selected_categorical_churn} vs Churn"
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

            st.subheader(
                "Proporción de Churn por categoría (%)"
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
                default=available_categories
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

                fig, ax = plt.subplots()

                sns.countplot(
                    data=filtered_df,
                    x=dynamic_variable,
                    hue="Churn",
                    ax=ax
                )

                ax.set_title(
                    f"{dynamic_variable} vs Churn "
                    f"(datos filtrados)"
                )

                ax.tick_params(
                    axis="x",
                    rotation=45
                )

                st.pyplot(fig)


        # ÍTEM 10 — Hallazgos clave

        with tabs[9]:

            st.header("10. Hallazgos clave")

            st.write(
                """
                Esta sección resume los principales patrones
                identificados durante el análisis exploratorio.
                Las conclusiones deben basarse en los resultados
                observados en las tablas y visualizaciones.
                """
            )

            # Distribución general del Churn

            churn_distribution = (
                df["Churn"]
                .value_counts(normalize=True)
                * 100
            )

            churn_yes = churn_distribution.get(
                "Yes",
                0
            )

            churn_no = churn_distribution.get(
                "No",
                0
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Clientes que abandonaron",
                    f"{churn_yes:.2f}%"
                )

            with col2:

                st.metric(
                    "Clientes que permanecieron",
                    f"{churn_no:.2f}%"
                )


            # Gráfico general de Churn

            fig, ax = plt.subplots()

            sns.countplot(
                data=df,
                x="Churn",
                ax=ax
            )

            ax.set_title(
                "Distribución general de Churn"
            )

            st.pyplot(fig)


            # Mensaje de interpretación

            st.info(
                "Los hallazgos definitivos deben redactarse "
                "a partir de la comparación de las variables "
                "analizadas en los tabs anteriores."
            )



# CONCLUSIONES

elif opcion == "📝 Conclusiones":

    st.header("Conclusiones finales")

    st.write(
        """
        Las siguientes conclusiones deberán construirse a partir
        de los resultados obtenidos durante el Análisis Exploratorio
        de Datos.
        """
    )

    st.subheader("Conclusión 1")
    st.write(
        "Completar después de analizar los resultados."
    )

    st.subheader("Conclusión 2")
    st.write(
        "Completar después de analizar los resultados."
    )

    st.subheader("Conclusión 3")
    st.write(
        "Completar después de analizar los resultados."
    )

    st.subheader("Conclusión 4")
    st.write(
        "Completar después de analizar los resultados."
    )

    st.subheader("Conclusión 5")
    st.write(
        "Completar después de analizar los resultados."
    )
