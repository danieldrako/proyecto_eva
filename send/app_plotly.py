import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Cargar los datos
@st.cache_data  
def load_data():
    file_path = 'datos_limpios.csv'  
    return pd.read_csv(file_path)  

data = load_data()  


st.title("Exploración de Datos Interactiva con Filtros Avanzados")  


st.subheader("Vista Previa de los Datos")  
st.dataframe(data.head())  


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


filtered_data = data[  
    (data["marca"].isin(selected_brands)) &  
    (data["tipo"].isin(selected_types)) &  
    (data["precio"] >= price_range[0]) &  
    (data["precio"] <= price_range[1])  
]


if keyword:  
    filtered_data = filtered_data[filtered_data["descripcion"].str.contains(keyword, case=False, na=False)]  
    


st.subheader("Datos Filtrados")  
st.write(f"Total de registros filtrados: {len(filtered_data)}")  
st.dataframe(filtered_data)  


# 1. Distribución de precios
st.subheader("Distribución de Precios")
data["precio"] = pd.to_numeric(data["precio"], errors='coerce')
precios = data["precio"].dropna()
fig1 = px.histogram(precios, nbins=15, title="Distribución de Precios", labels={'value': 'Precio', 'count': 'Frecuencia'})
st.plotly_chart(fig1)
st.write("""
- **Descripción**: Este histograma muestra cómo se distribuyen los precios en el dataset.
- **Objetivo**: Identificar rangos de precios más comunes y detectar posibles valores atípicos.
- **Uso**: Analizar tendencias de precios y ajustar estrategias de precios o inventario.
""")

# 2. Productos por marca
st.subheader("Productos por Marca")
fig2 = px.bar(data['marca'].value_counts().reset_index(), x='index', y='marca',
              title="Productos por Marca", labels={'index': 'Marca', 'marca': 'Cantidad de Productos'},
              color_discrete_sequence=px.colors.qualitative.Dark2 )
st.plotly_chart(fig2)
st.write("""
- **Descripción**: Visualiza la cantidad de productos ofrecidos por cada marca.
- **Objetivo**: Identificar qué marcas tienen mayor representación en el inventario.
- **Uso**: Ayuda a decidir qué marcas priorizar en términos de marketing o adquisiciones.
""")

# 3. Nube de palabras en descripciones
st.subheader("Nube de Palabras en Descripciones")
text = ' '.join(data['descripcion'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate(text)
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Nube de Palabras en Descripciones')
st.pyplot(plt)
st.write("""
- **Descripción**: Identifica las palabras más frecuentes en las descripciones de los productos.
- **Objetivo**: Detectar patrones en las características y descripciones comunes.
- **Uso**: Utilizar las palabras clave para optimizar la estrategia de SEO y campañas publicitarias.
""")

# 4. Comparativa por tipo de producto - Gráfico circular
st.subheader("Proporción por Tipo de Producto")
top_types = data['tipo'].value_counts().head(10)
fig4 = px.pie(top_types, values=top_types.values, names=top_types.index, title="Proporción por Tipo de Producto")
st.plotly_chart(fig4)
st.write("""
- **Descripción**: Este gráfico circular muestra la proporción de los tipos de productos más comunes.
- **Objetivo**: Visualizar cómo se distribuyen los productos entre las principales categorías.
- **Uso**: Ayuda a comprender las preferencias de los clientes y ajustar el enfoque de inventario.
""")

# 5. Comparativa de precios por tipo de producto - Boxplot
st.subheader("Distribución de Precios por Tipo de Producto")
fig5 = px.box(data, x='tipo', y='precio', color='tipo', title="Distribución de Precios por Tipo de Producto")
st.plotly_chart(fig5)
st.write("""
- **Descripción**: Compara la variación de precios dentro de cada tipo de producto.
- **Objetivo**: Detectar rangos de precios comunes y categorías con mayor dispersión de precios.
- **Uso**: Identificar oportunidades para ajustar precios según el tipo de producto.
""")

# 6. Relación entre precio y watts
st.subheader("Relación entre Precio y Potencia (Watts)")
data["watts"] = pd.to_numeric(data["watts"], errors='coerce')
fig6 = px.scatter(data.dropna(subset=['watts']), x='watts', y='precio', color='marca', title="Relación entre Precio y Potencia (Watts)")
st.plotly_chart(fig6)
st.write("""
- **Descripción**: Muestra cómo se relacionan la potencia (en watts) y el precio de los productos.
- **Objetivo**: Identificar si hay correlaciones significativas entre estas dos variables.
- **Uso**: Ayuda a analizar el impacto de la potencia en el costo de los productos.
""")

# 7. Relación entre precio y capacidad (GB)
st.subheader("Relación entre Precio y Capacidad (GB)")
data["GB"] = pd.to_numeric(data["GB"], errors='coerce')
fig7 = px.scatter(data.dropna(subset=['GB']), x='GB', y='precio', color='marca', title="Relación entre Precio y Capacidad (GB)")
st.plotly_chart(fig7)
st.write("""
- **Descripción**: Explora la relación entre la capacidad de almacenamiento (GB) y el precio.
- **Objetivo**: Determinar cómo la capacidad afecta el costo de los productos.
- **Uso**: Útil para evaluar tendencias en dispositivos con diferentes capacidades.
""")

# 8. Marcas Más Populares
st.subheader("Marcas Más Populares (Top 10)")
top_brands = data['marca'].value_counts().head(10)  
fig8 = px.bar(
    top_brands.reset_index(),  
    x='index',  
    y='marca',  
    title="Marcas Más Populares (Top 10)",  
    labels={'index': 'Marca', 'marca': 'Cantidad de Productos'},  
    text=top_brands.values,  
    color_discrete_sequence=px.colors.qualitative.Alphabet  
)
fig8.update_traces(textposition='outside')  
st.plotly_chart(fig8)  
st.write("""
- **Descripción**: Presenta las 10 marcas con mayor número de productos en el inventario.
- **Objetivo**: Identificar marcas líderes y su representación en los datos.
- **Uso**: Ayuda a planificar promociones o evaluar relaciones con proveedores.
""")

# 9. Precios Promedio por Marca
st.subheader("Precios Promedio por Marca (Top 10)")
avg_price = data.groupby('marca')['precio'].mean().sort_values(ascending=False).head(10)
fig9 = px.bar(avg_price.reset_index(), x='marca', y='precio', title="Precios Promedio por Marca (Top 10)",
              labels={'marca': 'Marca', 'precio': 'Precio Promedio'},
              color_discrete_sequence=px.colors.qualitative.Vivid )
st.plotly_chart(fig9)
st.write("""
- **Descripción**: Muestra las marcas con los precios promedio más altos.
- **Objetivo**: Identificar marcas premium con productos de mayor valor.
- **Uso**: Útil para diferenciar productos según su posicionamiento de precio.
""")

# 10. Productos por Tipo
st.subheader("Productos por Tipo (Top 10)")
fig10 = px.bar(top_types.reset_index(), x='index', y='tipo', title="Productos por Tipo (Top 10)",
               labels={'index': 'Tipo de Producto', 'tipo': 'Cantidad'},
              color_discrete_sequence=px.colors.qualitative.Pastel1 )
st.plotly_chart(fig10)
st.write("""
- **Descripción**: Visualiza las 10 categorías de productos más comunes.
- **Objetivo**: Comprender la composición del inventario.
- **Uso**: Ayuda a priorizar esfuerzos en categorías más representativas.
""")

# 11. Comparación de Precios entre Tipos de Productos
st.subheader("Comparación de Precios entre Tipos de Productos (Top 10)")
filtered_data = data[data['tipo'].isin(top_types.index)]
fig11 = px.box(filtered_data, x='precio', y='tipo', title="Comparación de Precios por Tipo de Producto (Top 10)",
               color='tipo', points="all")
st.plotly_chart(fig11)
st.write("""
- **Descripción**: Compara la variación de precios en los 10 tipos de productos principales.
- **Objetivo**: Evaluar la dispersión de precios dentro de cada categoría.
- **Uso**: Ayuda a identificar oportunidades para ajustar precios o detectar categorías exclusivas.
""")

# 12. Gráfico circular de las marcas Top 10 por suma de precios
st.subheader("Proporción de Precios por Marca (Top 10)")
top_brands_prices = data.groupby('marca')['precio'].sum().sort_values(ascending=False).head(10)
fig12 = px.pie(
    top_brands_prices,  # Datos
    values=top_brands_prices.values,  
    names=top_brands_prices.index,  
    title="Proporción de Precios por Marca (Top 10)",  
    color_discrete_sequence=px.colors.qualitative.Light24  
)
st.plotly_chart(fig12)
st.write("""
- **Descripción**: Este gráfico circular muestra la proporción del precio total de los productos para las 10 marcas principales.
- **Objetivo**: Identificar qué marcas contribuyen más al total de ingresos estimados por precio.
- **Uso**: Ayuda a priorizar esfuerzos en marcas que generan un mayor valor económico.
""")