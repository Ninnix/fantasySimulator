import csv
import numpy as np
import matplotlib.pyplot as plt
 
budget = 100

# id of your drivers and team
id_d0 = 'Leclerc'
id_d1 = 'Giovinazzi'
id_d2 = 'Perez'
id_d3 = 'Russel'
id_d4 = 'Grojean'
id_t0 = 'Red Bull'

# dictionary for the drivers, used to create lst_my_team
dic_drivers = {
    'Vettel': '20',
    'Leclerc': '844',
    'Hamilton': '1',
    'Bottas': '822',
    'Verstappen': '830',
    'Gasly': '842',
    'Sainz': '832',
    'Norris': '846',
    'Ricciardo': '817',
    'Hulk': '807',
    'Kvyat': '826',
    'Albon': '848',
    'Perez': '815',
    'Stroll': '840',
    'Raikkonen': '8',
    'Giovinazzi': '841',
    'Russel': '847',
    'Kubica': '9',
    'Grojean': '154',
    'Magnussen': '825',
}

# dictionary for the team, used to create my_team
dic_teams = {
    'Ferrari': '6',
    'Mercedes': '131',
    'Red Bull': '9',
    'Toro Rosso': '5',
    'Racing Point': '211',
    'Alfa Romeo': '51',
    'McLaren': '1',
    'Williams': '3',
    'Renault': '4',
    'Haas': '210',
}

class Driver:
    def __init__(self, name, id, team, team_id, mate, mate_id, price, turbo, points):
        self.name = name
        self.id = id
        self.team = team
        self.team_id = []
        self.mate = []
        self.mate_id = []
        self.price = price
        self.turbo = turbo
        self.points = points
        self.race = []
        self.grid = []
        self.race_mate = []
        self.grid_mate = []
        self.pole = []
        self.pole_mate = []
        self.rank_FL = []
        self.race_order = []
        self.mate_race_order = []
        self.status = []
        self.score_for_races = []

class Team:
    def __init__(self, name, id, price, points):
        self.name = name
        self.id = id
        self.price = price
        self.points = points
        self.drivers = []
        self.score_by_drivers = [[], [], []]
        self.score_for_races = []

with open('csv/races.csv') as f:
    reader_races = csv.reader(f)
    lst_races_id = []
    tab_races = []
    for row in reader_races:
        if '2019' == row[1]:
            lst_races_id.append(row[0])
            tab_races.append(row)
    #print(lst_races_id)

with open('csv/results.csv') as g:
    reader_results = csv.reader(g)
    tab_results = []
    for row in reader_results:
        for id in lst_races_id:
            if row[1] == id:
                tab_results.append(row)

with open('csv/qualifying.csv') as h:
    reader_qualifying = csv.reader(h)
    tab_qualifying = []
    for row in reader_qualifying:
        for id in lst_races_id:
            if row[1] == id:
                tab_qualifying.append(row)

with open('csv/fantasy_driver.csv') as d:
    reader_f_driver = csv.reader(d)
    lst_drivers = []
    for row in reader_f_driver:
        if row[0] != 'Driver':
            lst_drivers.append(Driver(row[0], row[1], row[2], row[3], row[4], row[5], row[6], False, 0))

with open('csv/fantasy_team.csv') as t:
    reader_f_team = csv.reader(t)
    lst_teams = []
    for row in reader_f_team:
        if row[0] != 'Team':
            lst_teams.append(Team(row[0], row[1], row[2], 0))

# add different properties to each driver based on race results
for driver in lst_drivers:
    for race1 in tab_results:
        if race1[2] == driver.id:
            driver.race_order.append(race1[8])
            driver.team_id.append(race1[3])
            driver.race.append(race1[7])
            driver.grid.append(race1[5])
            driver.status.append(race1[17])
            if race1[14] == r"\N":
                driver.rank_FL.append('21')
            else:
                driver.rank_FL.append(race1[14])
            for race2 in tab_results:
                if race2[1] == race1[1] and race2[3] == race1[3] and race2[2] != race1[2]:
                    driver.mate_id.append(race2[2])
                    driver.race_mate.append(race2[7])
                    driver.grid_mate.append(race2[5])
                    driver.mate_race_order.append(race2[8])

# add different properties to each driver based on qualifying results
for driver in lst_drivers:
    pole = []
    pole_mate = []
    for quali in tab_qualifying:
        if quali[2] == driver.id:
            pole.append(quali[5])
            for quali1 in tab_qualifying:
                if quali[1] == quali1[1] and quali[3] == quali1[3] and quali[2] != quali1[2]:
                    pole_mate.append(quali1[5])
    driver.pole = pole
    driver.pole_mate = pole_mate

# assign each driver to his team
for team in lst_teams:
    driver1 = []
    driver2 = []
    for race in lst_races_id:
        for i in range(0,20,2):
            j = lst_races_id.index(race)
            driver = lst_drivers[i]
            if driver.team_id[j] == team.id:
                driver1.append(driver)
        for i in range(1,20,2):
            j = lst_races_id.index(race)
            driver = lst_drivers[i]
            if driver.team_id[j] == team.id:
                driver2.append(driver)
    team.drivers = [driver1, driver2]

# compare our driver race results with his team mate for that race ID
def race_comp(driver, race_id):
    race_id = str(race_id)
    i = lst_races_id.index(race_id)
    if driver.race_order[i] < driver.mate_race_order[i]:
        return 1
    else:
        return 0

# compare our driver qualifying results with his team mate for that race ID
def quali_comp(driver, race_id):
    race_id = str(race_id)
    i = lst_races_id.index(race_id)
    if driver.pole[i] < driver.pole_mate[i]:
        return 1
    else:
        return 0

# check if a driver is in race streak
def race_streak(driver,race_id):
    race_id = str(race_id)
    i = lst_races_id.index(race_id)
    if i < 4:
        return 0
    j = 0
    bonus = 0
    while j <= i:
        if driver.race[j] == str("N") or driver.race[j] == str("R") or driver.race[j] == str("D"):
            bonus = 0
        else:
            if float(driver.race[j]) <= 10:
                bonus = bonus + 1
            else:
                bonus = 0
        j = j + 1
    if bonus%5 == 0 and bonus > 0: # 0%5 è 0 !
        return 1
    else:
        return 0

# check if a driver is in quali streak
def quali_streak(driver,race_id):
    race_id = str(race_id)
    i = lst_races_id.index(race_id)
    if i < 4:
        return 0
    j = 0
    bonus = 0
    while j <= i:
        if float(driver.pole[j]) <= 10:
            bonus = bonus + 1
        else:
            bonus = 0
        j = j + 1
    if bonus%5 == 0 and bonus > 0: # 0%5 è 0!
        return 1
    else:
        return 0

# check if a team is in race streak
def race_team_streak(team,race_id):
    race_id = str(race_id)
    i = lst_races_id.index(race_id)
    if i < 2:
        return 0
    j = 0
    bonus = 0
    while j <= i:
        if team.drivers[0][j].race[j] == str("N") or team.drivers[0][j].race[j] == str("R") or team.drivers[0][j].race[j] == str("D") or team.drivers[1][j].race[j] == str("N") or team.drivers[1][j].race[j] == str("R") or team.drivers[1][j].race[j] == str("D"):
            bonus = 0
        else:
            if float(team.drivers[0][j].race[j]) <= 10 and float(team.drivers[1][j].race[j]) <= 10:
                bonus = bonus + 1
            else:
                bonus = 0
        j = j + 1
    if bonus%3 == 0 and bonus > 0: # 0%3 è 0 !
        return 1
    else:
        return 0

# check if a team is in quali streak
def quali_team_streak(team,race_id):
    race_id = str(race_id)
    i = lst_races_id.index(race_id)
    if i < 2:
        return 0
    j = 0
    bonus = 0
    while j <= i:
        if float(team.drivers[0][j].pole[j]) <= 10 and float(team.drivers[1][j].pole[j]) <= 10:
            bonus = bonus + 1
        else:
            bonus = 0
        j = j + 1
    if bonus%3 == 0 and bonus > 0: # 0%3 è 0!
        return 1
    else:
        return 0

# return points driver has scored for his final race position
def race_point(driver,race_id):
    points = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
    i = lst_races_id.index(race_id)
    race_pos = driver.race_order[i]
    if float(race_pos) < 11:
        score = points[int(race_pos) - 1]
        return score
    else:
        return 0

# return bonus points for reaching the Q1, Q2 or Q3, for the position and the mate position
def quali_point(driver,race_id):
    points = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    i = lst_races_id.index(race_id)
    quali_pos = driver.pole[i]
    if float(quali_pos) < 11:
        score = points[int(quali_pos)-1]
        bonusQ3 = 3
        return score + bonusQ3
    if  float(quali_pos) > 10 and float(quali_pos) < 16:
        score = 0
        bonusQ2 = 2
        return score + bonusQ2
    else:
        score = 0
        bonusQ1 = 1
        return score + bonusQ1

# points only for drivers, return points
def driver_only(driver,race_id):
    i = lst_races_id.index(race_id)
    race_pos = driver.race[i]
    bonus_race_mate = 3 * race_comp(driver,race_id)
    bonus_quali_mate = 2 * quali_comp(driver,race_id)
    bonus_FL = 5 * fastest_lap(driver,race_id)
    if race_pos == 'R' or race_pos == 'N':
        return -10 + bonus_race_mate + bonus_quali_mate + bonus_FL
    if race_pos == 'D':
        return -20 + bonus_race_mate + bonus_quali_mate + bonus_FL
    else:
        return 0 + bonus_race_mate + bonus_quali_mate + bonus_FL

# number of position gained gives 2 pts per position up to 10 pts
# this function returns points!
def gain_position(driver,race_id):
    i = lst_races_id.index(race_id)
    gain = int(driver.grid[i]) - int(driver.race_order[i])
    if gain < 0:
        if int(driver.grid[i]) < 11:
            if gain < -6:
                return -10
            else:
                return 2 * gain # gain is negative
        else:
            if gain < -6:
                return -5
            else:
                return 2 * gain
    if gain > 5:
        return 2*5
    else:
        return 2*gain

# check for the fastest lap
def fastest_lap(driver,race_id):
    i = lst_races_id.index(race_id)
    if int(driver.rank_FL[i]) == 1:
        return 1
    else:
        return 0

# check for race finisher
def finisher(driver,race_id):
    i = lst_races_id.index(race_id)
    if driver.status[i] == '1':
        return 1
    else:
        return 0

# check if your team is valid, that means you didn't go under yout budget
def validate(lst_team,t):
    tot = float(t.price)
    for d in lst_team:
        tot = tot + float(d.price)
    if (tot > budget):
        print('invalid team, budget: ' + str(budget - tot))
        return False
    print('team is ok, budget: '+ str(budget - tot))
    return True

# it simulates a season
def simulation(lst_drivers,lst_team):
    score = []
    for race in lst_races_id:
        i = lst_races_id.index(race)
        race_score = []
        for d in lst_drivers:
            bonus_race_streak = 10 * race_streak(d,race)
            bonus_quali_strak = 5 * quali_streak(d,race)
            bonus_finischer = 1 * finisher(d,race)
            bonus_driver_only = driver_only(d,race)
            bonus_position = gain_position(d,race)
            race_points = race_point(d,race)
            quali_points = quali_point(d,race)

            race_score.append(bonus_race_streak + bonus_quali_strak + bonus_finischer + bonus_driver_only + bonus_position + race_points + quali_points)
            d.score_for_races.append(bonus_race_streak + bonus_quali_strak + bonus_finischer + bonus_driver_only + bonus_position + race_points + quali_points)

        for team in lst_team:
            team_score = []
            for t in team.drivers:
                bonus_race_streak = 10 * race_streak(t[i], race)
                bonus_quali_strak = 5 * quali_streak(t[i], race)
                bonus_finischer = 1 * finisher(t[i], race)
                bonus_position = gain_position(t[i], race)
                race_points = race_point(t[i], race)
                quali_points = quali_point(t[i], race)

                team_score.append(bonus_race_streak + bonus_quali_strak + bonus_finischer + bonus_position + race_points + quali_points)

            bonus_race_team_streak = 10 * race_team_streak(team, race)
            bonus_quali_team_streak = 5 * quali_team_streak(team, race)
            team_score.append(bonus_race_team_streak + bonus_quali_team_streak)

            team.score_by_drivers[0].append(team_score[0])
            team.score_by_drivers[1].append(team_score[1])
            team.score_by_drivers[2].append(team_score[2])
            team.score_for_races.append(sum(team_score))

        score.append(race_score)
    return score

def final_score(my_drivers,my_team):
    if validate(lst_my_drivers, my_team):
        tot = sum(my_team.score_for_races)
        for d in my_drivers:
            tot = tot + sum(d.score_for_races)
        return tot
    else:
        return 'Final score of invalid team is 0'

# create dictionary for races name
id = []
name_race = []
for row in tab_races:
    id.append(row[0])
    name_race.append(row[4])
dic_races = dict(zip(id,name_race))

# it moves your team in a list called lst_my_team
lst_my_drivers = []
for d in lst_drivers:
    if d.id == dic_drivers[id_d0]:
        lst_my_drivers.append(d)
    if d.id == dic_drivers[id_d1]:
        lst_my_drivers.append(d)
    if d.id == dic_drivers[id_d2]:
        lst_my_drivers.append(d)
    if d.id == dic_drivers[id_d3]:
        lst_my_drivers.append(d)
    if d.id == dic_drivers[id_d4]:
        lst_my_drivers.append(d)
for t in lst_teams:
    if t.id == dic_teams[id_t0]:
        my_team = t

simulation(lst_drivers,lst_teams)
print(final_score(lst_my_drivers,my_team))
print(sum(my_team.score_for_races))
# set width of bar
barWidth = 0.1

# set height of bar
bars1 = lst_my_drivers[0].score_for_races #list points driver1
bars2 = lst_my_drivers[1].score_for_races #list points driver2
bars3 = lst_my_drivers[2].score_for_races #list points driver3
bars4 = lst_my_drivers[3].score_for_races #list points driver4
bars5 = lst_my_drivers[4].score_for_races #list points driver5
bars6 = my_team.score_by_drivers[0] #list points driver 1 my team
bars7 = my_team.score_by_drivers[1] #list points driver 2 my team
bars8 = my_team.score_by_drivers[2] #list streak point
bars9 = my_team.score_for_races #list tot points
 
# Set position of bar on X axis
r1 = np.arange(len(bars1))
r2 = [x + barWidth for x in r1] 
r3 = [x + barWidth for x in r2]
r4 = [x + barWidth for x in r3]
r5 = [x + barWidth for x in r4]
r6 = [x + barWidth for x in r5]
r7 = [x + barWidth for x in r6]
r8 = [x + barWidth for x in r7]
r9 = [x + barWidth for x in r8]
 
# Make the plot
plt.bar(r1, bars1, color='#ebc83d', width=barWidth, edgecolor='white', label=lst_my_drivers[0].name)
plt.bar(r2, bars2, color='#badf55', width=barWidth, edgecolor='white', label=lst_my_drivers[1].name)
plt.bar(r3, bars3, color='#35b1c9', width=barWidth, edgecolor='white', label=lst_my_drivers[2].name)
plt.bar(r4, bars4, color='#b06dad', width=barWidth, edgecolor='white', label=lst_my_drivers[3].name)
plt.bar(r5, bars5, color='#e96060', width=barWidth, edgecolor='white', label=lst_my_drivers[4].name)
plt.bar(r6, bars6, color='#7f6d5f', width=barWidth, edgecolor='white', label=my_team.name + ' driver1')
plt.bar(r7, bars7, color='#557f2d', width=barWidth, edgecolor='white', label=my_team.name + ' driver2')
plt.bar(r8, bars8, color='#2d7f5e', width=barWidth, edgecolor='white', label='Team streak')
plt.bar(r9, bars9, color='#000000', width=barWidth, edgecolor='white', label='Team tot')

# create label list for the races
lst_label_race = []
for id in lst_races_id:
    lst_label_race.append(dic_races[id])

# Add xticks on the middle of the group bars
plt.xlabel('Races', fontweight='bold')
plt.ylabel('Points', fontweight='bold')
plt.xticks([r + barWidth for r in range(len(lst_races_id)+1)], lst_label_race, rotation=45)
 
# Create legend & Show graphic
plt.legend()
plt.show()
