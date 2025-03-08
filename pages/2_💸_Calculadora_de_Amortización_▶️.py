import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import scipy.optimize as opt
import io

st.set_page_config(page_title="Calculadora de Amortización", page_icon="💸", layout="wide")
st.title("💸 Calculadora de Amortización")

st.markdown(
    "<p style='position: absolute; top: -90px; right: 20px; font-size: 12px; color: white;'>Por Juan Sebastian Lopez</p>",
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    /* Aumentar tamaño de los nombres de las páginas en el sidebar */
    div[data-testid="stSidebarNav"] ul li a {
        font-size: 18px !important; /* Cambia el tamaño según prefieras */
        font-weight: bold !important; /* Opcional: poner en negrita */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            min-width: 350px;  /* Cambia el valor según el ancho deseado */
            max-width: 350px;
        }
    </style>
    """,
    unsafe_allow_html=True
)
st.sidebar.markdown("<h1 style='text-align: left; font-size: 24px;'>🔧 Parámetros del Préstamo</h1>", unsafe_allow_html=True)

# Función para convertir la entrada a número y manejar errores
def obtener_valor(texto, valor_default=0):
    try:
        return float(str(texto).replace(",", ""))
    except ValueError:
        return valor_default

# Entrada de datos
capital = obtener_valor(st.sidebar.text_input("💰 ¿Cuánto te van a prestar?", placeholder="Ej: 1000000"))
Interes = obtener_valor(st.sidebar.text_input("📈 ¿A qué % de Interés E.A.?", placeholder="Ej: 26"))
Meses = st.sidebar.selectbox("📆 ¿Durante cuántos meses?", list(range(12, 121)), index=0)
cuota_manejo = obtener_valor(st.sidebar.text_input("💳 Cuota de manejo mensual", placeholder="Ej: 100"))
seguro = obtener_valor(st.sidebar.text_input("🛡️ Seguro mensual", placeholder="Ej: 50"))
otros_cobros = obtener_valor(st.sidebar.text_input("📋 Otros Cobros", placeholder="Ej: 50"))

tasa_mensual = 0
cuota_base = 0
cuota_total = 0


# Validar que los valores sean correctos
if capital > 0 and Interes > 0 and Meses > 0:
    # Corregimos la conversión de tasa efectiva anual a tasa mensual
    tasa_mensual = (1 + Interes / 100) ** (1 / 12) - 1

    # Calcular cuota base y la cuota total con costos adicionales
    cuota_base = (capital * tasa_mensual) / (1 - (1 + tasa_mensual) ** -Meses)
    cuota_total = cuota_base + cuota_manejo + seguro + otros_cobros
    
    
    Total_pagado = cuota_total * Meses
    Total_intereses = Total_pagado - capital

    st.write(f"💰 La cuota mensual fija es: **${cuota_base:,.2f}**")
    st.write(f"💸 El costo financiero de tu prestamo es: **${Total_intereses:,.2f}**")
    st.markdown("""
    <p style="font-size: 12px; color: gray; margin-top: 0px; line-height: 1.2;">
        *Nota: Este valor es la diferencia entre el total pagado y el valor del préstamo.*
    </p>
""", unsafe_allow_html=True)
    if (cuota_manejo + seguro + otros_cobros) > 0:
        st.write(f"⚠️ La cuota total con costos adicionales es: **${cuota_total:,.2f}**")
   
    # Función para calcular tasa equivalente
    def calcular_tasa_equivalente(r):
        return (capital * r) / (1 - (1 + r) ** -Meses) - cuota_total

    try:
        tasa_mensual_equivalente = opt.fsolve(calcular_tasa_equivalente, 0.02)[0]
        tasa_efectiva_anual_equivalente = (1 + tasa_mensual_equivalente) ** 12 - 1
        tasa_efectiva_anual_equivalente *= 100  # Convertir a porcentaje
        if (cuota_manejo + seguro + otros_cobros) > 0:
            st.write(f"📊 La tasa efectiva anual equivalente con costos es: **{tasa_efectiva_anual_equivalente:.2f}%**")
            st.markdown("""
            <p style="font-size: 12px; color: gray;">
                *Nota: Esta tasa es un aproximado del efectivo anual incluyendo los costos adicionales como la cuota de manejo y el seguro mensual.*
            </p>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.write("⚠️ No se pudo calcular la tasa equivalente, revisa los valores ingresados.")
        st.write(f"Detalles del error: {e}")
else:
    st.write("⚠️ Ingrese en el panel de la izquierda los datos de su préstamo.")

        
# Generación de tabla de amortización con nuevo orden de columnas
df = pd.DataFrame(columns=["Mes", "Cuota", "Costos Adicionales", "Interés", "Capital", "Saldo"])
saldo = capital

for mes in range(1, Meses + 1):
    interes = saldo * tasa_mensual
    capital_pagado = cuota_base - interes
    
    # Si el capital pagado excede el saldo restante, ajustamos el capital pagado
    if saldo - capital_pagado < 0:
        capital_pagado = saldo
    
    saldo -= capital_pagado
    
    # Aseguramos que el saldo no sea negativo
    if saldo < 0:
        saldo = 0
    
    # Añadir la fila con el nuevo orden de columnas
    df.loc[mes] = [
        mes,
        round(cuota_total, 0),              
        round(cuota_manejo + seguro, 0),     
        round(interes, 0),                   
        round(capital_pagado, 0),            
        round(saldo, 0)                      
    ]




fig = go.Figure()

# Añadir la barra de Capital Pagado
fig.add_trace(go.Bar(
    x=df["Mes"], 
    y=df["Capital"], 
    name="Capital Pagado", 
    marker_color='green'
))

# Añadir la barra de Intereses
fig.add_trace(go.Bar(
    x=df["Mes"], 
    y=df["Interés"], 
    name="Intereses", 
    marker_color='red'
))

# Añadir la barra de Costos Adicionales
fig.add_trace(go.Bar(
    x=df["Mes"], 
    y=df["Costos Adicionales"], 
    name="Costos Adicionales", 
    marker_color='blue'
))

# Actualizar el layout para una gráfica apilada
fig.update_layout(
    title="Distribución de la Cuota Mensual",
    xaxis_title="Mes",
    yaxis_title="Valor Pagado",
    barmode='stack',  # Apilar las barras
    template="plotly_white"
)

# Mostrar la gráfica
st.plotly_chart(fig)

# Formatear valores numéricos
df_format = df
for col in df_format.columns:
    if col != "Mes":
        df_format[col] = df_format[col].apply(lambda x: f"${x:,.0f}")

# Mostrar la tabla reorganizada
st.write("### 📋 Tabla de Amortización")
st.dataframe(df_format, use_container_width=True)

## Función para convertir DataFrame a Excel en un buffer
def convertir_a_excel(df):
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    buf.seek(0)
    return buf

# Botón para descargar en Excel
st.download_button(
    label="📥 Descargar tabla en Excel",
    data=convertir_a_excel(df),
    file_name="Amortizacion.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)
