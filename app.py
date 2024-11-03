from flask import Flask, render_template, request, jsonify
import pandas as pd
import json

app = Flask(__name__)

# where our dataset is stored in the computer
file_path = "male_players.csv" 
# retrieving the actual dataset
df = pd.read_csv(file_path)
df = df[df['fifa_version'] == 24.0]
# the columns we care about
columns_to_keep = ['player_positions', 'long_name', 'overall', 'age', 'height_cm', 'club_name', 'league_name', 'skill_dribbling', 'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic', 'preferred_foot', 'goalkeeping_diving']
dataset = df[columns_to_keep]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_player', methods=['GET'])
def get_player():
    player_name = request.args.get('name')
    team_name = request.args.get('team')

    # we need to convert overall to a number
    overall = int(request.args.get('overall', 0))
    dataset['overall'] = dataset['overall'].astype(int)
    # THE USER IS NOT GIVING US AN OVERALL VALUE
    if overall == 0:
        result = dataset[dataset['long_name'].str.contains(player_name, case=False, na=False) & dataset['club_name'].str.contains(team_name, case=False, na=False)]

    # THE USER IS GIVING US A VALUE
    else:
        result = dataset[dataset['long_name'].str.contains(player_name, case=False, na=False) & dataset['club_name'].str.contains(team_name, case=False, na=False)]
        result = result[result['overall'] == overall]

        
    print(result.to_json(orient='records'))
    if result.empty:
        return jsonify({'message': 'Player not found'})
    else:
        result_json = result.to_json(orient='records')
        return jsonify(json.loads(result_json))

# THE JUDGE
# inputs: player1, player2, position
@app.route('/the_judge', methods=['GET', 'POST'])
def the_judge():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400

    player1 = data.get('player1', {})
    player2 = data.get('player2', {})
    position = data.get('position', '')

    # Extracting player 1 details
    player1_name = player1.get('name', 'Unknown')
    player1_position = player1.get('position', 'Unknown')
    player1_club = player1.get('club', 'Unknown')
    player1_league = player1.get('league', 'Unknown')
    player1_overall = int(player1.get('overall', 'Unknown'))
    player1_age = int(player1.get('age', 'Unknown'))
    player1_height = player1.get('height', 'Unknown')

    # player1_height is of the form 165 cm, but we want just 165
    # 154 cm

    # example
    # name = "Eli Gottlieb jr"
    # name = name[:-3]
    player1_height = int(player1_height[:-3])

    print(player1_height)






    player1_preferred_foot = player1.get('preferredFoot', 'Unknown')
    player1_pace = int(player1.get('pace', 'Unknown'))
    player1_shooting = int(player1.get('shooting', 'Unknown'))
    player1_passing = int(player1.get('passing', 'Unknown'))
    player1_dribbling = int(player1.get('dribbling', 'Unknown'))
    player1_defending = int(player1.get('defending', 'Unknown'))
    player1_physical = int(player1.get('physical', 'Unknown'))

    
    # Extracting player 2 details
    player2_name = player2.get('name', 'Unknown')
    player2_position = player2.get('position', 'Unknown')
    player2_club = player2.get('club', 'Unknown')
    player2_league = player2.get('league', 'Unknown')
    player2_overall = int(player2.get('overall', 'Unknown'))
    player2_age = int(player2.get('age', 'Unknown'))
    player2_height = player2.get('height', 'Unknown')
    player2_preferred_foot = player2.get('preferredFoot', 'Unknown')
    player2_pace = int(player2.get('pace', 'Unknown'))
    player2_shooting = int(player2.get('shooting', 'Unknown'))
    player2_passing = int(player2.get('passing', 'Unknown'))
    player2_dribbling = int(player2.get('dribbling', 'Unknown'))
    player2_defending = int(player2.get('defending', 'Unknown'))
    player2_physical = int(player2.get('physical', 'Unknown'))

    player2_height = int(player2_height[:-3])

    print(player2_height)


    # Scoring logic based on position
    if position == 'Defender':
        player1_score = 0.4 * player1_defending + 0.3 * player1_passing + 0.15 * player1_physical + 0.15 * player1_pace
        player2_score = 0.4 * player2_defending + 0.3 * player2_passing + 0.15 * player2_physical + 0.15 * player2_pace

        better_player = "player1" if player1_score > player2_score else "player2"
        reasons = []

        if better_player == "player1" and player1_overall < player2_overall:
            if player1_defending > player2_defending:
                reasons.append('defending')
            if player1_passing > player2_passing:
                reasons.append('passing')

        if better_player == "player2" and player1_overall > player2_overall:
            if player2_defending > player1_defending:
                reasons.append('defending')
            if player2_passing > player1_passing:
                reasons.append('passing')

        return_dictionary = {
            "better_player": player1_name if better_player == 'player1' else player2_name,
            "fifa_better_player": player1_name if player1_overall > player2_overall else player2_name,
            "reasons": reasons
        }

    elif position == 'Midfielder':
        player1_score = 0.3 * player1_passing + 0.2 * player1_dribbling + 0.15 * player1_physical + 0.15 * player1_shooting
        player2_score = 0.3 * player2_passing + 0.2 * player2_dribbling + 0.15 * player2_physical + 0.15 * player2_shooting

        better_player = "player1" if player1_score > player2_score else "player2"
        reasons = []

        if better_player == "player1" and player1_overall < player2_overall:
            if player1_dribbling > player2_dribbling:
                reasons.append('dribbling')
            if player1_passing > player2_passing:
                reasons.append('passing')

        if better_player == "player2" and player1_overall > player2_overall:
            if player2_dribbling > player1_dribbling:
                reasons.append('dribbling')
            if player2_passing > player1_passing:
                reasons.append('passing')

        return_dictionary = {
            "better_player": player1_name if better_player == 'player1' else player2_name,
            "fifa_better_player": player1_name if player1_overall > player2_overall else player2_name,
            "reasons": reasons
        }

    elif position == 'Forward':
        player1_score = 0.21 * player1_passing + 0.23 * player1_dribbling + 0.25 * player1_shooting + 0.10 * player1_physical + 0.10 * player1_height + 0.11 * player1_pace
        player2_score = 0.21 * player2_passing + 0.23 * player2_dribbling + 0.25 * player2_shooting + 0.10 * player2_physical + 0.10 * player2_height + 0.11 * player1_pace

        better_player = "player1" if player1_score > player2_score else "player2"
        reasons = []

        if better_player == "player1" and player1_overall < player2_overall:
            if player1_dribbling > player2_dribbling:
                reasons.append('dribbling')
            if player1_shooting > player2_shooting:
                reasons.append('shooting')

        if better_player == "player2" and player1_overall > player2_overall:
            if player2_dribbling > player1_dribbling:
                reasons.append('dribbling')
            if player2_shooting > player1_shooting:
                reasons.append('shooting')

        return_dictionary = {
            "better_player": player1_name if better_player == 'player1' else player2_name,
            "fifa_better_player": player1_name if player1_overall > player2_overall else player2_name,
            "reasons": reasons
        }

    else:
        return_dictionary = {
            "better_player": "no position selected",
            "fifa_better_player": "no position selected",
            "reasons": []
        }
    print(return_dictionary)
    return jsonify(return_dictionary)

if __name__ == '__main__':
    app.run(debug=True)
    
# output: giving a discrip andiser of wich player is beter overall just in some apecs or like hear this player has beter passing bu this player has beter shooting
