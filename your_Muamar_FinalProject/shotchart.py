from nba_api.stats.endpoints import shotchartdetail
import json
import pandas as pd

# List of seasons for which you want to get the shot chart data
seasons = ['1990-91', '1991-92', '1992-93', '1993-94', '1994-95', '1995-96',
    '1996-97', '1997-98', '1998-99', '1999-00', '2000-01', '2001-02',
    '2002-03', '2003-04', '2004-05', '2005-06', '2006-07', '2007-08',
    '2008-09', '2009-10', '2010-11', '2011-12', '2012-13', '2013-14',
    '2014-15', '2015-16', '2016-17', '2017-18', '2018-19', '2019-20',
    '2020-21', '2021-22']  # Add more seasons as needed

# DataFrame to hold all shot data
all_shot_data = pd.DataFrame()

for season in seasons:
    response = shotchartdetail.ShotChartDetail(
        team_id=0,
        player_id=0,
        season_nullable=season,
        season_type_all_star='Regular Season'
    )

    content = json.loads(response.get_json())

    results = content['resultSets'][0]
    headers = results['headers']
    rows = results['rowSet']
    season_df = pd.DataFrame(rows, columns=headers)
    season_df['SEASON'] = season.split('-')[0]  # Corrected line

    # Append the data for the season to the main DataFrame
    all_shot_data = pd.concat([all_shot_data, season_df])

# Write the combined data to a CSV file
all_shot_data.to_csv(r'nba_shot_charts.csv', index=False)