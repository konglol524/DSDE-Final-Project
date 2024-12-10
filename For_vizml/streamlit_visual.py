import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# File paths for HTML dashboards
path_to_html_heatmap = "heat_map.html"
path_to_html_geo = "city_collaboration_map.html"
path_to_html_network = "city_collaboration_network.html"

# Load HTML content
with open(path_to_html_heatmap, 'r', encoding='utf-8') as f:
    html_data_heatmap = f.read()

with open(path_to_html_geo, 'r', encoding='utf-8') as f:
    html_data_geo = f.read()

with open(path_to_html_network, 'r', encoding='utf-8') as f:
    html_data_network = f.read()

# Load data
@st.cache_data
def load_data():
    cocity_df = pd.read_csv('cocity.csv')
    city_df = pd.read_csv('city.csv')
    centrality_df = pd.read_csv('centrality_metrics.csv')
    return cocity_df, city_df, centrality_df

cocity_df, city_df, centrality_df = load_data()

# Title and description
st.title("City Collaboration and Citation Analysis")
st.markdown("Explore city collaborations, citations, and publications through visualizations and analytics.")

# Key metrics
total_cities = city_df['city_id'].nunique()
total_collaborations = cocity_df['colab_count'].sum()
total_citations = city_df['citation_sum'].sum()

st.header("Key Metrics")
st.metric("Total Cities", total_cities)
st.metric("Total Collaborations", total_collaborations)
st.metric("Total Citations", total_citations)

# Display centrality metrics
st.header("Centrality Metrics")
st.dataframe(centrality_df)

# Streamlit layout
st.title("Interactive Dashboards")
st.markdown("Explore the interactive visualizations below to gain insights into different datasets.")

# Heatmap Section
st.subheader("1. Heatmap Visualization")
st.markdown("This heatmap provides a comprehensive view of data density and patterns across various dimensions.")
st.components.v1.html(html_data_heatmap, scrolling=True, height=500)

# Geographical Map Section
st.subheader("2. Global Academic Collaboration Map")
st.markdown("The geographical map highlights collaborations between cities. Curved lines show collaborations, with thickness based on volume and color representing connected continents.")
st.components.v1.html(html_data_geo, scrolling=True, height=500)

# Network Graph Section
st.subheader("3. City Collaboration Network with Clusters")
st.markdown("This network highlights collaboration clusters and relationships, offering insights into regional and global academic partnerships.")
st.components.v1.html(html_data_network, height=500)