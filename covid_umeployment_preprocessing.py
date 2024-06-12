import pandas as pd

# Load the dataset
df = pd.read_csv('C:/Users/choon/Documents/Chi Ling/BCSCUN/Big Data/Project/global_unemployment_data.csv')  # Replace with the actual path to your file

# Display the first few rows
print(df.head())

# Display basic information about the DataFrame
print(df.info())

# Check for missing values
print(df.isnull().sum())

# Filter the DataFrame for Malaysia
df_malaysia = df[df['country_name'] == 'Malaysia']

# Display the first few rows of the filtered DataFrame
print(df_malaysia.head())


from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB connection string if different

# Create or connect to a database
db = client['CovidImpactNavigator']

# Create or connect to a collection
collection = db['MalaysiaUnemployment']

# Convert the DataFrame to a list of dictionaries for insertion into MongoDB
data_dict = df_malaysia.to_dict('records')

# Insert the filtered data into the MongoDB collection
collection.insert_many(data_dict)

print("Data successfully inserted into MongoDB!")

# Query the collection to verify the insertion
results = collection.find()

# Print the first few records to verify
for result in results.limit(5):
    print(result)
    
output_file_path = 'C:/Users/choon/Documents/Chi Ling/BCSCUN/Big Data/Project/cleaned_unemployment.csv'
df_malaysia.to_csv(output_file_path, index=False)
print(f"Cleaned data saved to {output_file_path}")