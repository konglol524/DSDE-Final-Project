import streamlit as st
import pandas as pd
from ml import preprocess_data, evaluate_features_with_stratified_sampling
import joblib


# Load HTML content
@st.cache_data
def load_html_content():
    with open("heat_map.html", "r", encoding="utf-8") as f:
        html_data_heatmap = f.read()


@st.cache_data
def load_html_content():
    with open("heat_map.html", "r", encoding="utf-8") as f:
        html_data_heatmap = f.read()

    with open("city_collaboration_map.html", "r", encoding="utf-8") as f:
        html_data_geo = f.read()
    with open("city_collaboration_map.html", "r", encoding="utf-8") as f:
        html_data_geo = f.read()

    with open("city_collaboration_network.html", "r", encoding="utf-8") as f:
        html_data_network = f.read()
    with open("city_collaboration_network.html", "r", encoding="utf-8") as f:
        html_data_network = f.read()
    with open("city_collaboration_network.html", "r", encoding="utf-8") as f:
        html_data_network = f.read()

    return html_data_heatmap, html_data_geo, html_data_network

    return html_data_heatmap, html_data_geo, html_data_network


# Load data
@st.cache_data
def load_data():
    papers_df = pd.read_csv("papers.csv")
    cocity_df = pd.read_csv("cocity.csv")
    city_df = pd.read_csv("city.csv")
    centrality_df = pd.read_csv("centrality_metrics.csv")
    cocity_df = pd.read_csv("cocity.csv")
    city_df = pd.read_csv("city.csv")
    centrality_df = pd.read_csv("centrality_metrics.csv")
    return cocity_df, city_df, centrality_df, papers_df


# App configuration
st.set_page_config(
    page_title="City Collaboration Analysis",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for modern look
st.markdown(
    """
    <style>
    /* Modern color scheme */
    :root {
        --primary-color: #4A90E2;
        --background-color: #F8F9FA;
        --secondary-color: #6C757D;
        --accent-color: #28A745;
    }
    
    /* Main content styling */
    .stApp {
        background-color: var(--background-color);
    }

    # Add this to your existing CSS within st.markdown()


    /* Existing CSS styles... */

    /* Hide Streamlit's default top menu 
    #MainMenu {visibility: hidden;}
    .stToolbar {display: none;}
    header {visibility: hidden;}
    /* Optional: Adjust the main content to fill the space */
    .main .block-container {
        padding-top: 1rem;
    }*/

 

    
    /* Card-like containers */
    div.css-1r6slb0.e1tzin5v2 {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Metrics styling */
    div[data-testid="metric-container"] {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #1E1E1E;
        font-weight: 600;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebarNav"] {
        background: linear-gradient(180deg, #2C3E50 0%, #3498DB 100%);
        padding-top: 2rem;
    }
    
    .stSidebar .sidebar-content {
        background-color: white;
    }
    
    /* Buttons and interactive elements */
    .stButton>button {
        background-color: var(--primary-color);
        color: white;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: var(--accent-color);
        transform: translateY(-2px);
    }
    
    /* DataFrames */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        border: none !important;
    }
    
    /* Selectbox */
    .stSelectbox {
        border-radius: 5px;
    }
    
    /* Cards for metrics */
    div.element-container:has(div[data-testid="metric-container"]) {
        background-color: white;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    div.element-container:has(div[data-testid="metric-container"]):hover {
        transform: translateY(-2px);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Load data and HTML content
cocity_df, city_df, centrality_df, papers_df = load_data()
html_data_heatmap, html_data_geo, html_data_network = load_html_content()

# Calculate key metrics
total_cities = city_df["city_id"].nunique()
total_papers = len(papers_df["pid"])
total_citations = papers_df["citedby_count"].sum()


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
    """Overview section with key metrics and summary"""
    st.title("🌍 Global Academic Collaboration Dashboard")
    st.markdown(
        """
        Explore intricate networks of academic collaborations across cities and continents. 
        Dive deep into visualization and analytics that reveal the interconnected world of research.
    """
    )

    col1, col2, col3 = st.columns(3)


    with col1:
        st.metric(
            "Total Cities", total_cities, help="Number of unique cities in the dataset"
        )

    with col2:
        st.metric(
            "Total Papers",
            total_papers,
            help="Total number of academic papers in the dataset",
        )

    with col3:
        st.metric(
            "Total Citations",
            int(total_citations),
            help="Cumulative citations across all cities",
        )

    # Additional context
    st.subheader("Quick Insights")
    # Quick Insights with modern styling
    st.markdown(
        """
        <div style='background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-top: 2rem;'>
            <h3 style='color: #1E1E1E; margin-bottom: 1rem;'>Quick Insights</h3>
            <ul style='list-style-type: none; padding-left: 0;'>
                <li style='margin-bottom: 0.5rem; padding-left: 1.5rem; position: relative;'>
                    <span style='color: #4A90E2; position: absolute; left: 0;'>▪</span>
                    Our dataset spans multiple continents and research domains
                </li>
                <li style='margin-bottom: 0.5rem; padding-left: 1.5rem; position: relative;'>
                    <span style='color: #4A90E2; position: absolute; left: 0;'>▪</span>
                    Collaborations represent cross-institutional and cross-geographical knowledge exchange
                </li>
                <li style='margin-bottom: 0.5rem; padding-left: 1.5rem; position: relative;'>
                    <span style='color: #4A90E2; position: absolute; left: 0;'>▪</span>
                    Metrics reflect the interconnected nature of global academic research
                </li>
            </ul>
        </div>
    """,
        unsafe_allow_html=True,
    )


def visualizations_page():
    """Interactive visualizations section"""
    st.title("🗺️ Interactive Visualizations")

    st.subheader("1. Heatmap: Data Density Visualization")
    st.markdown("Explore patterns and concentrations in academic data.")
    st.components.v1.html(html_data_heatmap, scrolling=True, height=500)

    st.subheader("2. Global Academic Collaboration Map")
    st.markdown(
        "Curved lines show inter-city collaborations, with line thickness representing collaboration volume."
    )
    st.components.v1.html(html_data_geo, scrolling=True, height=500)

    st.subheader("3. City Collaboration Network")
    st.markdown("Network graph highlighting collaborative clusters and relationships.")
    st.components.v1.html(html_data_network, height=500)


def analytics_page():
    """Detailed analytics and data exploration"""
    st.title("📊 Detailed Analytics")

    # Centrality metrics
    st.write("City Centrality Metrics:")
    st.dataframe(centrality_df, use_container_width=True)

    # Filtering and exploration
    st.subheader("Explore Collaboration Data")

    # City selection for detailed view
    selected_city = st.selectbox("Select a City", options=city_df["city"].unique())

    # Filter data for selected city
    city_data = city_df[city_df["city"] == selected_city]
    selected_city_id = city_data["city_id"].iloc[0]
    cocity_data = cocity_df[
        (cocity_df["city_id1"] == selected_city_id)
        | (cocity_df["city_id2"] == selected_city_id)
    ]

    # Create a mapping of city_id to city name
    city_id_to_name = dict(zip(city_df["city_id"], city_df["city"]))

    # Replace city IDs with city names
    cocity_data = cocity_data.copy()
    cocity_data["city1"] = cocity_data["city_id1"].map(city_id_to_name)
    cocity_data["city2"] = cocity_data["city_id2"].map(city_id_to_name)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Citations", city_data["citation_sum"].values[0])

    with col2:
        st.metric("Collaboration Count", len(cocity_data))

    st.write(f"Collaboration Details for {selected_city}:")
    st.dataframe(
        cocity_data[["city1", "city2", "colab_count"]],
        hide_index=True,
        use_container_width=True,
    )





best_model = joblib.load("best_model.pkl")


def ml_page():
    """Machine Learning Model Section"""
    st.title("🤖 Machine Learning Model")

    # Display precomputed best model details

    # Input fields for prediction
    st.subheader("Make a Prediction")
    input_values = {}
    best_features = ['population', 'gdp_per_capita', 'lon', 'safety_index']
    for feature in best_features:
        input_values[feature] = st.number_input(f"Enter value for {feature}:", value=0.0,format="%.2f")
    input_values['primary_language'] = st.number_input(f"Enter value for primary_language (1 if English, 0 otherwise):", value=0,max_value=1,min_value=0,step=1)


    # Predict using the best model
    if st.button("Predict"):
        with st.spinner("Making prediction..."):
            input_df = pd.DataFrame([input_values])  # Create a DataFrame for prediction
            prediction = best_model.predict(input_df)[0]  # Get prediction
        st.success(f"The citation average is: {prediction:.2f}")


# Main app logic
def main():
    # Add custom CSS to improve sidebar navigation
    st.markdown(
        """
    <style>
    [data-testid="stSidebarNav"] {
        background-image: linear-gradient(#2E2E2E, #2E2E2E);
        background-color: #2E2E2E;
    }
    [data-testid="stSidebarNav"]::before {
        content: "City Collaboration Analysis";
        margin-left: 20px;
        margin-top: 20px;
        font-size: 30px;
        position: relative;
        top: 20px;
        color: white;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Overview", "Visualizations", "Analytics", "ML Model"])

    # Page selection
    if page == "Overview":
        overview_page()
    elif page == "Visualizations":
        visualizations_page()
    elif page == "Analytics":
        analytics_page()
    elif page == "ML Model":
        ml_page()


# Run the app
if __name__ == "__main__":
    main()
