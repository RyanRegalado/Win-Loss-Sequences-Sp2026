# US Leagues Preprocess Directory

This subdirectory contains scripts and notebooks for data retrieval, scraping, and preprocessing of datasets for US professional leagues (NBA, MLB) in the win-loss sequences project.

## Files

- **fix_reversal.ipynb**: Fixes sequence reversals in NBA data by reversing the win-loss sequences in raw and processed CSV files.
- **nba_data_retrieval.ipynb**: Retrieves NBA regular season schedules and game data from 1955 to 2025 using the nba_api library (1983-2025) and a pandas html scraper (1955-1982). 
- **scrape_mlb.py**: Parses MLB game log text files to extract team win-loss sequences by season from retrosheet.org
- **scrape_nba_70s.py**: Scrapes NBA team sequences from 1970 to 1983 using Selenium to access basketball-reference.com (OUTDATED // NOT IN USE)

For detailed scraping procedures, data sources, and preprocessing workflows, refer to the individual files or their documentation.