import streamlit as st
import pandas as pd
import plotly.express as px

# '''if the lecturer want to fix the x/y axis to a specific column, need to change the x/y input to the specific column name instead of  line 36 and line 41'''
# Load the data
data_path_1 = 'C:/Users/User/Downloads/aefi_serious.csv'
data_path_2 = 'C:/Users/User/Downloads/aefi.csv'  

df1 = pd.read_csv(data_path_1)
df2 = pd.read_csv(data_path_2)

# Set the title of the Streamlit app
st.title('AEFI and Second Dataset Analysis')

# Dropdown menu to select the dataset
dataset = st.selectbox('Select Dataset', ['AEFI Serious', 'AEFI Normal'])

# Select the appropriate dataframe based on the dataset choice
if dataset == 'AEFI Serious':
    df = df1
else:
    df = df2

# Display the selected dataframe
st.header(f'Dataframe: {dataset}')
st.write(df)

# Dropdown menus for selecting x-axis and y-axis data
st.header('Select Data for Plots')
x_axis_column = st.selectbox(
    'Select a column for the x-axis', 
    df.columns
)

y_axis_column = st.selectbox(
    'Select a column for the y-axis', 
    df.columns
)

# Box Plot
st.header('Box Plot')
box_plot_fig = px.box(df,  x="vaxtype", y=y_axis_column,points="all")
st.plotly_chart(box_plot_fig)
st.write('**Graph Explaination**: The box plot is a standardized way of displaying the distribution of data based on a five number summary: minimum, first quartile, median, third quartile, and maximum. It is often used to identify the outliers in the dataset. ')
st.write('The box plot above shows the distribution of the selected data column. The box represents the interquartile range (IQR), which is the range between the first quartile (Q1) and the third quartile (Q3). The line inside the box represents the median value. The whiskers extend to the minimum and maximum values, with any points outside the whiskers considered outliers.')

# Scatter Plot
st.header('Scatter Plot')
scatter_plot_fig = px.scatter(df, x=x_axis_column, y=y_axis_column)
st.plotly_chart(scatter_plot_fig)
st.write('**Graph Explaination**: A scatter plot is a type of plot that shows the relationship between two variables.   Each point on the plot represents a single observation, with the x-coordinate representing one variable and the y-coordinate representing the other. Scatter plots are useful for visualizing patterns and relationships in the data.')
st.write('The scatter plot above shows the relationship between the selected x-axis and y-axis columns. Each point on the plot represents a single observation in the dataset. The plot can be used to identify patterns, trends, and correlations between the two variables.')
# Histogram
st.header('Histogram')
hist_fig = px.histogram(df, x=y_axis_column)
st.plotly_chart(hist_fig)

st.write('**Graph Explaination**: A histogram is a type of plot that shows the distribution of a continuous variable. It divides the data into bins or intervals and displays the frequency of observations in each bin. Histograms are useful for visualizing the shape of the data distribution and identifying patterns or outliers.')
st.write('The histogram above shows the distribution of the selected data column. The x-axis represents the values of the data column, while the y-axis represents the frequency of observations in each bin. The plot can be used to identify the central tendency, spread, and shape of the data distribution.')