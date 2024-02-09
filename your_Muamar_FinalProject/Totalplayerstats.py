import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

# Create directory for player total stats if it doesn't exist
directory = "player_totals"
if not os.path.exists(directory):
    os.makedirs(directory)

# Function to handle requests with error handling
def fetch_url(url, max_retries=3):
    retries = 0
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    while retries < max_retries:
        try:
            response = requests.get(url, headers=headers, timeout=10)  # added timeout and headers for safety
            response.raise_for_status()
            return response
        except (requests.ConnectionError, requests.HTTPError, requests.Timeout) as e:
            retries += 1
            print(f"Error fetching {url}: {e}. Retrying ({retries}/{max_retries})...")
            time.sleep(70)  # wait 70 seconds before retrying
    return None

years = list(range(1990, 2023))

# Player total stats data
for year in years:
    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_totals.html"
    response = fetch_url(url)
    if response:
        with open(f"{directory}/{year}_totals.html", "w+", encoding='utf-8') as f:
            f.write(response.text)

# Processing player total stats data
dfs = []
for year in years:
    with open(f"{directory}/{year}_totals.html", 'r', encoding='utf-8') as f:
        page = f.read()

    soup = BeautifulSoup(page, 'html.parser')
    soup.find('tr', class_="thead").decompose()
    # The id for the totals table could differ, here we assume it to be 'totals_stats'
    # You might need to inspect the webpage to find the correct id for the totals table
    player_table = soup.find_all(id="totals_stats")
    if player_table:
        player_df = pd.read_html(str(player_table[0]))[0]
        player_df["Year"] = year
        dfs.append(player_df)
    else:
        print(f"Couldn't find totals stats table for year {year}")

# Assuming all tables have a consistent format
players_totals = pd.concat(dfs, ignore_index=True)
players_totals.to_csv("players_totals.csv", index=False)

# Displaying the first few rows of the combined DataFrame
players_totals.head()
