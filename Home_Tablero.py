
# Cargando las Librerías:
    
import streamlit as st
import pandas as pd
# from pandas_profiling import ProfileReport
import streamlit.components.v1 as components


import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
# from numerize.numerize import numerize
from numerize import numerize

import time
from streamlit_extras.metric_cards import style_metric_cards
# st.set_option('deprecation.showPyplotGlobalUse', False)
import plotly.graph_objs as go


# Descomenta esta línea si usas MySQL:
# from query import *

st.set_page_config(page_title="Dashboard",page_icon="🌍",layout="wide")
st.header("MORBILIDAD:  Tratamiento Estadístico, KPI y Tendencias")

# Todos los gráficos se personalizan usando CSS , no Streamlit. 
theme_plotly = None 


# Cargar los estilo css:
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

# Descomenta estas dos líneas si obtienes datos de MySQL:
# result = view_all_data()
# df=pd.DataFrame(result,columns=["Policy","Expiry","Location","State","Investment","Construction","BusinessType","Earthquake","Flood","Rating","id"])

# cargar archivo Excel | comente esta línea cuando obtenga datos de MySQL:

# df = pd.read_excel("C:/Users/cesar/Downloads/TABLERO_STREAMLIT_DASHBOARD/DASHBOARD_Morbilidad_DESPLIEGUE/Tasas_Morbilidad.xlsx", sheet_name='Hoja1')
df = pd.read_excel('Tasas_Morbilidad.xlsx', sheet_name='Hoja1')

# Convirtiendo la columna Anio a Categórica:
    # Opción 2: Convertir a categórica (más eficiente)
df['anio'] = df['anio'].astype(str)
    
# ======================================================================



def safe_numerize(value):
    """Convierte un valor a formato numerize de forma segura"""
    try:
        # Manejar valores None o vacíos
        if value is None:
            return "0"
        
        # Convertir a string y limpiar
        str_value = str(value).strip().lower()
        if str_value in ['', 'nan', 'none', 'null']:
            return "0"
        
        # Convertir a número
        num_value = float(value)
        
        # Verificar si es NaN
        if num_value != num_value:  # NaN check sin pandas
            return "0"
        
        # Aplicar numerize
        return numerize(int(num_value))
        
    except (ValueError, TypeError, AttributeError):
        return "0"


# =============================================

# 📍 📎 🗺️ 🎯 🔗 ⚓ 🏠 🏢 🏭 🏬
# 🏷️ 🔖 📋 📝 📄 📊 📈 📉 🗂️ 📁
# 🔧 🔨 ⚙️ 🛠️ ⚡ 🔧 🗝️ 🔑 🎛️ ⚖️
#  ⚠️ ❗ ❓ ✅ ❌ 🟢 🔴 🟡 🟠 🔵
# 👆 👇 👈 👉 ↗️ ↘️ ↙️ ↖️ ⬆️ ⬇️ ⬅️ ➡️
# 💡 🔍 🎲 🎯 🎪 🎨 🎭 🎪 🎊 🎉
# 📊 📈 📉 💹 📋 🗃️ 🗄️ 💾 💿 📀
# 🏥 ⚕️ 💊 🩺 🧬 🦠 💉 🧪 🔬 📱

# =============================================



with st.expander("👉 Mostrar Filtros", expanded=False):
    Departamento = st.multiselect(
        "Selecciona Departamento",
        options=df["departamento"].unique(),
        default=df["departamento"].unique(),
    )

    Municipio = st.multiselect(
        "Selecciona Municipio",
        options=df["municipio"].unique(),
        default=df["municipio"].unique(),
    )

    Grupo = st.multiselect(
        "Selecciona el Grupo de Enfermedad",
        options=df["grupo"].unique(),
        default=df["grupo"].unique(),
    )








df_selection=df.query(
    "departamento==@Departamento & municipio==@Municipio & grupo ==@Grupo"
)



# Esta función realiza análisis descriptivos básicos como media, moda, suma, etc.
def Home():
    with st.expander("Ver el Conjunto de Datos en Excel"):
        showData=st.multiselect('Filter: ',df_selection.columns,default=["anio", "sexo", "nombre_cat_edad", "departamento", "municipio", "componente", "capitulo", "grupo", "Enfermedad_Evento", "pob10", "tasa_morb", "Tot_Eventos"])
        st.dataframe(df_selection[showData],use_container_width=True)
    # calcular los análisis:
    total_investment = float(pd.Series(df_selection['Tot_Eventos']).count())
    investment_mode = float(pd.Series(df_selection['tasa_morb']).mode())
    investment_mean = float(pd.Series(df_selection['tasa_morb']).mean())
    investment_median= float(pd.Series(df_selection['tasa_morb']).median()) 
    rating = float(pd.Series(df_selection['pob10']).mean())
    rating_percent = f"{rating:.1%}"


    total1,total2,total3,total4,total5=st.columns(5,gap='small')
    with total1:
        st.info('Total Eventos',icon="🎯")
        st.metric(label="Tot. Casos", value=f"{total_investment:,.0f}".replace(",", "."))
    with total2:
        st.info('Moda Tasa Morb.',icon="🎯")
        st.metric(label="Moda Morbilid.",value=f"{investment_mode:,.0f}")

    with total3:
        st.info('Prom. Tasa Morb.',icon="🎯")
        st.metric(label="Promedio Morbilid.",value=f"{investment_mean:,.0f}")

    with total4:
        st.info('Mediana Tasa Morb.',icon="🎯")
        st.metric(label="Mediana Morbilid.",value=f"{investment_median:,.0f}")

    with total5:
        st.info('Proy. Poblacional',icon="🎯")
        #st.metric(label="Rating",value=numerize(rating),help=f""" Total Rating: {rating} """)
        #st.metric(label="Rating", value=numerize(rating) if rating and not pd.isna(rating) else "0",
        #          help=f""" Total Rating: {rating if rating and not pd.isna(rating) else 0} """)
        
        #st.metric(label="Rating", value=numerize(rating) if rating is not None and rating != "" and str(rating) != 'nan' else "0", 
        #          help=f""" Total Rating: {rating if rating is not None else 0} """)
        
        st.metric(label="Proy. Pobl.", value=safe_numerize(rating_percent), help=f""" Proyección poblacional por cada 10 mil """ )
        
    style_metric_cards(background_color="#FFFFFF",border_left_color="#686664",border_color="#000000",box_shadow="#F71938")

    #variable distribution Histogram   # ERROR 1
    with st.expander("Distribución de Frecuencias - Tasa Morbilidad"):
     df.hist(figsize=(16,8),color='#898784', zorder=2, rwidth=0.9,legend = ['tasa_morb']);
     st.pyplot()

#graphs
def graphs():
    #total_investment=int(df_selection["Investment"]).sum()
    #averageRating=int(round(df_selection["Rating"]).mean(),2) 
    #Gráfico de barras simple de inversión por tipo de negocio
    investment_by_business_type=(
        df_selection.groupby(by=["anio"]).count()[["tasa_morb"]].sort_values(by="tasa_morb")
    )
    
    # Convertir el índice en una columna
    investment_by_business_type = investment_by_business_type.reset_index()
    
    # CORRECCIÓN: Usar 'tasa_morb' como y, no 'index'
    fig_investment = px.bar(
        investment_by_business_type,
        x="anio", 
        y="tasa_morb",  # ← Esta es la columna correcta
        title="Análisis de Morbilidad por Año", 
        color_discrete_sequence=["#0083B8"] * len(investment_by_business_type),
        template="plotly_white"
    )
    
    fig_investment.update_layout(
     plot_bgcolor="rgba(0,0,0,0)",
     font=dict(color="black"),
     yaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Mostrar la cuadrícula del eje y y establecer su color  
     paper_bgcolor='rgba(0, 0, 0, 0)',  # Establecer el color del fondo  en transparente
     xaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Mostrar la cuadrícula del eje x y establecer su color
     )
    
    # gráfico de regresión lineal simple de inversión por nombre_cat_edad
    investment_state = df_selection.groupby(by=["nombre_cat_edad"]).count()[["tasa_morb"]]
    
    investment_state_reset = investment_state.reset_index()    
    
    fig_state = px.line(investment_state_reset, 
                   x="nombre_cat_edad",  # Categorías de edad en el eje X
                   y="tasa_morb",        # Conteo/tasa en el eje Y
                   orientation="v", 
                   title="<b> TASA DE MORBILIDAD POR CATEGORÍA DE EDADES </b>",
                   color_discrete_sequence=["#0083b8"]*len(investment_state_reset), 
                   template="plotly_white",
                   
    )
    
    fig_state.update_layout(
        xaxis=dict(tickmode="linear"), 
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False))
        )
    
    left,right,center=st.columns(3)
    left.plotly_chart(fig_state,use_container_width=True)
    right.plotly_chart(fig_investment,use_container_width=True)
    
    with center:
      #pie chart
      fig = px.pie(df_selection, values='tasa_morb', names='departamento', title="<b> TASA  MORBILIDAD POR DEPARTAMENTO </b>")
      fig.update_layout(legend_title="Dptos.", legend_y=0.9)
      fig.update_traces(textinfo='percent+label', textposition='inside')
      st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)


# función para mostrar las ganancias actuales frente al objetivo esperado
def Progressbar():
    st.markdown("""<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99 , #FFFF00)}</style>""",unsafe_allow_html=True,)
    target=3000000000
    current=df_selection["Investment"].sum()
    percent=round((current/target*100))
    mybar=st.progress(0)

    if percent>100:
        st.subheader("Objetivo cumplido !")
    else:
     st.write("tienes ",percent, "% " ,"of ", (format(target, 'd')), "TZS")
     for percent_complete in range(percent):
        time.sleep(0.1)
        mybar.progress(percent_complete+1,text=" Objetivo Porcentual")

#menu bar
def sideBar():
 with st.sidebar:
    selected=option_menu(
        menu_title="Menú Principal",
        options=["Home","Progress"],
        icons=["house","eye"],
        menu_icon="cast",
        default_index=0
    )
 if selected=="Home":
    #st.subheader(f"Page: {selected}")
    Home()
    graphs()
 if selected=="Progress":
    #st.subheader(f"Page: {selected}")
    Progressbar()
    graphs()


sideBar()
#st.sidebar.image("data/Logo_UNILLANOS.png",caption="")      # LOGO
st.sidebar.image("Logo_UNILLANOS.png",caption="")            # LOGO



st.subheader('Seleccione Atributos para Observar Tendencias de Distrib. Por Cuartiles',)
#feature_x = st.selectbox('Select feature for x Qualitative data', df_selection.select_dtypes("object").columns)
feature_y = st.selectbox('Seleccionar función para (Y) Datos cuantitativos', df_selection.select_dtypes("number").columns)
fig2 = go.Figure(
    data=[go.Box(x=df['grupo'], y=df[feature_y])],
    layout=go.Layout(
        title=go.layout.Title(text="Distribución Numérica, por Grupo de Enfermedades"),
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Set plot background color to transparent
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper background color to transparent
        xaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show x-axis grid and set its color
        yaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show y-axis grid and set its color
        font=dict(color='#cecdcd'),  # Set text color to black
    )
)
# Display the Plotly figure using Streamlit
st.plotly_chart(fig2,use_container_width=True)



#theme
hide_st_style=""" 

<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""





# PARA EJECUTAR EL DASHBOARD, CORRER LAS SIGUIENTES LÍNEAS EN C:
# Invoca la carpeta donde está ubicado el archivo:  --->

# cd C:\Users\cesar\Downloads\TABLERO_STREAMLIT_DASHBOARD\DASHBOARD_STREAMLIT_COMPLETO




# Invocando el archivo: ---->
# python streamlit_app.py (este comando no corrió... entonces ejecutar el siguiente: ----> )

# streamlit run Home_Tablero.py



























