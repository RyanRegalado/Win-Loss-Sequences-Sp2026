import csv
import glob
import os


def parse_game_logs():
    output_file = 'mlb_team_sequences.csv'

    # In my local folder, find all files matching the pattern gl*.txt
    file_patterns = glob.glob('gl*.txt')
    file_patterns.sort()  # Ensure we process years in order

    if not file_patterns:
        print("No files found starting with 'gl'. Make sure they are in this folder.")
        return

    sequences = {}

    print(f"Found {len(file_patterns)} files to process...")

    for filename in file_patterns:
        print(f"Reading {filename}...")

        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row or len(row) < 11:
                    continue

                # Index 0: Date, 3: Visiting Team, 6: Home Team, 9: Vis Score, 10: Home Score
                date_str = row[0]
                season = date_str[:4]

                vis_team = row[3]
                home_team = row[6]

                try:
                    vis_score = int(row[9])
                    home_score = int(row[10])
                except ValueError:
                    continue

                # Initialize dictionary structure
                if season not in sequences:
                    sequences[season] = {}
                if vis_team not in sequences[season]:
                    sequences[season][vis_team] = []
                if home_team not in sequences[season]:
                    sequences[season][home_team] = []

                # Determine Winner (1 for Win, 0 for Loss)
                if vis_score > home_score:
                    sequences[season][vis_team].append(1)
                    sequences[season][home_team].append(0)
                elif home_score > vis_score:
                    sequences[season][vis_team].append(0)
                    sequences[season][home_team].append(1)
                else:
                    pass  # Tie

    # Write to CSV
    print(f"Writing results to {output_file}...")
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['League', 'Season', 'Team', 'Sequence'])

        sorted_seasons = sorted(sequences.keys())

        for season in sorted_seasons:
            sorted_teams = sorted(sequences[season].keys())
            for team in sorted_teams:
                # Format sequence as [1,0,1...]
                seq_list = sequences[season][team]
                seq_str = str(seq_list).replace(" ", "")

                writer.writerow(['MLB', season, team, seq_str])

    print("Done! CSV generated.")


if __name__ == "__main__":
    parse_game_logs()
