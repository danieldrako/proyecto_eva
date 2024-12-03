import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.io import output_notebook

# Cargar los datos
@st.cache_data
def load_data():
    file_path = 'datos_limpios.csv'
    return pd.read_csv(file_path)

data = load_data()

st.title("Exploración de Datos Interactiva")

# Gráfico interactivo de marcas más populares
st.subheader("Marcas Más Populares")
top_brands = data['marca'].value_counts().head(10)
source = ColumnDataSource(data=dict(marcas=top_brands.index, cantidad=top_brands.values))

p = figure(x_range=top_brands.index.tolist(), title="Marcas Más Populares",
           toolbar_location=None, tools="")
p.vbar(x='marcas', top='cantidad', width=0.9, source=source)
p.xgrid.grid_line_color = None
p.y_range.start = 0

st.bokeh_chart(p, use_container_width=True)
