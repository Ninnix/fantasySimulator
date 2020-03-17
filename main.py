import csv
import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import sys

budget = 100

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
        self.drivers = [[] for _ in range(22)]
        self.score_by_drivers = [[], [], []]
        self.score_for_races = []

csv_races = 'csv/races.csv'
csv_results = 'csv/results.csv'
csv_qualifying = 'csv/qualifying.csv'
csv_fantasy_drivers = 'csv/fantasy_driver_2018.csv'
csv_fantasy_teams = 'csv/fantasy_team_2018.csv'
year = '2018'

lst_races_id = []
tab_races = []
tab_results = []
tab_qualifying = []
lst_drivers = []
lst_teams = []
lst_my_drivers = []
my_team = []
dic_drivers = dict()
dic_teams = dict()
dic_races = dict()

def read_season(year):
    if year == '2019':
        csv_fantasy_drivers = 'csv/fantasy_driver_2019.csv'
        csv_fantasy_teams = 'csv/fantasy_team_2019.csv'
    if year == '2018':
        csv_fantasy_drivers = 'csv/fantasy_driver_2018.csv'
        csv_fantasy_teams = 'csv/fantasy_team_2018.csv'
    with open(csv_races) as f:
        reader_races = csv.reader(f)
        # lst_races_id = []
        # tab_races = []
        for row in reader_races:
            if year == row[1]:
                lst_races_id.append(row[0])
                tab_races.append(row)

    with open(csv_results) as g:
        reader_results = csv.reader(g)
        # tab_results = []
        for row in reader_results:
            for id in lst_races_id:
                if row[1] == id:
                    tab_results.append(row)

    with open(csv_qualifying) as h:
        reader_qualifying = csv.reader(h)
        # tab_qualifying = []
        for row in reader_qualifying:
            for id in lst_races_id:
                if row[1] == id:
                    tab_qualifying.append(row)

    with open(csv_fantasy_drivers) as d:
        reader_f_driver = csv.reader(d)
        # lst_drivers = []
        for row in reader_f_driver:
            if row[0] != 'Driver':
                lst_drivers.append(Driver(row[0], row[1], row[2], row[3], row[4], row[5], row[6], False, 0))

    with open(csv_fantasy_teams) as t:
        reader_f_team = csv.reader(t)
        # lst_teams = []
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
            j = lst_races_id.index(race)
            for d in lst_drivers:
                if d.team_id[j] == team.id:
                    team.drivers[j].append(d)
            driver1.append(team.drivers[j][0])
            driver2.append(team.drivers[j][1])
        team.drivers = [driver1, driver2]

    # create dictionary for drivers name
    lst_id_drivers = []
    lst_name_drivers = []
    for d in lst_drivers:
        lst_id_drivers.append(d.id)
        lst_name_drivers.append(d.name)
    dic_drivers_loc = dict(zip(lst_name_drivers, lst_id_drivers))
    dic_drivers.update(dic_drivers_loc)

    # create dictionary for teams name
    lst_id_teams = []
    lst_name_teams = []
    for t in lst_teams:
        lst_id_teams.append(t.id)
        lst_name_teams.append(t.name)
    dic_teams_loc = dict(zip(lst_name_teams, lst_id_teams))
    dic_teams.update(dic_teams_loc)

    # create dictionary for races name
    lst_id_races = []
    lst_name_races = []
    for row in tab_races:
        lst_id_races.append(row[0])
        lst_name_races.append(row[4])
    dic_races_loc = dict(zip(lst_id_races, lst_name_races))
    dic_races.update(dic_races_loc)

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
    for d in lst_drivers:
        print(d.name)
    return score

def final_score(my_drivers,my_team):
    if validate(my_drivers, my_team):
        tot = sum(my_team.score_for_races)
        for d in my_drivers:
            tot = tot + sum(d.score_for_races)
        return tot
    else:
        return 'Final score of invalid team is 0'

read_season(year)

# create list with drivers prices
lst_drivers_prices = []
for d in lst_drivers:
    lst_drivers_prices.append(d.price)

# create list with teams prices
lst_teams_prices = []
for t in lst_teams:
    lst_teams_prices.append(t.price)

# create a list of str that contains drivers names and prices
lst_d_with_prices = []
for d, p in zip(lst_drivers, lst_drivers_prices):
    lst_d_with_prices.append(d.name + ' (' + p + '€)')

# create a list of str that contains teams names and prices
lst_t_with_prices = []
for t, p in zip(lst_teams,lst_teams_prices):
    lst_t_with_prices.append(t.name + ' (' + p + '€)')

# it moves your team in a list called lst_my_drivers
def name_to_object(lst_my_drivers_fullname,my_team_fullname):
    lst_my_drivers_name = []
    for fullname in lst_my_drivers_fullname:
        splitted = fullname.split()
        lst_my_drivers_name.append(splitted[0])
    my_team_name = []
    splitted = my_team_fullname.split()
    splitted.pop()
    my_team_name = splitted
    if len(my_team_name) == 2:
         my_team_name = my_team_name[0] + ' ' + my_team_name[1]
    else:
        my_team_name = str(my_team_name[0])
    lst_my_drivers = []
    for d in lst_drivers:
        for name in lst_my_drivers_name:
            if d.id == dic_drivers[name]:
                lst_my_drivers.append(d)
    for t in lst_teams:
        if t.id == dic_teams[my_team_name]:
            my_team = t
    my_team_obj = [lst_my_drivers,my_team]
    return my_team_obj

# def simulation(lst_drivers,lst_teams):
#     simulation(lst_drivers,lst_teams)
#     total_points = final_score(lst_my_drivers,my_team)
#     Constrtuctor_points = sum(my_team.score_for_races)

def plot(lst_my_drivers,my_team):
    # set width of bar
    barWidth = 0.1

    # set height of bar
    bars1 = lst_my_drivers[0].score_for_races  # list points driver1
    bars2 = lst_my_drivers[1].score_for_races  # list points driver2
    bars3 = lst_my_drivers[2].score_for_races  # list points driver3
    bars4 = lst_my_drivers[3].score_for_races  # list points driver4
    bars5 = lst_my_drivers[4].score_for_races  # list points driver5
    bars6 = my_team.score_by_drivers[0]  # list points driver 1 my team
    bars7 = my_team.score_by_drivers[1]  # list points driver 2 my team
    bars8 = my_team.score_by_drivers[2]  # list streak point
    bars9 = my_team.score_for_races  # list tot points

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
    plt.bar(r8, bars8, color='#2d7f5e', width=barWidth, edgecolor='white', label=my_team.name + ' streak')
    plt.bar(r9, bars9, color='#000000', width=barWidth, edgecolor='white', label=my_team.name + ' tot')

    # create label list for the races
    lst_label_race = []
    for id in lst_races_id:
        lst_label_race.append(dic_races[id])

    # Add xticks on the middle of the group bars
    plt.xlabel('Races', fontweight='bold')
    plt.ylabel('Points', fontweight='bold')
    plt.xticks([r + barWidth for r in range(len(lst_races_id) + 1)], lst_label_race, rotation=45)

    # Create legend & Show graphic
    plt.legend()
    plt.show()

def year_selection(self):
    if self.year19.isChecked():
        year = '2019'

        del lst_races_id[:]
        del tab_races[:]
        del tab_results[:]
        del tab_qualifying[:]
        del lst_drivers[:]
        del lst_teams[:]
        del lst_my_drivers[:]
        del my_team[:]
        dic_drivers.clear()
        dic_teams.clear()
        dic_races.clear()

        read_season(year)
        self.b1.setEnabled(True)
    else:
        year = '2018'

        del lst_races_id[:]
        del tab_races[:]
        del tab_results[:]
        del tab_qualifying[:]
        del lst_drivers[:]
        del lst_teams[:]
        del lst_my_drivers[:]
        del my_team[:]
        dic_drivers.clear()
        dic_teams.clear()
        dic_races.clear()

        read_season(year)
        self.b1.setEnabled(True)

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow,self).__init__()
        self.initUI()

    def b1_clicked(self):
        simulation(lst_drivers, lst_teams)
        # self.label.setText("Season simulated")
        # self.update_label()
        # self.label.setGeometry(50, 80, 200, 30)

        self.b2.setEnabled(True)
        self.b1.setEnabled(False)

    def b2_clicked(self):
        if plt.fignum_exists(plt.gcf().number):
            plt.close() # close plot if already open

        lst_my_drivers = []
        range_d = range(0,int(self.list_selected_driver.count()))
        for i in range_d:
            lst_my_drivers.append(self.list_selected_driver.item(i).text())
        my_team = self.list_selected_team.item(0).text()

        my_team_obj = name_to_object(lst_my_drivers,my_team)
        self.lst_my_drivers = my_team_obj[0]
        self.my_team = my_team_obj[1]

        plot(self.lst_my_drivers,self.my_team)

    def get_driver(self):
        active_drivers = int(self.list_selected_driver.count())
        # print(active_drivers)
        if active_drivers + 1 < 6: # 1 represent the driver the "if" will add if true
            selected_driver =  self.list_driver.currentItem().text()
            self.list_selected_driver.addItem(selected_driver)
            # print(selected_driver)

    def get_team(self):
        active_team = int(self.list_selected_team.count())
        # print(active_drivers)
        if active_team + 1 < 2: # 1 represent the driver the "if" will add if true
            selected_team =  self.list_team.currentItem().text()
            self.list_selected_team.addItem(selected_team)
            # print(selected_driver)

    def remove_driver(self):
        selected_driver = self.list_selected_driver.currentItem()
        self.list_selected_driver.takeItem(self.list_selected_driver.row(selected_driver))

    def remove_team(self):
        selected_team = self.list_selected_team.currentItem()
        self.list_selected_team.takeItem(self.list_selected_team.row(selected_team))

    def year_switch(self):
        year_selection(self)


    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText("Simulate then plot")
        self.label.setGeometry(50, 50, 200, 30)

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setGeometry(0,0,100,30)
        self.b1.setText("Simulate season")
        self.b1.clicked.connect(self.b1_clicked)
        self.b1.setEnabled(False)

        self.b2 = QtWidgets.QPushButton(self)
        self.b2.setGeometry(700, 450, 80, 30)
        self.b2.setText("Plot results")
        self.b2.clicked.connect(self.b2_clicked)
        self.b2.setDisabled(True)

        self.centraldock = QDockWidget('',self)
        self.setCentralWidget(self.centraldock)

        self.list_driver = QListWidget()
        self.list_driver.addItems(lst_d_with_prices)

        self.list_team = QListWidget()
        self.list_team.addItems(lst_t_with_prices)

        self.list_selected_driver = QListWidget()
        self.list_selected_team = QListWidget()

        self.list_driver.itemDoubleClicked.connect(self.get_driver)
        self.list_team.itemDoubleClicked.connect(self.get_team)
        self.list_selected_driver.itemDoubleClicked.connect(self.remove_driver)
        self.list_selected_team.itemDoubleClicked.connect(self.remove_team)

        self.year19 = QRadioButton('2019')
        self.year19.toggled.connect(self.year_switch)
        self.year18 = QRadioButton('2018')

        self.dock1 = QDockWidget('Select Drivers',self)
        self.addDockWidget(Qt.LeftDockWidgetArea,self.dock1)
        self.dock1.setWidget(self.list_driver)
        self.dock1.setFloating(False)

        self.dock2 = QDockWidget('Select Team',self)
        self.addDockWidget(Qt.LeftDockWidgetArea,self.dock2)
        self.dock2.setWidget(self.list_team)

        self.dock3 = QDockWidget('Your Drivers',self)
        self.addDockWidget(Qt.RightDockWidgetArea,self.dock3)
        self.dock3.setWidget(self.list_selected_driver)

        self.dock4 = QDockWidget('Your Team',self)
        self.addDockWidget(Qt.RightDockWidgetArea,self.dock4)
        self.dock4.setWidget(self.list_selected_team)
        self.dock2.setFloating(False)

        hbox = QHBoxLayout()
        box_year = QVBoxLayout()
        box_year.addWidget(self.year18)
        box_year.addWidget(self.year19)
        hbox.addLayout(box_year)
        hbox.addStretch(1)
        hbox.addWidget(self.b1)
        hbox.addWidget(self.b2)
        #
        vbox = QVBoxLayout()
        # vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addStretch(1)


        self.dockedWidget = QWidget(self)
        self.centraldock.setWidget(self.dockedWidget)
        self.dockedWidget.setLayout(vbox)
        # self.dockedWidget.layout().addWidget(self.b1)
        # self.dockedWidget.layout().addWidget(self.b2)
        # self.dockedWidget.layout().addWidget(self.year18)
        # self.dockedWidget.layout().addWidget(self.year19)

        self.setGeometry(200, 200, 800, 1000)
        self.setWindowTitle("Fantasy Simulator")

    def update_label(self):
        self.label.adjustSize()

def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

window()