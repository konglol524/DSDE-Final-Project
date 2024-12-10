import streamlit as st
import pandas as pd

# Load HTML content
@st.cache_data
def load_html_content():
    with open("heat_map.html", "r", encoding="utf-8") as f:
        html_data_heatmap = f.read()

    with open("city_collaboration_map.html", "r", encoding="utf-8") as f:
        html_data_geo = f.read()

    with open("city_collaboration_network.html", "r", encoding="utf-8") as f:
        html_data_network = f.read()

    return html_data_heatmap, html_data_geo, html_data_network


# Load data
@st.cache_data
def load_data():
    cocity_df = pd.read_csv("cocity.csv")
    city_df = pd.read_csv("city.csv")
    centrality_df = pd.read_csv("centrality_metrics.csv")
    return cocity_df, city_df, centrality_df


# App configuration
st.set_page_config(
    page_title="City Collaboration Analysis", page_icon="🌐", layout="wide"
)

# Load data and HTML content
cocity_df, city_df, centrality_df = load_data()
html_data_heatmap, html_data_geo, html_data_network = load_html_content()

# Calculate key metrics
total_cities = city_df["city_id"].nunique()
total_collaborations = cocity_df["colab_count"].sum()
total_citations = city_df["citation_sum"].sum()

st.markdown(
    """
    <style>
        /* Global font styling */
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

        body, .stApp {
            font-family: 'Roboto', sans-serif;
            background-color: #1e1e2f; /* Dark background */
            color: #ffffff; /* Make all text white */
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #33334d; /* Dark sidebar */
            color: #ffffff; /* Sidebar text color */
        }

        /* Adjust sidebar text */
        [data-testid="stSidebar"] .css-1v3fvcr {
            color: #ffffff; /* Make all sidebar text white */
        }

        /* Header and title styling */
        h1, h2, h3, h4 {
            font-family: 'Roboto', sans-serif;
            font-weight: 700;
            color: #ffdd57; /* Accent color for headings */
        }

        /* Top bar (default Streamlit header) */
        .css-18ni7ap.e8zbici0 {
            background-color: #33334d !important; /* Dark top bar */
            color: #ffffff !important; /* White text for the bar */
        }

        /* Metric text */
        .stMetric label {
            font-weight: 400;
            font-size: 16px;
            color: #ffffff; /* Ensure metric text is white */
        }
        
        /* Regular text and paragraphs */
        p, div {
            font-family: 'Roboto', sans-serif;
            font-weight: 400;
            color: #ffffff; /* Ensure all general text is white */
        }

        /* Dropdowns, buttons, and inputs */
        .css-1e5imcs, .css-1cpxqw2 {
            background-color: #444466 !important; /* Dark background for inputs */
            color: #ffffff !important; /* White text for inputs */
            border: 1px solid #8888aa !important; /* Light border */
        }

        /* Dataframe font */
        .dataframe-container {
            font-family: 'Roboto', sans-serif;
            font-size: 14px;
            color: #ffffff; /* White text in dataframes */
            background-color: #28283e; /* Dark background for dataframes */
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Navigation
def nav_page(page_name):
    """Helper function to manage page navigation"""
    js = f"""
    <script>
        var frames = window.parent.document.querySelectorAll('iframe');
        var navButtons = window.parent.document.querySelectorAll('[data-testid="stSidebarNav"] ul li a');
        for (var i = 0; i < navButtons.length; i++) {{
            if (navButtons[i].text.includes('{page_name}')) {{
                navButtons[i].click();
                break;
            }}
        }}
    </script>
    """
    st.components.v1.html(js)


# Pages
def overview_page():
    st.title("🌍 Global Academic Collaboration Dashboard")
    st.markdown(
        """
        Welcome to the City Collaboration Analysis Dashboard! This platform highlights academic collaboration patterns and metrics across cities worldwide. Delve into the data to uncover global research trends.
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Cities", total_cities)

    with col2:
        st.metric("Total Collaborations", total_collaborations)

    with col3:
        st.metric("Total Citations", total_citations)

    st.subheader("Quick Insights")
    st.markdown(
        """
    - **Diverse Dataset**: Collaborations span continents and institutions.
    - **Impact**: Reflects inter-geographical and cross-disciplinary research dynamics.
    """
    )


def visualizations_page():
    st.title("🗺️ Interactive Visualizations")
    st.subheader("1. Heatmap: Data Density Visualization")
    st.components.v1.html(html_data_heatmap, scrolling=True, height=500)

    st.subheader("2. Global Academic Collaboration Map")
    st.components.v1.html(html_data_geo, scrolling=True, height=500)

    st.subheader("3. City Collaboration Network")
    st.components.v1.html(html_data_network, height=500)


def analytics_page():
    st.title("📊 Detailed Analytics")
    st.subheader("City Centrality Metrics")
    st.dataframe(centrality_df)

    st.subheader("Explore Collaboration Data")
    selected_city_id = st.selectbox("Select a City", options=city_df["city_id"].unique())
    city_data = city_df[city_df["city_id"] == selected_city_id]
    cocity_data = cocity_df[
        (cocity_df["city_id1"] == selected_city_id)
        | (cocity_df["city_id2"] == selected_city_id)
    ]

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Citations", city_data["citation_sum"].values[0])

    with col2:
        st.metric("Collaboration Count", len(cocity_data))

    st.write(f"Collaboration Details for City ID {selected_city_id}:")
    st.dataframe(cocity_data)


# Main app logic
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Overview", "Visualizations", "Analytics"])
    if page == "Overview":
        overview_page()
    elif page == "Visualizations":
        visualizations_page()
    elif page == "Analytics":
        analytics_page()


if __name__ == "__main__":
    main()
