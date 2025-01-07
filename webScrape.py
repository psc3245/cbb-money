# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 16:24:07 2024

@author: Logmo
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import random

#%% Scraping web function
def scrape_cbb(url):
    print(f"Scraping: {url}")
    try:
        # Get list of tables
        df = pd.read_html(url, header=[1])
        
        # Turn to dataframe
        df = df[0]
        
        return df
   
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

#%% Create function to go through each season
def scrape_seasons(base_url, seasons):
    all_data = pd.DataFrame()
    
    for season in seasons:
        url = f"{base_url}/seasons/{season}-school-stats.html"
        df = scrape_cbb(url)
        
        if df is not None:
            df['Season'] = season
            all_data = pd.concat([all_data, df], ignore_index=True)
        
        # Random delay between 3 and 6 seconds to avoid detection and keep within limits
        time.sleep(random.randint(3, 6))
        
    return all_data

#%% Create function to get each teams wins and losses data
def scrape_team_gamelog(base_url, seasons, schools):
    all_data = pd.DataFrame()
    
    for season in seasons:
        for school in schools:
            url = f"{base_url}/schools/{school}/men/{season}-gamelogs.html"
            df = scrape_cbb(url)    
            
            if df is not None:
                df['Season'] = season
                df['School'] = school
                all_data = pd.concat([all_data, df], ignore_index=True)
                
            # Random delay between 3 and 6 seconds to avoid detection and keep within limits
            time.sleep(random.randint(3, 6))
    
    return all_data
    
#%% Cleaning function (data should be clean?)
def cleanSeasonData(url):
    if (cbb_data.isnull.values.any()):
        print("Null values appear.")
    else:
        print("No null values appear.")
#%% Function to get list of all schools
def getSchoolList():
    url = 'https://www.sports-reference.com/cbb/seasons/men/2025-school-stats.html'
    print(f"Scraping: {url}")
    tables = pd.read_html(url, header=[1])
    
    # Extract the 'School' column and drop all Nan values
    schools_df = (tables[0][tables[0].columns[1]]).dropna()

    # Apply the formatting function to the school names
    school_list = [format_school_name(school) for school in schools_df.tolist()]
    
    # Remove 'school' from list (scrape grabs the 'school' headers)
    school_list = [school for school in school_list if school.lower() != 'school']
    
    return school_list

#%% Function to format school names for the url
def format_school_name(school):
    school = school.replace('East Texas A&M', 'texas-am-commerce')
    school = school.replace('(','')
    school = school.replace(')','')
    school = school.replace(' ', '-')
    school = school.replace('&','')
    school = school.replace("'","")
    school = school.replace('.','')
    school = school.lower()
    return school
        
#%% Run scrape function

# BASE URL
base_url = "https://www.sports-reference.com/cbb"

# For now use seasons 2022, 2023, 2024, 2025
seasons = [2022,2023,2024,2025]

##### Scrape overall cbb data #####

cbb_data = scrape_seasons(base_url, seasons)

## Get data frames for each season
df_list = []
for season in seasons:
    season_df = cbb_data[cbb_data['Season'] == season]
    # Save to csv (could save to variable here but think its redundant)
    season_df.to_csv(f'DataFrames/Overall-Data/{season}_stats.csv')

print("Finished scraping overall data.")

##### Now scrape team gamelogs #####

# Get list of schools
schools = getSchoolList()

# scrape function
all_teams_logs = scrape_team_gamelog(base_url, seasons, schools)

# Get data frames for each season
df_list = []
for season in seasons:
    for school in schools:
        season_df = all_teams_logs[all_teams_logs['Season'] == season]
        school_df = season_df[season_df['School']]
        # Save to csv
        season_df.to_csv(f'DataFrames/Team-Gamelogs/{season}/{school}-gamelogs.csv')
        
print("Finished scraping team gamelogs")







