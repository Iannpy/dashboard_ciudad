import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


st.set_page_config(
    page_title="Dashboard ANATO VIVE BAQ",
    layout="wide",
    theme="light"
)

# -----------------------------
# DATA
# -----------------------------
hoy = datetime.now().date()
fechas = [hoy - timedelta(days=2), hoy - timedelta(days=1), hoy]
horas = list(range(8, 18))

rows = []
for fecha in fechas:
    for hora in horas:
        rows.append({
            "fecha": fecha,
            "hora": f"{hora:02d}:00"
        })

df = pd.DataFrame(rows)
n = len(df)

def distribuir(total, n):
    base = total // n
    resto = total % n
    return [base + 1 if i < resto else base for i in range(n)]

df["agencias_conectadas"] = distribuir(69, n)
df["agencias_nacionales"] = distribuir(63, n)
df["agencias_internacionales"] = distribuir(4, n)
df["organismos_internacionales"] = distribuir(4, n)

df["total_visitantes"] = (
    df["agencias_conectadas"]
    + df["agencias_nacionales"]
    + df["agencias_internacionales"]
    + df["organismos_internacionales"]
)

# -----------------------------
# HEADER
# -----------------------------
st.image("assets/AB2026_ANATO_LETRERO_3,80x0,70mts.svg", width=720)
st.divider()
st.title("📊 Dashboard de Visitantes – ANATO Vive BAQ")

# -----------------------------
# KPIs
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("👥 Total visitantes", int(df["total_visitantes"].sum()))
col2.metric("🏢 Agencias conectadas", int(df["agencias_conectadas"].sum()))
col3.metric("🇨🇴 Agencias nacionales", int(df["agencias_nacionales"].sum()))
col4.metric("🌍 Agencias internacionales", int(df["agencias_internacionales"].sum()))

st.divider()

# -----------------------------
# VISITANTES POR HORA (TOTAL)
# -----------------------------
st.subheader("⏰ Visitantes por hora (total)")

visitas_hora = df.groupby("hora")["total_visitantes"].sum().reset_index()

st.line_chart(
    visitas_hora,
    x="hora",
    y="total_visitantes",
    use_container_width=True
)

# -----------------------------
# COMPARACIÓN POR DÍA
# -----------------------------
st.subheader("📅 Visitantes por día")

visitas_dia = df.groupby("fecha")["total_visitantes"].sum().reset_index()

st.bar_chart(
    visitas_dia,
    x="fecha",
    y="total_visitantes",
    use_container_width=True
)


    #diagrama de torta+
    