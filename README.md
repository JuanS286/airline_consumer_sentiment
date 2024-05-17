# Airline Passenger Satisfaction Analysis

## Project Overview
This project involves the analysis of passenger satisfaction surveys from airlines around the world. The dataset used consists of numerical ratings and textual feedback from passengers, collected from the Airline Quality and Centre For Aviation websites. The main goals were to analyze trends in customer satisfaction over time and compare satisfaction levels across different regions.

## Hypotheses
1. As time progresses, customer satisfaction with airlines' quality of service decreases.
2. Customer satisfaction levels vary significantly based on the country of the airline, with European airlines expected to have higher ratings.

## Tools and Technologies
- **Web Scraping**: `requests`, `BeautifulSoup`, `re`, `datetime`, `pandas`, `pymongo`
- **Data Cleaning and Processing**: `MongoDB`, `pandas`, `VADER` sentiment analysis
- **Data Visualization**: `Tableau`

## Data Collection and Processing
1. **Data Collection**:
    - Data was collected from the [Airline Quality](https://www.airlinequality.com/review-pages/latest-airline-reviews/) and [Centre For Aviation](https://centreforaviation.com/data/profiles) websites.
    - Web scraping techniques were used to gather reviews and country information for various airlines.

2. **Data Cleaning**:
    - Missing values and inconsistent data entries were handled using `pandas` and `MongoDB` commands.
    - Sentiment analysis was performed using the VADER library to categorize feedback as positive, neutral, or negative.

3. **Data Processing**:
    - Data was structured and stored in a MongoDB database.
    - Additional features like identifying stopovers in routes and categorizing traveler types were implemented.

## Visualizations
Several visualizations were created using Tableau to present the data analysis effectively:
1. **Statistics by Country**: An interactive map displaying satisfaction statistics by country.
2. **Average Rating per Airline**: A bar chart showing average customer satisfaction ratings for different airlines.
3. **Average Rating per Type of Cabin**: A comparison of satisfaction levels across different cabin types.
4. **Pie Chart for Airline Recommendations**: A pie chart illustrating the percentage of recommendations versus non-recommendations.
5. **Average Rating per Type of Traveler**: Satisfaction ratings based on different traveler types (e.g., solo, couple, family).
6. **Average Rating per Year**: Trends in customer satisfaction over time.
7. **Sentiment Analysis**: Sentiment trends over time to assess the emotional tone of passenger feedback.

## Results and Conclusions
1. **Hypothesis 1**: Disproved. Customer satisfaction has decreased over time, with negative ratings increasing and positive ratings decreasing year by year.
2. **Hypothesis 2**: Confirmed. There is a significant variation in customer satisfaction based on the airline's country, with Asian airlines generally receiving higher ratings.

## References
- [Airline Quality](https://www.airlinequality.com/review-pages/latest-airline-reviews/)
- [Centre For Aviation](https://centreforaviation.com/data/profiles)

