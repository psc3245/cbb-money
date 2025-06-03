# Notes for myself about what I need to change up in how the dataframes are saved

## Season DataFrames
- First column needs to be deleted, index
- Every 20st and 21st row is column names reiterated (rows 20,21,42,43,64,65.... need to be deleted)
- Rk. column (2nd col) can also be deleted, another index
- has column for season number, not sure if we want this still or not (something to think about)

## Gamelogs DataFrames
- First two columns are an index (can be deleted) (maybe keep one for game number in season but dataframes have built in index pogCHAMP)
- Third (Unnamed:...) column is if it was home or away, need to deal with that
- Columns are reiterated like in season dataframes, address that
- missing some opponent names apparently?, at least in the dataframe I am viewing, look further into that
- Type column is if it is a conference game or not, can rename
- Rslt column rename to Result, Win/Loss, etc. just make column name more clear
- Season column also listed here like above not sure if we want to keep or not
- Tm + Opp, are the scores for the team and their opponent
- There is stats for team and their opponent, opponent stats start on SECOND "FG" column

## DraftKings Odds DataFrames
uh ill look another time, cbb a long time away so no odds out right now (could use old odds but ehhh KEKL)
