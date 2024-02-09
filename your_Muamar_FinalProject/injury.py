import pandas as pd

# Load the data from the CSV file
file_path = 'NBA Player Injury Stats(1951 - 2023).csv'

# Read the data into a pandas DataFrame
df = pd.read_csv(file_path)

df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Create lists to store data
player_list = []
injury_start_date_list = []
return_date_list = []
injury_duration_list = []
days_since_injury_list = []
teams_list = []  # List to store teams

# Initialize variables to keep track of the current player and their teams
current_player = None
current_teams = set()

# Iterate over the DataFrame to calculate injury duration and days since injury
for i, row in df.iterrows():
    if pd.notnull(row['Relinquished']):
        # Check if the player has changed since the last injury
        if row['Relinquished'] != current_player:
            # Save the current player's information and teams
            if current_player is not None:
                player_list.append(current_player)
                injury_start_date_list.append(current_injury_start_date)
                return_date_list.append(current_return_date)
                injury_duration_list.append(current_injury_duration)
                days_since_injury_list.append(None)  # This will be calculated only for current injuries
                teams_list.append(current_teams)

            # Update the current player and teams
            current_player = row['Relinquished']
            current_teams = set()

        # Find the index of the return entry for the player
        return_idx = df[(df['Acquired'] == row['Relinquished']) & (df['Date'] > row['Date'])].index
        injury_duration = None
        if not return_idx.empty:
            # Calculate injury duration
            return_date = df.at[return_idx[0], 'Date']
            injury_duration = (return_date - row['Date']).days
            # Update current injury information
            current_injury_start_date = row['Date']
            current_return_date = return_date
            current_injury_duration = injury_duration

            # Add the team(s) to the current teams set
            current_teams.add(row['Team'])
        else:
            days_since_injury = (pd.Timestamp.now() - row['Date']).days
            # Update current injury information
            current_injury_start_date = row['Date']
            current_return_date = None
            current_injury_duration = None

 
        current_teams.add(row['Team'])

if current_player is not None:
    player_list.append(current_player)
    injury_start_date_list.append(current_injury_start_date)
    return_date_list.append(current_return_date)
    injury_duration_list.append(current_injury_duration)
    days_since_injury_list.append(None)  # This will be calculated only for current injuries
    teams_list.append(current_teams)

# Create a DataFrame from the lists
injury_info = pd.DataFrame({
    'Player': player_list,
    'Injury Start Date': injury_start_date_list,
    'Return Date': return_date_list,
    'Injury Duration': injury_duration_list,
    'Days Since Injury': days_since_injury_list,
    'Teams': teams_list  # Include the teams list
})

# Save the injury_info DataFrame to a new CSV file
output_file_path = 'Processed_NBA_Injury_Info.csv'
injury_info.to_csv(output_file_path, index=False)

output_file_path
