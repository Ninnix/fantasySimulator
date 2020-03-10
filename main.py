import csv

budget = 100

# id dei tuoi piloti e del tuo team
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
        self.team_id = team_id
        self.mate = mate
        self.mate_id = mate_id
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

class Team:
    def __init__(self, name, id, price, points):
        self.name = name
        self.id = id
        self.price = price
        self.points = points


with open('csv/races.csv') as f:
    reader_races = csv.reader(f)
    lst_races_id = []
    for row in reader_races:
        if '2019' == row[1]:
            lst_races_id.append(row[0])
    # print(lst_races_id)

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
    team = []
    mate = []
    results = []
    grid = []
    race_mate = []
    grid_mate = []
    rank_FL = []
    race_order = []
    mate_race_order = []
    for race in tab_results:
        if race[2] == driver.id:
            race_order.append(race[8])
            team.append(race[3])
            results.append(race[7])
            grid.append(race[5])
            if race[14] == r"\N":
                rank_FL.append('21')
            else:
                rank_FL.append(race[14])
            for race1 in tab_results:
                if race1[1] == race[1] and race1[3] == race[3] and race1[2] != race[2]:
                    mate.append(race1[2])
                    race_mate.append(race1[7])
                    grid_mate.append(race1[5])
                    mate_race_order.append(race1[8])
    driver.mate_race_order = mate_race_order
    driver.rank_FL = rank_FL
    driver.mate_id = mate
    driver.team_id = team
    driver.race = results
    driver.race_order = race_order
    driver.grid = grid
    driver.race_mate = race_mate
    driver.grid_mate = grid_mate

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

def race_comp1(driver):
    i = 0
    race_comp = []
    for race in lst_races_id:
        if driver.race[i] < driver.race_mate[i]:
            race_comp.append(1)
        else:
            race_comp.append(0)
        i = i + 1
    return race_comp


def quali_comp1(driver):
    i = 0
    quali_comp = []
    for quali in lst_races_id:
        if driver.pole[i] < driver.pole_mate[i]:
            quali_comp.append(1)
        else:
            quali_comp.append(0)
        i = i + 1
    return quali_comp

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

# controlla se un driver è in race streak
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

# controlla se un driver è in quali streak
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

# return points driver has scored for his final race position
def race_point(driver,race_id):
    points = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
    i = lst_races_id.index(race_id)
    race_pos = driver.race[i]
    bonus_mate = 3 * race_comp(driver, race_id)
    if race_pos == 'R' or race_pos == 'N':
        return -10
    if race_pos == 'D':
        return -20
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
    bonus_mate = 2*quali_comp(driver,race_id)
    if float(quali_pos) < 11:
        score = points[int(quali_pos)-1]
        bonusQ3 = 3
        return score + bonusQ3 + bonus_mate
    if  float(quali_pos) > 10 and float(quali_pos) < 16:
        score = 0
        bonusQ2 = 2
        return score + bonusQ2 + bonus_mate
    else:
        score = 0
        bonusQ1 = 1
        return score + bonusQ1 + bonus_mate

# number of position gained gives 2 pts per position up to 10 pts
def gain_position(driver,race_id):
    i = lst_races_id.index(race_id)
    gain = int(driver.grid[i]) - int(driver.race_order[i])
    if gain < 0:
        return 0
    if gain > 5:
        return 5
    else:
        return gain

# check for the fastest lap
def fastest_lap(driver,race_id):
    i = lst_races_id.index(race_id)
    if int(driver.rank_FL[i]) == 1:
        return 1
    else:
        return 0

# controlla se il team è valido ( cioè non supero il budget)
def validate(lst_team):
    tot = 0
    for d in lst_team:
        tot = tot + float(d.price)
    if (tot > budget):
        print('invalid team')
        return False
    print('team is ok')
    return True


# simula una stagione
def simulation(lst_team):
    if validate(lst_team) == False:
        return

# crea la tua squadra in una lista lst_my_team
lst_my_team = []
for d in lst_drivers:
    if d.id == id_d0:
        lst_my_team.append(d)
    if d.id == id_d1:
        lst_my_team.append(d)
    if d.id == id_d2:
        lst_my_team.append(d)
    if d.id == id_d3:
        lst_my_team.append(d)
    if d.id == id_d4:
        lst_my_team.append(d)
for t in lst_teams:
    if t.id == id_t0:
        lst_my_team.append(t)

validate(lst_my_team)

#for d in lst_my_team[:-1]:
#    print(d.name)

#print(lst_drivers[2].pole)
print(lst_drivers[0].race_order)
print(lst_drivers[0].grid)
for race in lst_races_id:
#    for d in lst_drivers:
    print(fastest_lap(lst_drivers[1],race))