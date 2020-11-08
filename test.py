import tensorflow as tf
from tensorflow import keras
import csv
import json
import requests
teamdict={"Arsenal":1, "Aston Villa":2, "Brighton":3, "Burnley":4, "Chelsea":5, "Crystal Palace":6, "Everton":7, "Fulham":8, "Leicester":9, 
"Leeds": 10,
"Liverpool":11, "Man City":12, "Man United":13, "Newcastle":14, "Norwich": 22, "Sheffield United":15, "Southampton":16, "Tottenham":17, 
"West Brom":18,
"Watford":23, "West Ham":19, "Wolves":20, "Bournemouth":21
}
inv_map = {v: k for k, v in teamdict.items()}

card={"Arsenal":0, "Aston Villa":0, "Brighton":0, "Burnley":0, "Chelsea":0, "Crystal Palace":0, "Everton":0, "Fulham":0, "Leicester":0, 
"Leeds": 0,
"Liverpool":0, "Man City":0, "Man United":0, "Newcastle":0, "Norwich": 0, "Sheffield United":0, "Southampton":0, "Tottenham":0, 
"West Brom":0,
"Watford":0, "West Ham":0, "Wolves":0, "Bournemouth":0
}
goals={"Arsenal":0, "Aston Villa":0, "Brighton":0, "Burnley":0, "Chelsea":0, "Crystal Palace":0, "Everton":0, "Fulham":0, "Leicester":0, 
"Leeds": 0,
"Liverpool":0, "Man City":0, "Man United":0, "Newcastle":0, "Norwich": 0, "Sheffield United":0, "Southampton":0, "Tottenham":0, 
"West Brom":0,
"Watford":0, "West Ham":0, "Wolves":0, "Bournemouth":0
}
teamratings={"Arsenal":0, "Aston Villa":0, "Brighton":0, "Burnley":0, "Chelsea":0, "Crystal Palace":0, "Everton":0, "Fulham":0, "Leicester":0, 
"Leeds": 0,
"Liverpool":0, "Man City":0, "Man United":0, "Newcastle":0, "Norwich": 0, "Sheffield United":0, "Southampton":0, "Tottenham":0, 
"West Brom":0,
"Watford":0, "West Ham":0, "Wolves":0, "Bournemouth":0
}
pogplayers={"Arsenal":0, "Aston Villa":0, "Brighton":0, "Burnley":0, "Chelsea":0, "Crystal Palace":0, "Everton":0, "Fulham":0, "Leicester":0, 
"Leeds": 0,
"Liverpool":0, "Man City":0, "Man United":0, "Newcastle":0, "Norwich": 0, "Sheffield United":0, "Southampton":0, "Tottenham":0, 
"West Brom":0,
"Watford":0, "West Ham":0, "Wolves":0, "Bournemouth":0
}

windict={"A":0, "D":1, "H":2}

data=[]
ans=[]
premier=requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
premierdata=premier.json()
for players in premierdata["elements"]:
    team=inv_map[players["team"]]
    if team=="Man Utd":
        team="Man United"
    if team=="Spurs":
        team="Tottenham"
    pogplayers[team]= float(players["points_per_game"]) + pogplayers[team]
print(pogplayers)
for teams in premierdata["teams"]:
    team=teams["name"]
    if team=="Man Utd":
        team="Man United"
    if team=="Spurs":
        team="Tottenham"
    teamratings[team]=float(teams["strength_overall_away"])

input_file = csv.DictReader(open("/Users/ericwang/Desktop/shit/PremierProfit/E0.csv"))
for rows in input_file:
    home= rows["HomeTeam"]
    away= rows["AwayTeam"]
    temp= [teamdict[home], teamdict[away], 0, goals[home], goals[away], card[home], card[away], pogplayers[home], pogplayers[away]]
    if card[home]>=1:
        card[home]=0
    if card[away]>=1:
        card[home]=0
    if int(rows["HR"])>0:
        card[home]=int(rows["HR"])
    if int(rows["AR"])>0:
        card[home]=int(rows["AR"])
    goals[home]=goals[home]+int(rows["FTHG"])
    goals[away]=goals[away]+int(rows["FTAG"])
    tempans=windict[rows["FTR"]]
    ans.append(tempans)
    data.append(temp)

goals={"Arsenal":0, "Aston Villa":0, "Brighton":0, "Burnley":0, "Chelsea":0, "Crystal Palace":0, "Everton":0, "Fulham":0, "Leicester":0, 
"Leeds": 0,
"Liverpool":0, "Man City":0, "Man United":0, "Newcastle":0, "Norwich": 0, "Sheffield United":0, "Southampton":0, "Tottenham":0, 
"West Brom":0,
"Watford":0, "West Ham":0, "Wolves":0, "Bournemouth":0
}
input_file = csv.DictReader(open("/Users/ericwang/Desktop/shit/PremierProfit/E0 (5).csv"))
for rows in input_file:
    home= rows["HomeTeam"]
    away= rows["AwayTeam"]
    temp= [teamdict[home], teamdict[away], 0, goals[home], goals[away], card[home], card[away], pogplayers[home], pogplayers[away]]
    if card[home]>=1:
        card[home]=0
    if card[away]>=1:
        card[home]=0
    if int(rows["HR"])>0:
        card[home]=int(rows["HR"])
    if int(rows["AR"])>0:
        card[home]=int(rows["AR"])
    goals[home]=goals[home]+int(rows["FTHG"])
    goals[away]=goals[away]+int(rows["FTAG"])
    tempans=windict[rows["FTR"]]
    ans.append(tempans)
    data.append(temp)

model= keras.Sequential()
model.add(keras.layers.Dense(128, activation="relu", input_shape=(9,)))
model.add(keras.layers.Dense(3, activation="softmax"))


model.compile(optimizer='adam',   loss=tf.keras.losses.SparseCategoricalCrossentropy(),
              metrics=['accuracy'])
model.fit(data, ans, epochs=200)

def getOdds(team1, team2):
    return (model.predict([[teamdict[team1], teamdict[team2], 0, goals[team1], goals[team2], card[team1], card[team2], pogplayers[team1], pogplayers[team2]]]))
print(getOdds("Chelsea", "Leicester"))



