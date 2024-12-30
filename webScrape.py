# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 16:24:07 2024

@author: Logmo
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

#%% Scraping web function
def scrape_cbb(url):
    print(f"Scraping: {url}")
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve {url} - Status Code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'id': 'basic_school_stats'})

    if not table:
        print(f"No table found on {url}")
        return None

    # Extract headers from <thead>
    headers = [th.text.strip() for th in table.find('thead').find_all('th')]

    # Extract rows from <tbody>
    rows = []
    for row in table.find('tbody').find_all('tr'):
        cols = [td.text.strip() for td in row.find_all(['th', 'td'])]
        
        # Ensure the number of columns matches the header length
        if len(cols) != len(headers):
            while len(cols) < len(headers):
                cols.append('')

        rows.append(cols)

    # Convert to DataFrame
    df = pd.DataFrame(rows, columns=headers)
    return df


#%% Create function to go through each season
def scrape_seasons(base_url, seasons):
    all_data = pd.DataFrame()
    
    for season in seasons:
        url = f"{base_url}/{season}-school-stats.html"
        df = scrape_cbb(url)
        
        if df is not None:
            df['Season'] = season
            all_data = pd.concat([all_data, df], ignore_index=True)
        
        
        time.sleep(3) # For rate limits on sports-reference
        
    return all_data

#%% Create function to go through every team for certain season (alphabetical order)


#%% Create function to go through each conference for certain season


#%% Create function to go through each team for certain conference

#%% Run scrape function

# BASE URL
base_url = "https://www.sports-reference.com/cbb/seasons/"

# For now use seasons 2022, 2023, 2024
seasons = [2022,2023,2024]

# Scrape cbb data
cbb_data = scrape_seasons(base_url, seasons)
cbb_data.to_csv('cbb_stats.csv', index=False)

print(cbb_data.head())

#%% Testing and what not








