# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 18:27:56 2025

@author: Logmo
"""

import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


#%% Load Data and Prepare data
# Load datasets
print('Loading Datasets')
seasons = ['2022', '2023','2024','2025']
for season in seasons:
    team_stats = pd.read_csv(f'C:/Users/Logmo/cbb-money/DataFrames/Overall-Data/{season}_stats.csv')
    # Get all gamelogs
    path = f'C:/Users/Logmo/cbb-money/DataFrames/Team-Gamelogs/{season}'
    gamelogs = [f for f in os.listdir(path) if f.endswith('.csv')]
print('Done loading datasets')

#%% Merge gamelogs with Team Stats
merged_data = []

for gamelog in gamelogs:
    # Merge each gamelog with team stats
    merged = pd.merge(gamelog. team_stats, on=['School', 'Season'], how='left')
    merged_data.append(merged)
    
# Combine all merged DataFrames into one
final_data = pd.concat(merged_data, ignore_index=True)

#%% Feature Engineering
# Calculate point differential
final_data['point_diff'] = final_data['Tm'] - final_data['Opp.']

# Calculate win percentage
final_data['win_pct'] = final_data['W'] / (final_data['W'] + final_data['L'])

#%% Train predictive model
# Define features
features = ['point_diff', 'win_pct', 'SRS', 'SOS', 'FG%', '3P%', 'FT%']
target = 'outcome'  # Assuming 'outcome' is a binary column (1 for win, 0 for loss)

# Filter the dataset
X = final_data[features]
y = final_data[target]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a model
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Model Accuracy: {accuracy:.2f}')





