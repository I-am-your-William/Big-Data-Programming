# Step 1: Import necessary libraries
import pandas as pd
from pymongo import MongoClient

# Step 2: Load the CSV data into a DataFrame
df = pd.read_csv('C:/Users/choon/Documents/Chi Ling/BCSCUN/Big Data/Project/cases_state.csv')

# Step 3: Drop the specified columns
columns_to_drop = [
    'cases_unvax', 'cases_pvax', 'cases_fvax', 'cases_boost', 
    'cases_0_4', 'cases_5_11', 'cases_12_17', 'cases_18_29', 
    'cases_30_39', 'cases_40_49', 'cases_50_59', 'cases_60_69', 
    'cases_70_79', 'cases_80'
]
df = df.drop(columns=columns_to_drop)

# Display the first few rows of the cleaned DataFrame
print(df.head())
print(df.isnull().sum()) 

# Step 4: Drop rows with any missing values
df = df.dropna()

# Save the cleaned DataFrame locally
output_file_path = 'C:/Users/choon/Documents/Chi Ling/BCSCUN/Big Data/Project/cleaned_cases_state.csv'
df.to_csv(output_file_path, index=False)
print(f"Cleaned data saved to {output_file_path}")

# Step 5: Connect to MongoDB
client = MongoClient('localhost', 27017)
db = client['CovidImpactNavigator']  # Use or create a database named 'CovidImpactNavigator'
collection = db['cases_state']  # Use or create a collection named 'cases_state'

# Step 6: Insert the cleaned data into MongoDB
# Convert DataFrame to dictionary format
data_dict = df.to_dict('records')

# Insert the data into the MongoDB collection
collection.insert_many(data_dict)

print("Data successfully inserted into MongoDB!")

# Verify by retrieving one document
print(collection.find_one())