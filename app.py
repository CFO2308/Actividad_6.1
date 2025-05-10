# Cada que hagamos un cambio en el dashboard debo de cargar esta celda
######################################################################
# Importamos librerías
import streamlit as st 
import plotly.express as px
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
######################################################################
# Definimos la instancia
@st.cache_resource
def load_data():
    df = pd.read_csv('DataAnalytics.csv')
    df['Usuario'] = df['Usuario'].str.strip().str.upper()
    Lista = ['color presionado', 'mini juego', 'dificultad', 'Juego']
    Usuario = ['ADRIAN', 'ALEIDA', 'ARLETT', 'AUSTIN']
    return df, Lista, Usuario

######################################################################
# Cargo los datos de la función "load_data"
df, Lista, Usuario = load_data()
######################################################################
# Mostrar imagen en la parte superior del dashboard
st.sidebar.image("PHOTO-2025-05-09-18-08-42.jpg", width=200)

# CREACIÓN DEL DASHBOARD
######################################################################
st.sidebar.title("ANÁLISIS UNIVARIADO WUPPI")

# Widget para seleccionar tipo de análisis
View = st.sidebar.selectbox(
    label="Tipo de Análisis", 
    options=["Extracción de Características", "Regresión Lineal", "Regresión No Lineal", "Regresión Logistica", "ANOVA"]
)

# Vista 1: Extracción de características

if View == "Extracción de Características":
    Variable_Cat = st.sidebar.selectbox(label="Variable a analizar", options=Lista)

    st.title("Extracción de Características por Usuario")
    st.subheader("Variable seleccionada: " + Variable_Cat)

    df_filtrado = df[(df['Usuario'] == 'ADRIAN') | (df['Usuario'] == 'ALEIDA') | (df['Usuario'] == 'ARLETT') | (df['Usuario'] == 'AUSTIN')]

    # Crear columnas principales
    col1, col2 = st.columns(2)

    usuarios_col1 = ['ADRIAN', 'ARLETT']
    usuarios_col2 = ['ALEIDA', 'AUSTIN']

    # Checkbox para mostrar variables numéricas por usuario
    mostrar_numericas = st.checkbox("**¿Mostrar variables numéricas por usuario?**", key="num_checkbox")

    # Mostrar tablas numéricas por usuario
    if mostrar_numericas:
        st.subheader("Tablas de variables numéricas por usuario")
        col3, col4 = st.columns(2)
        with col3:
            for usuario in usuarios_col1:
                df_usuario = df_filtrado[df_filtrado['Usuario'] == usuario]
                df_numericas = df_usuario.select_dtypes(include='number')
                if not df_numericas.empty:
                    st.markdown(f"**{usuario}**")
                    st.dataframe(df_numericas)
        with col4:
            for usuario in usuarios_col2:
                df_usuario = df_filtrado[df_filtrado['Usuario'] == usuario]
                df_numericas = df_usuario.select_dtypes(include='number')
                if not df_numericas.empty:
                    st.markdown(f"**{usuario}**")
                    st.dataframe(df_numericas)

    # Función auxiliar para graficar según variable

    
    def mostrar_grafica(usuario, df_usuario):
        st.markdown(f"**Usuario: {usuario}**")
        tabla = df_usuario[Variable_Cat].value_counts().reset_index()
        tabla.columns = ['categorias', 'frecuencia']

        if Variable_Cat == 'color presionado':
            fig = px.bar(tabla, x='categorias', y='frecuencia', title=f"{Variable_Cat} - {usuario}",
                         color='categorias', color_discrete_map={color: color for color in tabla['categorias']})
            st.plotly_chart(fig, use_container_width=True)

        elif Variable_Cat == 'mini juego':
            fig = px.pie(tabla, names='categorias', values='frecuencia', hole=0.4, title=f"{Variable_Cat} - {usuario}")
            st.plotly_chart(fig, use_container_width=True)

        elif Variable_Cat == 'dificultad':
            fig = px.pie(tabla, names='categorias', values='frecuencia', title=f"{Variable_Cat} - {usuario}")
            st.plotly_chart(fig, use_container_width=True)

        elif Variable_Cat == 'Juego':
            tabla = df_usuario[Variable_Cat].value_counts().reset_index()
            tabla.columns = ['categorias', 'frecuencia']
            fig = px.scatter(tabla, x='categorias', y='frecuencia', size='frecuencia',
                             title=f"Juegos más utilizados - {usuario}", color='categorias')
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)

    # Columna 1: ADRIAN y ARLETT
    with col1:
        for usuario in usuarios_col1:
            df_usuario = df_filtrado[df_filtrado['Usuario'] == usuario]
            mostrar_grafica(usuario, df_usuario)

    # Columna 2: ALEIDA y AUSTIN
    with col2:
        for usuario in usuarios_col2:
            df_usuario = df_filtrado[df_filtrado['Usuario'] == usuario]
            mostrar_grafica(usuario, df_usuario)

