import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def main():
    # Load the dataset
    data_path = 'C:/zhengyang/Inti/BCSCUN/Sem 6/Big Data/cleaned_dataset/vax-vs-death_ratio_my.csv'
    df = pd.read_csv(data_path)

    # Convert the date column to datetime format, specify the date format
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y', errors='coerce')

    # Extract month and year for filtering
    df['month'] = df['date'].dt.month_name()  # Get month names instead of numbers
    df['year'] = df['date'].dt.year

    # Title
    st.title("Malaysia COVID-19 Vaccination and Death Data Analysis")

    # Options for user to select the graph type
    st.subheader("Graph Type Selection")
    graph_type = st.selectbox("Choose the type of graph", 
                              ["Overall Vaccinations and Deaths", 
                               "Vaccinations vs. Deaths Analysis", 
                               "Vaccination Effectiveness Over Time",
                               "Year and Monthly Data Analysis of Vaccinations and Deaths"])

    if graph_type == "Overall Vaccinations and Deaths":
        st.subheader("Overall Vaccinations and Deaths Over Time")

        fig = go.Figure()

        # Add total vaccinations trace
        fig.add_trace(go.Scatter(x=df['date'], y=df['total_vaccinations'], mode='lines', name='Total Vaccinations', line=dict(color='#ff80c1')))

        # Add new deaths trace
        fig.add_trace(go.Scatter(x=df['date'], y=df['New_deaths'], mode='lines', name='New Deaths', line=dict(color='#cc00ff')))

        fig.update_layout(title="Overall Vaccinations and Deaths Over Time",
                          xaxis_title="Date",
                          yaxis_title="Count",
                          xaxis_rangeslider_visible=False)
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("""
        **Graph Explanation:**
        - **Graph Type**: Line graph.
        - **X-axis**: Date.
        - **Y-axis**: Count (Total Vaccinations and New Deaths).
        - **Relationship**: This graph displays the relationship between the total number of vaccinations administered and the number of new deaths over time.
        - **Output**: The pink line represents the total vaccinations, while the purple line represents the new deaths.
        - **Meaning**: This graph helps visualize the overall trend of vaccinations and deaths over the entire period. If the deaths decrease as vaccinations increase, it indicates a positive impact of the vaccination program.
        """)

    elif graph_type == "Vaccinations vs. Deaths Analysis":
        st.subheader("Vaccinations vs. Deaths Analysis")

        fig = go.Figure()

        # Scatter plot for Vaccinations vs Deaths
        fig.add_trace(go.Scatter(x=df['total_vaccinations'], y=df['New_deaths'], mode='markers', marker=dict(color='#2ca02c'), name='Vaccinations vs Deaths'))

        fig.update_layout(title="Vaccinations vs. Deaths",
                          xaxis_title="Total Vaccinations",
                          yaxis_title="New Deaths")

        st.plotly_chart(fig, use_container_width=True)

        st.write("""
        **Graph Explanation:**
        - **Graph Type**: Scatter plot.
        - **X-axis**: Total Vaccinations.
        - **Y-axis**: New Deaths.
        - **Relationship**: This graph shows the relationship between the total number of vaccinations and the number of new deaths.
        - **Output**: Each point represents a day, with the x-axis showing the total vaccinations and the y-axis showing the new deaths.
        - **Meaning**: This helps to understand if there is a correlation between the number of vaccinations and the number of deaths. A denser cluster of points in any region of the graph indicates a stronger relationship.
        """)

    elif graph_type == "Vaccination Effectiveness Over Time":
        st.subheader("Vaccination Effectiveness Over Time")

        fig = go.Figure()

        # Line plot for Ratio over time
        fig.add_trace(go.Scatter(x=df['date'], y=df['ratio'], mode='lines', name='Vaccination Effectiveness', line=dict(color='#FFA500')))  # Orange color

        fig.update_layout(title="Vaccination Effectiveness Over Time",
                          xaxis_title="Date",
                          yaxis_title="Ratio (Deaths per 100,000 Vaccinations)",
                          xaxis_rangeslider_visible=False)

        st.plotly_chart(fig, use_container_width=True)

        st.write("""
        **Graph Explanation:**
        - **Graph Type**: Line graph.
        - **X-axis**: Date.
        - **Y-axis**: Ratio (Deaths per Vaccination).
        - **Relationship**: This graph shows the ratio of deaths to vaccinations over time.
        - **Output**: The orange line represents the ratio, indicating the number of deaths per vaccination.
        - **Meaning**: 
            - A **higher ratio** means fewer deaths per vaccination, indicating **higher effectiveness** of the vaccination program.
            - A **lower ratio** means more deaths per vaccination, indicating **lower effectiveness** of the vaccination program.
        """)


    elif graph_type == "Year and Monthly Data Analysis of Vaccinations and Deaths":
        st.subheader("Year and Monthly Data Analysis of Vaccinations and Deaths")

        # Year and month range validation
        valid_months = {
            2021: ["February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
            2022: ["January", "February", "March"]
        }

        year = st.selectbox("Select Year", valid_months.keys())
        month = st.selectbox("Select Month", valid_months[year])

        # Filter data based on user selection
        filtered_df = df[(df['year'] == year) & (df['month'] == month)]
        
        fig = go.Figure()

        # Add total vaccinations bar trace
        fig.add_trace(go.Bar(x=filtered_df['date'], y=filtered_df['total_vaccinations'], name='Total Vaccinations', marker_color='#B2D9F7'))  # Pastel blue color

        # Add new deaths line trace
        fig.add_trace(go.Scatter(x=filtered_df['date'], y=filtered_df['New_deaths'], name='New Deaths', line=dict(color='#FF6347'), yaxis='y2'))  # Tomato color

        fig.update_layout(title="Monthly Vaccinations and Deaths",
                          xaxis_title="Date",
                          yaxis=dict(title="Total Vaccinations", side='left'),
                          yaxis2=dict(title="New Deaths", overlaying='y', side='right'),
                          barmode='group')

        st.plotly_chart(fig, use_container_width=True)

        st.write("""
        **Graph Explanation:**
        - **Graph Type**: Bar chart for total vaccinations and line chart for new deaths.
        - **X-axis**: Date.
        - **Y-axis**: Total Vaccinations (left) and New Deaths (right).
        - **Relationship**: This section allows you to analyze the data by specific year and month.
        - **Output**: The bar chart shows the total vaccinations, and the line chart shows the new deaths for the selected period.
        - **Meaning**: This helps to understand the trends in a more granular timeframe. A high number of vaccinations with low deaths suggests a positive impact of the vaccination program.
        """)

if __name__ == "__main__":
    main()
