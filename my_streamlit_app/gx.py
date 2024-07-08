import streamlit as st
import pandas as pd
import plotly.express as px

def main(): 
    # Load the data
    data_path_1 = 'C:/zhengyang/Inti/BCSCUN/Sem 6/Big Data/cleaned_dataset/aefi_serious.csv'
    data_path_2 = 'C:/zhengyang/Inti/BCSCUN/Sem 6/Big Data/cleaned_dataset/aefi.csv'  

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
    box_plot_fig = px.box(df, y=y_axis_column)
    st.plotly_chart(box_plot_fig)

    # Scatter Plot
    st.header('Scatter Plot')
    scatter_plot_fig = px.scatter(df, x=x_axis_column, y=y_axis_column)
    st.plotly_chart(scatter_plot_fig)

    # Histogram
    st.header('Histogram')
    hist_fig = px.histogram(df, x=y_axis_column)
    st.plotly_chart(hist_fig)

if __name__ == "__main__":
    main()