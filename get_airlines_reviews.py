# Importing required modules
import requests
from bs4 import BeautifulSoup

import re
from datetime import datetime

import pandas as pd

from pymongo import MongoClient

MONGODB_URI = 'mongodb+srv://nosqlg2:lambtoncollege@cluster0.ffdl0mq.mongodb.net/?retryWrites=true&w=majority'

client = MongoClient(MONGODB_URI)

db = client.airlines
reviews_collection = db.reviews

# Get the total number of reviews
def totReviews():
    # Find all <div> elements on the page 
    alldivs = soup.findAll('div')
    # Select the first <div> element from the list and finds all the nested <div> elements inside it
    divs = alldivs[0].findAll('div')

    # It iterates over the nested <div> elements and checks if the span tag with the attribute itemprop set to 'reviewCount' exists
    for oned in divs:
        COpinions = oned.find('span',{'itemprop': 'reviewCount'})
        # If it does not exist (str(COpinions) == 'None'), it sets the COpinions variable to 0.
        if str(COpinions) == 'None':
            COpinions = 0
        # If the span tag exists, it retrieves the text value of that element and assigns it to COpinions
        else:
            COpinions = oned.find('span',{'itemprop': 'reviewCount'}).text 
            # The loop breaks after finding the first occurrence of the span tag, because it represents the total review count
            break; 
    COpinions=int(COpinions)

    #The function returns the total number of reviews as an integer
    return COpinions

# Get a list of dictionaries representing the rating records for that airline
def getRatingRecords(airline):
    # Empty list data to store the rating records
    data = []

    # Finds all <article> elements on the page
    allarticles = soup.findAll('article')
    # selects the first <article> element from the list and finds all the nested <article> elements inside
    articles = allarticles[0].findAll('article')
 
    # Iteration over the nested <article> elements
    for one in articles:
        # Here a dictionary is created for every article element to store the record information
        record = {}
        
        # Here it adds the airline name in the airlane key
        record['airline'] = airline
        
        # Get the overall raiting value
        overallRating = one.find('span',{'itemprop': 'ratingValue'})
            
        if overallRating is not None:
            record['ratingValue'] = int(overallRating.text)
                
        # Getting the name of the review's author
        # record['author'] = one.find('span',{'itemprop': 'name'}).text.strip()

        # Getting the date of the review
        tempdate = one.find('time',{'itemprop': 'datePublished'}).text  # Get the date as text
        tempdate = re.sub(r'(\d)(st|nd|rd|th)', r'\1', tempdate)    # Replace a pattern with something else that we can use to set the date
        date_time_obj = datetime.strptime(tempdate, '%d %B %Y')        # Set the date as a datetime object
        record['datePublished'] = date_time_obj     # Adding the date to the dictionary

        # Getting the text of the review and the verification
        tmptext = one.find('div',{'class': 'text_content'}).text
        # Split the text to divide the verification and the text review parts
        text = tmptext.split('|')
        # If there is a review text
        if len(text)>1:
            textindex=1
            verifyindex=0
        # If there is not a reviw text
        else:
            textindex=0 
            verifyindex=-1
        record['reviewText'] = text[textindex].strip()

        ## Here the information in the little table with stars and other information is retrieved
        
        # Iterates over each <tr> element within the <article> element to extract ratings for different aspects
        for element in one.find_all('tr'):
            # Identifies the rating category from the class of the first <td> and extracts the second element that has the element name
            rating_element = element.find_all('td')[0]['class'][1]
            # Identifies the number of stars counting the element 'class': 'star fill'
            stars = len(element.find_all('span',{'class': 'star fill'}))

            # Taking the information that is in text format (Aircraft, Type of traveler ...etc), don't considering the stars
            if stars == 0:
                rating_value = (element.find_all('td')[1]).text
                record[rating_element] = rating_value.strip()
            # Taking the number of stars in the parameters that counts stars
            else:
                record[rating_element] = int(stars)
        
        if 'route' in record:
                                 
            # Getting the departure and arrival values and if there was a scale
            if ' to ' in record['route']:
                record['departure_city'] = record['route'].split(" to ")[0].strip()
                if len(record['route'].split(" to "))>1:
                    record['arrival_city'] = record['route'].split(" to ")[1].split(' via ')[0].strip()                
                
            if 'via' in record['route'].split():                
                record['scale'] = True
                
            else:
                record['scale'] = False
                
            # Getting the country name
            if airline in airlines_country['name'].values:
                country = airlines_country.loc[airlines_country['name'] == airline, 'country'].values[0]
                record['country'] = country     
        
        reviews_collection.insert_one(record)       

# Get the airline name from the CSV in folder
airlines_list = pd.read_csv(r".\airlines.csv")

# Get the airline country from the CSV in folder
airlines_country = pd.read_csv(r".\airlines_country.csv")

# Define the User-Agent string. The User-Agent header is used in the HTTP request to simulate a web browser
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

# Print the time that the code starts to run
print(datetime.now())

# Iterate over the airline list (name, URL)
for i, j in airlines_list.iterrows():
    
    # Get the URL from the csv that now is a dataframe
    cur_url = j['URL'] 

    # sends an HTTP GET request to the cur_url using requests.get() 
    # and passes the headers dictionary to simulate a web browser
    response = requests.get(cur_url, headers=headers)

    # Creating a BeautifulSoup object soup by parsing the HTML content of the response
    soup = BeautifulSoup(response.text, "html.parser")

    # Get the total number of reviews calling the function
    tot_reviews=totReviews()
    
    # Set the total reviews per page as 100 if there are more than 20 reviews
    if tot_reviews>=20:
        tot_rev_per_page=100
    else:
        tot_rev_per_page=10 # looks like there is abug sometimes wher there are few reviews

    # Defines the maximum number of pages that it needs to look at
    tot_pages=tot_reviews//tot_rev_per_page + 1

    # Iterates over every page of the current airline
    for npag in range(1,tot_pages+1):
        # Construction of every URL
        urlpostf='/page/'+ str(npag) +'/?sortby=post_date%3ADesc&pagesize='+ str(tot_rev_per_page)
        cur_url = j['URL'] + urlpostf
        
        # Making a request to the URL
        response = requests.get(cur_url, headers=headers)

        # Parsing all the HTML content in the object soup
        soup = BeautifulSoup(response.text, "html.parser")

        # Extracting the information with the getRatingRecords function
        #Bdata=Bdata + getRatingRecords(j['AirLine'])
        getRatingRecords(j['AirLine'])

client.close()

# Print the date time now to know how long it took
print(datetime.now())


