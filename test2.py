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

#Ignore warnings
warnings.filterwarnings("ignore")

df = pd.read_csv('C:/Users/Joe Shen/Downloads/cleaned_monthlyecon_19-22.csv')

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

st.write("ARIMAX Machine Learning Model")
st.header("2023 Forecast for Unemployment Rate with ARIMAX Models")

# Keep only numeric columns for differencing
numeric_df = df.select_dtypes(include=[np.number])

# Handle missing values if any
df.fillna(method='ffill', inplace=True)

# First Order Differencing
df_diff = numeric_df.diff().dropna()

st.subheader("Stationarity Test for p-values After Differencing")
# Check stationarity after differencing
p_value_unemployment = adf_test(df_diff['Unemployment Rate'], 'Unemployment Rate')
p_value_inflation = adf_test(df_diff['Inflation Rate'], 'Inflation Rate')
p_value_cpi = adf_test(df_diff['Consumer Price Index'], 'Consumer Price Index')
p_value_yoy = adf_test(df_diff['YoY GDP Growth'], 'Real Year-on-Year GDP Growth')
p_value_qoq = adf_test(df_diff['QoQ GDP Growth'], 'Real Quarter-on-Quarter GDP Growth')
p_value_gdp = adf_test(df_diff['GDP [RM, in billion]'], 'Real GDP')


st.subheader("ACF and PACF Plots for Unemployment Rate")

# Plot ACF and PACF for Unemployment Rate
acf, axes = plt.subplots(1, 2, figsize=(30, 10))

# ACF plot
plot_acf(df_diff['Unemployment Rate'], ax=axes[0], title='ACF of Unemployment Rate')
plot_pacf(df_diff['Unemployment Rate'], ax=axes[1], title='PACF of Unemployment Rate')
st.pyplot(acf)

st.write("The ACF and PACF plots outlines the lag for determining the value of p and q in the ARIMA model. \
         The ACF plot shows a significant lag at 0,1, while the PACF plot shows a significant lag at 0,1,2 as well. \
         This suggests that the ARIMA model should have parameters of (2,1,1).")


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
        MAE for ARIMAX(2,1,1): {mae_211} \
         
        MAPE for ARIMAX(2,1,1): {mape_211} \
        
        RMSE for ARIMAX(2,1,1): {rmse_211} \
         \n                                   
        MAE for ARIMAX(0,0,1): {mae_101}   \
        
        MAPE for ARIMAX(0,0,1): {mape_101} \
        
        RMSE for ARIMAX(0,0,1): {rmse_101} \
         \n                                 
        MAE for ARIMAX(0,1,1): {mae_011}   \
        
        MAPE for ARIMAX(0,1,1): {mape_011} \
        
        RMSE for ARIMAX(0,1,1): {rmse_011}""")
      