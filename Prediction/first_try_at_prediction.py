# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 15:47:30 2025

@author: Logmo
"""

#%% import libraries
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import os

#%% Get all csv gamelogs and combine them into dataframe
def getAllGamelogs(path):
    # Get all files in the folder (directory)
    csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]
    
    # Extract team names and their corresponding dataframes
    team_names = [file.replace("-gamelogs.csv", "") for file in csv_files]
    dataframes = [pd.read_csv(os.path.join(path, file)) for file in csv_files]
    
    gamelogs = pd.DataFrame({
        "Team": team_names,
        "DataFrame": dataframes
    })
    
    cleanAllGamelogs(df = gamelogs)
    
    return gamelogs
    
#%% Get certain gamelog 
def cleanAllGamelogs(df):
    for gamelog in gamelogs['DataFrame']:
        
    
    
    
    
#%% hrmm (villager noise)
file = "C:/Users/Logmo/cbb-money/DataFrames/Team-Gamelogs/2025"
school = "iowa-state"

gamelogs = getAllGamelogs(path = file)

iowaSt = gamelogs[gamelogs["Team"] == "iowa-state"]
iowaSt = iowaSt['DataFrame'].iloc[0]

df = gamelogs['DataFrame'].iloc[0]
df = df['']

