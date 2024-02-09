import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium import webdriver
import os

# Create directories if they don't exist
directories = ["mvp", "player", "team"]
for directory in directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to handle requests with error handling
def fetch_url(url, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response
        except (requests.ConnectionError, requests.HTTPError) as e:
            retries += 1
            print(f"Error fetching {url}: {e}. Retrying ({retries}/{max_retries})...")
            time.sleep(70)
    return None

years = list(range(1990,2023))

# MVP data
for year in years:
    url = f"https://www.basketball-reference.com/awards/awards_{year}.html"
    response = fetch_url(url)
    if response:
        with open(f"mvp/{year}.html", "w+") as f:
            f.write(response.text)

# Player stats data
for year in years:
    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html"
    response = fetch_url(url)
    if response:
        with open(f"player/{year}.html", "w+") as f:
            f.write(response.text)

# Player total stats data
for year in years:
    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_totals.html"
    response = fetch_url(url)
    if response:
        with open(f"player/{year}_totals.html", "w+") as f:
            f.write(response.text)

# Team stats data
for year in years:
    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_standings.html"
    response = fetch_url(url)
    if response:
        with open(f"team/{year}.html", "w+") as f:
            f.write(response.text)

# Processing MVP data
dfs = []
for year in years:
    with open(f"mvp/{year}.html") as f:
        page = f.read()

    soup = BeautifulSoup(page, 'html.parser')
    soup.find('tr', class_="over_header").decompose()
    mvp_table = soup.find_all(id="mvp")[0]
    mvp_df = pd.read_html(str(mvp_table))[0]
    mvp_df["Year"] = year
    dfs.append(mvp_df)
mvps = pd.concat(dfs)
mvps.to_csv("mvps.csv")

# Processing player stats data
dfs = []
for year in years:
    with open(f"player/{year}.html") as f:
        page = f.read()

    soup = BeautifulSoup(page, 'html.parser')
    soup.find('tr', class_="thead").decompose()
    player_table = soup.find_all(id="per_game_stats")[0]
    player_df = pd.read_html(str(player_table))[0]
    player_df["Year"] = year
    dfs.append(player_df)
players = pd.concat(dfs)
players.to_csv("players.csv")

# Processing player total stats data
dfs = []
for year in years:
    with open(f"player/{year}_totals.html") as f:  # Note the file name change to indicate totals
        page = f.read()

    soup = BeautifulSoup(page, 'html.parser')
    soup.find('tr', class_="thead").decompose()
    player_table = soup.find_all(id="totals_stats")[0]  # Adjusted to the correct ID for totals
    player_df = pd.read_html(str(player_table))[0]
    player_df["Year"] = year
    dfs.append(player_df)
players_totals = pd.concat(dfs)
players_totals.to_csv("players_totals.csv")

# Processing team stats data
dfs = []
for year in years:
    with open(f"team/{year}.html") as f:
        page = f.read()
    soup = BeautifulSoup(page, 'html.parser')
    soup.find('tr', class_="thead").decompose()
    e_table = soup.find_all(id="divs_standings_E")[0]
    e_df = pd.read_html(str(e_table))[0]
    e_df["Year"] = year
    e_df["Team"] = e_df["Eastern Conference"]
    del e_df["Eastern Conference"]
    dfs.append(e_df)
    
    w_table = soup.find_all(id="divs_standings_W")[0]
    w_df = pd.read_html(str(w_table))[0]
    w_df["Year"] = year
    w_df["Team"] = w_df["Western Conference"]
    del w_df["Western Conference"]
    dfs.append(w_df)
teams = pd.concat(dfs)
teams.to_csv("teams.csv")
