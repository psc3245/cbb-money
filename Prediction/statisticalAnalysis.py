# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 18:27:56 2025

@author: Logmo
"""

import pandas as pd
import os


#%% Load Data and Prepare data
print('Loading Datasets')
seasons = ['2022', '2023','2024','2025']
team_stats_list = []
for season in seasons:
    team_stats = pd.read_csv(f'C:/Users/Logmo/cbb-money/DataFrames/Overall-Data/{season}_stats.csv')
    team_stats_list.append(team_stats)
    # Get all gamelogs
    path = f'C:/Users/Logmo/cbb-money/DataFrames/Team-Gamelogs/{season}'
    gamelogs = [f for f in os.listdir(path) if f.endswith('.csv')]
    
    # Extract team names and their corresponding dataframes
    team_names = [file.replace("-gamelogs.csv", "") for file in gamelogs]
    gamelogs_dfs = [pd.read_csv(os.path.join(path, file)) for file in gamelogs]
    
team_stats = pd.concat(team_stats_list, ignore_index=True)

print('Done loading datasets')

#%% Merge gamelogs with Team Stats
merged_data = []

for gamelog in gamelogs_dfs:
    # Merge each gamelog with team stats
    merged = pd.merge(gamelog, team_stats, on=['School', 'Season'], how='left')
    merged_data.append(merged)
    
# Combine all merged DataFrames into one
final_data = pd.concat(merged_data, ignore_index=True)

