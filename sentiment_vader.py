'''
Last update: 29/11/2023

Code modified to update documents in a bulk operation in order to avoid connection loses.

'''
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pymongo import MongoClient, UpdateOne
from datetime import datetime

client = MongoClient("mongodb+srv://nosqlg2:lambtoncollege@cluster0.ffdl0mq.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp")
db = client["airlines"]
collection = db["reviews"]

# Initialize Vader library
analyzer = SentimentIntensityAnalyzer()

# Find documents where reviewText is not equal to "" or null
filter_criteria = {"$and": [{"reviewText": {"$ne": ""}}, {"reviewText": {"$ne": None}}, {"sentimentConclusion": {"$eq": None}}]}
documents_to_update = collection.find(filter_criteria)
documents_count = collection.count_documents(filter_criteria)

if documents_count > 0:
    print(f"Documents available to analyze: {documents_count}.")
    # Specify the updates to apply
    updates = []

    for document in documents_to_update:
        vs = analyzer.polarity_scores(document["reviewText"])
        
        if vs['compound'] >= 0.05:
            conclusion = 'Positive'
        elif vs['compound'] > -0.05 and vs['compound'] < 0.05:
            conclusion = 'Neutral'
        else:
            conclusion = 'Negative'

        update_operation = UpdateOne(
            {"_id": document["_id"]},
            {"$set": {
                        "sentimentIndexNeg": vs['neg'],
                        "sentimentIndexNeu": vs['neu'],
                        "sentimentIndexPos": vs['pos'],
                        "sentimentIndexCom": vs['compound'],
                        "sentimentConclusion": conclusion,
                    }}
        )
        updates.append(update_operation)

    # Execute the update
    result = collection.bulk_write(updates)
    # Print the result
    print(f"Documents analyzed: {result.modified_count}.")
else:
    print("There is not more documents to analyze!")

# Close the MongoDB connection
client.close()