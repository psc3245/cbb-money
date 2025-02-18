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
import numpy as np
from scipy.stats import poisson

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
        
#%% Get overall cbb stats dataframe for 2025
def getOverallStats:
    cbb_data = pd.read_csv('DataFrames/Overall-Data/2025_stats.csv')
#%% Poisson distribution
# Convert relevant columns to numeric values
cbb_data["Tm_Pts"] = pd.to_numeric(cbb_data["Tm_Pts"], errors="coerce")
cbb_data["Opp_Pts"] = pd.to_numeric(cbb_data["Opp_Pts"], errors="coerce")
cbb_data["G"] = pd.to_numeric(cbb_data["G"], errors="coerce")

# Extract team stats
kansas_stats = cbb_data[cbb_data["School"].str.contains("Kansas", case=False, na=False)].iloc[0]
byu_stats = cbb_data[cbb_data["School"] == "Brigham Young"].iloc[0]

# Compute average points per game (offensive and defensive)
kansas_offense = kansas_stats["Tm_Pts"] / kansas_stats["G"]
kansas_defense = kansas_stats["Opp_Pts"] / kansas_stats["G"]
byu_offense = byu_stats["Tm_Pts"] / byu_stats["G"]
byu_defense = byu_stats["Opp_Pts"] / byu_stats["G"]

# Compute expected points using Poisson means
kansas_expected = (kansas_offense + byu_defense) / 2
byu_expected = (byu_offense + kansas_defense) / 2

print(f"Expected Score Prediction:\nKansas: {kansas_expected:.2f} points\nBYU: {byu_expected:.2f} points")

#simulatePoisson(kansas_expected,byu_expected)
    
#%% Simulate games using poisson Kansas BYU
#def simulatePoisson(team1, team2):    
    # Simulate points using Poisson
    kansas_simulated_points = poisson.rvs(mu=kansas_expected, size=10000)
    byu_simulated_points = poisson.rvs(mu=byu_expected, size=10000)
    
    # Calculate the probability of of each team winning
    kansas_wins = np.sum(kansas_simulated_points > byu_simulated_points) / 10000
    byu_wins = np.sum(byu_simulated_points > kansas_simulated_points) / 10000
    ties = np.sum(byu_simulated_points == kansas_simulated_points) / 10000
    
    # Calculate avg points from simulations
    kansas_avg_points = np.sum(kansas_simulated_points / 10000)
    byu_avg_points = np.sum(byu_simulated_points / 10000)
    
    print(f"Probability of BYU winning: {byu_wins:.2%}")
    print(f"Probability of Kansas winning: {kansas_wins:.2%}")
    print(f"Probability of a tie: {ties:.2%}")
    print(f"Average Kansas Points: {kansas_avg_points}")
    print(f"Average BYU Points: {byu_avg_points}")
#%% hrmm (villager noise)
file = "C:/Users/Logmo/cbb-money/DataFrames/Team-Gamelogs/2025"
school = "iowa-state"

gamelogs = getAllGamelogs(path = file)

iowaSt = gamelogs[gamelogs["Team"] == "iowa-state"]
iowaSt = iowaSt['DataFrame'].iloc[0]

df = gamelogs['DataFrame'].iloc[0]
df = df['']

