import pandas as pd

# where our dataset is stored in the computer
file_path = "/Users/erinnatter/fifawebsite/male_players.csv" 

# retrieving the actual dataset
df = pd.read_csv(file_path)

df = df[df['fifa_version'] == 24.0]

# the columns we care about
columns_to_keep = ['player_positions', 'long_name', 'overall', 'age', 'height_cm', 'club_name', 'league_name',  'skill_dribbling', 'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic', 'preferred_foot', 'goalkeeping_diving']

dataset = df[columns_to_keep]

# dataset['overall'] = dataset['overall'].astype(int)

player_name = 'ha'
team_name = 'manchester'
overall = 81

result = dataset[dataset['long_name'].str.contains(player_name, case=False, na=False) & dataset['club_name'].str.contains(team_name, case=False, na=False)]

result = result[result['overall'] == 91]
result_json = result.to_json(orient='records')
print(result_json)

'''
# set variable clubname
clubname = ''
playername = 'kevin'
result = dataset[dataset['long_name'].str.contains(playername, case=False, na=False) & dataset['club_name'].str.contains(clubname, case=False, na=False)]

def print_players(dataset):
    # if the dataset is empty, print a message to the user saying that it is empty
    if dataset.empty:
        print("no data found")
    else:
        # Now, we KNOW that we have players to print
        for idx, row in dataset.iterrows():
            print(f"Name: {row['long_name']}")
            print(f"Position: {row['player_positions']}")
            print(f"club: {row['club_name']}")
            print(f"overall: {row['overall']}")
            print(f"age: {row['age']}")
            print(f"shooting: {row['shooting']}")
            print("-" * 20)


def compare_players(player1, player2):
    print(f"Player1 name: {player1.iloc[0]['long_name']}                    Player2 Name: {player2.iloc[0]['long_name']}")
    print(f"Player1 postition: {player1.iloc[0]['player_positions']}        Player2 positions: {player2.iloc[0]['player_positions']}")
    print(f"Player1 overall: {player1.iloc[0]['overall']}                   Player2 overall: {player2.iloc[0]['overall']}")
    print(f"Player1 age: {player1.iloc[0]['age']}                           Player2 age: {player2.iloc[0]['age']}")
    print(f"Player1 club name: {player1.iloc[0]['club_name']}               Player2 club name: {player2.iloc[0]['club_name']}")

            


# PLAYER 1
clubname = 'inter miami'
playername = 'messi'
player1 = dataset[dataset['long_name'].str.contains(playername, case=False, na=False) & dataset['club_name'].str.contains(clubname, case=False, na=False)]


# PLAYER 2
clubname = 'manchester city'
playername = 'kevin'
player2 = dataset[dataset['long_name'].str.contains(playername, case=False, na=False) & dataset['club_name'].str.contains(clubname, case=False, na=False)]

print(type(player2))

'''