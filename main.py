import csv
import numpy as np
import matplotlib.pyplot as plt
 
budget = 100

# id of your drivers and team
id_d0 = '1'
id_d1 = '815'
id_d2 = '154'
id_d3 = '825'
id_d4 = '847'
id_t0 = '131'

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

class Team:
    def __init__(self, name, id, price, points):
        self.name = name
        self.id = id
        self.price = price
        self.points = points
        self.drivers = []

with open('csv/races.csv') as f:
    reader_races = csv.reader(f)
    lst_races_id = []
    for row in reader_races:
        if '2019' == row[1]:
            lst_races_id.append(row[0])
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
        if driver.id == quali[2]:
            pole.append(quali[5])
            for quali1 in tab_qualifying:
                if quali1[1] == quali[1] and quali1[3] == quali[3] and quali1[2] != quali[2]:
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
def simulation(lst_my_drivers,my_team):
    global race_point
    if validate(lst_my_drivers,my_team) == False:
        return
    score = []
    for race in lst_races_id:
        i = lst_races_id.index(race)
        race_score = []
        for d in lst_my_drivers:
            bonus_race_streak = 10 * race_streak(d,race)
            bonus_quali_strak = 5 * quali_streak(d,race)
            bonus_finischer = 1 * finisher(d,race)
            bonus_driver_only = driver_only(d,race)
            bonus_position = gain_position(d,race)
            race_points = race_point(d,race)
            quali_points = quali_point(d,race)

            race_score.append(bonus_race_streak + bonus_quali_strak + bonus_finischer + bonus_driver_only + bonus_position + race_points + quali_points)

            bonus_race_team_streak = race_team_streak(my_team,race)
            bonus_quali_team_streak = quali_team_streak(my_team,race)
            race_score.append(bonus_race_team_streak + bonus_quali_team_streak)
        for t in my_team.drivers:
            bonus_race_streak = 10 * race_streak(t[i],race)
            bonus_quali_strak = 5 * quali_streak(t[i],race)
            bonus_finischer = 1 * finisher(t[i],race)
            bonus_position = gain_position(t[i],race)
            race_points = race_point(t[i],race)
            quali_points = quali_point(t[i],race)

            race_score.append(bonus_race_streak + bonus_quali_strak + bonus_finischer + bonus_position + race_points + quali_points)
        score.append(race_score)
    return score

def final_score(score):
    tot = 0
    for race in score:
        for x in race:
            tot = tot + x
    return tot



# it moves your team in a list called lst_my_team
lst_my_drivers = []
for d in lst_drivers:
    if d.id == id_d0:
        lst_my_drivers.append(d)
    if d.id == id_d1:
        lst_my_drivers.append(d)
    if d.id == id_d2:
        lst_my_drivers.append(d)
    if d.id == id_d3:
        lst_my_drivers.append(d)
    if d.id == id_d4:
        lst_my_drivers.append(d)
for t in lst_teams:
    if t.id == id_t0:
        my_team = t

validate(lst_my_drivers, my_team)

#for d in lst_my_team[:-1]:
#    print(d.name)

#print(lst_drivers[2].pole)
print(lst_teams[1].drivers[0][0].pole)
print(lst_teams[1].drivers[1][0].pole)

results = simulation(lst_my_drivers,my_team)
print(str(results))
if validate(lst_my_drivers, my_team):
    print(str(final_score(results)))

# set width of bar
barWidth = 0.1
 
# set height of bar
bars1 = [12, 30, 1, 8, 22] #list points driver1
bars2 = [28, 6, 16, 5, 10] #list points driver2
bars3 = [29, 3, 24, 25, 17] #list points driver3
bars4 = [28, 6, 16, 5, 10] #list points driver4
bars5 = [29, 3, 24, 25, 17] #list points driver5
bars6 = [28, 6, 16, 5, 10] #list points team driver1
bars7 = [29, 3, 24, 25, 17] #list points team driver2
bars8 = [28, 6, 16, 5, 10] #list streak point
bars9 = [29, 3, 24, 25, 17] #list tot points
 
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
plt.bar(r8, bars8, color='#2d7f5e', width=barWidth, edgecolor='white', label='Streak')
plt.bar(r9, bars9, color='#000000', width=barWidth, edgecolor='white', label='Tot')

 
# Add xticks on the middle of the group bars
plt.xlabel('Races', fontweight='bold')
plt.ylabel('Points', fontweight='bold')
plt.xticks([r + barWidth for r in range(len(lst_races_id)+1)], lst_races_id)
 
# Create legend & Show graphic
plt.legend()
plt.show()
