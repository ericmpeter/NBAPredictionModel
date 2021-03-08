from NBASim import predictLines, printFile
import requests as req
import pandas as pd
from bs4 import BeautifulSoup as bs


# Scrapes vegasinsider.com for the professional lines given for the game passed in as a parameter. Calls printFile and
# predictLines from NBASim.py. Outputs the lines given by NBASim and compares them to Vegas's lines, and saves them
# in simEvaluation.txt.
def simEval(date, homeTeam, awayTeam):
    cols = ['Game', 'Team', 'Vegas Line', 'My Line', 'Result']
    data = []
    gameName = ''
    teamName = ''
    line = ''

    printFile(homeTeam, awayTeam, date)
    mySpread, myTotal, homeTeamWins = predictLines(homeTeam, awayTeam, date)

    # NBA API uses abbreviation NOP but vegasinsider.com uses NOR. So we translate it here
    if homeTeam == "NOP":
        homeTeam = "NOR"
    elif awayTeam == "NOP":
        awayteam = "NOR"

    if homeTeamWins == 1:
        awayLine = myTotal
        homeLine = (-1)* mySpread
        if mySpread == 0.0:
            homeLine = -0.5
    else:
        awayLine = (-1)* mySpread
        homeLine = myTotal
        if mySpread == 0.0:
            awayLine = -0.5

    URL = 'https://www.vegasinsider.com/nba/scoreboard/scores.cfm/game_date/{}'
    res = req.get(URL.format(date))
    soup = bs(res.content, 'lxml')
    games = soup.find_all('td', {'class': 'sportPicksBorder'})
    sourceFile = open('simEvaluation.txt', 'a')


    for game in games:
        teams = game.find_all('tr', {'class': 'tanBg'})
        gameName = game.find('td', {'colspan':'9'}).text
        for team in teams:
            teamName = team.find('a').text
            if teamName == homeTeam:
                vegasLine = team.find('td', {'align':'middle'}).text
                vegasLine = ' '.join(vegasLine.split())

                result = team.find('td', {"align":"right", "class":"sportPicksBorderR2", "nowrap":"", "width":"100"})
                if result == None:
                    result = team.find('td',{"align": "right", "class": "sportPicksBorderR", "nowrap": "", "width": "100"})
                if result != None:
                    result = result.text
                    result = ' '.join(result.split())
                    dict = {'Game': gameName, 'Team': teamName, 'Vegas Line': vegasLine, 'My Line': homeLine,
                            'Result': result}
                    data.append(dict)
                else:
                    dict = {'Game': gameName, 'Team': teamName, 'Vegas Line': vegasLine, 'My Line': homeLine,
                            'Result': 'N/A'}
                    data.append(dict)

            elif teamName == awayTeam:
                vegasLine = team.find('td', {'align': 'middle'}).text
                vegasLine = ' '.join(vegasLine.split())

                result = team.find('td', {"align": "right", "class": "sportPicksBorderR", "nowrap": "", "width": "100"})
                if result == None:
                    result = team.find('td', {"align":"right", "class":"sportPicksBorderR2", "nowrap":"", "width":"100"})
                if result != None:
                    result = result.text
                    result = ' '.join(result.split())
                    dict = {'Game': gameName, 'Team': teamName, 'Vegas Line': vegasLine, 'My Line': awayLine, 'Result': result}
                    data.append(dict)
                else:
                    dict = {'Game': gameName, 'Team': teamName, 'Vegas Line': vegasLine, 'My Line': awayLine, 'Result': 'N/A'}
                    data.append(dict)


    df = pd.DataFrame(data, columns=cols)
    if df.empty:
        print("\nThese games are not yet available.", file = sourceFile)
    else:
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(df, file = sourceFile)
    print("\n\n", file = sourceFile)
    sourceFile.close()
