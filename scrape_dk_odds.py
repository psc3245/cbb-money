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
def scrape_dk(url,day):
    print(f"Scraping: {url}")
    try:
        # Returns list of tables on the html page
        df = pd.read_html(base_url)
        
        if day == 'Today':
            df = df[0]
        else:
            df = df[1]
        
        df = circumsize(df,day)
        
        return df
    
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None


#%% General clean/reformating data
def circumsize(df,day):
    # I THOUGHT I WAS GOATED BUT SLIGHTLY FAILED THIS IS CLAUDE RECONSTRUCTION (ABSOLUTE GOAT AI)
    # Split dataframe into away and home teams
    away = df.iloc[::2].reset_index(drop=True)
    home = df.iloc[1::2].reset_index(drop=True)
    
    # Create combined dataframe
    paired_df = pd.DataFrame({
        'Time': away[f'{day}'].str.extract(r'(\d{1,2}:\d{2}(?:AM|PM))')[0],
        'Away': away[f'{day}'].str.extract(r'\d{1,2}:\d{2}(?:AM|PM)(.+)')[0].str.strip(),
        'Home': home[f'{day}'].str.extract(r'\d{1,2}:\d{2}(?:AM|PM)(.+)')[0].str.strip(),
        'Spread (A)': away['Spread'].str.extract(r'([+-]?\d*\.?\d+|PK)')[0],
        'Spread Odds (A)': away['Spread'].str.extract(r'[+-]?\d*\.?\d+\s*([-−]\d+)')[0].str.replace('−', '-'),
        'Spread (H)': home['Spread'].str.extract(r'([+-]?\d*\.?\d+|PK)')[0],
        'Spread Odds (H)': home['Spread'].str.extract(r'[+-]?\d*\.?\d+\s*([-−]\d+)')[0].str.replace('−', '-'),
        'Total': away['Total'].str.extract(r'O\s*(\d+\.?\d*)')[0],
        'Over Odds': away['Total'].str.extract(r'O\s*\d+\.?\d*\s*([-−]\d+)')[0].str.replace('−', '-'),
        'Under Odds': home['Total'].str.extract(r'U\s*\d+\.?\d*\s*([-−]\d+)')[0].str.replace('−', '-'),
        'Moneyline (A)': away['Moneyline'].str.replace('−', '-'),
        'Moneyline (H)': home['Moneyline'].str.replace('−', '-')
    })
    
    return paired_df
#%% Run scrape function
base_url = "https://sportsbook.draftkings.com/leagues/basketball/ncaab"
 
odds_data = scrape_dk(base_url, day = 'Tomorrow')
odds_data.to_csv('DataFrames/Betting-Odds/first-betting-odds.csv')
 
 
 
 
 