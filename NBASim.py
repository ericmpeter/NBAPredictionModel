import pandas as pd
import random as rnd
import plotly.express as px
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder
from datetime import datetime, timedelta
import psycopg2

teamsDict = {"ATL":"Atlanta Hawks",              "BOS":"Boston Celtics",            "BKN":"Brooklyn Nets",
            "CHA":"Charlotte Hornets",          "CHI":"Chicago Bulls",             "CLE":"Cleveland Cavaliers",
            "DAL":"Dallas Mavericks",           "DEN":"Denver Nuggets",            "DET":"Detroit Pistons",
            "GSW":"Golden State Warriors",      "HOU":"Houston Rockets",           "IND":"Indiana Pacers",
            "LAC":"Los Angeles Clippers",       "LAL":"Los Angeles Lakers",        "MEM":"Memphis Grizzlies",
            "MIA":"Miami Heat",                 "MIL":"Milwaukee Bucks",           "MIN":"Minnesota Timberwolves",
            "NOR":"New Orleans Pelicans",       "NYK":"New York Knicks",           "OKC":"Oklahoma City Thunder",
            "ORL":"Orlando Magic",              "PHI":"Philadelphia 76ers",        "PHO":"Phoenix Suns",
            "POR":"Portland Trail Blazers",     "SAC":"Sacramento Kings",          "SAS":"San Antonio Spurs",
            "TOR":"Toronto Raptors",            "UTH":"Utah Jazz",                 "WAS":"Washington Wizards",
            "NOP":"New Orleans Pelicans"}
simNum = 100000
teams = teams.get_teams()

def getTeamStatsAPI(homeTeam, awayTeam, date, getDF = 0):
    #Ensures we use statistics beyond the date of the game. And convert from mm-dd-yyyy to mm/dd/yyyy for use in API.
    date_obj = datetime.strptime(str(date), '%m-%d-%Y')
    date_obj = date_obj - timedelta(days=1)
    date = date_obj.strftime("%m/%d/%Y")

    #Get both team's offensive stats
    home = [x for x in teams if x['full_name'] == teamsDict[homeTeam]][0]
    homeID = home['id']
    homeGamesDF = leaguegamefinder.LeagueGameFinder(team_id_nullable=homeID, date_from_nullable='12/22/2020', date_to_nullable= date, timeout=30).get_data_frames()[0]
    homeGamesDF['PTS_ALLOWED'] = homeGamesDF.apply(lambda row: row['PTS'] - row['PLUS_MINUS'], axis=1)
    homeMeanPts = round(homeGamesDF.PTS.mean(), 2)
    homeSD_Pts = round(homeGamesDF.PTS.std(), 2)
    homeMeanFGPct = round(homeGamesDF.FG_PCT.mean(), 2)
    homeSD_FGPct = round(homeGamesDF.FG_PCT.std(), 2)
    homeMean3PM = round(homeGamesDF.FG3M.mean(), 2)
    homeSD_3PM = round(homeGamesDF.FG3M.std(), 2)
    homeMeanFG3Pct = round(homeGamesDF.FG3_PCT.mean(), 2)
    homeSD_FG3Pct = round(homeGamesDF.FG3_PCT.std(), 2)
    homeMeanFT = round(homeGamesDF.FTM.mean(), 2)
    homeSD_FT = round(homeGamesDF.FTM.std(), 2)

    away = [x for x in teams if x['full_name'] == teamsDict[awayTeam]][0]
    awayID = away['id']
    awayGamesDF = leaguegamefinder.LeagueGameFinder(team_id_nullable=awayID, date_from_nullable='12/22/2020',date_to_nullable= date,timeout=30).get_data_frames()[0]
    awayGamesDF['PTS_ALLOWED'] = awayGamesDF.apply(lambda row: row['PTS'] - row['PLUS_MINUS'], axis=1)
    awayMeanPts = round(awayGamesDF.PTS.mean(), 2)
    awaySD_Pts = round(awayGamesDF.PTS.std(), 2)
    awayMeanFGPct = round(awayGamesDF.FG_PCT.mean(), 2)
    awaySD_FGPct = round(awayGamesDF.FG_PCT.std(), 2)
    awayMean3PM = round(awayGamesDF.FG3M.mean(), 2)
    awaySD_3PM = round(awayGamesDF.FG3M.std(), 2)
    awayMeanFG3Pct = round(awayGamesDF.FG3_PCT.mean(), 2)
    awaySD_FG3Pct = round(awayGamesDF.FG3_PCT.std(), 2)
    awayMeanFT = round(awayGamesDF.FTM.mean(), 2)
    awaySD_FT = round(awayGamesDF.FTM.std(), 2)

    #Get both team's defensive stats
    homeDefDF = leaguegamefinder.LeagueGameFinder(date_from_nullable='12/22/2020', vs_team_id_nullable=homeID, date_to_nullable= date, timeout=30).get_data_frames()[0]
    homeMeanPtsAllowed = round(homeDefDF.PTS.mean(), 2)
    homeSD_PtsAllowed = round(homeDefDF.PTS.std(), 2)
    homeMean3PAllowed = round(homeDefDF.FG3M.mean(), 2)
    homeSD_3PAllowed = round(homeDefDF.FG3M.std(), 2)
    homeMeanFTAllowed = round(homeDefDF.FTM.mean(), 2)
    homeSD_FTAllowed = round(homeDefDF.FTM.std(), 2)

    awayDefDF = leaguegamefinder.LeagueGameFinder(team_id_nullable=awayID, date_from_nullable='12/22/2020',date_to_nullable= date, timeout=30).get_data_frames()[0]
    awayMeanPtsAllowed = round(awayGamesDF.PTS.mean(), 2)
    awaySD_PtsAllowed = round(awayGamesDF.PTS.std(), 2)
    awayMean3PAllowed = round(awayGamesDF.FG3M.mean(), 2)
    awaySD_3PAllowed = round(awayGamesDF.FG3M.std(), 2)
    awayMeanFTAllowed = round(awayGamesDF.FTM.mean(), 2)
    awaySD_FTAllowed = round(awayGamesDF.FTM.std(), 2)

    # Combine the offensive and defensive stats of each team individually into a dictionary, used in
    homeStatsDict = {"Mean Pts":homeMeanPts, "Std Dev Pts":homeSD_Pts,
                        "Mean FG Pct":homeMeanFGPct, "Std Dev FG Pct":homeSD_FGPct,
                        "Mean 3Pt":homeMean3PM,"Std Dev 3pt":homeSD_3PM,
                        "Mean 3Pt Pct":homeMeanFG3Pct, "Std Dev 3Pt":homeSD_FG3Pct,
                        "Mean FT":homeMeanFT, "Std Dev FT":homeSD_FT,
                        "Mean Pts Allowed":homeMeanPtsAllowed,"Std Dev Pts Allowed":homeSD_PtsAllowed,
                        "Mean 3Pt Allowed": homeMean3PAllowed, "Std Dev 3Pt Allowed": homeSD_3PAllowed,
                        "Mean FT Allowed": homeMeanFTAllowed, "Std Dev FT Allowed": homeSD_FTAllowed}

    awayStatsDict = {"Mean Pts": awayMeanPts, "Std Dev Pts": awaySD_Pts,
                        "Mean FG Pct": awayMeanFGPct, "Std Dev FG Pct": awaySD_FGPct,
                        "Mean 3Pt": awayMean3PM, "Std Dev 3pt": awaySD_3PM,
                        "Mean 3Pt Pct": awayMeanFG3Pct, "Std Dev 3Pt Pct": awaySD_FG3Pct,
                        "Mean FT": awayMeanFT, "Std Dev FT": awaySD_FT,
                        "Mean Pts Allowed": awayMeanPtsAllowed, "Std Dev Pts Allowed": awaySD_PtsAllowed,
                        "Mean 3Pt Allowed": awayMean3PAllowed, "Std Dev 3Pt Allowed": awaySD_3PAllowed,
                        "Mean FT Allowed": awayMeanFTAllowed, "Std Dev FT Allowed": awaySD_FTAllowed}

    # Combine the offensive stats of both teams into a single dictionary, used for printing stats (same with defensive)
    teamOffensiveStats = {"Pts":[homeMeanPts, awayMeanPts], "SD Pts":[homeSD_Pts, awaySD_Pts],
                          "FG Pct":[homeMeanFGPct, awayMeanFGPct],"3Pt":[homeMean3PM,awayMean3PM],
                          "FT":[homeMeanFT, awayMeanFT]}
    teamDefenseStats = {"Pts Allowed": [homeMeanPtsAllowed, awayMeanPtsAllowed],
                        "SD Pts Allowed": [homeSD_PtsAllowed, awaySD_PtsAllowed],
                        "3Pt Allowed": [homeMean3PAllowed, awayMean3PAllowed],
                        "FT Allowed": [homeMeanFTAllowed, awayMeanFTAllowed]}
    teamOffStatsDF = pd.DataFrame(teamOffensiveStats, index=[homeTeam, awayTeam])
    teamDefStatsDF = pd.DataFrame(teamDefenseStats, index=[homeTeam, awayTeam])
    # Goes to printStats for nice formatting
    if getDF == 1:
        return teamOffStatsDF, teamDefStatsDF
    # Goes to statVisuals to create histograms
    elif getDF == -1:
        return homeGamesDF, awayGamesDF
    # Goes to runSim for faster performance
    else:
        return homeStatsDict, awayStatsDict

def getTeamStats(homeTeam, awayTeam, getDF = 0):
    fileName = 'games20-21.csv'
    data = pd.read_csv(fileName)
    # Retrieve Home Stats
    # Retrieve Offensive stats
    filterHomeTeam = data[data.TEAM == homeTeam]
    homeStatsDF = filterHomeTeam[filterHomeTeam.Home == 1]
    homeMeanPts = round(homeStatsDF.PTS.mean(),2)
    homeSD_Pts = round(homeStatsDF.PTS.std(),2)
    homeMeanFGPct = round(homeStatsDF.FGP.mean(),2)
    homeSD_FGPct = round(homeStatsDF.FGP.std(),2)
    homeMean3P = round(3 * homeStatsDF.M3P.mean(),2)
    homeSD_3P = round(3 * homeStatsDF.M3P.std(),2)
    homeMean2P = round(2 * homeStatsDF.M2P.mean(),2)
    homeSD_2P = round(2 * homeStatsDF.M2P.std(),2)
    homeMeanFT = round(homeStatsDF.FTM.mean(),2)
    homeSD_FT = round(homeStatsDF.FTM.std(),2)

    # Retrieve Defensive stats
    filterHomeTeam_Allowed = data[data.Opponent == homeTeam]
    homeStatsAllowed = filterHomeTeam_Allowed[filterHomeTeam_Allowed.Home == 0]
    homeMeanPtsAllowed = round(homeStatsAllowed.PTS.mean(),2)
    homeSD_PtsAllowed = round(homeStatsAllowed.PTS.std(),2)
    homeMean3PAllowed = round(3 * homeStatsAllowed.M3P.mean(),2)
    homeSD_3PAllowed = round(3 * homeStatsAllowed.M3P.std(),2)
    homeMean2PAllowed = round(2 * homeStatsAllowed.M2P.mean(),2)
    homeSD_2PAllowed = round(2 * homeStatsAllowed.M2P.std(),2)
    homeMeanFTAllowed = round(homeStatsAllowed.FTM.mean(),2)
    homeSD_FTAllowed = round(homeStatsAllowed.FTM.std(),2)

    # Team is away
    # Retrieve Offensive stats
    filterAwayTeam = data[data.TEAM == awayTeam]
    awayStatsDF = filterAwayTeam[filterAwayTeam.Home == 0]
    awayMeanPts = round(awayStatsDF.PTS.mean(), 2)
    awaySD_Pts = round(awayStatsDF.PTS.std(), 2)
    awayMeanFGPct = round(awayStatsDF.FGP.mean(), 2)
    awaySD_FGPct = round(awayStatsDF.FGP.std(), 2)
    awayMean3P = round(3 * awayStatsDF.M3P.mean(), 2)
    awaySD_3P = round(3 * awayStatsDF.M3P.std(), 2)
    awayMean2P = round(2 * awayStatsDF.M2P.mean(), 2)
    awaySD_2P = round(2 * awayStatsDF.M2P.std(), 2)
    awayMeanFT = round(awayStatsDF.FTM.mean(), 2)
    awaySD_FT = round(awayStatsDF.FTM.std(), 2)

    # Retrieve Defensive stats
    filterTeam_Allowed = data[data.Opponent == awayTeam]
    awayStatsAllowed = filterTeam_Allowed[filterTeam_Allowed.Home == 1]
    awayMeanPtsAllowed = round(awayStatsAllowed.PTS.mean(), 2)
    awaySD_PtsAllowed = round(awayStatsAllowed.PTS.std(), 2)
    awayMean3PAllowed = round(3 * awayStatsAllowed.M3P.mean(), 2)
    awaySD_3PAllowed = round(3 * awayStatsAllowed.M3P.std(), 2)
    awayMean2PAllowed = round(2 * awayStatsAllowed.M2P.mean(), 2)
    awaySD_2PAllowed = round(2 * awayStatsAllowed.M2P.std(), 2)
    awayMeanFTAllowed = round(awayStatsAllowed.FTM.mean(), 2)
    awaySD_FTAllowed = round(awayStatsAllowed.FTM.std(), 2)

    # Dictionaries used in RunSim to improve performance *** needs to change for both teams
    homeStatsDict = {"Mean Pts":homeMeanPts, "Std Dev Pts":homeSD_Pts,
                        "Mean FG Pct":homeMeanFGPct, "Std Dev FG Pct":homeSD_FGPct,
                        "Mean 3Pt":homeMean3P,"Std Dev 3pt":homeSD_3P,
                        "Mean 2Pt":homeMean2P, "Std Dev 3Pt":homeSD_2P,
                        "Mean FT":homeMeanFT, "Std Dev FT":homeSD_FT,
                        "Mean Pts Allowed":homeMeanPtsAllowed,"Std Dev Pts Allowed":homeSD_PtsAllowed,
                        "Mean 3Pt Allowed":homeMean3PAllowed, "Std Dev 3Pt Allowed":homeSD_3PAllowed,
                        "Mean 2Pt Allowed":homeMean2PAllowed,"Std Dev 2Pt PAllowed":homeSD_2PAllowed,
                        "Mean FT Allowed":homeMeanFTAllowed, "Std Dev FT Allowed":homeSD_FTAllowed}

    awayStatsDict = {"Mean Pts": awayMeanPts, "Std Dev Pts": awaySD_Pts,
                        "Mean FG Pct": awayMeanFGPct, "Std Dev FG Pct": awaySD_FGPct,
                        "Mean 3Pt": awayMean3P, "Std Dev 3pt": awaySD_3P,
                        "Mean 2Pt": awayMean2P, "Std Dev 3Pt": awaySD_2P,
                        "Mean FT": awayMeanFT, "Std Dev FT": awaySD_FT,
                        "Mean Pts Allowed": awayMeanPtsAllowed, "Std Dev Pts Allowed": awaySD_PtsAllowed,
                        "Mean 3Pt Allowed": awayMean3PAllowed, "Std Dev 3Pt Allowed": awaySD_3PAllowed,
                        "Mean 2Pt Allowed": awayMean2PAllowed, "Std Dev 2Pt PAllowed": awaySD_2PAllowed,
                        "Mean FT Allowed": awayMeanFTAllowed, "Std Dev FT Allowed": awaySD_FTAllowed}

    teamOffensiveStats = {"Pts":[homeMeanPts, awayMeanPts], "SDPts":[homeSD_Pts, awaySD_Pts],"FG Pct":[homeMeanFGPct, awayMeanFGPct],
                          "3Pt":[homeMean3P,awayMean3P], "2Pt":[homeMean2P,awayMean2P], "FT":[homeMeanFT,awayMeanFT]}

    teamDefenseStats = {"Pts Allowed":[homeMeanPtsAllowed,awayMeanPtsAllowed],"SD Pts Allowed":[homeSD_PtsAllowed,awaySD_PtsAllowed],
                 "3Pt Allowed":[homeMean3PAllowed,awayMean3PAllowed], "2Pt Allowed":[homeMean2PAllowed,awayMean2PAllowed],
                 "FT Allowed":[homeMeanFTAllowed,awayMeanFTAllowed]}
    # Used in printing for clean formatting.
    teamOffStatsDF = pd.DataFrame(teamOffensiveStats, index=[homeTeam + " HOME", awayTeam + " AWAY"])
    teamDefStatsDF = pd.DataFrame(teamDefenseStats, index=[homeTeam + " HOME", awayTeam + " AWAY"])

    # Goes to printStats for nice formatting
    if getDF == 1:
        return teamOffStatsDF, teamDefStatsDF
    # Goes to statVisuals to create histograms
    elif getDF == -1:
        return homeStatsDF, awayStatsDF
    # Goes to runSim for faster performance
    else:
        return homeStatsDict, awayStatsDict

# Runs the simulation simNum times using the mean and standard deviation of points scored and points allowed for each
# team. Returns the win percentage for each team as well as the points each team scores in the simulations.
def runSim(homeTeam, awayTeam, date):
    sourceFile = open('results.txt', 'a')
    homeWinCount = 0
    awayWinCount = 0
    tieCount = 0
    homePtsCount = 0
    awayPtsCount = 0
    homeStats, awayStats = getTeamStatsAPI(homeTeam, awayTeam, date = date)


    for i in range(0, simNum):
        '''homeSimPts = ((rnd.gauss(homeStats["mean3P"], homeStats["SD_3P"]) +
                       rnd.gauss(awayStats["mean3PAllowed"],awayStats["SD_3PAllowed"]))/2) +\
                     ((rnd.gauss(homeStats["mean2P"], homeStats["SD_2P"]) +
                       rnd.gauss(awayStats["mean2PAllowed"],awayStats["SD_2PAllowed"]))/2) +\
                     ((rnd.gauss(homeStats["meanFT"], homeStats["SD_FT"]) +
                       rnd.gauss(awayStats["meanFTAllowed"],awayStats["SD_FTAllowed"]))/2)
        awaySimPts = ((rnd.gauss(awayStats["mean3P"], awayStats["SD_3P"]) +
                       rnd.gauss(homeStats["mean3PAllowed"], homeStats["SD_3PAllowed"])) / 2) + \
                     ((rnd.gauss(awayStats["mean2P"], awayStats["SD_2P"]) +
                       rnd.gauss(homeStats["mean2PAllowed"], homeStats["SD_2PAllowed"])) / 2) + \
                     ((rnd.gauss(awayStats["meanFT"], awayStats["SD_FT"]) +
                       rnd.gauss(homeStats["meanFTAllowed"], homeStats["SD_FTAllowed"])) / 2)'''

        homeSimPts = (rnd.gauss(homeStats["Mean Pts"],homeStats["Std Dev Pts"])+
                      rnd.gauss(awayStats["Mean Pts Allowed"],awayStats["Std Dev Pts Allowed"]))/2

        awaySimPts = (rnd.gauss(awayStats["Mean Pts"],awayStats["Std Dev Pts"])+
                      rnd.gauss(homeStats["Mean Pts Allowed"],homeStats["Std Dev Pts Allowed"]))/2

        homePtsCount = homePtsCount + homeSimPts
        awayPtsCount = awayPtsCount + awaySimPts

        if homeSimPts > awaySimPts:
            homeWinCount = homeWinCount + 1
        elif homeSimPts < awaySimPts:
            awayWinCount = awayWinCount + 1
        else: tieCount = tieCount + 1

    homeWinPct = round(homeWinCount / simNum * 100, 2)
    awayWinPct = round(awayWinCount / simNum * 100, 2)
    print("\n" + str(simNum) + " GAME SIMULATION: ", file = sourceFile)
    print(teamsDict[homeTeam] + " won " + str(homeWinPct) + " percent of games. (" + str(homeWinCount) + " games)", file = sourceFile)
    print(teamsDict[awayTeam] + " won " + str(awayWinPct) + " percent of games. (" + str(awayWinCount) + " games)", file = sourceFile)
    if tieCount != 0:
        print(teamsDict[homeTeam], "and ", teamsDict[awayTeam], "tied", tieCount/simNum, "percent of games. (", tieCount, " games)", file = sourceFile)
    sourceFile.close()
    return homeWinPct, awayWinPct, homePtsCount, awayPtsCount

# Uses the win percentages from runSim and points count to predict a winner, a winning margin, and betting lines
# (including a 10% house edge) for each game.
def predictLines(homeTeam, awayTeam, date):
    sourceFile = open('results.txt', 'a')
    favoredLine = -110
    underdogLine = -110
    homeWinPct, awayWinPct, homePtsCount, awayPtsCount = runSim(homeTeam, awayTeam, date)
    ptsCount = awayPtsCount + homePtsCount

    predictedTotal = round(ptsCount / simNum * 2) / 2
    predictedSpread = round(((homePtsCount / simNum) - (awayPtsCount / simNum)) * 2) / 2

    if homeWinPct > awayWinPct:
        favored = homeTeam
        underdog = awayTeam
        homeTeamWins = 1
        favoredLine = round(((-1)* homeWinPct / (1 - (homeWinPct / 100))) * 0.9)
        underdogLine = round((100 / (awayWinPct / 100)-100) * 0.9)
    else:
        favored = awayTeam
        underdog = homeTeam
        homeTeamWins = 0
        favoredLine = round((-1)* awayWinPct / (1 - (awayWinPct / 100))) - 10
        underdogLine = round(100 / (homeWinPct / 100) - 100) - 10

    if favoredLine > -100:
        favoredLine = 100 + (100 + favoredLine)
    if underdogLine < 100:
        underdogLine = 100 + (100 - underdogLine)

    print("\nSPREAD:", file = sourceFile)
    if predictedSpread > 0:
        print(teamsDict[homeTeam], "are favored at", predictedSpread * (-1), file = sourceFile)
    elif predictedSpread < 0:
        print(teamsDict[awayTeam], "are favored at", predictedSpread, file = sourceFile)
    else:
        print(teamsDict[favored], "are favored at -0.5", file = sourceFile)
    print("\nMONEYLINE:", file = sourceFile)
    print(teamsDict[favored], "to win:", favoredLine, file = sourceFile)
    print(teamsDict[underdog] + " to win: +" + str(underdogLine), file=sourceFile)
    print("\nOVER/UNDER:", file = sourceFile)
    print("The projected total points is", predictedTotal, file = sourceFile)

    sourceFile.close()
    return abs(predictedSpread), predictedTotal, homeTeamWins

# Prints the offensive and defensive stats for each team. Includes mean and standard deviation of points scored and
# allowed, mean field goal percentage, as well as the mean 3 point field goals and free throws made and allowed for each team.
def printStats(homeTeam, awayTeam, date):
    sourceFile = open('results.txt', 'a')
    teamOffStats, teamDefStats = getTeamStatsAPI(homeTeam, awayTeam, date, getDF = 1)
    print("OFFENSIVE STATS", file = sourceFile)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(teamOffStats,file = sourceFile)

    print("\nDEFENSIVE STATS", file = sourceFile)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(teamDefStats, file = sourceFile)

    sourceFile.close()

# Calls getStats, printStats and statVisuals and outputs them to results.txt.
def printFile(homeTeam, awayTeam, date):
    sourceFile = open('results.txt', 'a')
    print("\n" + teamsDict[awayTeam] + " at " + teamsDict[homeTeam], file=sourceFile)
    sourceFile.close()
    getTeamStatsAPI(homeTeam, awayTeam,date)

    printStats(homeTeam, awayTeam,date)
    statVisuals(homeTeam, awayTeam, date)

# Creates an interactive histogram of each team's points scored and allowed using plotly express and saves them as
# first_figure.html and second_figure.html respectively.
def statVisuals(homeTeam, awayTeam, date):
    homeStats, awayStats = getTeamStatsAPI(homeTeam, awayTeam, date, -1)
    combinedStats = pd.concat([homeStats, awayStats])

    fig = px.histogram(data_frame = combinedStats, x = "PTS", color = "TEAM_NAME", nbins=15, title = "Points Scored 20-21", opacity=.5, barmode="overlay", range_x=["75","150"])
    fig.write_html('first_figure.html', auto_open=True)

    fig = px.histogram(data_frame=combinedStats, x="PTS_ALLOWED", color="TEAM_NAME", nbins=15, title="Points Allowed 20-21", opacity=.5,barmode="overlay", range_x=["75","150"])
    fig.write_html('second_figure.html', auto_open=True)

