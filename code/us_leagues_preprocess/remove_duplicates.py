import pandas as pd

# Load
us_leagues = pd.read_csv("../../data/processed/us_leagues.csv")

# Check duplicates before
dupes = us_leagues[us_leagues.duplicated(subset=['Team', 'Season'], keep=False)]
print(f"Found {len(dupes)} rows involved in duplicates:")
print(dupes[['League', 'Season', 'Team']].sort_values(['Team', 'Season']))

# Drop duplicates, keeping first occurrence
us_leagues_clean = us_leagues.drop_duplicates(subset=['Team', 'Season'], keep='first')

print(f"\nRows before: {len(us_leagues)} → after: {len(us_leagues_clean)}")

# Output
us_leagues_clean.to_csv("../../data/processed/us_leagues.csv", index=False)
print("Saved.")