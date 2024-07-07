import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

udf0 = pd.read_csv('C:/Users/Joe Shen/Downloads/BIGDATA CHECKPOINT/CSV/cleaned_unemployment1.csv')  #Update File Path
odf0 = pd.read_csv('C:/Users/Joe Shen/Downloads/BIGDATA CHECKPOINT/CSV/gdp+unemployment+inflation.csv') #Update File Path

# Functions

def filter_data(df, demographic_list):
    """Filter the dataframe based on selected demographics."""
    return df[df['Demographic'].isin(demographic_list)]

def plot_bar_chart(df, x_col, y_col, color_col, title):
    """Plot a bar chart using Plotly."""
    fig = px.bar(df, x=x_col, y=y_col, color=color_col, title=title)
    return fig

def plot_line_chart(df, x_col, y_col, color_col, title):
    """Plot a line chart using Plotly."""
    fig = px.line(df, x=x_col, y=y_col, color=color_col, title=title)
    return fig

def plot_histogram(df, x_col, title):
    """Plot a histogram using Plotly."""
    fig = px.histogram(df, x=x_col, title=title)
    return fig

def plot_box_plot(df, y_col, title):
    """Plot a box plot using Plotly."""
    fig = px.box(df, y=y_col, title=title)
    return fig

def plot_scatter_matrix(df, dimensions, title):
    """Plot a scatter matrix using Plotly."""
    fig = px.scatter_matrix(df, dimensions=dimensions, title=title)
    return fig

def plot_heatmap(df, cols, title):
    """Plot a correlation heatmap using Plotly."""
    corr = df[cols].corr()
    fig = px.imshow(corr, text_auto=True, title=title)
    return fig

# Streamlit Visualisation
st.title("COVID-19 Impact on Malaysia's Economy From 2019-2022")
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Unemployment Rate", "GDP Per Capita", "Inflation Rate", "Overall Analysis", "Machine Learning Model"])

# Tab1
with tab1:
    st.write("The Unemployment Rate is filtered by different demographics such as Age Group and Gender.")
    st.header("Unemployment Rate per Demographic in Malaysia")
    demo = st.multiselect("Select Demographic(s)", options=sorted(udf0['Demographic'].unique()), default=sorted(udf0['Demographic'].unique()))
    filtered_data = filter_data(udf0, demo)
    # Time Series Line Plot
    fig = plot_line_chart(filtered_data, x_col="Year", y_col="Unemployment Rate(%)", color_col='Demographic', title='Overall Unemployment Rate in Malaysia from 2019-2022')
    st.plotly_chart(fig)
    # Bar Plot(Group)
    bar_fig = plot_bar_chart(filtered_data, x_col="Year", y_col="Unemployment Rate(%)", color_col='Demographic', title='Unemployment Rate by Demographic Group')
    st.plotly_chart(bar_fig)

# Tab2
with tab2:
    st.write("GDP Per Capita stands for the economic output per person in a country. The GDP Per Capita is visualised in the graphs below.")
    # Time Series Line Plot
    gdp_line_fig = plot_line_chart(odf0, x_col="Year", y_col="GDP per Capita", color_col=None, title='GDP per Capita in Malaysia from 2019-2022')
    st.plotly_chart(gdp_line_fig)
    # Histogram
    gdp_hist_fig = plot_histogram(odf0, x_col="GDP per Capita", title='Distribution of GDP per Capita in Malaysia')
    st.plotly_chart(gdp_hist_fig)

# Tab3
with tab3:
    st.write("The Inflation Rate affects the purchasing power of a country's currency. The Inflation Rate is visualised in the graphs below.")
    # Time Series Line Plot
    inflation_line_fig = plot_line_chart(odf0, x_col="Year", y_col="Inflation Rate(%)", color_col=None, title='Inflation Rate in Malaysia from 2019-2022')
    st.plotly_chart(inflation_line_fig)
    # Box Plot
    inflation_box_fig = plot_box_plot(odf0, y_col="Inflation Rate(%)", title='Box Plot of Inflation Rate in Malaysia')
    st.plotly_chart(inflation_box_fig)

# Tab4
with tab4:
    st.write("The Overall Analysis combines all 3 economic indicators to provide a comprehensive view of the impact of COVID-19 on Malaysia's economy.")
    st.write("This shows the relationship between the Unemployment Rate, GDP Per Capita, and Inflation Rate. How these 3 indicators affect each other and the economy as a whole.")
    # Scatter Plot
    scatter_fig = plot_scatter_matrix(odf0, dimensions=["Average Unemployment Rate(%)", "GDP per Capita", "Inflation Rate(%)"], title='Scatter Matrix of Economic Indicators')
    st.plotly_chart(scatter_fig)
    # Correlation Heatmap
    heatmap_fig = plot_heatmap(odf0, cols=["Average Unemployment Rate(%)", "GDP per Capita", "Inflation Rate(%)"], title='Correlation Heatmap of Economic Indicators')
    st.plotly_chart(heatmap_fig)

#Tab5
with tab5:
    st.write("Here we will be using a machine learning model based on ARIMA to predict the economic performance of Malaysia in the future.")
    

