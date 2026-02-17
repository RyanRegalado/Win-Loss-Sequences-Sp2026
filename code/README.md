# File:


- Data_Cleaning_Soccer.ipynb :
  Notebook that includes the code used to clean the initial dataset (Matches.csv). Dataset was filtered to only include the first division in English, Germany, and Spain. As initial dataset only had a column for home team and away team, two separate dataframes had to be created - one for the home teams and one for the away teams - before we concatenated both to create a finalized dataset. 

- scrape_nba_70s.py :
  Traverse through NBA seasons from 1968-1969 to 1982-1983 on Baseketball Reference to collect win loss sequence for each team.

- scrape_mlb.py :
  Traverse through local MLB gamelogs to formulate win loss sequences in the csv file.
