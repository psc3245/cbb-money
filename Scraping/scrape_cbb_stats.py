# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 16:24:07 2024

@author: Logmo
"""

import pandas as pd
import time
import random


#%% RUN FIRST
# BASE URL
base_url = "https://www.sports-reference.com/cbb"

# For now use seasons 2022, 2023, 2024, 2025
seasons = [2022,2023,2024,2025]
#%% Scraping web function
def scrape_cbb(url):
    print(f"Scraping: {url}")
    try:
        # Returns list of tables (In our case there is one table)
        df = pd.read_html(url, header=[1])
        
        # Get first table
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
        df = cleanSeasonData(df)
        
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
                
            df = clean_gamelogs(df)
                
            # Random delay between 3 and 6 seconds to avoid detection and keep within limits
            time.sleep(random.randint(3, 6))
    
    return all_data
#%% Cleaning and preparing gamelog dataframe function    
def clean_gamelogs(df):    
    # delete index columns
    if 'Unnamed: 0' in df and 'Rk' in df and 'Gtm' in df:
        df = df.drop(['Unnamed: 0','Rk','Gtm'], axis = 1)
    # Delete season and school columns if you want (ill leave commented out)
    # if 'Season' in df and 'School' in df:
    #     df = df.drop(['Season', 'School'], axis = 1)
    
    # Delete date column
    if 'Date' in df:
        df = df.drop('Date', axis = 1)
    
    # change name of home or away column     Rename Reslt to Result     Tm to TeamPts     Opp to AwayPts
    df = df.rename(columns= {'Unnamed: 3': 'Location', 'Rslt': 'Result', 'Tm': 'TeamPts', 'Opp.1': 'AwayPts'})
    # change name of team and opponent stats
    df = df.rename(columns= {'FG': 'Team_FG', 'FGA': 'Team_FGA', 'FG%': 'Team_FG%', '3P': 'Team_3P', '3PA': 'Team_3PA',
                             '3P%': 'Team_3P%', '2P': 'Team_2P', '2PA': 'Team_2PA', '2P%': 'Team_2P%', 'eFG%': 'Team_eFG%',
                             'FT': 'Team_FT', 'FTA': 'Team_FTA', 'FT%': 'Team_FT%', 'ORB': 'Team_ORB', 'DRB': 'Team_DRB', 
                             'TRB': 'Team_TRB', 'AST': 'Team_AST', 'STL': 'Team_STL', 'BLK': 'Team_BLK', 'TOV': 'Team_TOV',
                             'PF': 'Team_PF'})
    df = df.rename(columns= {'FG.1': 'Away_FG', 'FGA.1': 'Away_FGA', 'FG%.1': 'Away_FG%', '3P.1': 'Away_3P', '3PA.1': 'Away_3PA',
                             '3P%.1': 'Away_3P%', '2P.1': 'Away_2P', '2PA.1': 'Away_2PA', '2P%.1': 'Away_2P%', 'eFG%.1': 'Away_eFG%',
                             'FT.1': 'Away_FT', 'FTA.1': 'Away_FTA', 'FT%.1': 'Away_FT%', 'ORB.1': 'Away_ORB', 'DRB.1': 'Away_DRB', 
                             'TRB.1': 'Away_TRB', 'AST.1': 'Away_AST', 'STL.1': 'Away_STL', 'BLK.1': 'Away_BLK', 'TOV.1': 'Away_TOV',
                             'PF.1': 'Away_PF'})
    
    # change the values in the column
    df['Location'] = df['Location'].fillna('Home')
    df.loc[df['Location'].str.contains('@', na=False), 'Location'] = 'Away'
    df.loc[df['Location'].str.contains('N', na=False), 'Location'] = 'Neutral'
    
    # Change the value names of 'type' column
    df.loc[df['Type'].str.contains('REG (Conf)', na = False, regex = False), 'Type'] = 'Conference'
    df.loc[df['Type'].str.contains('REG (Non-Conf)', na = False, regex = False), 'Type'] = 'Non-Conference'
    df.loc[df['Type'].str.contains('CTOURN',na = False), 'Type'] = 'CTOURN' #PLACEHOLDER if we want to change it later
    
    # Change values in OT column so we don't have null values
    df['OT'] = df['OT'].fillna(0)
    df.loc[df['OT'].str.contains('OT', na = False), 'OT'] = 1
    df['OT'] = df['OT'].astype(int)
    
    # Delete extra rows with column names
    df = df[df['Opp'] != 'Opp']
    
    # Delete last row, just totals for the season but we have season stats
    df = df[df['Opp'].notna()]
    
    return df

#%% Cleaning and preparing season dataframe function
def cleanSeasonData(df):
    # Need to drop rows with no team name still (hi past self, I am still unsure why there are team names missing in gamelogs ill look another time)
    
    # Drop 'unnamed' columns
    df = df.loc[:, ~df.columns.str.startswith('Unnamed')] # IDK if this is working tbh
    # Rename wins and losses columns
    df = df.rename(columns={'W': 'W_Tot', 'L': 'L_Tot','W.1': 'W_Conf', 'L.1': 'L_Conf', 'W.2': 'W_Home', 'L.2': 'L_Home', 'W.3': 'W_Away', 'L.3': 'L_Away'})    
    # Rename points columns
    df = df.rename(columns={'Tm.': 'Tm_Pts', 'Opp.': 'Opp_Pts'})
    # Rename SRS and SOS for clarity
    df = df.rename(columns={'SRS': 'Simple_Rating_System', 'SOS': 'Stregnth_Of_Schedule'})

    # Delete first unnamed column (just an index column)
    if 'Unnamed: 0' in df.columns:
        df = df.drop('Unnamed: 0', axis = 1)   
    # Delete Rk column as well (another index column)
    if 'Rk' in df.columns:    
        df = df.drop('Rk', axis = 1)
    
    # Delete Season column as file organization shows years
    # (ILL LEAVE COMMENTED OUT DOESNT MATTER TOO MUCH IF SEASON COLUMN IS THERE OR NOT TBH)
    # if 'Season' in df.columns:
    #     df = df.drop('Season', axis = 1) # I act like its hard to drop column if we want to later xD
    
    # Delete extra rows with column names
    df = df.dropna(subset='School') # Drop category row that is iterated
    df = df[df['School'] != 'School'] # Drop second reiterated column row with Rk value in Rk column
    
    return df

#%% Function to get list of all schools
def getSchoolList(season): # urlNeeeded is for when you need the school names to be changed for the url
    url = f'https://www.sports-reference.com/cbb/seasons/men/{season}-school-stats.html'
    print(f"Scraping for school list for season {season}")
    tables = pd.read_html(url, header=[1])
    
    # Extract the 'School' column and drop all Nan values
    schools_df = (tables[0][tables[0].columns[1]]).dropna()

    # Convert to list
    school_list = schools_df.tolist()
    
    school_list = [format_school_name(school) for school in school_list]
    
    # Remove 'school' from list (scrape grabs the 'school' headers)
    school_list = [school for school in school_list if school.lower() != 'school']
    
    # Random delay between 3 and 6 seconds to avoid detection and keep within limits
    time.sleep(random.randint(3, 6))
    
    print(f"Done scraping for school list, season {season}.")
    
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
    school = school.lower()
    return school

#%% Scrape overall cbb data
cbb_data = scrape_seasons(base_url, seasons)

## Get data frames for each season
df_list = []
# MAKE SURE YOUR DIRECTORY IS SET CORRECTLY IN ORDER TO SAVE THE CSV IN THE CORRECT PLACE
for season in seasons:
    season_df = cbb_data[cbb_data['Season'] == season]
    
    # Reset index for each season
    season_df.reset_index(drop=True, inplace=True)
    
    # Save to csv (could save to variable here but think its redundant)
    season_df.to_csv(f'C:/Users/Logmo/cbb-money/DataFrames/Overall-Data/{season}_stats.csv')

print("Finished scraping and creating overall data dataframes.")

#%% Scrape team game logs (WILL TAKE 3+ HOURS) UNCOMMENT WHEN NEEDING TO RUN
all_teams_logs = scrape_team_gamelog(base_url, seasons)

# Get data frames for each season
df_list = []
for season in seasons:
    schools = getSchoolList(season)
    for school in schools:
        season_df = all_teams_logs[all_teams_logs['Season'] == season]
        school_df = season_df[season_df['School'] == school]
        # Save to csv
        school_df.to_csv(f'C:/Users/Logmo/cbb-money/DataFrames/Team-Gamelogs/{season}/{school}-gamelogs.csv')
    print(f'Done saving season {season} to csv.')
        
print("Finished scraping and creating dataframes for all team gamelogs.")







