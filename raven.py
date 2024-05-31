import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import base64

ruta_excel = 'C:/Users/ADMIN/Documents/LP/PROYECTO/DATOS.xlsx'
ruta_imagen1 = 'C:/Users/ADMIN/Documents/LP/PROYECTO/raven.jpg'
ruta_imagen2 = 'C:/Users/ADMIN/Documents/LP/PROYECTO/images.png'

if not os.path.exists(ruta_excel):
    st.error(f"No se encontró el archivo Excel en la ruta: {ruta_excel}")
else:
    datos = pd.read_excel(ruta_excel)
    datos['COMPONENTES'] = datos['COMPONENTES'].ffill()
    datos = datos.dropna(subset=['ESPECIFICACIONES TECNICAS', 'COSTOS'])
    mapeo_categorias = {
        'MOTHERBOARD': 'MB',
        'COOLER': 'COOLER',
        'CPU': 'CPU',
        'DISCO DURO': 'DISCO DURO',
        'MEM DDR': 'MEM DDR',
        'MONITOR': 'MONITOR',
        'MOUSE': 'MOUSE',
        'SSD': 'SSD',
        'TECLADO': 'TECLADO',
        'TARJETA DE VIDEO': 'TARJETA DE VIDEO'
    }
    componentes_dict = {value: [] for value in mapeo_categorias.values()}
    precios_dict = {value: {} for value in mapeo_categorias.values()}

    for categoria_excel, categoria_app in mapeo_categorias.items():
        especificaciones = datos[datos['COMPONENTES'].str.contains(categoria_excel, na=False)]
        for _, fila in especificaciones.iterrows():
            componentes_dict[categoria_app].append(fila['ESPECIFICACIONES TECNICAS'])
            precios_dict[categoria_app][fila['ESPECIFICACIONES TECNICAS']] = fila['COSTOS']

    categorias = list(componentes_dict.keys())

    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h1>FINESI</h1>
            <div style="text-align: center;">
                <img src="data:image/png;base64,{base64.b64encode(open(ruta_imagen2, "rb").read()).decode()}" width="150">
            </div>
            <img src="data:image/png;base64,{base64.b64encode(open(ruta_imagen1, "rb").read()).decode()}" width="150">
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <style>
        .reportview-container .main .block-container{
            padding-top: 20px;
            padding-bottom: 20px;
            padding-left: 5px;
            padding-right: 5px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.header("Calculadora de costos de Pc's")

    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Selecciones de la PC")
            componentes_seleccionados = {}
            costo_total = 0
            for categoria in categorias:
                opciones = componentes_dict.get(categoria, ["No disponible"])
                componente_seleccionado = st.selectbox(f"{categoria}", opciones)
                componentes_seleccionados[categoria] = componente_seleccionado
                if componente_seleccionado in precios_dict[categoria]:
                    costo_total += precios_dict[categoria][componente_seleccionado]

        with col2:
            st.subheader("Costo de componentes seleccionados")
            for categoria, componente in componentes_seleccionados.items():
                if componente in precios_dict[categoria]:
                    precio = precios_dict[categoria][componente]
                    st.write(f"**{categoria}:** {componente} - ${precio:.2f}")

            st.subheader("Costo total")
            st.write(f"${costo_total:.2f}")

    def generar_recomendaciones(componentes):
        recomendaciones = []
        if "i7" in componentes.get("CPU", ""):
            recomendaciones.append("Considera aumentar la capacidad del SSD para mejorar el rendimiento.")
        if "Ryzen 9" in componentes.get("CPU", ""):
            recomendaciones.append("Asegúrate de tener un buen sistema de enfriamiento para el CPU.")
        if "RTX 3080" in componentes.get("TARJETA DE VIDEO", ""):
            recomendaciones.append("Un monitor de alta resolución complementará bien tu tarjeta gráfica.")
        if "16GB" in componentes.get("MEM DDR", ""):
            recomendaciones.append("Para tareas intensivas, considera aumentar la memoria RAM a 32GB.")
        return recomendaciones

    recomendaciones = generar_recomendaciones(componentes_seleccionados)
    st.header("Recomendaciones:")
    if recomendaciones:
        for rec in recomendaciones:
            st.write(f"- {rec}")
    else:
        st.write("No hay recomendaciones adicionales.")

    def graficar_precios(componentes_seleccionados, precios_dict):
        componentes = list(componentes_seleccionados.keys())
        precios = [precios_dict[comp].get(componentes_seleccionados[comp], 0) for comp in componentes]

        fig, ax = plt.subplots()
        ax.barh(componentes, precios, color='skyblue')
        ax.set_xlabel('Precio ($)')
        ax.set_title('Precios de los Componentes Seleccionados')
        return fig

    fig = graficar_precios(componentes_seleccionados, precios_dict)
    st.pyplot(fig)
