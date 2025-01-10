# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 23:11:59 2025

@author: Logmo
"""

import pandas as pd
import time
import random
import re

#%% Scrape function
def scrape_dk(url):
    print(f"Scraping: {url}")
    try:
        # Returns list of tables on the html page
        df = pd.read_html(base_url)
        
        df = df[0] # EITHER 1 OR 0 THE DK TABLES ARE WEIRD DEPENDING ON THE GAMES (I CAN EXPLAIN)
        
        df = circumsize(df)
        
        return df
    
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None


#%% General clean/reformating data
def circumsize(df):
    # Manually make column names I want in my dataframe
    cols = ["Time", "Home", "Away", "Spread (H)", "Spread Odds (H)", "Spread (A)", "Spread Odds (A)", "Total", "Over Odds", "Under Odds", "Moneyline (H)", "Moneyline (A)"]
    
    # Create new dataframe
    new_df = pd.DataFrame(columns = cols)
    
    # Recreate dataframe organized and clean
    for i in range(0,df.shape[0]): # Go through every row of data
    
        if i % 2 == 0: # Away teams always listed first
            # "TODAY" / "TOMORROW" COLUMN
            new_df[['Time', 'Away']] = df['Today'].str.extract(r"(\d{1,2}:\d{2}(?:AM|PM))(.+)") # GPT regex pattern to split time and team name
            # "SPREAD" COLUMN
            new_df[['Spread (A)', 'Spread Odds (A)']] = df['Spread'].str.extract(r"([+-]?\d*\.?\d+|PK)([−+-]?\d+)") # GPT regex pattern to split spread and spread odds
            # "TOTAL" COLUMN (get total AND over odds)
            new_df[['Total', 'Over Odds']] = df['Total'].str.extract(r"O\s*(\d*\.?\d+)([−+]?\d+)")
            # "MONEYLINE" COLUMN
            new_df['Moneyline (A)'] = df['Moneyline']
        else:
            # "TODAY" / "TOMORROW" COLUMN
            new_df[['Time', 'Home']] = df['Today'].str.extract(r"(\d{1,2}:\d{2}(?:AM|PM))(.+)") # GPT regex pattern to split time and team name
            # "SPREAD" COLUMN
            new_df[['Spread (H)', 'Spread Odds (H)']] = df['Spread'].str.extract(r"([+-]?\d*\.?\d+|PK)([−+-]?\d+)") # GPT regex pattern to split spread and spread odds
            # "TOTAL" COLUMN (only the under odds already have total)
            new_df['Under Odds'] = df['Total'].str.extract(r"U\s*\d*\.?\d+\s*([−+]?\d+)")
            # "MONEYLINE" COLUMN
            new_df['Moneyline (H)'] = df['Moneyline']
            
    return new_df
            
            
            
    # # GPT FIXES
    # # Manually define the columns you want in your cleaned dataframe
    # cols = ["Time", "Home", "Away", "Spread (H)", "Spread Odds (H)", "Spread (A)", "Spread Odds (A)", "Total", "Over Odds", "Under Odds", "Moneyline (H)", "Moneyline (A)"]
    
    # # Create a new dataframe with the desired columns
    # new_df = pd.DataFrame(columns=cols)
    
    # # Iterate through each row and extract the required data
    # for i in range(0, df.shape[0], 2):  # Go through every pair of rows (home/away)
        
    #     # Extract data for the "Away" team (even rows)
    #     new_df.loc[i, ['Time', 'Away']] = df.loc[i, 'Tomorrow'].str.extract(r"(\d{1,2}:\d{2}(?:AM|PM))(.+)").values[0]
    #     new_df.loc[i, ['Spread (A)', 'Spread Odds (A)']] = df.loc[i, 'Spread'].str.extract(r"([+-]?\d*\.?\d+|PK)([−+-]?\d+)").values[0]
    #     new_df.loc[i, ['Total', 'Over Odds']] = df.loc[i, 'Total'].str.extract(r"O\s*(\d*\.?\d+)([−+]?\d+)").values[0]
    #     new_df.loc[i, 'Moneyline (A)'] = df.loc[i, 'Moneyline']
        
    #     # Extract data for the "Home" team (odd rows)
    #     new_df.loc[i + 1, ['Time', 'Home']] = df.loc[i + 1, 'Tomorrow'].str.extract(r"(\d{1,2}:\d{2}(?:AM|PM))(.+)").values[0]
    #     new_df.loc[i + 1, ['Spread (H)', 'Spread Odds (H)']] = df.loc[i + 1, 'Spread'].str.extract(r"([+-]?\d*\.?\d+|PK)([−+-]?\d+)").values[0]
    #     new_df.loc[i + 1, 'Under Odds'] = df.loc[i + 1, 'Total'].str.extract(r"U\s*(\d*\.?\d+)\s*([−+]?\d+)").values[0]
    #     new_df.loc[i + 1, 'Moneyline (H)'] = df.loc[i + 1, 'Moneyline']
    
    # return new_df

    
#%% Run scrape function
 base_url = "https://sportsbook.draftkings.com/leagues/basketball/ncaab"
 
 odds_data = scrape_dk(base_url)
 odds_data.to_csv('Odds_HEHEHE.csv')
 odds_data.to_csv('DataFrames/Overall-Data/10_stats.csv')
 
 
 
 
 