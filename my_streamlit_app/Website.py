import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

# Importing the individual page modules
import zy
import gx
import cl
import js

# Set custom CSS for macaroon pink color scheme and logo
st.markdown("""
    <style>
    /* Change sidebar background color */
    .css-1d391kg {
        background: linear-gradient(135deg, #FFCCCB, #D6A4A4, #B2D9F7); /* Gradient from light pink to light purple to light blue */
        color: #000000;
    }
    /* Center the logo at the top of the sidebar */
    .css-1d391kg img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        padding-top: 10px;  /* Add padding if needed */
    }
    /* Style the sidebar buttons */
    .css-1wa3e0r {
        background-color: #550A35; /* Macaroon pink */
        border: none;
        border-radius: 5px;
        color: #FFC0CB;
        font-size: 18px;
        margin-bottom: 10px;
        text-align: center;
        padding: 10px;
        width: 100%;
    }
    .css-1wa3e0r:hover {
        background-color: #550A35; /* Lighter macaroon pink on hover */
    }
    </style>
    """, unsafe_allow_html=True)

def format_number(n):
    if n >= 1_000_000:
        return f"{n/1_000_000:.3f}m"  # Format with three decimal places
    elif n >= 1_000:
        return f"{n/1_000:.3f}k"
    else:
        return str(n)


# Function to load and process vaccination data
def load_vaccine_data():
    vaccine_data_path = 'C:/zhengyang/Inti/BCSCUN/Sem 6/Big Data/cleaned_dataset/vax_state_cleaned.csv'
    df_vaccine = pd.read_csv(vaccine_data_path)
    
    # Aggregate total full vaccinations by state
    df_state_vaccine = df_vaccine.groupby('state').agg({
        'daily_full': 'sum'  # Sum of daily_full vaccinations for each state
    }).reset_index()

    # Rename columns to match GeoJSON properties if needed
    df_state_vaccine.rename(columns={'state': 'name', 'daily_full': 'total_full_vaccinations'}, inplace=True)
    
    return df_state_vaccine

# Function to load and process COVID-19 cases and recoveries data
def load_cases_data():
    cases_data_path = 'C:/zhengyang/Inti/BCSCUN/Sem 6/Big Data/cleaned_dataset/cleaned_cases_state.csv'
    df_cases = pd.read_csv(cases_data_path)
    
    # Aggregate total cases and recoveries by state
    df_state_cases = df_cases.groupby('state').agg({
        'cases_new': 'sum',       # Sum of new cases for each state
        'cases_recovered': 'sum'  # Sum of recovered cases for each state
    }).reset_index()

    # Rename columns to match GeoJSON properties if needed
    df_state_cases.rename(columns={'state': 'name', 'cases_new': 'total_cases', 'cases_recovered': 'total_recoveries'}, inplace=True)
    
    return df_state_cases

# Function to merge vaccine and cases data
def merge_data(df_vaccine, df_cases):
    df_merged = pd.merge(df_vaccine, df_cases, on='name', how='outer')
    return df_merged

# Function to load GeoJSON data
def load_geojson():
    geojson_path = 'C:/zhengyang/Inti/BCSCUN/Sem 6/Big Data/Malaysia_GeoJSON_Map/malaysia.state.geojson'
    with open(geojson_path) as response:
        geojson = json.load(response)
    return geojson

# Function to calculate RVEI
def calculate_rvei(df):
    df['RVEI'] = (df['total_recoveries'] + df['total_full_vaccinations']) / df['total_cases']
    return df

# Function to create the combined map figure
def create_combined_map(df, geojson):
    fig = go.Figure()

    # Define color scales for different metrics
    color_scales = {
        'RVEI': [
            [0.0, "#FF69B4"],  
            [0.5, "#800080"],  
            [1.0, "#06D6A0"]   
        ],
        'Total Cases': [
            [0.0, "#FFBE0B"],  
            [0.5, "#FF006E"],  
            [1.0, "#3A86FF"]   
        ],
        'Total Vaccinations': [
            [0.0, "#020202"],  
            [0.5, "#7B2CBF"],  
            [1.0, "#BB0A21"]   
        ],
        'Total Recoveries': [
            [0.0, "#FEE440"],  
            [0.5, "#FE7F2D"],  
            [1.0, "#D90429"]   
        ]
    }

    # Ensure columns for formatted data are present
    df['formatted_cases'] = df['total_cases'].apply(format_number)
    df['formatted_vaccinations'] = df['total_full_vaccinations'].apply(format_number)
    df['formatted_recoveries'] = df['total_recoveries'].apply(format_number)

    # List of metrics to avoid hardcoding
    metrics = {
        'RVEI': 'RVEI',
        'Total Cases': 'total_cases',
        'Total Vaccinations': 'total_full_vaccinations',
        'Total Recoveries': 'total_recoveries'
    }

    # Add trace for each metric
    for metric_name, metric_column in metrics.items():
        fig.add_trace(go.Choroplethmapbox(
            geojson=geojson,
            locations=df['name'],
            z=df[metric_column] if metric_name != 'RVEI' else df['RVEI'],
            featureidkey="properties.name",
            colorscale=color_scales[metric_name],
            zmin=df[metric_column].min() if metric_name != 'RVEI' else df['RVEI'].min(),
            zmax=df[metric_column].max() if metric_name != 'RVEI' else df['RVEI'].max(),
            marker_opacity=0.5,
            marker_line_width=0.5,
            name=metric_name,
            visible=False,
            hovertemplate=(
                f'<b>%{{location}}</b><br>' +
                f'{metric_name}: %{{z:.2f}}<br>' +
                'Total Cases: %{customdata[0]}<br>' +
                'Total Full Vaccinations: %{customdata[1]}<br>' +
                'Total Recoveries: %{customdata[2]}<br>'
            ),
            customdata=df[['formatted_cases', 'formatted_vaccinations', 'formatted_recoveries']].values
        ))

    # Set default visible trace
    fig.data[0].visible = True

    # Update layout with dropdown menu
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=5,
        mapbox_center={"lat": 4.0, "lon": 113.5},
        margin={"r":0,"t":0,"l":0,"b":0},
        updatemenus=[
            {
                'buttons': [
                    {
                        'label': metric_name,
                        'method': 'update',
                        'args': [{'visible': [metric_name == trace.name for trace in fig.data]}]
                    } for metric_name in metrics.keys()
                ],
                'direction': 'down',
                'showactive': True,
                'x': 0.0,          # Position x to 0.0 (left edge)
                'xanchor': 'left', # Anchor to the left
                'y': 1.0,          # Position y to 1.0 (top edge)
                'yanchor': 'top'   # Anchor to the top
            }
        ],
        legend=dict(
            title=dict(text='Metrics', font=dict(size=12)),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig



# Define the main function for each page
def home_app():
    st.title("COVID-19 Impact Navigator - Home")
    st.write("The graph shows RVEI (Recovery and Vaccination Effectiveness Index) across Malaysia, indicating recovery and vaccination effectiveness by state.")

    # Load data
    df_vaccine = load_vaccine_data()
    df_cases = load_cases_data()
    df_merged = merge_data(df_vaccine, df_cases)
    df_merged = calculate_rvei(df_merged)
    geojson = load_geojson()
    
    # Create and display combined map
    fig = create_combined_map(df_merged, geojson)
    st.plotly_chart(fig, use_container_width=True)

    # Graph explanation
    st.markdown("""
    **Graph Explanation:**
    - **Graph Type**: Choropleth map.
    - **Metric Displayed**: RVEI (Recovery and Vaccination Effectiveness Index).
    - **Color Scale**: Represents the RVEI with bright pink, purple, and blue colors.
    - **Hover Information**: Displays total cases, total full vaccinations, and total recoveries for each state.
    - **Meaning**: This map visualizes the relationship between total cases, vaccinations, and recoveries. Higher RVEI values indicate higher effectiveness of recoveries and vaccinations relative to the number of cases.
    - **Significance**: 
      - **High RVEI**: Indicates that a region has a high number of recoveries and full vaccinations relative to its total number of cases, suggesting effective management of the pandemic.
      - **Low RVEI**: Indicates a lower proportion of recoveries and full vaccinations relative to the total number of cases, suggesting a need for improved recovery and vaccination efforts.
    - **Visualization**: The choropleth map uses a color scale ranging from bright pink to blue, where bright pink indicates lower RVEI values and blue indicates higher RVEI values.
    """)

def zy_page():
    zy.main()  # Call the main function from zy.py

def gx_page():
    gx.main()  # Call the main function from gx.py

def cl_page():
    cl.main()  # Call the main function from cl.py

def js_page():
    js.main()  # Call the main function from js.py

# Sidebar navigation
st.sidebar.image('C:/zhengyang/Inti/BCSCUN/Sem 6/Big Data/logo.jpg', width=200)  # Add logo image to the sidebar

# Use buttons for page navigation
button_home = st.sidebar.button("COVID-19 Impact Navigator", key="home")
button_zy = st.sidebar.button("Malaysia COVID-19 Vaccination and Death Data Analysis", key="zy")
button_gx = st.sidebar.button("AEFI and Second Dataset Analysis", key="gx")
button_cl = st.sidebar.button("COVID-19 Data Visualization for Malaysia", key="cl")
button_js = st.sidebar.button("JS Page", key="js")

# Define page rendering based on button clicks
if 'selected_page' not in st.session_state:
    st.session_state.selected_page = "COVID-19 Impact Navigator - Home"

if button_home:
    st.session_state.selected_page = "COVID-19 Impact Navigator - Home"
elif button_zy:
    st.session_state.selected_page = "Malaysia COVID-19 Vaccination and Death Data Analysis"
elif button_gx:
    st.session_state.selected_page = "AEFI and Second Dataset Analysis"
elif button_cl:
    st.session_state.selected_page = "COVID-19 Data Visualization for Malaysia"
elif button_js:
    st.session_state.selected_page = "JS Page"

# Render the selected page
if st.session_state.selected_page == "COVID-19 Impact Navigator - Home":
    home_app()
elif st.session_state.selected_page == "Malaysia COVID-19 Vaccination and Death Data Analysis":
    zy_page()
elif st.session_state.selected_page == "AEFI and Second Dataset Analysis":
    gx_page()
elif st.session_state.selected_page == "COVID-19 Data Visualization for Malaysia":
    cl_page()
elif st.session_state.selected_page == "JS Page":
    js_page()
