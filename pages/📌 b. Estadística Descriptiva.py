


# Cargando las Librerías:
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize import numerize
import time
from streamlit_extras.metric_cards import style_metric_cards
import plotly.graph_objs as go
import plotly.graph_objects as go

# =====================================
# TITULO Y ESTILO DEL ENCABEZADO:
st.set_page_config(page_title="Dashboard ", page_icon="📈", layout="wide")  
st.header("Resumen Gráfico Exploratorio Multidimensional")
st.markdown("##")
 
# Cargar CSS si existe el archivo
try:
    with open('style.css') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("Archivo style.css no encontrado. Continuando sin estilos personalizados.")

# LLAMANDO EL DATAFRAME:
try:
    # Importando la tabla agregada con los resúmenes de las variables:
    df_subsectores = pd.read_excel('TablaMorbilidad_Subsectores.xlsx', sheet_name='Hoja1')
    df_subsectores["conteos"] = round(df_subsectores["conteos"], 0)
    df_subsectores["tasas"] = round(df_subsectores["tasas"], 1) 

    
    # Estructura jerárquica: País > Departamento > Enfermedad
    labels = df_subsectores['labels'].tolist()
    parents = df_subsectores['parents'].tolist()
    conteos = df_subsectores['conteos'].tolist()
    tasas = df_subsectores['tasas'].tolist()
    
    # Etiquetas personalizadas con conteo y tasa
    custom_labels = [f"{l}<br>Casos: {v:,.0f}<br>Tasa: {t:.1f}/10k".replace(',', '.') if v != 0 else l 
                 for l, v, t in zip(labels, conteos, tasas)]
    
    # Sunburst plot
    #colors = ['#2A3180', '#39A8E0', '#F28F1C', '#E5352B', '#662681', '#009640', '#9D9D9C']
    fig = go.Figure(go.Sunburst(
        labels=custom_labels,
        parents=parents,
        values=conteos,
        branchvalues="remainder" #,  # ahora los padres no necesitan tener suma directa
        #marker=dict(colors=colors * (len(labels) // len(colors) + 1))  # Repetir colores si son necesarios
    ))
    
    # Agregando el Titulo (Elegante)
    fig.update_layout(
        title={
            "text": "Enfermedades más Frecuentes por Departamento",
            "y": 0.95, 
            "x": 0.5, 
            "xanchor": "center", 
            "yanchor": "top", 
            "font": dict(size=34, family="Agency FB", color="black")
        }, 
        margin=dict(t=80, l=10, r=10, b=10)
    )
    
    
    
    # ¡AQUÍ ESTÁ LA LÍNEA QUE FALTABA!
    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
except FileNotFoundError:
    st.error("Archivo 'TablaMorbilidad_Subsectores.xlsx' no encontrado. Verifica que el archivo esté en el directorio correcto.")
except Exception as e:
    st.error(f"Error al cargar los datos: {str(e)}")
    
 













