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
def scrape_team_gamelog(base_url, seasons):
    all_data = pd.DataFrame()
    
    for season in seasons:
        schools = getSchoolList(season)
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
def getSchoolList(season, urlNeeded): # urlNeeeded is for when you need the school names to be changed for the url
    url = f'https://www.sports-reference.com/cbb/seasons/men/{season}-school-stats.html'
    print(f"Scraping for school list for season {season}")
    tables = pd.read_html(url, header=[1])
    
    # Extract the 'School' column and drop all Nan values
    schools_df = (tables[0][tables[0].columns[1]]).dropna()

    # Convert to list
    school_list = schools_df.tolist()
    
    if urlNeeded:
        # Apply the formatting function to the school names if using for url
        school_list = [format_school_name(school) for school in school_list]
    
    # Remove 'school' from list (scrape grabs the 'school' headers)
    school_list = [school for school in school_list if school.lower() != 'school']
    
    # Random delay between 3 and 6 seconds to avoid detection and keep within limits
    time.sleep(random.randint(3, 6))
    
    print("Done scraping for school list, season {season}.")
    
    return school_list

#%% Function to format school names for the url
def format_school_name(school):
    # Past seasons have ncaa in them for some teams
    school = school.replace('\xa0NCAA','')
    school = school.replace('(','')
    school = school.replace(')','')
    school = school.replace(' ', '-')
    school = school.replace('&','')
    school = school.replace("'","")
    school = school.replace('.','')
    
    # Random school changes in their url
    school = school.replace('east-texas-am', 'texas-am-commerce')
    school = school.replace('fdu','fairleigh-dickinson')
    school = school.replace('houston-christian','houston-baptist')
    school = school.replace('iu-indy','iupui')
    school = school.replace('kansas-city', 'missouri-kansas-city')
    school = school.replace('little-rock','arkansas-little-rock')
    school = school.replace('louisiana','louisiana-lafayette')
    school = school.replace('nc-state','north-carolina-state')
    school = school.replace('omaha','nebraska-omaha')
    school = school.replace('purdue-fort-wayne','ipfw')
    school = school.replace('sam-houston','sam-houston-state')
    school = school.replace('siu-edwardsville','southern-illinois-edwardsville')
    school = school.replace('st-thomas','st-thomas-mn')
    school = school.replace('tcu','texas-christian')
    school = school.replace('texas-rio-grande-valley','texas-pan-american')
    school = school.replace('the-citadel','citadel')
    school = school.replace('uab','alabama-birmingham')
    school = school.replace('uc-davis','california-davis')
    school = school.replace('uc-irvine','california-irvine')
    school = school.replace('uc-riverside','california-riverside')
    school = school.replace('uc-san-diego','california-san-diego')
    school = school.replace('uc-santa-barbara','california-santa-barbara')
    school = school.replace('ucf','central-florida')
    school = school.replace('unc-asheville','north-carolina-asheville')
    school = school.replace('unc-greensboro','north-carolina-greensboro')
    school = school.replace('unc-wilmington','north-carolina-wilmington')
    school = school.replace('ut-arlington','texas-arlington')
    school = school.replace('utah-tech','dixie-state')
    school = school.replace('utep','texas-el-paso')
    school = school.replace('utsa','texas-san-antonio')
    school = school.replace('vmi','virginia-military-institute')
    school = school.replace('william--mary','william-mary')
    school = school.replace('','')
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

print("Finished scraping and creating overall data dataframes.")

##### Now scrape team gamelogs #####

# scrape function
all_teams_logs = scrape_team_gamelog(base_url, seasons)

# Get data frames for each season
df_list = []
for season in seasons:
    schools = getSchoolList(season, urlNeeded=True)
    for school in schools:
        season_df = all_teams_logs[all_teams_logs['Season'] == season]
        school_df = season_df[season_df['School'] == school]
        # Save to csv
        school_df.to_csv(f'DataFrames/Team-Gamelogs/{season}/{school}-gamelogs.csv')
    print(f'Done saving season {season} to csv.')
        
print("Finished scraping and creating dataframes for all team gamelogs.")







