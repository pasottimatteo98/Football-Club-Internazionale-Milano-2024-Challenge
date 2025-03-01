# Football Player Analysis Project

## Overview
This project involves the analysis of football players' statistics, with a particular focus on defenders. The data is collected from multiple sources including FBref, Kickest, and WhoScored, then processed, cleaned, and analyzed using various machine learning techniques to identify players with similar characteristics to a specific target player (Francesco Acerbi).

## Project Structure

### Data Retrieval
The project begins with data collection from three main sources:
- `fbref.py`: Scrapes player statistics from FBref.com, focusing on defenders
- `kickest.py`: Extracts data from Kickest.it for different seasons and performance categories
- `whoscored.py`: Gathers defensive statistics from WhoScored.com for various Serie A teams

### Data Preparation
The collected data is processed and combined in the preparation phase:
- `fbref_data_preparation.py`: Processes raw FBref data, corrects player names, and aggregates statistics
- `kickest_data_preparation.py`: Combines and aggregates Kickest data from different seasons and categories
- `whoscored_data_preparation.py`: Cleans and aggregates WhoScored defensive data

### Data Modeling
Multiple modeling approaches are implemented to find players similar to Francesco Acerbi:
- `autoencoder.py`: Implements an autoencoder neural network for dimensionality reduction and similarity analysis
- `clustering.py`: Uses K-means clustering to group players based on similar characteristics
- `distance.py`: Calculates Euclidean distances between players for direct similarity comparison
- `knn.py`: Implements K-nearest neighbors algorithm to find the most similar players

### Data Visualization
Results are visualized for easy interpretation:
- Generated HTML files for each modeling technique
- Interactive visualizations highlighting players similar to Acerbi
- Comparative analysis across different statistical categories

## Key Features
- Multi-source data integration from leading football statistics providers
- Comprehensive player statistics covering defensive abilities, passing, technical skills, and more
- Multiple modeling approaches providing different perspectives on player similarity
- Interactive visualizations for better understanding of player comparisons
- Categorized analysis by performance areas (Defensive Actions, Passing, Technical Skills, etc.)

## Technical Stack
- Python for data retrieval, processing and analysis
- Selenium and BeautifulSoup for web scraping
- Pandas for data manipulation
- Scikit-learn for clustering and KNN models
- TensorFlow for autoencoder implementation
- Plotly for interactive visualizations

## How It Works
1. Data is collected from multiple sources using web scraping techniques
2. The raw data is processed, cleaned, and aggregated into a unified dataset
3. Various machine learning models analyze the data to find players with similar characteristics to Acerbi
4. Results are visualized through interactive charts and graphs
5. Different statistical categories are analyzed separately to provide a comprehensive similarity assessment

## Results
The analysis provides lists of players most similar to Francesco Acerbi across different statistical categories, offering valuable insights for scouting and team composition decisions.
