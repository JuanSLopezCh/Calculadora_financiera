#streamlit run Calculadora_LF.py
import streamlit as st

st.set_page_config(page_title="Bienvenido", page_icon="📊", layout="wide")

# Título principal con emoji
st.title("📊 Bienvenido a la Calculadora Financiera")

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
    Esta aplicación te permite realizar cálculos clave para mejorar tu planificación financiera.
    Puedes utilizar dos herramientas principales:
    """
)

# Crear columnas para organizar las tarjetas
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 💰 Calculadora de Ahorro e Inversión")
    st.markdown(
        """
        Proyecta el crecimiento de tus ahorros con interés compuesto.
        - Ingresa tu **capital inicial** y **aportes mensuales**.
        - Define la **tasa de interés esperada**.
        - Visualiza el crecimiento de tu inversión en el tiempo.
        """
    )
    

with col2:
    st.markdown("### 💸 Calculadora de Amortización")
    st.markdown(
        """
        Analiza el pago de préstamos y créditos con un plan de amortización detallado.
        - Ingresa el **monto del préstamo** y la **tasa de interés**.
        - Define el **plazo en meses**.
        - Obtén una tabla de amortización y gráficos explicativos.
        """
    )
    

# Mensaje motivador al final
st.markdown("---")
st.markdown(
    "🔎 *¡Optimiza tu dinero con decisiones informadas y mejora tu futuro financiero!* 🚀"
)


# Documentación de las calculadoras
st.markdown("---")
st.subheader("📚 Documentación de las Calculadoras")

# Expander para la calculadora de Ahorro e Inversión
with st.expander("💰 Calculadora de Ahorro"):
    st.markdown("""
    ### Fórmulas Utilizadas:

    #### Cálculo de Valor Final con Interés Compuesto (Iterativo):

    Si tienes **capital inicial** (mes 1):
    - **Mes 1 (capital inicial)**:  
    $$
    V_{1} = C_0 \times (1 + r)
    $$

    - **Meses 2 a n** (aportando mensualmente):  
    $$
    V_{n} = (V_{n-1} + A) \times (1 + r)
    $$

    Donde:
    - $V_{n}$ es el valor final acumulado en el mes $n$.
    - $C_0$ es el capital inicial.
    - $A$ es el aporte mensual.
    - $r$ es la tasa de interés mensual (derivada de la tasa anual).

    Si **no tienes capital inicial**, la fórmula se aplica desde el mes 1 solo con los aportes mensuales:
    - **Mes 1 a n** (solo aportes):  
    $$
    V_{n} = (V_{n-1} + A) \times (1 + r)
    $$

    ### Proceso:
    1. Se ingresa el capital inicial, los aportes mensuales, la tasa de interés anual y el tiempo de inversión (en años).
    2. Si existe un **capital inicial**, el cálculo comienza con el capital inicial y luego se suman los aportes mensuales a partir del segundo mes. Si **no hay capital inicial**, se comienza con los aportes mensuales desde el mes 1.
    3. La herramienta realiza los cálculos mes a mes, acumulando el capital y aplicando la rentabilidad mensual sobre el monto total acumulado hasta ese mes.
    4. Se muestra el resumen de la inversión, incluyendo:
        - El capital inicial.
        - Los aportes mensuales totales.
        - La rentabilidad ponderada estimada anual.
        - El ahorro total y la ganancia en intereses después del tiempo especificado.
    5. Se genera un gráfico de lineas para visualizar el **ahorro total** 
    si no se estuviera rentando y el **ahorro con rentabbilidad** para poder ver como crece el capital basado en el ahorro.

    6. El usuario puede descargar las inversiones en formato Excel para su análisis.

    ### Consideraciones:
    - La tasa de interés **es anual** y se convierte a **mensual** para los cálculos. La tasa mensual se obtiene con la fórmula:
        $$
        r_{\text{mensual}} = (1 + r_{\text{anual}})^{1/12} - 1
        $$

    
    - El resultado muestra tanto el **ahorro total** (suma de aportes) como la **ganancia por intereses**, y el total acumulado después de aplicar el interés compuesto.
    """)




# Expander para la calculadora de Amortización
with st.expander("💸 Calculadora de Amortización"):
    st.markdown("""
    ## Fórmulas Utilizadas:
    - **Cuota fija (sistema francés)**:
    $$
    C = P \\times \\frac{r(1 + r)^n}{(1 + r)^n - 1}
    $$

    donde:
    - $ C $ es la cuota mensual.
    - $ P $ es el monto del préstamo.
    - $ r $ es la tasa de interés mensual.
    - $ n $ es el número total de pagos.

    ### Proceso:
    1. **Entrada de Datos**: El usuario ingresa los siguientes parámetros:
        - **Monto del préstamo**: El valor total que se pide prestado.
        - **Tasa de interés anual (E.A.)**: La tasa de interés anual en porcentaje.
        - **Plazo**: El número total de meses para pagar el préstamo.
        - **Cuotas adicionales**: Costos como cuota de manejo, seguro mensual y otros cargos.

    2. **Cálculo de la cuota base**: Usamos la fórmula del sistema francés para calcular la cuota mensual fija:

    $$ 
    C = P \\times \\frac{r(1 + r)^n}{(1 + r)^n - 1} 
    $$

    Donde:
    - $ r $ es la tasa de interés mensual, derivada de la tasa de interés anual:
    $$
    r_{\\text{mensual}} = \left( 1 + \\frac{r_{\\text{anual}}}{100} \\right)^{\\frac{1}{12}} - 1
    $$
    3. **Cálculo de la cuota total**: Se suman los costos adicionales como cuota de manejo, seguro y otros cobros a la cuota base para obtener la cuota total mensual a pagar.

    4. **Cálculo de la tasa efectiva anual equivalente**: Si hay costos adicionales, se calcula la tasa efectiva anual que refleja el impacto de esos costos adicionales sobre el préstamo.

    5. **Generación de la tabla de amortización**: Se genera una tabla que muestra:
        - El **mes**.
        - La **cuota mensual** (con costos adicionales si existen).
        - Los **intereses** pagados.
        - El **capital pagado**.
        - El **saldo pendiente** después de cada pago.

    6. **Visualización Gráfica**: Se genera un gráfico de barras apiladas para visualizar la distribución de la cuota mensual entre **capital pagado**, **intereses** y **costos adicionales**.

    7. **Descarga en Excel**: El usuario puede descargar la tabla de amortización en formato Excel para su análisis.

    ### Consideraciones:
    - La **tasa de interés** proporcionada es anual y se convierte a **mensual** para los cálculos.
    - Si se ingresan costos adicionales como cuota de manejo, seguro y otros, estos se suman a la cuota base, lo que afecta el monto total que el usuario deberá pagar.
    - La **tasa efectiva anual equivalente** tiene en cuenta estos costos adicionales y puede ser útil para comparar el préstamo con otros productos financieros.
    """)
