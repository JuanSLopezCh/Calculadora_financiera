# streamlit run LF_app.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd
import io

st.set_page_config(page_title="Calculadora de Ahorro", page_icon="📊", layout="wide")


st.title("💰 Calculadora de Ahorro con Interés Compuesto")

st.markdown(
    "<p style='position: absolute; top: -90px; right: 20px; font-size: 12px; color: white;'>Por Juan Sebastian Lopez</p>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    /* Aumentar tamaño de los nombres de las páginas en el sidebar */
    div[data-testid="stSidebarNav"] ul li a {
        font-size: 20px !important; /* Cambia el tamaño según prefieras */
        font-weight: bold !important; /* Opcional: poner en negrita */
    }
    </style>
    """,
    unsafe_allow_html=True
)


# region Inversion_Inicial

# Usar la barra lateral para los inputs
st.sidebar.markdown("<h1 style='text-align: left; font-size: 24px;'>🔧 Parámetros de inversión</h1>", unsafe_allow_html=True)

# Inversión principal
capital_inicial = st.sidebar.text_input("💰 ¿Con cuánto dinero inicias?", placeholder="Ej: 1000000")
aporte_mensual = st.sidebar.text_input("📥 ¿Cuánto vas a ahorrar mensualmente?", placeholder="Ej: 50000")
rentabilidad = st.sidebar.text_input("📈 ¿Qué % de rentabilidad esperas tener anual?", placeholder="Ej: 5.0")

años = st.sidebar.selectbox("📆 Años para alcanzar mi LF", list(range(1, 21)), index=4)

# Convertir los valores ingresados a números
try:
    capital_inicial = int(str(capital_inicial).replace(",", ""))
except ValueError:
    capital_inicial = 0

try:
    aporte_mensual = int(str(aporte_mensual).replace(",", ""))
except ValueError:
    aporte_mensual = 0

try:
    rentabilidad = float(str(rentabilidad).replace(",", ""))
except ValueError:
    rentabilidad = 0.0
    
meses = años * 12

if capital_inicial > 0:  
    aporte_total_inicial = aporte_mensual * (meses - 1)  # Solo 11 meses si hay capital inicial  
else:  
    aporte_total_inicial = aporte_mensual * meses  # 12 meses si NO hay capital inicial  

aporte_inicial = capital_inicial + aporte_total_inicial

ponderado_inicial = aporte_inicial*(rentabilidad/100)

#debug
# capital_inicial
# aporte_mensual
# rentabilidad
# aporte_inicial
# ponderado_inicial


# endregion Inversion_inicial

# region Inversiones_adicionales

if "mostrar_inversiones" not in st.session_state:
    st.session_state.mostrar_inversiones = False
if "inversiones" not in st.session_state:
    st.session_state.inversiones = []

# Botón para agregar inversiones adicionales
if st.sidebar.button("➕ Agregar otra inversión"):
    st.session_state.mostrar_inversiones = True
    st.session_state.inversiones.append({"capital": 0, "monto": 0, "rentabilidad": 0.0})

# Mostrar inversiones adicionales
if st.session_state.mostrar_inversiones:
    st.sidebar.markdown("### 💰 Inversiones adicionales")

    # Generar un índice para cada inversión y mostrar el formulario para cada una
    for i, inversion in enumerate(st.session_state.inversiones):
        with st.sidebar.expander(f"Inversión {i + 1}", expanded=True):
            capital = st.number_input(f"Capital Inicial 💰 (Inv {i + 1})", min_value=0, step=100, key=f"capital_{i}")
            monto = st.number_input(f"Inversión Mensual 💰 (Inv {i + 1})", min_value=0, step=100, key=f"monto_{i}")
            rentabilidad_inv = st.number_input(f"Rentabilidad % 📈 (Inv {i + 1})", min_value=0.0, step=0.1, format="%.2f", key=f"rentabilidad_{i}") 
            if  capital > 0:
                total_mes_inv = monto * (meses - 1)
            else:
                total_mes_inv = monto * (meses)
            total_inv = capital + total_mes_inv
            ponderado_inv = total_inv*(rentabilidad_inv/100)
            
            # Actualizar la inversión en el estado de sesión
            st.session_state.inversiones[i] = {"capital": capital, "monto": monto, "rentabilidad": rentabilidad_inv, 
                                               "Total_Inv": total_inv, "Ponderado":ponderado_inv }
            
            # Botón para eliminar inversión
            if st.button(f"❌ Eliminar Inversión {i + 2}", key=f"delete_{i}"):
                del st.session_state.inversiones[i]  # Eliminar inversión
                st.rerun()  # Recargar la app para actualizar la lista
                
# endregion Inversiones_adicionales

# region totales
inversiones_completas = [{"capital": capital_inicial, "monto": aporte_mensual, "rentabilidad": rentabilidad}]  # Primera inversión individual
inversiones_completas += st.session_state.inversiones  # Agregar las adicionales sin modificarlas

# Unificar valores de inversión
total_capital = capital_inicial + sum(inv["capital"] for inv in st.session_state.inversiones)

# Calcular el total invertido (capital inicial + aportes mensuales de todas las inversiones)

aporte_mensual_total = (aporte_mensual + sum(inv["monto"] for inv in st.session_state.inversiones)) 

aporte_mensual_total2 = sum(
    inv["monto"] * (meses - 1) if inv["capital"] > 0 else inv["monto"] * meses
    for inv in inversiones_completas
)


aporte_total = total_capital + aporte_mensual_total2

total_ponderado = ponderado_inicial + sum(inv["Ponderado"] for inv in st.session_state.inversiones) # Solo el capital inicial está invertido todo el tiempo

rentabilidad_ponderada = (total_ponderado / aporte_total) if aporte_total > 0 else 0.0

# st.write(f"📌 Debug - Total capital: {total_capital}") 
# st.write(f"📌 Debug - aporte_mensual_total: {aporte_mensual_total}") 
# st.write(f"📌 Debug - aporte_mensual_total2: {aporte_mensual_total2}") 
# st.write(f"📌 Debug - Total aporte_total: {aporte_total}") 

# endregion totales

# region calculo_rendimiento

# Calcular tasa nominal anual
tasa_nominal = 12 * ((1 + rentabilidad_ponderada) ** (1 / 12) - 1)


# Calcular tasa mensual
tasa_mensual = tasa_nominal / 12

vf_total = 0  # Reiniciar el total

# Crear lista con todas las inversiones (incluyendo la principal)


# Debug para verificar
# st.write("📊 Debug - Inversiones Completas:", inversiones_completas)

for inv in inversiones_completas:
    capital = inv["capital"]
    aporte_mensual = inv["monto"]
    rentabilidad_efectiva_anual = inv["rentabilidad"] / 100

    # Convertir a tasa mensual efectiva
    tasa_mensual = (1 + rentabilidad_efectiva_anual) ** (1/12) - 1

    # Calcular valor futuro iterativo
    if capital == 0:
        acumulado = 0
        for i in range(meses):
            acumulado = (acumulado + aporte_mensual) * (1 + tasa_mensual)
    # Si hay capital inicial
    else:
        acumulado = capital * (1 + tasa_mensual)
        for i in range(meses-1):
            acumulado = (acumulado + aporte_mensual) * (1 + tasa_mensual)
            
    vf_total += acumulado  # Sumar cada inversión al total

# Calcular la ganancia total
aporte_total = sum(inv["capital"] + (inv["monto"] * (meses if inv["capital"] == 0 else meses - 1)) for inv in inversiones_completas)


ganancia = vf_total - aporte_total

# endregion calculo_rendimiento

#region Resumen
# Mostrar el resumen
st.write("### 📌 Resumen de tu inversión:")
st.write(f"Capital Total Inicial: **${total_capital:,.0f}**")
st.write(f"Aporte mensual total: **${aporte_mensual_total2:,.0f}**")
st.write(f"**Rentabilidad Ponderada Estimada Anual:** {rentabilidad_ponderada*100:.2f}%")

if años == 1:
    años_txt = "1 año"
else:
    años_txt = f"{años} años"

st.write(f"### 💰 Al pasar {años_txt} habrás:")
st.write(f"**Ahorrado:** ${aporte_total:,.0f}")
st.write(f"**Ganado en intereses:** ${ganancia:,.0f}")
st.write(f"**Total acumulado:** ${vf_total:,.0f}")

#endregion Resumen

# region Tabla de Datos

# Crear un diccionario con la columna de Periodo
datos_tabla = {"Periodo": list(range(1, meses + 1))}

# Recorrer cada inversión
for idx, inv in enumerate(inversiones_completas, start=1):
    if inv["capital"] == 0:
        capital_inicial = inv["monto"]  # Si no hay capital inicial, se asigna el aporte mensual
    else:
        capital_inicial = inv["capital"]  # Si hay capital inicial, se asigna el valor de capital inicial
    
    aporte_mensual = inv["monto"]  # El aporte mensual
    rentabilidad_efectiva_anual = inv["rentabilidad"] / 100  # Rentabilidad anual
    rentabilidad_mensual = (1 + rentabilidad_efectiva_anual) ** (1/12) - 1  # Convertir a tasa mensual

    # Inicializar valores
    acumulado = capital_inicial
    ahorro_lista = []
    acumulado_lista = []
    
    # Calcular mes a mes
    for periodo in range(1, meses + 1):
        if periodo == 1:
            # El primer mes muestra la rentabilidad del capital inicial
            rendimiento = capital_inicial * rentabilidad_mensual
            acumulado += rendimiento  # Se actualiza el acumulado con rentabilidad
            ahorro = capital_inicial # El ahorro en el primer mes es el capital inicial + rendimiento
        else:
            ahorro = aporte_mensual  # A partir del segundo mes, es solo el aporte mensual
            acumulado += ahorro  # Sumar el aporte mensual antes de calcular la rentabilidad
            rendimiento = acumulado * rentabilidad_mensual
            acumulado += rendimiento  # Sumar la rentabilidad al acumulado

        # Guardar valores en las listas
        ahorro_lista.append(ahorro)  # Guardar el ahorro mensual
        acumulado_lista.append(acumulado)  # Guardar el acumulado actualizado

    # Agregar las listas al diccionario con nombres dinámicos
    datos_tabla[f"Inv {idx}"] = ahorro_lista
    datos_tabla[f"Rentabilidad {idx}"] = acumulado_lista

# Convertir a DataFrame
df_tabla = pd.DataFrame(datos_tabla)


# Formatear valores numéricos
for col in df_tabla.columns:
    if col != "Periodo":
        df_tabla[col] = df_tabla[col].apply(lambda x: f"${x:,.2f}")

# endregion Tabla de Datos

# region grafica

# Convertimos las columnas de ahorro y rentabilidad a numéricas (quitamos los signos $ y , si están en string)
df_numerico = df_tabla.copy()
for col in df_numerico.columns:
    if col != "Periodo":
        df_numerico[col] = df_numerico[col].replace('[\$,]', '', regex=True).astype(float)

# Sumar todas las columnas de inversión y rentabilidad
df_numerico["Ahorro Total"] = df_numerico.filter(like="Inv").sum(axis=1).cumsum()
df_numerico["Acumulado Total"] = df_numerico.filter(like="Rentabilidad").sum(axis=1)

# Crear gráfica
fig, ax = plt.subplots(figsize=(13, 8))

ax.plot(df_numerico["Periodo"], df_numerico["Ahorro Total"], label="Ahorro Total", linestyle="-", 
        linewidth=2, alpha=0.8, color="#FFAA00")  # Naranja
ax.plot(df_numerico["Periodo"], df_numerico["Acumulado Total"], label="Rentabilidad Total", linestyle="-", 
        linewidth=2.5, color="#00FFAA")  # Verde claro

# Configurar ejes y grid
ax.set_facecolor("#1E1E1E")  # 🔹 Mantener el fondo oscuro
ax.set_title("Crecimiento del Ahorro", fontsize=16, fontweight="bold", color="white")
ax.set_xlabel("Meses", fontsize=12, fontweight="bold", color="white")
ax.set_ylabel("Total\nAcumulado ($)", fontsize=12, fontweight="bold", color="#F2F2F2", labelpad=40, rotation=0)

ax.legend(fontsize=10, loc="upper left", frameon=True, shadow=True)
ax.grid(color="#FFFFFF", linestyle="--", linewidth=0.7, alpha=0.7)

# Mejorar etiquetas del eje Y
yticks = np.linspace(min(df_numerico["Acumulado Total"]), max(df_numerico["Acumulado Total"]), num=6)
ax.set_yticks(yticks)
ax.set_yticklabels([f"${int(y):,}" for y in yticks], color="white", fontsize=12)

# Cambiar color de los números en los ejes
ax.tick_params(axis="x", colors="white", labelsize=10)
ax.tick_params(axis="y", colors="white", labelsize=10)

# Cambiar el fondo de la gráfica a negro
fig.patch.set_facecolor('#2C2C2C')  # Color de fondo de la figura
ax.set_facecolor('#2C2C2C')  # Color de fondo del área de la gráfica

# Mostrar en Streamlit con ajuste de tamaño
st.pyplot(fig, use_container_width=True)

# endregion grafica

# region descargar excel

# Mostrar tabla en Streamlit
st.write("### 📋 Tabla de Crecimiento del Ahorro")
st.dataframe(df_tabla, use_container_width=True)

# Función para convertir DataFrame a Excel en un buffer
def convertir_a_excel(df):
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    buf.seek(0)
    return buf

# Botón para descargar en Excel
st.download_button(
    label="📥 Descargar tabla en Excel",
    data=convertir_a_excel(df_numerico),
    file_name="proyeccion_ahorro.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)

# endregion descargar excel
