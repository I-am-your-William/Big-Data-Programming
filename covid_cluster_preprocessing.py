# Step 1: Import necessary libraries
import pandas as pd # For data manipulation and analysis
from pymongo import MongoClient

# Step 2: Load the CSV data into a DataFrame
df = pd.read_csv('C:/Users/choon/Documents/Chi Ling/BCSCUN/Big Data/Project/clusters.csv')

# Step 3: Drop the specified columns
columns_to_drop = [ 'date_last_onset','state','status','cases_new',
                   'cases_active', 'tests','recovered', 'icu','deaths',
                   'summary_bm', 'summary_en'
]

df = df.drop(columns=columns_to_drop)

# Display the first few rows of the cleaned DataFrame
print(df.head())
print(df.isnull().sum()) 

# Step 4: Drop rows with any missing values
df = df.dropna()


# Save the cleaned DataFrame locally
output_file_path = 'C:/Users/choon/Documents/Chi Ling/BCSCUN/Big Data/Project/cleaned_cluster.csv'
df.to_csv(output_file_path, index=False)
print(f"Cleaned data saved to {output_file_path}")

# Step 5: Connect to MongoDB
client = MongoClient('localhost', 27017)
db = client['CovidImpactNavigator']  # Use or create a database named 'CovidImpactNavigator'
collection = db['cluster']  # Use or create a collection named 'cases_state'

# Step 6: Insert the cleaned data into MongoDB
# Convert DataFrame to dictionary format
data_dict = df.to_dict('records')

# Insert the data into the MongoDB collection
collection.insert_many(data_dict)

print("Data successfully inserted into MongoDB!")

# Verify by retrieving one document
print(collection.find_one())