# Import necessary libraries
from pymongo import MongoClient
import pandas as pd
from datetime import datetime

# Load the data from an Excel file into a DataFrame
missing_countries_df = pd.read_excel(r'.\airline_missing_countries.xlsx')

# Define the MongoDB connection string
MONGODB_URI = 'mongodb+srv://nosqlg2:lambtoncollege@cluster0.ffdl0mq.mongodb.net/?retryWrites=true&w=majority&charset=utf8'

# Create a MongoClient object
client = MongoClient(MONGODB_URI)

# Access the 'airlines' database
db = client.airlines

# Access the 'reviews' collection within the database
reviews_collection = db.reviews

# Initialize an empty list to store the changes
changes = []

# Iterate over documents in the 'reviews' collection with missing 'country' field
for document in reviews_collection.find({'country': None}):
    # Check if there are any matching rows in the DataFrame
    matching_rows = missing_countries_df[missing_countries_df['Airline'] == document['airline']]
    
    # If there are matching rows, retrieve the country from the first matching row
    if not matching_rows.empty:
        country = matching_rows['Country'].values[0]
        
        # Append the changes to the 'changes' list
        changes.append([document['_id'], document['airline'], country])

# Print the current time before starting the update operations
print(datetime.now())

# Iterate over the changes
for value in changes:
    # Update the 'country' field of the document with the corresponding '_id'
    reviews_collection.update_one({'_id': value[0]}, {'$set': {'country': value[2]}})

# Print the current time after completing the update operations
print(datetime.now())


 