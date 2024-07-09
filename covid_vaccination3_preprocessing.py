import pandas as pd
from pymongo import MongoClient

df = pd.read_csv('C:/Users/choon/Documents/Chi Ling/BCSCUN/Big Data/Project/vax_state.csv')

# Drop the specified columns
columns_to_drop = [
 'pending1', 'pending2', 'pending3', 'pending4',
 'cumul_partial', 'cumul_full', 'cumul_booster', 'cumul_booster2', 'cumul',
    'cumul_partial_adol', 'cumul_full_adol', 'cumul_booster_adol', 'cumul_booster2_adol',
    'cumul_partial_child', 'cumul_full_child', 'cumul_booster_child', 'cumul_booster2_child'
]

df = df.drop(columns=columns_to_drop)

print(df.isnull().sum()) # Check for missing values

df = df.dropna()

output_save_path = 'C:/Users/choon/Documents/Chi Ling/BCSCUN/Big Data/Project/vax_state_cleaned.csv'
df.to_csv(output_save_path, index=False)
