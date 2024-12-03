import streamlit as st
import pandas as pd
import altair as alt

# Cargar los datos
@st.cache_data
def load_data():
    file_path = 'datos_limpios.csv'
    return pd.read_csv(file_path)

data = load_data()

st.title("Exploración de Datos Interactiva")

# Gráfico interactivo de distribución de precios
st.subheader("Distribución de Precios")
hist_chart = alt.Chart(data).mark_bar().encode(
    alt.X('precio:Q', bin=alt.Bin(maxbins=30), title='Precio'),
    alt.Y('count()', title='Frecuencia')
).properties(title="Distribución de Precios")
st.altair_chart(hist_chart, use_container_width=True)

# Gráfico interactivo de marcas más populares
st.subheader("Marcas Más Populares")
top_brands = data['marca'].value_counts().head(10)
top_brands_df = top_brands.reset_index()
top_brands_df.columns = ['Marca', 'Cantidad']
bar_chart = alt.Chart(top_brands_df).mark_bar().encode(
    x=alt.X('Marca:N', sort='-y', title='Marca'),
    y=alt.Y('Cantidad:Q', title='Cantidad de Productos'),
    tooltip=['Marca', 'Cantidad']
).properties(title="Marcas Más Populares")
st.altair_chart(bar_chart, use_container_width=True)

# Gráfico interactivo de precios por tipo de producto
st.subheader("Precios por Tipo de Producto")
top_types = data['tipo'].value_counts().head(10).index
filtered_data = data[data['tipo'].isin(top_types)]
box_chart = alt.Chart(filtered_data).mark_boxplot().encode(
    x=alt.X('precio:Q', title='Precio'),
    y=alt.Y('tipo:N', title='Tipo de Producto'),
    tooltip=['precio', 'tipo']
).properties(title="Precios por Tipo de Producto")
st.altair_chart(box_chart, use_container_width=True)
