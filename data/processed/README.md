# Processed Data

## Soccer Data
### Dataset Structure
The initial dataset had observations for 27 countries and 42 leagues worldwide across 2020 to 2025. The final processed csv file contains values for only three important leagues that we chose, the English Premier League in England, La Liga in Spain, and the Bundesliga in Germany. Each row corresponds to a specific team's Win-Loss Sequence for that particular season and in which league they played in. 

#### Column meanings : 
- League : League in which said team played in that year. (D1 = Bundesliga, E0 = English Premier League, SP1 = La Liga). The letter code corresponds to the country and the number corresponds to the division in which the team is playing. For example, E1 would mean the first or highest division/league in England.
- Season : The season in which the team played in. As soccer seasons mostly start around July or August and end in April or May the following year,any game that was played from July onwards would be considered the season of the following year. For example, a match in July 2025 would be considered the 2026 season. A match in March 2026 would also be considered to be in the 2026 season.
- Team : The team that corresponds to the Win-Loss sequence of that season in that division.
- Sequence : The Win-Loss sequence that corresponds to that specific team of that season. This is coded as a list in the Sequence column. The soccer.csv file contains values of 0,1, and 3 in the Sequence column. In soccer, if a team wins a match, they would be awarded 3 points. If the match ends in a draw, both teams would be awarded 1 point each. If a team loses a match, they are awarded 0 points. Hence, the Sequence column has values of 0,1, and 3. (0 = The team lost the match, 1 = the team drew the match, 3 = the team won the match).

In the soccer_binary.csv, all matches that ended in a draw are removed from the dataset, and only matches where a team wins or loses are counted. In this file, a Sequence value of 1 would mean that the team won the match, and 0 would mean that the team lost the match. This soccer_binary.csv will be easier to use for win-loss streaks analysis as it contains only binary outcomes.   
