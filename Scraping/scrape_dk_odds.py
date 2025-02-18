# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 23:11:59 2025

@author: Logmo
"""

import pandas as pd
import time
import random
import re
import datetime

#%% Scrape function
def scrape_dk():
    url = "https://sportsbook.draftkings.com/leagues/basketball/ncaab"
    print(f"Scraping: {url}")
    try:
        # Returns list of tables on the html page
        df = pd.read_html(url)
        
        # Get first and second table and turn to one dataframe (draftkings is weird, this will get all games)
        df1 = df[0]
        df2 = df[1]
        df = pd.concat([df1,df2],ignore_index=True)
        
        # Combine time columns (again draftkings tables are weird) (grab first column and last)
        df['Time'] = df[df.columns[0]].fillna('') + df[df.columns[-1]].fillna('')
        
        df = clean(df)
        
        return df
    
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None


#%% General clean/reformating data
def clean(df):
    # Split dataframe into away and home teams
    away = df.iloc[::2].reset_index(drop=True)
    home = df.iloc[1::2].reset_index(drop=True)
    
    # Create combined dataframe
    paired_df = pd.DataFrame({
        'Time': away['Time'].str.extract(r'(\d{1,2}:\d{2}(?:AM|PM))')[0],
        'Away': away['Time'].str.extract(r'\d{1,2}:\d{2}(?:AM|PM)(.+)')[0].str.strip(),
        'Home': home['Time'].str.extract(r'\d{1,2}:\d{2}(?:AM|PM)(.+)')[0].str.strip(),
        'Spread (A)': away['Spread'].str.extract(r'([+-]?\d*\.?\d+|PK)')[0],
        'Spread Odds (A)': away['Spread'].str.extract(r'[+-]?\d*\.?\d+\s*([+-−]\d+)')[0].str.replace('−', '-'),
        'Spread (H)': home['Spread'].str.extract(r'([+-]?\d*\.?\d+|PK)')[0],
        'Spread Odds (H)': home['Spread'].str.extract(r'[+-]?\d*\.?\d+\s*([+-−]\d+)')[0].str.replace('−', '-'),
        'Total': away['Total'].str.extract(r'O\s*(\d+\.?\d*)')[0],
        'Over Odds': away['Total'].str.extract(r'O\s*\d+\.?\d*\s*([-−]\d+)')[0].str.replace('−', '-'),
        'Under Odds': home['Total'].str.extract(r'U\s*\d+\.?\d*\s*([-−]\d+)')[0].str.replace('−', '-'),
        'Moneyline (A)': away['Moneyline'].str.replace('−', '-'),
        'Moneyline (H)': home['Moneyline'].str.replace('−', '-')
    })
    
    return paired_df

#%% Run scrape function
odds_data = scrape_dk()
date = datetime.date.today().strftime("%d-%m-%Y")
odds_data.to_csv(f'DataFrames/Betting-Odds/{date}-Odds.csv')
 
 
 
 
 