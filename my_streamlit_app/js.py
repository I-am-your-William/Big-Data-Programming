import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pmdarima import auto_arima
import statsmodels.api as sm
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import warnings

def main():

    # Load the updated dataset
    udemodf0 = pd.read_csv('C:/zhengyang/Inti/BCSCUN/Sem 6/Big Data/cleaned_dataset/cleaned_unemployment1.csv')  #Update File Path
    odf0 = pd.read_csv('C:/zhengyang/Inti/BCSCUN/Sem 6/Big Data/cleaned_dataset/cleaned_monthlyecon_19-22.csv') #Update File Path
    #ML Training Data

    # Convert Date to datetime format and set as index
    odf0['Date'] = pd.to_datetime(odf0['Date'], format='%b-%y') 
    odf0.set_index('Date', inplace=True)

    # Functions
    def filter_data(df, column_name, value_list):
        return df[df[column_name].isin(value_list)]

    # Streamlit Visualization
    st.title("COVID-19 Impact on Malaysia's Economy From 2019-2022")
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Unemployment Rate", "GDP", "Inflation Rate", "Consumer Price Index",
                                                            "YoY & QoQ GDP Growth", "Overall Analysis", "Machine Learning Model"])

    # T1: Unemployment Rate
    with tab1:
        st.write("The Unemployment Rate is filtered by different demographics such as Age Group and Gender.")
        st.header("Unemployment Rate per Demographic in Malaysia")
        demo = st.multiselect("Select Demographic(s)", options=sorted(udemodf0['Demographic'].unique()), default=sorted(udemodf0['Demographic'].unique()))
        filtered_data = filter_data(udemodf0, "Demographic", demo)

        # Bar Plot(Group)
        bar_fig = go.Figure()
        for demographic in demo:
            demo_data = filtered_data[filtered_data['Demographic'] == demographic]
            bar_fig.add_trace(go.Bar(x=demo_data['Year'], y=demo_data['Unemployment Rate(%)'], name=demographic))
            
        bar_fig.update_layout(
            title='Bar Plot of Unemployment Rate by Demographic Group',
            xaxis_title='Year',yaxis_title='Unemployment Rate(%)',barmode='group')
        st.plotly_chart(bar_fig)
        
        # Time Series Line Plot
        unemp_fig = px.line(odf0, x=odf0.index, y='Unemployment Rate', title='Line Plot of Unemployment Rate Over Time')
        st.plotly_chart(unemp_fig)

        st.write("""
            **Graph Analysis:**
            - **Relationship**: This graph shows the relationship between the overall unemployment rate and time period.
            - **Explanation**: 
                - Line plots helps visualize the trend as time passes. This is useful for identifying patterns, such as the significant spike in
            unemployment rate during the COVID-19 pandemic in 2020.
            """)



    # T2: Real GDP
    with tab2:
        st.write("GDP also known as Gross Domestic Product is a measure of the economic performance of a country. It is the monetary value of all finished goods and services produced within a country's borders in a specific time period.")
        st.header("Malaysia's GDP Over Time")
        # Time Series Line Plot
        gdp_line_fig = px.line(odf0, x=odf0.index, y='GDP [RM, in billion]', title='Line Plot of Real GDP Over Time')
        st.plotly_chart(gdp_line_fig)
        st.write("""
            **Graph Analysis:**
            - **Relationship**: This graph shows the relationship between the real GDP of Malaysia and time period.
            - **Explanation**: 
                - As for the patterns of this graph, a noticable drop can be seen during 2020. This suggests that the economy performance was affected by the COVID-19 pandemic.
            """)

        # Histogram
        gdp_hist_fig = px.histogram(odf0, x='GDP [RM, in billion]', title="Histogram of Malaysia's Distribution of Real GDP")
        st.plotly_chart(gdp_hist_fig)
        st.write("""
            **Graph Analysis:**
            - **Relationship**: This graph shows the distribution of Malaysia's real GDP.
            - **Explanation**: 
                - A histogram highlights the frequency of GDP values. This can help identify the most common GDP values and the spread of the data.
            """)




    # Tab3: Inflation Rate
    with tab3:
        st.write("Inflation Rate is the rate at which the general level of prices for goods and services is rising and, subsequently, purchasing power is falling.")
        st.header("Malaysia's Inflation Rate Over Time")
        # Time Series Line Plot
        inflation_line_fig = px.line(odf0, x=odf0.index, y='Inflation Rate', title='Line Plot Inflation Rate Over Time')
        st.plotly_chart(inflation_line_fig)
        st.write("""
            **Graph Analysis:**
            - **Relationship**: This graph shows the relationship between the inflation rate of Malaysia and time period.
            - **Explanation**: 
                - The huge drop of inflation rate in 2020 suggests that it was affected by the COVID-19 pandemic, same as the countru's GDP.
                This shows that the inflation rate of a country may have a direct relationship with the country's GDP.
            """)

        # Box Plot
        inflation_box_fig = px.box(odf0, y='Inflation Rate', title='Box Plot of Inflation Rate', points="all")
        st.plotly_chart(inflation_box_fig)
        explanation = """
        ### **Graph Analysis**:
        
        - **Relationship**: This box plot shows the distribution of Malaysia's inflation rate over a specified period.
        
        - **Explanation**: 
        - The **box plot** provides a visual summary of the inflation rate data by highlighting key statistical measures:
            - **Median**: The line inside the box represents the median (50th percentile), indicating the central tendency of the inflation rate.
            - **Quartiles**: The edges of the box represent the first quartile (25th percentile) and the third quartile (75th percentile), showing the middle 50% of the data.
            - **Whiskers**: The lines extending from the box represent the range of the data, excluding outliers. They typically extend to 1.5 times the interquartile range (IQR) from the quartiles.
            - **Outliers**: Individual points outside the whiskers are considered outliers, indicating inflation rates that are significantly higher or lower than the rest of the data.
        
        - **Insight**: 
        - This visualization helps identify the central tendency and spread of the inflation rate.
        - By examining the box plot, you can quickly assess the variability and identify any extreme values in the data.
        - It provides a comprehensive view of how the inflation rate fluctuates over time, revealing any potential trends or anomalies.
        """
        st.markdown(explanation)





    #T4: Consumer Price Index
    with tab4:
        st.write("Consumer Price Index, short for CPI, is a measure that examines the average change in prices paid by consumers for goods and services over time. It is a key economic indicator used to assess a country's economic performance.")
        st.header("Malaysia's Consumer Price Index Over Time")
        #Time Series Line Plot
        cpi_line_fig = px.line(odf0, x=odf0.index, y='Consumer Price Index', title='Line Plot of Consumer Price Index Over Time')
        st.plotly_chart(cpi_line_fig)
        st.write("""
            **Graph Analysis:**
            - **Relationship**: This graph shows the relationship between the CPI of Malaysia and time period.
            - **Explanation**: 
                - The same behaviour can be seen in the CPI as in the GDP and Inflation Rate. The drop in 2020 suggests that the economy was affected by the COVID-19 pandemic.
            """)

        #Histogram
        cpi_hist_fig = px.histogram(odf0, x='Consumer Price Index', title='Histogram of Distribution of Consumer Price Index')
        st.plotly_chart(cpi_hist_fig)
        st.write("""
            **Graph Analysis:**
            - **Relationship**: This graph shows the distribution of Malaysia's Consumer Price Index.
            - **Explanation**: 
                - The histogram highlights the frequency of CPI values. The most common range of value for the CPI seems to be between 120 and 124 in Malaysia.
            """)





    #T5: YoY & QoQ GDP Growth
    with tab5:
        st.write("""YoY GDP Growth  is the percentage change in GDP from one period to the corresponding period in the previous year. 
                QoQ GDP Growth is the percentage change in GDP from one quarter to the next quarter.""")
        st.header("Malaysia's GDP Growth Over Time")
        #Time Series Line Plot YoY
        yoy_line_fig = px.line(odf0, x=odf0.index, y='YoY GDP Growth', title="Malaysia's Real Year-to-Year GDP Growth Over Time")
        st.plotly_chart(yoy_line_fig)
        st.write("""
            **Graph Analysis:**
            - **Relationship**: This graph  illustrates the percentage change in Malaysia's GDP compared to the same period in the previous year.
            - **Explanation**:
                - **Trends**: Upward trends indicating economic growth ;Downward trends indicating economic decline.
                - **Insight**: This helps identify long-term economic trends and the overall health of the economy over time.
        """)

        #Histogram YoY
        yoy_hist_fig = px.histogram(odf0, x='YoY GDP Growth', title='Distribution of Real Year-to-Year GDP Growth')
        st.plotly_chart(yoy_hist_fig)
        st.write("""
            **Graph Analysis:**
            - **Relationship**: This graph shows the distribution of Malaysia's real year-to-year GDP growth.
            - **Explanation**:
                - **Distribution**: Look for the spread and central tendency of the growth rates.
                - **Insight**: Helps identify common growth rates and the variability in economic performance.
        """)

        #Time Series Line Plot QoQ
        qoq_line_fig = px.line(odf0, x=odf0.index, y='QoQ GDP Growth', title="Malaysia's Real Quarter-to-Quarter GDP Growth Over Time")
        st.plotly_chart(qoq_line_fig)
        st.write("""
            **Graph Analysis:**
            - **Relationship**: This graph shows the percentage change in Malaysia's GDP from one quarter to the next.
            - **Explanation**:
                - The line plot tracks short-term economic changes on a quarterly basis.
                - **Trends**: Identify periods of rapid economic changes or stability within each year.
                - **Insight**: This provides a more granular view of economic performance compared to YoY growth.
        """)

        #Histogram QoQ
        qoq_hist_fig = px.histogram(odf0, x='QoQ GDP Growth', title='Distribution of Real Quarter-to-Quarter GDP Growth')
        st.plotly_chart(qoq_hist_fig)
        st.write("""
            **Graph Analysis:**
            - **Relationship**: This graph displays the frequency distribution of QoQ GDP growth rates.
            - **Explanation**:
                - **Distribution**: Understand the typical range and frequency of quarterly GDP changes.
                - **Insight**: This could assists in identifying periods of consistent economic performance or volatility within each year.
        """)




    #T6: Overall Analysis
    with tab6:
        st.write("The overall analysis of the economic indicators will be presented in the form of a scatter matrix and a correlation heatmap.")
        st.header("Overall Analysis of Economic Indicators")
        #Scatter Matrix
        pair_fig = px.scatter_matrix(odf0, title='Scatter Matrix of Economic Indicators')
        st.plotly_chart(pair_fig)
        st.write("""
                **Graph Analysis:**
                - **Relationship**: This scatter matrix shows the relationship between pairs of economic indicators.
                - **Explanation**: 
                    - The **scatter matrix** includes scatter plots for each pair of indicators, helping to visualize potential correlations.
                    - **Relationships**: Look for patterns such as linear relationships, clusters, or outliers.
                    - **Insight**: Identifies how different economic variables interact with each other, revealing potential dependencies or independent behaviors.
        """)

        #Correlation Heatmap
        correlation_matrix = odf0.corr()
        heatmap_fig = px.imshow(correlation_matrix,labels=dict(color="Correlation"), title='Correlation Heatmap of Economic Indicators', text_auto=True)
        st.plotly_chart(heatmap_fig)
        st.write("""
            **Graph Analysis:**
            - **Relationship**: This heatmap shows the correlation coefficients between different economic indicators.
            - **Explanation**:
                - Positive values (closer to 1) indicate a positive correlation: as one variable increases, the other tends to increase.
                - Negative values (closer to -1) indicate a negative correlation: as one variable increases, the other tends to decrease.
                - Values close to 0 suggest little to no linear relationship.
                - **Insight**: Helps identify strongly correlated pairs of indicators, which can be crucial for economic analysis and forecasting.
                - **Example**: If the correlation between the Unemployment Rate and Consumer Price Index is -0.3189, it means that as the unemployment rate increases, the consumer price index tends to decrease slightly, suggesting an inverse relationship.
        """)





    #T7: Machine Learning Model
    with tab7:
        warnings.filterwarnings("ignore")
        df = pd.read_csv('C:/zhengyang/Inti/BCSCUN/Sem 6/Big Data/cleaned_dataset/cleaned_monthlyecon_19-22.csv')

        # ADF Test for stationarity
        def adf_test(series, title=''):
            result = adfuller(series)
            print((f'ADF Statistic for {title}: {result[0]}'))
            st.write(f'p-value for {title}: {result[1]}')
            return result[1]

        def run_auto_arima(df):
            model = auto_arima(df['Unemployment Rate'], trace=True, suppress_warnings=True)
            print(model.summary())
            return model

        #run_auto_arima(df)

        st.write("""
        ### ARIMAX Machine Learning Model
        ARIMAX stands for AutoRegressive Integrated Moving Average with Exogenous variables. 
        This model is used to predict a time series by incorporating both its own past values (AutoRegressive part), 
        the past forecast errors (Moving Average part), and other external variables (Exogenous part).
        """)
        st.header("2023 Forecast for Unemployment Rate with ARIMAX Models")
        st.write("""
        #### Explanation of Parameters:
        - **p**: Number of lag observations included in the model (lag order).
        - **d**: Number of times that the raw observations are differenced (degree of differencing).
        - **q**: Number of lagged forecast errors in the prediction equation (order of moving average).
        """)

        # Keep only numeric columns for differencing
        numeric_df = df.select_dtypes(include=[np.number])

        # Handle missing values if any
        df.fillna(method='ffill', inplace=True)

        # First Order Differencing
        df_diff = numeric_df.diff().dropna()

        st.subheader("Stationarity Test for p-values After Differencing (d=1)")

        # Check stationarity after differencing
        p_value_unemployment = adf_test(df_diff['Unemployment Rate'], 'Unemployment Rate')
        p_value_inflation = adf_test(df_diff['Inflation Rate'], 'Inflation Rate')
        p_value_cpi = adf_test(df_diff['Consumer Price Index'], 'Consumer Price Index')
        p_value_yoy = adf_test(df_diff['YoY GDP Growth'], 'Real Year-on-Year GDP Growth')
        p_value_qoq = adf_test(df_diff['QoQ GDP Growth'], 'Real Quarter-on-Quarter GDP Growth')
        p_value_gdp = adf_test(df_diff['GDP [RM, in billion]'], 'Real GDP')

        st.subheader("ACF and PACF Plots for Unemployment Rate (Determine value of p and q)")

        # Plot ACF and PACF for Unemployment Rate
        acf, axes = plt.subplots(1, 2, figsize=(30, 10))

        # ACF plot
        plot_acf(df_diff['Unemployment Rate'], ax=axes[0], title='ACF of Unemployment Rate')
        plot_pacf(df_diff['Unemployment Rate'], ax=axes[1], title='PACF of Unemployment Rate')
        st.pyplot(acf)
        st.write("""
        The ACF (Autocorrelation Function) and PACF (Partial Autocorrelation Function) plots help to identify the appropriate lag for the ARIMA model.
        - **ACF plot**: Shows the correlation between the series and its lagged values. Significant lags at 0 and 1 suggest including these terms.
        - **PACF plot**: Shows the partial correlation between the series and its lagged values. Significant lags at 0, 1, and 2 suggest including these terms.
        This analysis suggests that the ARIMA model should have parameters (2,1,1).
        """)


        # Define the exogenous variables
        exog0 = df[['Inflation Rate', 'Consumer Price Index', 'GDP [RM, in billion]', 'YoY GDP Growth', 'QoQ GDP Growth']]
        exog1 = df_diff[['Inflation Rate', 'Consumer Price Index', 'GDP [RM, in billion]', 'YoY GDP Growth', 'QoQ GDP Growth']]

        # Ensure exogenous variables have the same index as the endogenous variable
        exog0 = exog0.loc[df.index]
        exog1 = exog1.loc[df_diff.index]

        # Fit the ARIMAX(2,1,1) model
        endog_211 = df.loc[exog1.index, 'Unemployment Rate']
        model_211 = SARIMAX(endog_211, order=(2, 1, 1), exog=exog1)
        results_211 = model_211.fit()

        # Fit the ARIMAX(1,0,1) model
        endog_101 = df.loc[exog0.index, 'Unemployment Rate']
        model_101 = SARIMAX(endog_101, order=(1, 0, 1), exog=exog0)
        results_101 = model_101.fit()

        # Fit the ARIMAX(0,1,1) model
        endog_011 = df.loc[exog0.index, 'Unemployment Rate']
        model_011 = SARIMAX(endog_011, order=(0, 1, 1), exog=exog0)
        results_011 = model_011.fit()

        # Make predictions for the next 12 months
        forecast_steps = 12
        forecast_index = pd.date_range(start=df.index[-1], periods=forecast_steps + 1, freq='M')[1:]

        forecast_211 = results_211.get_forecast(steps=forecast_steps, exog=exog1[-forecast_steps:])
        forecast_211_df = forecast_211.conf_int()
        forecast_211_df['forecast'] = forecast_211.predicted_mean

        forecast_101 = results_101.get_forecast(steps=forecast_steps, exog=exog0[-forecast_steps:])
        forecast_101_df = forecast_101.conf_int()
        forecast_101_df['forecast'] = forecast_101.predicted_mean

        forecast_011 = results_011.get_forecast(steps=forecast_steps, exog=exog0[-forecast_steps:])
        forecast_011_df = forecast_011.conf_int()
        forecast_011_df['forecast'] = forecast_011.predicted_mean

        # Combine predictions
        forecast_211_df['model'] = 'ARIMAX(2,1,1)'
        forecast_101_df['model'] = 'ARIMAX(1,0,1)'
        forecast_011_df['model'] = 'ARIMAX(0,1,1)'

        # Plot the forecast
        fig = go.Figure()

        # Actual Unemployment Rate
        fig.add_trace(go.Scatter(x=df.index, y=df['Unemployment Rate'], mode='lines', name='Actual Unemployment Rate', line=dict(color='blue')))

        # Forecasted Unemployment Rate - ARIMAX(2,1,1)
        fig.add_trace(go.Scatter(x=forecast_211_df.index, y=forecast_211_df['forecast'], mode='lines', name='Forecast Unemployment Rate - ARIMAX(2,1,1)', line=dict(color='green')))

        # Forecasted Unemployment Rate - ARIMAX(0,0,1)
        fig.add_trace(go.Scatter(x=forecast_211_df.index, y=forecast_101_df['forecast'], mode='lines', name='Forecast Unemployment Rate - ARIMAX(0,0,1)', line=dict(color='cyan')))

        # Forecasted Unemployment Rate - ARIMAX(0,1,1)
        fig.add_trace(go.Scatter(x=forecast_211_df.index, y=forecast_011_df['forecast'], mode='lines', name='Forecast Unemployment Rate - ARIMAX(0,1,1)', line=dict(color='red')))

        # Update layout
        fig.update_layout(
            title='Forecasted Unemployment Rate with ARIMAX Models',
            xaxis_title='Months Starting From 2019 Until Forecast Period(2023)',
            yaxis_title='Unemployment Rate',
            template='plotly_dark')

        # Display the plot
        st.plotly_chart(fig)
        st.write("Among the models tested, ARIMAX(0,1,1) was the best model as the forecast managed to match the actual data the closest.")

        # Ensure alignment with forecast indices starting from 48
        actual_values = df['Unemployment Rate'].iloc[48:]

        # Calculate errors with aligned data
        mae_211 = mean_absolute_error(actual_values, forecast_211_df['forecast'])
        mape_211 = mean_absolute_percentage_error(actual_values, forecast_211_df['forecast'])
        rmse_211 = np.sqrt(mean_squared_error(actual_values, forecast_211_df['forecast']))

        mae_101 = mean_absolute_error(actual_values, forecast_101_df['forecast'])
        mape_101 = mean_absolute_percentage_error(actual_values, forecast_101_df['forecast'])
        rmse_101 = np.sqrt(mean_squared_error(actual_values, forecast_101_df['forecast']))

        mae_011 = mean_absolute_error(actual_values, forecast_011_df['forecast'])
        mape_011 = mean_absolute_percentage_error(actual_values, forecast_011_df['forecast'])
        rmse_011 = np.sqrt(mean_squared_error(actual_values, forecast_011_df['forecast']))

        st.write(f"""
                **Model Evaluation Metrics:**
                - **ARIMAX(2,1,1)**
                    - MAE: {mae_211}
                    - MAPE: {mape_211}
                    - RMSE: {rmse_211}
                - **ARIMAX(1,0,1)**
                    - MAE: {mae_101}
                    - MAPE: {mape_101}
                    - RMSE: {rmse_101}
                - **ARIMAX(0,1,1)**
                    - MAE: {mae_011}
                    - MAPE: {mape_011}
                    - RMSE: {rmse_011}
                """)

        st.write("""
        These metrics help in understanding the accuracy of the models:
        - **Mean Absolute Error (MAE)**: Measures the average magnitude of errors in a set of forecasts, without considering their direction. Lower values indicate better fit.
        - **Mean Absolute Percentage Error (MAPE)**: Expresses the accuracy as a percentage of the error. Lower percentages are better.
        - **Root Mean Square Error (RMSE)**: Measures the square root of the average squared differences between predicted and actual values. It is more sensitive to large errors. Lower values indicate a better fit.
        """)

if __name__ == "__main__":
    main()