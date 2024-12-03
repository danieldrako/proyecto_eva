import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar los datos
@st.cache_data
def load_data():
    file_path = 'datos_limpios.csv'  # Asegúrate de que el archivo esté en la ruta correcta
    return pd.read_csv(file_path)

data = load_data()

# Título de la aplicación
st.title("Exploración de Datos Interactiva con Filtros Avanzados")

# Vista previa de los datos
st.subheader("Vista Previa de los Datos")
st.dataframe(data.head())

# Filtros interactivos
st.sidebar.header("Filtros")
selected_brands = st.sidebar.multiselect(
    "Selecciona Marcas", 
    options=data["marca"].unique(), 
    default=data["marca"].unique()
)

selected_types = st.sidebar.multiselect(
    "Selecciona Tipos de Productos", 
    options=data["tipo"].unique(), 
    default=data["tipo"].unique()
)

price_range = st.sidebar.slider(
    "Rango de Precios", 
    min_value=int(data["precio"].min()), 
    max_value=int(data["precio"].max()), 
    value=(int(data["precio"].min()), int(data["precio"].max()))
)

keyword = st.sidebar.text_input(
    "Busca por palabra clave en las descripciones", 
    value=""
)

# Aplicar los filtros al dataset
filtered_data = data[
    (data["marca"].isin(selected_brands)) &
    (data["tipo"].isin(selected_types)) &
    (data["precio"] >= price_range[0]) &
    (data["precio"] <= price_range[1])
]

if keyword:
    filtered_data = filtered_data[filtered_data["descripcion"].str.contains(keyword, case=False, na=False)]

# Mostrar los datos filtrados
st.subheader("Datos Filtrados")
st.write(f"Total de registros filtrados: {len(filtered_data)}")
st.dataframe(filtered_data)

# Gráfico interactivo: Distribución de precios
st.subheader("Distribución de Precios")
fig_price = px.histogram(filtered_data, x="precio", nbins=30, 
                         title="Distribución de Precios (Filtrada)", 
                         template="plotly_white")
st.plotly_chart(fig_price)

# Gráfico interactivo: Marcas más populares
st.subheader("Marcas Más Populares")
top_brands = filtered_data['marca'].value_counts().head(10)
top_brands_df = top_brands.reset_index()
top_brands_df.columns = ['Marca', 'Cantidad']
fig_brands = px.bar(top_brands_df, x='Marca', y='Cantidad', 
                    title='Marcas Más Populares (Filtradas)', 
                    template="plotly_white")
st.plotly_chart(fig_brands)

# Gráfico interactivo: Comparación de precios por tipo de producto
st.subheader("Precios por Tipo de Producto")
fig_types = px.box(filtered_data, x="precio", y="tipo", 
                   title="Precios por Tipo de Producto (Filtrados)", 
                   template="plotly_white",
                   #template="plotly_dark",  # Tema oscuro
                    color="tipo",  # Asignar colores únicos por tipo
                    color_discrete_sequence=px.colors.qualitative.Set3  # Paleta de colores variada
)

st.plotly_chart(fig_types)

# Gráfico adicional: Relación entre precio y marcas
st.subheader("Relación entre Precios y Marcas")
fig_relation = px.scatter(filtered_data, x="marca", y="precio", 
                           title="Relación entre Precios y Marcas (Filtradas)", 
                           template="plotly_white")
st.plotly_chart(fig_relation)

# Gráfico adicional: Correlaciones entre atributos técnicos y precio
st.subheader("Correlaciones entre Atributos Técnicos y Precio")
if "watts" in data.columns and "GB" in data.columns:
    fig_corr = px.scatter(filtered_data, x="watts", y="precio", 
                           title="Relación entre Watts y Precio", 
                           template="plotly_white")
    st.plotly_chart(fig_corr)

    fig_corr_gb = px.scatter(filtered_data, x="GB", y="precio", 
                              title="Relación entre Capacidad (GB) y Precio", 
                              template="plotly_white")
    st.plotly_chart(fig_corr_gb)
else:
    st.write("No se encontraron atributos técnicos como 'watts' o 'GB' en los datos.")


# Filtrar los datos según el top 10 tipos
top_types = data["tipo"].value_counts().head(10).index
filtered_data = data[data["tipo"].isin(top_types)]

# Comparación de precios por tipo de producto con colores personalizados
st.subheader("Precios por Tipo de Producto (Filtrados)")

# Personalización de colores
fig_types = px.box(
    filtered_data, 
    x="precio", 
    y="tipo", 
    title="Precios por Tipo de Producto (Filtrados)",
    template="plotly_dark",  # Tema oscuro
    color="tipo",  # Asignar colores únicos por tipo
    color_discrete_sequence=px.colors.qualitative.Set3  # Paleta de colores variada
)
fig_types.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",  # Fondo negro
    paper_bgcolor="rgba(0,0,0,0)",  # Fondo del gráfico negro
    font=dict(color="white"),  # Texto blanco
    xaxis=dict(
        showline=True,  # Mostrar línea del eje X
        linecolor="white",  # Color de la línea del eje X
        showgrid=True,  # Mostrar líneas de la cuadrícula
        gridcolor="gray",  # Color de la cuadrícula
        tickcolor="white",  # Color de las etiquetas del eje X
        tickfont=dict(color="white"),  # Color del texto de las etiquetas
    ),
    yaxis=dict(
        showline=True,  # Mostrar línea del eje Y
        linecolor="white",  # Color de la línea del eje Y
        showgrid=False,  # Ocultar líneas de la cuadrícula
        tickcolor="white",  # Color de las etiquetas del eje Y
        tickfont=dict(color="white"),  # Color del texto de las etiquetas
        ticks="outside"  # Mostrar etiquetas hacia afuera del eje
    )
)
st.plotly_chart(fig_types)

