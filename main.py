'''The main class reads in a date from user input and finds all the games played on that day. It calls simEval
for each game using the home team, away team and date of the game.'''
from SimEval import *
import pandas as pd
from datetime import datetime, timedelta
import psycopg2

today = datetime.today()
tomorrow = today + timedelta(days = 1)


teams = {   "ATL":"Atlanta Hawks",              "BOS":"Boston Celtics",            "BKN":"Brooklyn Nets",
            "CHA":"Charlotte Hornets",          "CHI":"Chicago Bulls",             "CLE":"Cleveland Cavaliers",
            "DAL":"Dallas Mavericks",           "DEN":"Denver Nuggets",            "DET":"Detroit Pistons",
            "GSW":"Golden State Warriors",      "HOU":"Houston Rockets",           "IND":"Indiana Pacers",
            "LAC":"Los Angeles Clippers",       "LAL":"Los Angeles Lakers",        "MEM":"Memphis Grizzlies",
            "MIA":"Miami Heat",                 "MIL":"Milwaukee Bucks",           "MIN":"Minnesota Timberwolves",
            "NOR":"New Orleans Pelicans",       "NYK":"New York Knicks",           "OKC":"Oklahoma City Thunder",
            "ORL":"Orlando Magic",              "PHI":"Philadelphia 76ers",        "PHO":"Phoenix Suns",
            "POR":"Portland Trail Blazers",     "SAC":"Sacramento Kings",          "SAS":"San Antonio Spurs",
            "TOR":"Toronto Raptors",            "UTH":"Utah Jazz",                 "WAS":"Washington Wizards"}
homeTeam = "NULL"
awayTeam = "NULL"
date = "NULL"

print("WELCOME TO NBA SIMULATION!\n")
print("ATL - Atlanta Hawks              BOS - Boston Celtics            BKN - Brooklyn Nets")
print("CHA - Charlotte Hornets          CHI - Chicago Bulls             CLE - Cleveland Cavaliers")
print("DAL - Dallas Mavericks           DEN - Denver Nuggets            DET - Detroit Pistons")
print("GSW - Golden State Warriors      HOU - Houston Rockets           IND - Indiana Pacers")
print("LAC - Los Angeles Clippers       LAL - Los Angeles Lakers        MEM - Memphis Grizzlies")
print("MIA - Miami Heat                 MIL - Milwaukee Bucks           MIN - Minnesota Timberwolves")
print("NOP - New Orleans Pelicans       NYK - New York Knicks           OKC - Oklahoma City Thunder")
print("ORL - Orlando Magic              PHI - Philadelphia 76ers        PHO - Phoenix Suns")
print("POR - Portland Trail Blazers     SAC - Sacramento Kings          SAS - San Antonio Spurs")
print("TOR - Toronto Raptors            UTA - Utah Jazz                 WAS - Washington Wizards")

'''while awayTeam not in teams or homeTeam not in teams:
    homeTeam = input("\nPlease enter the three-letter abbreviation for the HOME team: ").upper()
    awayTeam = input("Please enter the three-letter abbreviation for the AWAY team: ").upper()
    if awayTeam not in teams or homeTeam not in teams:
        print("Abbreviation not recognized. Try again.")'''

while date == "NULL":
    print("\n*Game dates must on or between the dates 12-21-2020 and " + tomorrow.strftime("%m-%d-%Y"))
    date = str(input("Please enter the date of games desired in the form (dd-mm-yyyy):"))
    date.replace('/','-')
    if len(date) != 10 or date[2] != '-' or date[5] != '-':
        date = "NULL"

fileName = '20-21 Schedule.csv'
data = pd.read_csv(fileName)
dailyGames = data[(data['DATE'] == date)]

'''from sqlalchemy import create_engine

# connect string format:
# 'driver://username:password@host:port/db_name'
connect_str = 'postgresql://postgres:postgres@localhost:5432/nbasim'
engine = create_engine(connect_str)
cursor = engine.connect()
data.to_sql(name='schedule',
        con=engine,
        if_exists='append',
        index=False)
print(list(cursor.execute('SELECT * FROM schedule;')))'''

sourceFile = open('results.txt', 'w')
print("RESULTS", file=sourceFile)
sourceFile.close()

sourceFile = open('simEvaluation.txt', 'w')
print("Games for " + date + ":", file = sourceFile)
sourceFile.close()
for i in range(len(dailyGames)) :
    homeTeam= dailyGames.iloc[i, 3]
    awayTeam = dailyGames.iloc[i, 2]
    simEval(date, homeTeam, awayTeam)

print("\nThanks for using NBA SIMULATION!")
