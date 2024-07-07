import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import plotly.graph_objects as go

def load_data_state():
    # Load the data
    file_path = 'C:/Users/choon/Documents/Chi Ling/BCSCUN/Big Data/Project/cleaned_cases_state.csv'  # Update with your file path if running locally
    data = pd.read_csv(file_path)
    
    # Convert 'date' to datetime
    data['date'] = pd.to_datetime(data['date'])
    
    return data


# Preprocess the data
def preprocess_data_state(data, month, year, states):
    # Filter the data based on the month and year
    data['month'] = data['date'].dt.month
    data['year'] = data['date'].dt.year
    data = data[(data['month'] == month) & (data['year'] == year)]
    
    # Filter by state if provided
    if states:
        data = data[data['state'].isin(states)]
        
    return data

# Load the data
data = load_data_state()

# Streamlit App
st.title("COVID-19 Data Visualization for Malaysia")

tab1, tab2 = st.tabs([ "Cases Data","Cluster Data"])

# Tab 1: Cases Data
with tab1: 
    st.write("Filter and visualize COVID-19 data by state, month, and year.")
    type_of_graph = st.selectbox("Select Type of Graph", ["Kmeans Cluster","Bar Chart","State Data Analysis by Month and Year"])


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
        from sklearn.cluster import KMeans
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
    
        # Standardize the data
        scaler = StandardScaler()
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

    
    elif type_of_graph == "Bar Chart":
        # Use the existing `state_data` with cluster information
        # Summarize the data for each age group per state
        age_group_sums = state_data.groupby('state').agg({
            'cases_child': 'sum',
            'cases_adolescent': 'sum',
            'cases_adult': 'sum',
            'cases_elderly': 'sum'
        }).reset_index()

        # Plotting the bar graph using Plotly
        fig = go.Figure()

        # Add bars for each age group
        fig.add_trace(go.Bar(x=age_group_sums['state'], y=age_group_sums['cases_child'],
                             name='Child', marker_color='blue'))
        fig.add_trace(go.Bar(x=age_group_sums['state'], y=age_group_sums['cases_adolescent'],
                             name='Adolescent', marker_color='green'))
        fig.add_trace(go.Bar(x=age_group_sums['state'], y=age_group_sums['cases_adult'],
                             name='Adult', marker_color='red'))
        fig.add_trace(go.Bar(x=age_group_sums['state'], y=age_group_sums['cases_elderly'],
                             name='Elderly', marker_color='orange'))

        # Update layout
        fig.update_layout(
            title='Total COVID-19 Cases by Age Group in Each State',
            xaxis_title='State',
            yaxis_title='Total Cases',
            barmode='group',  # Group bars together
            xaxis={'categoryorder': 'total descending'},  # Sort states by total cases
            template='plotly_white'
        )
        st.plotly_chart(fig)
        
    elif type_of_graph == "State Data Analysis by Month and Year":
            st.write("Choose a month and year to filter the data:")
            # Month and Year selection
            months = range(1, 13)
            month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December']
            selected_month = st.selectbox("Select Month", month_names)
            selected_month_index = month_names.index(selected_month) + 1
            years = data['date'].dt.year.unique()
            selected_year = st.selectbox("Select Year", years)
            states = st.multiselect("Select State(s)", options=sorted(data['state'].unique()), default=sorted(data['state'].unique()))

            # Preprocess data based on selected month and year
            filtered_data = preprocess_data_state(data, selected_month_index, selected_year, states)

            st.subheader(f"Data Summary for {selected_month} {selected_year}")

            if filtered_data.empty:
                st.write(f"No data available for {selected_month} {selected_year}.")
            else:
                fig = px.line(filtered_data, x='date', y='cases_new', color='state',
                  title=f'Daily New Cases for {selected_month} {selected_year}',
                  labels={'cases_new': 'New Cases', 'date': 'Date'})
                st.plotly_chart(fig)

                age_group_cols = ['cases_child', 'cases_adolescent', 'cases_adult', 'cases_elderly']
                age_group_data = filtered_data[age_group_cols].sum().reset_index()
                age_group_data.columns = ['age_group', 'cases']

                fig = px.bar(age_group_data, x='age_group', y='cases',
                            title=f'Cases by Age Group for {selected_month} {selected_year}',
                            labels={'cases': 'Number of Cases', 'age_group': 'Age Group'},
                            color='age_group')
                st.plotly_chart(fig)

                category_cols = ['cases_import', 'cases_recovered', 'cases_active', 'cases_cluster']
                category_data = filtered_data[category_cols].sum().reset_index()
                category_data.columns = ['category', 'cases']

                fig = px.bar(category_data, x='category', y='cases',
                            title=f'Cases by Category for {selected_month} {selected_year}',
                            labels={'cases': 'Number of Cases', 'category': 'Category'},
                            color='category')
                st.plotly_chart(fig)

           




