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
    def __init__(self, name , id, team, team_id, mate, mate_id, price, turbo, points):
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

class Team:
    def __init__(self, name, id, price, points):
        self.name = name
        self.id = id
        self.price = price
        self.points = points

with open('races.csv') as f:
    reader_races = csv.reader(f)
    lst_races_id = []
    for row in reader_races:
        if '2019' == row[1]:
            lst_races_id.append(row[0])
    #print(lst_races_id)

with open('results.csv') as g:
    reader_results = csv.reader(g)
    tab_results = []
    for row in reader_results:
        for id in lst_races_id:
            if row[1] == id:
                tab_results.append(row)
        
with open('qualifying.csv') as h:
    reader_qualifying = csv.reader(h)
    tab_qualifying = []
    for row in reader_qualifying:
        for id in lst_races_id:
            if row[1] == id:
                tab_qualifying.append(row)

with open('fantasy_driver.csv') as d:
    reader_f_driver = csv.reader(d)
    lst_drivers = []
    for row in reader_f_driver:
        if row[0] != 'Driver':
            lst_drivers.append(Driver(row[0], row[1], row[2], row[3], row[4], row[5], row[6], False, 0))

with open('fantasy_team.csv') as t:
    reader_f_team = csv.reader(t)
    lst_teams = []
    for row in reader_f_team:
        if row[0] != 'Team':
            lst_teams.append(Team(row[0], row[1], row[2], 0))

for driver in lst_drivers:
        team = []
        mate = []
        results = []
        grid = []
        for race in tab_results:
            if race[2] == driver.id:
                team.append(race[3])
                results.append(race[6])
                grid.append(race[5])
                for race1 in tab_results:
                    if race1[1] == race[1] and race1[3] == race[3] and race1[2] != race[2]:
                        mate.append(race1[2])
        driver.mate_id = mate
        driver.team_id = team
        driver.race = results
        driver.grid = grid

def race_comp(driver):
    i = 0
    race_comp = []
    for race in lst_races_id:
        if driver.race[i] < driver.race_mate[i]:
            race_comp.append(1)
        else:
            race_comp.append(0)
        i = i + 1
    return race_comp

def quali_comp(driver):
    i = 0
    quali_comp = []
    for quali in lst_races_id:
        if driver.pole[i] < driver.pole_mate[i]:
            quali_comp.append(1)
        else:
            quali_comp.append(0)
        i = i + 1
    return quali_comp

def race_comp1(driver,race_id):
    race_id = str(race_id)
    i = lst_races_id.index(race_id)
    if driver.race[i] < driver.race_mate[i]:
        return 1
    else:
        return 0

def quali_comp1(driver,race_id):
    race_id = str(race_id)
    race_id = str(race_id)
    i = lst_races_id.index(race_id)
    if driver.race[i] < driver.race_mate[i]:
        return 1
    else:
        return 0

#controlla se il team è valido    
def validate(d0, d1, d2, d3, d4, t0):
    tot = float(d0.price) + float(d1.price) + float(d2.price) + float(d3.price) + float(d4.price) + float(t0.price)
    if (tot > budget):
        print('invalid team')
        return False
    print('team is ok')
    return True

#simula una stagione
def simulation(d0, d1, d2, d3, d4, t0):
    if validate(d0, d1, d2, d3, d4, t0) == False: 
        return

#crea la tua squadra my_driver0, my_driver1, my_driver2, my_driver3, my_driver4, my_team
for d in lst_drivers:
    if d.id == id_d0: 
        my_driver0 = d
    if d.id == id_d1: 
        my_driver1 = d
    if d.id == id_d2: 
        my_driver2 = d
    if d.id == id_d3: 
        my_driver3 = d
    if d.id == id_d4: 
        my_driver4 = d
for t in lst_teams:
    if t.id == id_t0:
        my_team = t
        
validate(my_driver0, my_driver1, my_driver2, my_driver3, my_driver4, my_team)