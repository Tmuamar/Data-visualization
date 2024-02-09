import pandas as pd
from sklearn.linear_model import LinearRegression

# Load the dataset
teams_df = pd.read_csv('teams.csv')

# Cleaning and preprocessing
teams_df.drop(teams_df.columns[0], axis=1, inplace=True)

# Convert W/L% to a float
teams_df['W/L%'] = pd.to_numeric(teams_df['W/L%'], errors='coerce')

teams_df.dropna(inplace=True)

# Define the features and target variable for the regression model
features = ['PS/G', 'PA/G', 'SRS']
target = 'W/L%'

# Initialize an empty list to store DataFrames for each year
results_dfs = []

# Iterate through each year and create a linear regression model
for year in teams_df['Year'].unique():
    # Filter the dataframe for the year
    df_year = teams_df[teams_df['Year'] == year]
    
    # Define features and target
    X = df_year[features]
    y = df_year[target]
    
    # Initialize and train the Linear Regression model
    lr_model = LinearRegression()
    lr_model.fit(X, y)  # Fit the model to the entire dataset for the year
    
    # Predict
    y_pred = lr_model.predict(X)

    # Create a DataFrame to store the results for the current year
    year_results_df = pd.DataFrame({
        'Team': df_year['Team'],  # Include the team names
        'Actual W/L%': y,
        'Predicted W/L%': y_pred,
        'Year': df_year['Year']
    })
    
    # Append the results DataFrame for the current year to the list
    results_dfs.append(year_results_df)

# Concatenate all results DataFrames into one DataFrame
results_df = pd.concat(results_dfs, ignore_index=True)

# Save the combined results to a CSV file
results_df.to_csv('combined_linear_regression_results.csv', index=False)
