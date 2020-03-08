import csv

budget = 100

class Driver:
    def __init__(self, name , id, team, team_id, mate, mate_id, price, points):
        self.name = name
        self.id = id
        self.team = team
        self.team_id = team_id
        self.mate = mate
        self.mate_id = mate_id
        self.price = price
        self.points = points

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
            lst_drivers.append(Driver(row[0], row[1], row[2], row[3], row[4], row[5], row[6], 0))
    for d in lst_drivers:
        print(d.name)

with open('fantasy_team.csv') as t:
    reader_f_team = csv.reader(t)
    lst_teams = []
    for row in reader_f_team:
        if row[0] != 'Team':
            lst_teams.append(Team(row[0], row[1], row[2], 0))
    for t in lst_teams:
        print(t.name)

def validate(d0, d1, d2, d3, d4, t0):
    tot = d0.price + d1.price + d2.price + d3.price + d4.price + t0.price
    if (tot > budget):
        print('invalid team')
        return False
    return True

def simulation(d0, d1, d2, d3, d4, t0):
    if validate == False: 
        return
