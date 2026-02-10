import time
import pandas as pd
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

START_YEAR = 1970
END_YEAR = 1983
CSV_FILENAME = "nba_sequences_1970_to_1983.csv"


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def main():
    driver = get_driver()
    data_rows = []

    print(f"Starting Robust Scrape: {START_YEAR} to {END_YEAR}...")

    try:
        for year in range(START_YEAR, END_YEAR + 1):
            print(f"\n--- SEASON {year} ({year-1}-{year}) ---")

            summary_url = f"https://www.basketball-reference.com/leagues/NBA_{year}.html"
            driver.get(summary_url)
            time.sleep(random.uniform(3, 4))

            unique_teams = {}

            try:
                all_links = driver.find_elements(By.TAG_NAME, "a")

                for link in all_links:
                    href = link.get_attribute("href")
                    if href and f"/teams/" in href and f"/{year}.html" in href:
                        # Extract Abbreviation (e.g., 'BOS')
                        # Format: https://.../teams/BOS/1970.html
                        try:
                            parts = href.split("/teams/")
                            if len(parts) > 1:
                                abbr = parts[1].split("/")[0]
                                name = link.text.replace("*", "").strip()

                                # Filter out junk links or empty names
                                if len(abbr) == 3 and len(name) > 2:
                                    # specific exclusion for "NBA" or "ABA" if they appear as teams
                                    if abbr not in unique_teams:
                                        unique_teams[abbr] = name
                        except:
                            continue

            except Exception as e:
                print(f"  Error finding teams: {e}")

            # Convert to list
            team_list = list(unique_teams.items())
            print(f"  Found {len(team_list)} unique teams.")

            if len(team_list) == 0:
                print(
                    "  WARNING: No teams found! The page structure might be very different.")
                continue

            # 2. Loop through teams
            for index, (team_abbr, team_name) in enumerate(team_list):
                print(f"  [{index+1}/{len(team_list)}] {team_name}...",
                      end="", flush=True)

                schedule_url = f"https://www.basketball-reference.com/teams/{team_abbr}/{year}_games.html"
                driver.get(schedule_url)
                time.sleep(random.uniform(1.5, 2.5))

                sequence = []
                try:
                    # Robust Result Finder
                    results = driver.find_elements(
                        By.CSS_SELECTOR, "td[data-stat='game_result']")
                    for res in results:
                        text = res.text.strip()
                        if text == 'W':
                            sequence.append('1')
                        elif text == 'L':
                            sequence.append('0')

                    if sequence:
                        seq_str = "".join(sequence)
                        data_rows.append({
                            'teamname': team_name,
                            'year': year,
                            'league': 'NBA',
                            # Force string format by adding a distinct marker if needed,
                            # but here we just ensure it is a string type.
                            'win_loss_sequence': str(seq_str)
                        })
                        print(f" Done ({len(seq_str)} games)")
                    else:
                        print(" No games (Skipping)")

                except Exception as e:
                    print(f" Error: {e}")

            # SAVE PROGRESS
            current_df = pd.DataFrame(data_rows)
            # FORCE string type for the sequence column to prevent 10^ notation in pandas
            current_df['win_loss_sequence'] = current_df['win_loss_sequence'].astype(
                str)
            current_df.to_csv(CSV_FILENAME, index=False)
            print(f"  > Saved progress to {CSV_FILENAME}")

    except Exception as e:
        print(f"\nCRITICAL ERROR: {e}")
    finally:
        driver.quit()
        if data_rows:
            df = pd.DataFrame(data_rows)
            df['win_loss_sequence'] = df['win_loss_sequence'].astype(str)
            df.to_csv(CSV_FILENAME, index=False)
            print(f"\nDone. Saved {len(df)} rows.")


if __name__ == "__main__":
    main()
