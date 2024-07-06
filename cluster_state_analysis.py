import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import plotly.graph_objects as go
import os

# Suppress joblib's CPU cores warning
os.environ['LOKY_MAX_CPU_COUNT'] = '4'

def load_data_state():
    # Load the data
    file_path = 'C:/Users/choon/Documents/Chi Ling/BCSCUN/Big Data/Project/cleaned_cases_state.csv'  # Update with your file path if running locally
    data = pd.read_csv(file_path)
    
    # Convert 'date' to datetime
    data['date'] = pd.to_datetime(data['date'])
    
    return data

# Preprocess the data
def preprocess_data_state(data, start_month, start_year, end_month, end_year, states, show_full_data):
    if not show_full_data:
        # Create a datetime column for the first day of the start month and year
        start_date = pd.to_datetime(f"{start_year}-{start_month}-01")
        # Create a datetime column for the last day of the end month and year
        end_date = pd.to_datetime(f"{end_year}-{end_month}-01") + pd.offsets.MonthEnd(1)
        
        # Filter the data based on the date range
        data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]

    # Filter by state if provided
    if states:
        data = data[data['state'].isin(states)]
        
    return data

# Load the data
data = load_data_state()

# Streamlit App
st.title("COVID-19 Data Visualization for Malaysia")

tab1, tab2 = st.tabs(["Cases Data", "Cluster Data"])

# Tab 1: Cases Data
with tab1:
    st.write("Filter and visualize COVID-19 data by state, month, and year.")
    type_of_graph = st.selectbox("Select Type of Graph", ["Kmeans Cluster", "State Data Analysis by Month and Year"])

    # Convert the appropriate columns to numeric types
    numeric_columns = ['cases_new', 'cases_import', 'cases_recovered', 'cases_active',
                       'cases_cluster', 'cases_child', 'cases_adolescent', 'cases_adult', 'cases_elderly']
    for column in numeric_columns:
        data[column] = pd.to_numeric(data[column], errors='coerce')

    # Aggregate data by state: calculate mean for each numeric column
    state_data = data.groupby('state')[numeric_columns].mean()

    if type_of_graph == "Kmeans Cluster":
        # Standardize the data
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(state_data)

        # Use the Elbow Method to determine the optimal number of clusters
        inertia = []
        for k in range(1, 11):
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(scaled_data)
            inertia.append(kmeans.inertia_)

        # Plot the Elbow Method results using Plotly
        fig = go.Figure(data=go.Scatter(x=list(range(1, 11)), y=inertia, mode='lines+markers'))
        fig.update_layout(title='Elbow Method for Optimal K',
                          xaxis_title='Number of Clusters',
                          yaxis_title='Inertia',
                          template='plotly_white')
        st.plotly_chart(fig)
    
        # Standardize the data again (it might be redundant)
        scaled_data = scaler.fit_transform(state_data)

        # Based on the Elbow plot, we select the optimal number of clusters (e.g., 3)
        optimal_clusters = 3  # Change this based on your Elbow plot    
        kmeans = KMeans(n_clusters=optimal_clusters, random_state=42)
        state_data['cluster'] = kmeans.fit_predict(scaled_data)

        # Rename the clusters for better interpretation
        cluster_names = ['Cluster 1', 'Cluster 2', 'Cluster 3']  # Add more names if needed
        state_data['cluster'] = state_data['cluster'].map(lambda x: cluster_names[x])

        # Visualize the renamed clusters using Plotly
        fig = px.scatter(
            state_data,
            x='cases_new',
            y='cases_active',
            color='cluster',
            size='cases_new',
            hover_data={'cases_recovered': True, 'cases_cluster': True, 'State': state_data.index},  # Show state names in hover data
            title='COVID-19 Clusters by State',
            labels={'cases_new': 'New Cases', 'cases_active': 'Active Cases'}
        )

        # Update layout for better visual presentation
        fig.update_layout(
            template='plotly_white',
            showlegend=True,
            title={'x': 0.5},  # Center the title
            xaxis={'title': 'New Cases'},
            yaxis={'title': 'Active Cases'}
        )

        st.plotly_chart(fig)

        # Optionally, display the states in each cluster below the chart
        st.write("### States by Cluster")
        for cluster in cluster_names:
            st.write(f"**{cluster}:**")
            states_in_cluster = state_data[state_data['cluster'] == cluster].index.tolist()
            st.write(", ".join(states_in_cluster))

    elif type_of_graph == "State Data Analysis by Month and Year":
        st.write("Choose a range of months and years to filter the data:")

        min_date = data['date'].min()
        max_date = data['date'].max()

        # Month and Year selection
        months = range(1, 13)
        month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December']
        years = data['date'].dt.year.unique()
        
        col1, col2 = st.columns(2)
        with col1:
            start_month = st.selectbox("Start Month", month_names)
            start_month_index = month_names.index(start_month) + 1
            start_year = st.selectbox("Start Year", sorted(years))

        with col2:
            end_month = st.selectbox("End Month", month_names)
            end_month_index = month_names.index(end_month) + 1
            end_year = st.selectbox("End Year", sorted(years))
        
        # States selection
        states = st.multiselect("Select State(s)", options=sorted(data['state'].unique()), default=sorted(data['state'].unique()))

        # Checkbox for full dataset
        show_full_data = st.checkbox("Show full dataset")
        # Disable filters if "Show full dataset" is checked
        disable_filters = show_full_data

        if disable_filters:
            st.warning("Filtering options are disabled because 'Show full dataset' is selected.")
            start_month = "January"
            start_year = "2020"
            end_month = "June"
            end_year = "2024"
        
        else:
            button = st.button("Apply Filter")
            if end_year < start_year or (end_year == start_year and end_month_index < start_month_index):
                st.error("End date must be after the start date.")
            if not states:
                st.error("Please select at least one state.")  
            if start_month_index >=7 and start_year == 2024:
                st.error("The range of the date must be between January 2020 and June 2024.")
            if end_month_index >=7 and end_year == 2024:
                st.error("The range of the date must be between January 2020 and June 2024.")

        # Apply filter and update visualization
        if disable_filters or button:
            filtered_data = preprocess_data_state(data, start_month_index, start_year, end_month_index, end_year, states, show_full_data)

            if show_full_data:
                st.write(f"**Full dataset range:** {min_date.strftime('%B %Y')} to {max_date.strftime('%B %Y')}")
                st.subheader("Full Dataset")

            
            if filtered_data.empty:
                st.write(f"No data available for the selected range.")
            else:
                st.subheader(f"Data Summary from {start_month} {start_year} to {end_month} {end_year}")
                fig = px.line(filtered_data, x='date', y='cases_new', color='state',
                            title=f'Daily New Cases from {start_month} {start_year} to {end_month} {end_year}',
                            labels={'cases_new': 'New Cases', 'date': 'Date'})
                st.plotly_chart(fig)

                #Each State by Cases and Age Group

                state_cols = ['cases_new', 'cases_active', 'cases_recovered', 'cases_cluster']
                state_data = filtered_data.groupby('state')[state_cols].sum().reset_index()

                fig = go.Figure()

                for col in state_cols:
                    fig.add_trace(go.Bar(x=state_data['state'], y=state_data[col], name=col))

                fig.update_layout(
                        title=f'COVID-19 Cases by State for {start_month} {start_year} to {end_month} {end_year}',
                        xaxis_title='State',
                        yaxis_title='Number of Cases',
                        barmode='group',
                        template='plotly_white')

                st.plotly_chart(fig)

                age_group_cols = ['cases_child', 'cases_adolescent', 'cases_adult', 'cases_elderly']
                age_group_data = filtered_data.groupby('state')[age_group_cols].sum().reset_index()

                    
                fig = go.Figure()

                for col in age_group_cols:
                    fig.add_trace(go.Bar(x=age_group_data['state'], y=age_group_data[col], name=col))

                fig.update_layout(
                        title=f'COVID-19 Cases by Age Group for {start_month} {start_year} to {end_month} {end_year}',
                        xaxis_title='State',
                        yaxis_title='Number of Cases',
                        barmode='group',
                        template='plotly_white')

                st.plotly_chart(fig)        

def load_data_district():
    # Load the data
    file_path = 'C:/Users/choon/Documents/Chi Ling/BCSCUN/Big Data/Project/cleaned_cluster.csv'
    data1 = pd.read_csv(file_path)

    # Convert the 'date' columns to datetime
    data1['date_announced'] = pd.to_datetime(data1['date_announced'])

    return data1

# Load data
data1 = load_data_district()
# Create 'year_month' column before any further processing
data1['year_month'] = data1['date_announced'].dt.to_period('M')
data1['year_month_str'] = data1['year_month'].astype(str)

with tab2:
    st.title("Visualize COVID-19 data by cluster and district.")
    #type_of_graph = st.selectbox("Select Type of Graph", ["Histograms and Density Plots for Numerical Features", "Trends and Patterns Over Time", "Relationship between Features", "Bar Charts for Categorical Variables", "Box Plots for Identifying Outliers in Numerical Features"])

    # 1. Bar Charts for Categorical Variables

    # Top 10 Districts by Frequency
    top_districts = data1['district'].value_counts().nlargest(10).reset_index()
    top_districts.columns = ['district', 'count']  # Rename columns for clarity
    fig = px.bar(top_districts, x='district', y='count', color='district', title='Top 10 Districts by Frequency',
                 labels={'district': 'District', 'count': 'Number of Clusters'})
    fig.update_layout(template='plotly_white', xaxis={'categoryorder': 'total descending'})
    st.plotly_chart(fig)

    # Category Distribution
    fig = px.bar(data1, x=data1['category'].value_counts().index, y=data1['category'].value_counts().values,
                 title='Category Distribution of Clusters',
                 labels={'x': 'Category', 'y': 'Number of Clusters'})
    fig.update_layout(template='plotly_white')
    st.plotly_chart(fig)

    # Calculate top clusters by total cases
    top_clusters = data1.groupby('cluster')['cases_total'].sum().nlargest(10)

    # Top Clusters by Total Cases
    fig = px.bar(data1, x=top_clusters.values, y=top_clusters.index, orientation='h',
                 title='Top 10 Clusters by Total Cases',
                 labels={'x': 'Total Cases', 'y': 'Cluster'})
    fig.update_layout(template='plotly_white', yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig)

    # 2. Box Plots for Identifying Outliers in Numerical Features

    # Box Plot for Cases Total
    fig = px.box(data1, y='cases_total', title='Box Plot of Cases Total', labels={'cases_total': 'Cases Total'})
    fig.update_layout(template='plotly_white')
    st.plotly_chart(fig)

    # 3. Trends and Patterns Over Time
    # Scatter plot for Year-Month vs. Cases Total with Category color
    fig = px.scatter(data1, x='year_month_str', y='cases_total', color='category',
                     title='Relationship between Year-Month and Cases Total', labels={'year_month_str': 'Year-Month', 'cases_total': 'Cases Total'})
    fig.update_layout(template='plotly_white')
    st.plotly_chart(fig)

    # 4. Histograms and Density Plots for Numerical Features
    fig = px.histogram(data1, x='cases_total', nbins=50, marginal='rug', color_discrete_sequence=['blue'],
                       title='Distribution of Cases Total', labels={'cases_total': 'Cases Total'})
    fig.update_layout(template='plotly_white')
    st.plotly_chart(fig)



