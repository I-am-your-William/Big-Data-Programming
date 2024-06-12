import pandas as pd

# Load the dataset
df = pd.read_csv('C:/Users/choon/Documents/Chi Ling/BCSCUN/Big Data/Project/cases_malaysia.csv')

column_to_drop=  [
    'cases_unvax', 'cases_pvax', 'cases_fvax', 'cases_boost','cases_child' ,'cluster_import', 
    'cluster_religious', 'cluster_community', 'cluster_highRisk', 'cluster_education', 'cluster_detentionCentre', 'cluster_workplace', 
    'cases_new', 'cases_import', 'cases_recovered', 'cases_cluster', 
    'cases_0_4', 'cases_5_11', 'cases_12_17', 'cases_18_29', 
    'cases_30_39', 'cases_40_49', 'cases_50_59', 'cases_60_69', 
    'cases_70_79', 'cases_80'
]


# Drop the columns
df = df.drop(column_to_drop, axis=1)


# Display the first few rows
print(df.head())

# Display basic information about the DataFrame
print(df.info())

# Check for missing values
print(df.isnull().sum())
df = df.dropna()

# Save the cleaned DataFrame locally
output_file_path = 'C:/Users/choon/Documents/Chi Ling/BCSCUN/Big Data/Project/cleaned_cases_malaysia.csv'
df.to_csv(output_file_path, index=False)
print(f"Cleaned data saved to {output_file_path}")


from pymongo import MongoClient

# Create a connection to MongoDB
client = MongoClient('localhost', 27017)
db = client['CovidImpactNavigator']  # Use or create a database named 'CovidImpactNavigator'
collection = db['cases_malaysia']  # Use or create a collection named 'cases_state'

# Step 6: Insert the cleaned data into MongoDB
# Convert DataFrame to dictionary format
data_dict = df.to_dict('records')

# Insert the data into the MongoDB collection
collection.insert_many(data_dict)

print("Data successfully inserted into MongoDB!")

# Verify by retrieving one document
print(collection.find_one())

