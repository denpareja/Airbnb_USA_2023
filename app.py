import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Airbnb Explorer", page_icon="🏠", layout="wide")

@st.cache_data(show_spinner=False)
def load_data(path: str) -> pd.DataFrame:
    # encoding 'latin1' por si hay caracteres especiales en columnas/valores
    df = pd.read_csv(path, encoding="latin1", low_memory=False)
    # Normalizaciones mínimas
    # Ocupación aproximada = 1 - disponibilidad/365
    if "availability_365" in df.columns:
        df["occupancy_rate"] = 1 - (df["availability_365"].astype("float32") / 365.0)
        df["occupancy_rate"] = df["occupancy_rate"].clip(0, 1)
    else:
        df["occupancy_rate"] = np.nan

    # Asegurar tipos numéricos clave
    for col in ["price", "number_of_reviews", "reviews_per_month", "latitude", "longitude"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Algunas columnas opcionales pueden no existir según dataset
    for col in ["city", "neighbourhood", "room_type"]:
        if col not in df.columns:
            df[col] = "Unknown"

    # Limpieza básica de coordenadas
    if "latitude" in df.columns and "longitude" in df.columns:
        df = df.dropna(subset=["latitude", "longitude"])
        df = df[(df["latitude"].between(-90, 90)) & (df["longitude"].between(-180, 180))]

    return df

df = load_data("airbnb_data_2023.csv")

st.title("🏠 Airbnb Explorer")
st.caption("Análisis rápido por ciudad: precios, reviews vs. ocupación y mapa de calor (Plotly).")

# -----------------------------
# Sidebar de filtros
# -----------------------------
with st.sidebar:
    st.header("Filtros")

    # Ciudad
    cities = df["city"].dropna().sort_values().unique().tolist()
    city = st.selectbox("Ciudad", options=cities, index=0)

    df_city = df[df["city"] == city].copy()
    if df_city.empty:
        st.warning("No hay datos para la ciudad seleccionada.")
        st.stop()

    # Rango de precios — usar percentiles para evitar outliers extremos
    p1, p99 = np.nanpercentile(df_city["price"], [1, 99])
    price_min, price_max = st.slider(
        "Precio por noche (USD)",
        min_value=int(max(0, p1)),
        max_value=int(max(p1, p99)),
        value=(int(max(0, p1)), int(max(p1, p99))),
        step=1,
    )

    # Room type
    room_types = df_city["room_type"].dropna().unique().tolist()
    selected_rooms = st.multiselect("Tipo de habitación", options=room_types, default=room_types)

    # Neighbourhood (mostrar solo los más frecuentes para no saturar)
    top_neigh = (
        df_city["neighbourhood"].value_counts()
        .head(50)
        .index.tolist()
    )
    neigh_opt = ["(Todos)"] + top_neigh
    neighbourhood = st.selectbox("Barrio (Top 50 por cantidad)", neigh_opt, index=0)

# Aplicar filtros
mask = (
    df_city["price"].between(price_min, price_max)
    & df_city["room_type"].isin(selected_rooms)
)
if neighbourhood != "(Todos)":
    mask &= (df_city["neighbourhood"] == neighbourhood)
dff = df_city[mask].copy()

# -----------------------------
# KPIs
# -----------------------------
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Listados", f"{len(dff):,}")
with col2:
    st.metric("Precio mediano", f"${np.nanmedian(dff['price']):,.0f}")
with col3:
    rpm = np.nanmean(dff["reviews_per_month"]) if "reviews_per_month" in dff.columns else np.nan
    st.metric("Reviews/mes (prom.)", f"{rpm:,.2f}" if not np.isnan(rpm) else "n/d")
with col4:
    occ = np.nanmean(dff["occupancy_rate"]) if "occupancy_rate" in dff.columns else np.nan
    st.metric("Ocupación aprox. (prom.)", f"{100*occ:,.0f}%" if not np.isnan(occ) else "n/d")

st.divider()

# -----------------------------
# Vista previa y tabla filtrada (opcional)
# -----------------------------
st.subheader("Vista previa y filtros")
st.write(f"**Ciudad:** {city} | **Rango de precio:** ${price_min}–${price_max} | **Tipo:** {', '.join(selected_rooms)}")
if neighbourhood != "(Todos)":
    st.write(f"**Barrio:** {neighbourhood}")

with st.expander("Ver tabla filtrada"):
    st.dataframe(
        dff[
            [
                c for c in ["id", "name", "neighbourhood", "room_type", "price",
                            "number_of_reviews", "reviews_per_month",
                            "availability_365", "occupancy_rate", "latitude", "longitude"]
                if c in dff.columns
            ]
        ].reset_index(drop=True),
        use_container_width=True,
    )

# -----------------------------
# Distribución de precios por barrio
# -----------------------------
st.subheader("Distribución de precios por barrio (Top 15 por cantidad)")
top15 = dff["neighbourhood"].value_counts().head(15).index.tolist()
dff_top = dff[dff["neighbourhood"].isin(top15)].copy()

if not dff_top.empty:
    fig_box = px.box(
        dff_top,
        x="neighbourhood",
        y="price",
        points="suspectedoutliers",
        title="Precio por noche (USD) – Boxplot",
    )
    fig_box.update_layout(xaxis_title="Barrio", yaxis_title="Precio (USD)", showlegend=False)
    st.plotly_chart(fig_box, use_container_width=True)
else:
    st.info("No hay suficientes datos para mostrar el boxplot por barrio.")

# -----------------------------
# Reviews vs Ocupación
# -----------------------------
st.subheader("Relación: número de reviews vs. ocupación")
if "number_of_reviews" in dff.columns and "occupancy_rate" in dff.columns:
    fig_scatter = px.scatter(
        dff,
        x="number_of_reviews",
        y="occupancy_rate",
        color="room_type" if "room_type" in dff.columns else None,
        hover_data=[c for c in ["name", "neighbourhood", "price"] if c in dff.columns],
        title="Reviews totales vs. tasa de ocupación (aprox.)",
        labels={"occupancy_rate": "Ocupación (0–1)"},
        opacity=0.7,
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
else:
    st.info("Faltan columnas para este gráfico (number_of_reviews u occupancy_rate).")

# -----------------------------
# Mapa de calor (densidad)
# -----------------------------
st.subheader("Mapa de calor de oferta (densidad de listados)")
if {"latitude", "longitude"}.issubset(dff.columns) and not dff.empty:
    # Usamos density_mapbox con estilos públicos (no requiere token)
    # Si el dataset es muy grande, muestrear para rendimiento
    sample = dff.sample(n=min(5000, len(dff)), random_state=42) if len(dff) > 5000 else dff

    # Centro aproximado
    center_lat = float(sample["latitude"].mean())
    center_lon = float(sample["longitude"].mean())

    fig_map = px.density_mapbox(
        sample,
        lat="latitude",
        lon="longitude",
        radius=12,
        center=dict(lat=center_lat, lon=center_lon),
        zoom=10,
        height=600,
        title=f"Densidad de listados en {city}",
    )
    fig_map.update_layout(mapbox_style="carto-positron", margin=dict(l=0, r=0, t=50, b=0))
    st.plotly_chart(fig_map, use_container_width=True)
else:
    st.info("No hay coordenadas válidas para dibujar el mapa.")

st.caption("Ocupación estimada como 1 - availability_365/365; solo orientativa.")