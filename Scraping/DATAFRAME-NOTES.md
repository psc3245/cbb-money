# Notes for myself about what I need to change up in how the dataframes are saved

## Season DataFrames (DONE) (when scraping season stats the dataframe you get should be goated (LGTM))
- (DONE) First column needs to be deleted, index 
- (DONE) Every 20st and 21st row is column names reiterated (rows 20,21,42,43,64,65.... need to be deleted)
- (DONE) Rk. column (2nd col) can also be deleted, another index
- (DONE) has column for season number, not sure if we want this still or not (something to think about)

## Gamelogs DataFrames
- (DONE) First two columns are an index (can be deleted) (maybe keep one for game number in season but dataframes have built in index pogCHAMP)
- (DONE) Third (Unnamed:...) column is if it was home or away, need to deal with that
- (DONE) Columns are reiterated like in season dataframes, address that
- (IDK, PROBABLY IRRELEVANT TEAMS) missing some opponent names apparently?, at least in the dataframe I am viewing, look further into that
- (ehhhh maybe thats fine) Type column is if it is a conference game or not, can rename 
- (DONE) Rslt column rename to Result, Win/Loss, etc. just make column name more clear
- (DONE) Season column also listed here like above not sure if we want to keep or not
- (DONE) Tm + Opp, are the scores for the team and their opponent
- (DONE) There is stats for team and their opponent, opponent stats start on SECOND "FG" column
- (DONE) last row is totals (not sure if we need (we have team seasons stats))
- (DONE) Date might not matter, a lot of them are empty
- (DONE) OT col should be 1s and 0s no NaNs

## DraftKings Odds DataFrames (DONE)
uh ill look another time, cbb a long time away so no odds out right now (could use old odds but ehhh KEKL)
- (DONE) looks like all I need to do is delete the first column (index column)