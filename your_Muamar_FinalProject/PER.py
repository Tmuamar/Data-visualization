import pandas as pd

# Load the data from the CSV file
players_totals_df = pd.read_csv('players_totals.csv')

# Convert the necessary columns to numeric types
numeric_cols = ['MP', 'FG', 'FGA', 'FT', 'FTA', 'PTS', 'ORB', 'TOV', 'PF', 'AST', 'STL', 'BLK', 'TRB']
players_totals_df[numeric_cols] = players_totals_df[numeric_cols].apply(pd.to_numeric, errors='coerce')

# Define the simplified PER calculation function with checks for division by zero
def calculate_simple_per(row):
    # Check for division by zero or undefined operations
    if row['MP'] == 0 or row['FGA'] == 0 or row['FT'] == 0:
        return 0

    factor = (2 / 3) - (0.5 * (row['AST'] / (row['FGA'] if row['FGA'] != 0 else 1))) / (2 * (row['FGA'] / (row['FT'] if row['FT'] != 0 else 1)))
    vop = row['PTS'] / ((row['FGA'] - row['ORB'] + row['TOV'] + 0.44 * row['FTA']) if row['FGA'] != 0 else 1)
    uPER = (1 / (row['MP'] if row['MP'] != 0 else 1)) * (
        row['PTS'] 
        + row['TRB'] 
        + row['AST'] 
        + row['STL'] 
        + row['BLK'] 
        - row['PF'] 
        - ((row['FGA'] - row['FG']) * factor) 
        - ((row['FTA'] - row['FT']) * 0.44 * (1 - (row['AST'] / (row['FGA'] if row['FGA'] != 0 else 1)))) 
        - row['TOV']
    )
    return uPER

# Calculate the simplified PER for each row
players_totals_df['simplified_PER'] = players_totals_df.apply(calculate_simple_per, axis=1)

# Specify the file path for the new Excel file
output_file_path = 'players_totals_with_PER.xlsx'

# Save the DataFrame with the simplified_PER column to an Excel file
players_totals_df.to_excel(output_file_path, index=False)