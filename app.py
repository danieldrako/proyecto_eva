import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Cargar los datos
@st.cache_data
def load_data():
    file_path = 'datos_limpios.csv'  # Cambia a la ruta correcta
    return pd.read_csv(file_path, engine='python')

data = load_data()

# Título de la aplicación
st.title("Exploración de Datos de Productos")

# Visualización de la tabla de datos
st.subheader("Vista previa de los datos")
st.write(data.head())

# Gráfica de distribución de precios
st.subheader("Distribución de Precios")
fig, ax = plt.subplots()
sns.histplot(data=data, x='precio', bins=30, kde=True, color='skyblue', ax=ax)
ax.set_title('Distribución de Precios')
ax.set_xlabel('Precio')
ax.set_ylabel('Frecuencia')
st.pyplot(fig)

# Gráfica de marcas más populares
st.subheader("Marcas Más Populares")
top_brands = data['marca'].value_counts().head(10)
fig, ax = plt.subplots()
sns.barplot(x=top_brands.values, y=top_brands.index, palette='coolwarm', ax=ax)
ax.set_title('Marcas Más Populares (Top 10)')
ax.set_xlabel('Cantidad de Productos')
ax.set_ylabel('Marca')
st.pyplot(fig)

# Comparación de precios por tipo de producto
st.subheader("Comparación de Precios por Tipo de Producto")
top_types = data['tipo'].value_counts().head(10).index
filtered_data = data[data['tipo'].isin(top_types)]
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=filtered_data, x='precio', y='tipo', palette='Set2', ax=ax)
ax.set_title('Comparación de Precios por Tipo de Producto')
ax.set_xlabel('Precio')
ax.set_ylabel('Tipo de Producto')
st.pyplot(fig)
