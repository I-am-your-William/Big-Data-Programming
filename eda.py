import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

udf0 = pd.read_csv('C:/Users/Joe Shen/Downloads/BIGDATA CHECKPOINT/CSV/cleaned_unemployment1.csv')  #Update File Path
odf0 = pd.read_csv('C:/Users/Joe Shen/Downloads/BIGDATA CHECKPOINT/CSV/overallecon.csv') #Update File Path
#ML Training Data


# Functions
def filter_data(df, column_name, value_list):
    return df[df[column_name].isin(value_list)]

# Streamlit Visualisation
st.title("COVID-19 Impact on Malaysia's Economy From 2019-2022")
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Unemployment Rate", "GDP Per Capita", "Inflation Rate", "Overall Analysis", "Machine Learning Model"])

# Tab1
with tab1:
    st.write("The Unemployment Rate is filtered by different demographics such as Age Group and Gender.")
    st.header("Unemployment Rate per Demographic in Malaysia")
    demo = st.multiselect("Select Demographic(s)", options=sorted(udf0['Demographic'].unique()), default=sorted(udf0['Demographic'].unique()))
    filtered_data = filter_data(udf0, "Demographic", demo)
    # Time Series Line Plot
    demo_fig = px.line(filtered_data, title='Overall Unemployment Rate in Malaysia from 2019-2022',
                        x="Year", y="Unemployment Rate(%)", color='Demographic')
    st.plotly_chart(demo_fig)
    line_colors = {trace.name: trace.line.color for trace in demo_fig['data']}

    # Bar Plot(Group)
    bar_fig = go.Figure()
    for demographic in demo:
        demo_data = filtered_data[filtered_data['Demographic'] == demographic]
        bar_fig.add_trace(go.Bar(x=demo_data['Year'], y=demo_data['Unemployment Rate(%)'], name=demographic, marker_color=line_colors.get(demographic)))
        
    bar_fig.update_layout(
        title='Unemployment Rate by Demographic Group',
        xaxis_title='Year',yaxis_title='Unemployment Rate(%)',barmode='group')
    st.plotly_chart(bar_fig)

# Tab2
with tab2:
    st.write("GDP Per Capita stands for the economic output per person in a country. The GDP Per Capita is visualised in the graphs below.")
    gdp_data = filter_data(odf0, "Economic Indicator", ['GDP per Capita'])
    
    # Time Series Line Plot
    gdp_line_fig = px.line(gdp_data, x="Year", y="Value", title='GDP per Capita in Malaysia from 2019-2022')
    st.plotly_chart(gdp_line_fig)
    
    # Histogram
    gdp_hist_fig = px.histogram(gdp_data, x="Value", title='Distribution of GDP per Capita in Malaysia')
    st.plotly_chart(gdp_hist_fig)

# Tab3
with tab3:
    st.write("The Inflation Rate affects the purchasing power of a country's currency. The Inflation Rate is visualised in the graphs below.")
    infla_data = filter_data(odf0, "Economic Indicator", ['Inflation Rate(%)'])
    
    # Time Series Line Plot
    inflation_line_fig = px.line(infla_data, x="Year", y="Value", title='Inflation Rate in Malaysia from 2019-2022')
    st.plotly_chart(inflation_line_fig)
    
    # Box Plot
    inflation_box_fig = px.box(infla_data, y="Value", title='Box Plot of Inflation Rate in Malaysia', points="all")
    st.plotly_chart(inflation_box_fig)

# Tab4
with tab4:
    st.write("The Overall Analysis combines all 3 economic indicators to provide a comprehensive view of the impact of COVID-19 on Malaysia's economy.")
    st.write("This shows the relationship between the Unemployment Rate, GDP Per Capita, and Inflation Rate. How these 3 indicators affect each other and the economy as a whole.")
    
    # Pivot the data to reshape it for scatter plot
    pivot_data = odf0.pivot(index='Year', columns='Economic Indicator', values='Value').reset_index()
    
    # Handle negative values by setting a minimum size
    pivot_data['Inflation Rate(%)'] = pivot_data['Inflation Rate(%)'].clip(lower=0)
    
    # 3D Scatter Plot
    scatter_fig_3d = px.scatter_3d(
        pivot_data,
        x="GDP per Capita", 
        y="Average Unemployment Rate(%)",
        z="Inflation Rate(%)",
        title='3D Scatter Plot of Economic Indicators',
        hover_name='Year'
    )
    scatter_fig_3d.update_layout(scene=dict(
        xaxis_title='GDP per Capita',
        yaxis_title='Average Unemployment Rate(%)',
        zaxis_title='Inflation Rate(%)'
    ))
    
    # Display 3D Scatter Plot
    st.plotly_chart(scatter_fig_3d)

    # Correlation Heatmap
    correlation_matrix = pivot_data[['Average Unemployment Rate(%)', 'GDP per Capita', 'Inflation Rate(%)']].corr()
    heatmap_fig = px.imshow(
        correlation_matrix, 
        labels=dict(x="Economic Indicators", y="Economic Indicators", color="Correlation"), 
        title='Correlation Heatmap of Economic Indicators',
        text_auto=True
    )
    st.plotly_chart(heatmap_fig)

#Tab5
with tab5:
    st.write("Here we will be using a machine learning model based on ARIMA to predict the economic performance of Malaysia in the future.")
    

