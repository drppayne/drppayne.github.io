
# Version 10/15/2019
# No db connection, all variables are lists.
# Game is entirely text based

#Starts up the game

#import global modules
import random
from collections import defaultdict
# import pandas as pd
import numpy as np
from datetime import date
import math
import csv

#import game modules
# from buy_functions import *

##create global variables

#gameplay variables
turn = 0
year = 2019
score = []
points_earned = []
liv_point = []
ent_point = []
home_point = []
car_point = []
ret_point = []
event_point = [0]
event_pmt = [0]
ong_event_points = float(0)
ong_event_costs = float(0)

#income variables
wage_inc = [0]
debt_inc = [0]
other_inc = [0]
net_inc = [0]

#expense variables
tax_pmt = [0]
liv_pmt = [0]
util_pmt = [0]
home_tax_pmt = [0]
home_ins_pmt = [0]
home_maint_pmt = [0]
car_maint_pmt = [0]
car_ins_pmt = [0]
health_ins_pmt = [0]
mort_pmt = [0]
car_pmt = [0]
cc_pmt = [0]
student_pmt = [0]
misc_pmt = [0]
ret_pmt = [0]
ent_pmt = [0]
car_xtra_pmt = [0]
cc_xtra_pmt = [0]
mort_xtra_pmt = [0]
stu_xtra_pmt = [0]

#asset variables
sav_val = [5000]
car_val = [0]
home_val = [0]
ret_val = [0]
net_worth = [0]

sav_grow_rate = float(.01)
car_dep_rate = float(0.13)
home_app_rate = float(0.02)
ret_grow_rate = float(.08)
cc_limit = float(0)

#debt variables
mort_bal = [0]
cc_bal = [0]
student_bal = [0]
car_bal = [0]

mort_rate = float(.065)
car_rate = float(.045)
cc_rate = float(.18)
student_rate = float(.047)

#car MASH options
car_dict = {'style' : [], 'Original value' : [], 'Current value' : []}
with open('txt_files/car_mash.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter = ',')
    car_styles = []
    car_min = []
    car_max = []

    for row in readCSV:
        style = row[0]
        car_styles.append(style)

        mn = row[1]
        car_min.append(mn)

        mx = row[2]
        car_max.append(mx)

#home MASH options
home_dict = {'style' : [], 'Original value' : [], 'Current value' : []}
with open('txt_files/home_mash.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter = ',')
    home_styles = []
    home_min = []
    home_max = []

    for row in readCSV:
        style = row[0]
        home_styles.append(style)

        mn = row[1]
        home_min.append(mn)

        mx = row[2]
        home_max.append(mx)

#event options
# event_dict = {'event_id' : [], 'event_type' : [], 'event_text' : [], 'xmin' : [], 'xmax' : [], 'buttonAtext' : [], 'buttonBtext' : []}
with open('txt_files/events.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter = ',')
    next(readCSV, None)  # skip the headers
    
    event_id = []
    event_type = []
    event_text = []
    event_xmin = []
    event_xmax = []
    event_ymin = []
    event_ymax = []
    event_a = []
    event_b = []
    row = 1
    
    for row in readCSV:
        _d = row[0]
        event_id.append(int(_d))

        _t = row[1]
        event_type.append(_t)
        
        _x = row[2]
        event_text.append(_x)

        mn = row[3]
        event_xmin.append(mn)

        mx = row[4]
        event_xmax.append(mx)

        ymn = row[5]
        event_ymin.append(ymn)

        ymx = row[6]
        event_ymax.append(ymx)

        a = row[7]
        event_a.append(a)

        b = row[8]
        event_b.append(b)

def dashboard():
    global turn

    print('\nWhat would you like to do?')
    print('Enter (0) to start a new game.')
    print('Enter (1) to view and edit your budget.')
    print('Enter (2) to view your income statement.')
    print('Enter (3) to view your balance sheet.')
    print('Enter (4) to go to the next turn.')
    print('Enter (5) to buy a new car.')
    print('Enter (6) to buy a new house.')
    
    choose = int(input())
    if choose not in range(0,7):
        print('Please enter a value between 0 and 6.')
    elif turn == 11:
        print('The game is over!  You scored ' + str(score[-1]) + '!  Great job!')
        quit()
    elif choose == 0:
        init()
    elif choose == 1:
        budget()
    elif choose == 2:
        inc_sheet(turn)
    elif choose == 3:
        bal_sheet(turn)
    elif choose == 4:
        new_turn()
    elif choose == 5:
        car_buy()
    elif choose == 6:
        home_buy()
    

#inititalize game
def init():
    global turn
    global cc_limit
    turn = 0
    
    # ret_pmt.append(0)
    # ent_pmt.append(0)
    # liv_pmt.append(0)

    print('\nWelcome! What is your name?')
    player_name = input()
    
    #generate starting income
    wage_inc[0] = (random.randrange(30000, 120000, 5000))
    print('Congratulations ' + player_name + ', you have just started your dream  job earning ' + str.format('${:,.0f}'.format(wage_inc[-1])) + ' per year!')
    cc_limit = wage_inc[0] * 0.50

    #buy a house
    home_buy()

    #buy a car
    car_buy()
    
    #calculate student loans
    student_bal[0] = (wage_inc[0]/4)

    #set entry [0] for credit card balance
    cc_bal.clear()
    cc_bal.append(0)
    
    #set entry [0] for points earned in year 0
    points_earned.clear()

    #set entry [0] for score
    score.clear()
    # score.append(0)

    #start the next turn
    #new_turn()

    #intialize expenses
        #calculate the tax payment, based on income
    tax_pmt[turn] = round(math.log1p(wage_inc[turn])/100*wage_inc[turn],0)

    #calculate the student loan payment
    student_pmt[turn] = (abs(np.pmt(student_rate, 10, student_bal[0])))
    
    #calculate other home expenses
    util_pmt[turn] = home_val[turn]*.013
    home_tax_pmt[turn] = home_val[turn]*.005
    home_ins_pmt[turn] = home_val[turn]*.012
    home_maint_pmt[turn] = home_val[turn]*random.randrange(1,25)/1000

    #calculate other car expenses
    car_maint_pmt[turn] = car_val[turn]*random.randrange(5,25)/1000
    car_ins_pmt[turn] = round(car_val[turn]*.02,-2)

    #calculate other expenses
    cc_pmt[turn] = cc_bal[turn]/50
    health_ins_pmt[turn] = .03*wage_inc[0]
    misc_pmt[turn] = random.randrange(17,33)/1000*wage_inc[turn] + ong_event_costs

    # Initialize Net Worth
    net_worth[turn] = (sav_val[turn] + car_val[turn] + home_val[turn] + ret_val[turn] 
        - cc_bal[turn] - student_bal[turn] - mort_bal[turn] - car_bal[turn] )

    dashboard()

#function to buy a new home - called at beginning of game and upon player request
def home_buy():
    repick = 'No'
    rate = mort_rate
    bal = float(0)
    equity = float(0)
    if turn > 0:
        equity = home_val[turn] - mort_bal[turn]
    while repick in ('No', 'no', 'n', 'N'):
        print('Which house would you like to buy? (enter 1-5)')
        choose = int(input())
        if choose not in range(1,6):
            print('Please enter a value between 1 and 5!')
        else:
            home_value = round(random.uniform(int(home_min[choose-1]),int(home_max[choose-1])),-3)
            bal = round(home_value - equity,0)
            house_pmt = abs(np.pmt(rate, 30, bal))
            print('You found a ' + home_styles[choose-1]
                  + ' for sale for ' + str.format('${:,.0f}'.format(home_value))
                  + '.  You currently have ' + str.format('${:,.0f}'.format(equity)) 
                  + ' of equity in your home, so you will have to borrow ' + str.format('${:,.0f}'.format(bal)) 
                  + ' and make annual loan payments of ' + str.format('${:,.0f}'.format(house_pmt))
                  + '.\nDo you want to buy this house?')
            repick = input()
        
    print('Very good, please enjoy your new ' + home_styles[choose-1] + '!')

    home_dict['style'] = home_styles[choose-1]
    home_dict['Original Value'] = home_value
    home_dict['Current Value'] = home_value

    #print(pd.DataFrame.from_dict(home_dict))
    mort_pmt[turn] = house_pmt
    mort_bal[turn] = bal
    home_val[turn] = home_value
    net_inc[turn] = net_inc[turn] + house_pmt - mort_pmt[turn-1]

#function to buy a new car - called at beginning of game and upon player request
def car_buy():
    repick = 'No'
    rate = car_rate
    c_pmt = float(0)
    equity = float(0)
    if turn > 0:
        equity = car_val[turn] - car_bal[turn]
    while repick in ('No', 'no', 'n', 'N'):
        print('Which car would you like to buy? (enter 1-5)')
        choose = int(input())
        if choose not in range(1,6):
            print('please enter a value between 1 and 5!')
        else:
            car_value = round(choose * 10000 + random.uniform(-5000,5000),-3)
            bal = round(car_value - equity,0)
            c_pmt = abs(np.pmt(rate, 5, bal))
            print('You found a ' + car_styles[choose-1]
                  + ' vehicle for sale for ' + str.format('${:,.0f}'.format(car_value))
                  + '.  You currently have ' + str.format('${:,.0f}'.format(equity)) 
                  + ' of equity in your car, so you will have to borrow ' + str.format('${:,.0f}'.format(bal)) 
                  + ' and make annual loan payments of ' + str.format('${:,.0f}'.format(c_pmt))
                  + '.\nDo you want to buy this vehicle?')
            repick = input()

    print('Very good, please enjoy your new ' + car_styles[choose-1] + ' vehicle!')

    car_dict['style'] = car_styles[choose-1]
    car_dict['Original Value'] = car_value
    car_dict['Current Value'] = car_value
    
    car_pmt[turn] = c_pmt
    car_bal[turn] = bal
    car_val[turn] = car_value
    net_inc[turn] = net_inc[turn] + c_pmt - car_pmt[turn-1]

#calculate the annual payment for an amortizing loan    

# def pmt(principal, annual_interest_rate, years):
#     payment = (principal*annual_interest_rate)/(1 - (1 + annual_interest_rate)**(-years))
#     return payment

#print the income statement
def inc_sheet(period):
    print('Income and Expense Statement for ' + str(year + period))
    total_pmt = float(0)
    total_pmt = tax_pmt[period] + util_pmt[period] \
    + home_tax_pmt[period] + home_ins_pmt[period] + home_maint_pmt[period] \
    + car_maint_pmt[period] + car_ins_pmt[period] + health_ins_pmt[period] \
    + mort_pmt[period] + car_pmt[period] + cc_pmt[period] + student_pmt[period] + misc_pmt[period] \
    + ret_pmt[period] + ent_pmt[period] + liv_pmt[period] \
    + cc_xtra_pmt[period] + car_xtra_pmt[period] + mort_xtra_pmt[period] + stu_xtra_pmt[period] \
    
    net_inc[period] = round(wage_inc[period] + debt_inc[period] + other_inc[period] - total_pmt, 0)

    print('\n--------------------- Income ----------------------')
    print('Salary \t\t\t\t' + str('${:,.0f}'.format(wage_inc[period])))
    print('Amount Borrowed \t\t' + str('${:,.0f}'.format(debt_inc[period])))
    print('Other Income \t\t\t' + str('${:,.0f}'.format(other_inc[period])))
    
    print('\n----------------- Fixed Expenses ------------------')
    print('Taxes \t\t\t\t' + str('${:,.0f}'.format(tax_pmt[period])))
    print('Mortgage Payment \t\t' + str('${:,.0f}'.format(mort_pmt[period])))
    print('Property Taxes \t\t\t' + str('${:,.0f}'.format(home_tax_pmt[period]))) 
    print('Home Maintenance \t\t' + str('${:,.0f}'.format(home_maint_pmt[period]))) 
    print('Home Insurance \t\t\t' + str('${:,.0f}'.format(home_ins_pmt[period])))
    print('Utilities \t\t\t' + str('${:,.0f}'.format(util_pmt[period])))
    print('Student Loan Payment \t\t' + str('${:,.0f}'.format(student_pmt[period])))
    print('Car Payment \t\t\t' + str('${:,.0f}'.format(car_pmt[period])))
    print('Car Maintenance \t\t' + str('${:,.0f}'.format(car_maint_pmt[period])))
    print('Car Insurance \t\t\t' + str('${:,.0f}'.format(car_ins_pmt[period])))
    print('Health Insurance \t\t' + str('${:,.0f}'.format(health_ins_pmt[period])))
    print('Credit Card Payment \t\t' + str('${:,.0f}'.format(cc_pmt[period])))
    print('Misc. Expenses \t\t\t' + str('${:,.0f}'.format(misc_pmt[period])))
    
    print('\n------------ Discretionary Expenses -------------')
    print('Living Expenses \t\t' + str('${:,.0f}'.format(liv_pmt[period])))
    print('Entertainment Expenses  \t' + str('${:,.0f}'.format(ent_pmt[period])))
    print('Retirement Contributions \t' + str('${:,.0f}'.format(ret_pmt[period])))
    print('\nExtra Mortgage Payment \t\t' + str('${:,.0f}'.format(mort_xtra_pmt[period])))
    print('Extra Student Loan Payment \t' + str('${:,.0f}'.format(stu_xtra_pmt[period])))
    print('Extra Car Payment \t\t' + str('${:,.0f}'.format(car_xtra_pmt[period])))
    print('Extra Credit Card Payment \t' + str('${:,.0f}'.format(cc_xtra_pmt[period])))
    print('\n-------------------------------------------------')
    print('Free Cash Flow \t\t\t' + str('${:,.0f}'.format(net_inc[period])))
    dashboard()
    # quit()

#Calculate the expenses for turn number, appends to lists
def calc_exp():
    global turn
    #get current home and car values from respective dicts
    # car_val = car_dict['Current Value']
    # home_val = home_dict['Current Value']

    wage_inc.append(wage_inc[turn-1])
    debt_inc.append(0)
    other_inc.append(0)
    net_inc.append(0)

    #calculate the tax payment, based on income
    tax_pmt.append(round(math.log1p(wage_inc[turn-1])/100*wage_inc[turn-1],0))

    #calculate the student loan payment
    if  student_bal[-1] <= 0:
        student_pmt.append(0)
    else:
        student_pmt.append(student_pmt[turn-1])
    
    #calculate the mort payment
    if mort_bal[-1] <=0:
        sav_val[turn] = sav_val[turn] + abs(min(mort_bal[-1],0))
        mort_bal[turn]
        mort_pmt.append(0)
    else:
        mort_pmt.append(mort_pmt[-1])

    #calculate other home expenses
    util_pmt.append(home_val[turn]*.013)
    home_tax_pmt.append(home_val[turn]*.005)
    home_ins_pmt.append(home_val[turn]*.012)
    home_maint_pmt.append(home_val[turn]*random.randrange(1,25)/1000)

    #calculate the car payment
    if car_bal[-1] <=0:
        sav_val[turn] = sav_val[turn] + abs(min(car_bal[-1],0))
        car_pmt.append( 0)
    else:
        car_pmt.append(car_pmt[-1])

    #calculate other car expenses
    car_maint_pmt.append(car_val[turn] * random.randrange(5,25) / 1000)
    car_ins_pmt.append(round(car_val[turn] * .02,-2))

    #calculate other expenses
    cc_pmt.append( cc_bal[turn]/50)
    health_ins_pmt.append(.03 * wage_inc[turn])
    misc_pmt.append(random.randrange(17,33)/1000 * wage_inc[turn] + ong_event_costs)

    #initialize new entry for variable expenses
    liv_pmt.append(liv_pmt[turn-1])
    ent_pmt.append(ent_pmt[turn-1])
    ret_pmt.append(ret_pmt[turn-1])
    stu_xtra_pmt.append(stu_xtra_pmt[turn-1])
    cc_xtra_pmt.append(cc_xtra_pmt[turn-1])
    car_xtra_pmt.append(car_xtra_pmt[turn-1])
    mort_xtra_pmt.append(mort_xtra_pmt[turn-1])

# Events
def event():
    global cc_bal
    global ong_event_points
    global ong_event_costs
    global turn
    
    
    cost = float(0)
    points = float(0)
    event_point.append(0)

    eid = random.randrange(0,event_id[-1])
    
    txt = event_text[eid]
    x = float(random.randrange(int(event_xmin[eid]),int(event_xmax[eid])))

    if int(event_ymin[eid]) == 0:
        points = cost / 100
    else:
        y = float(random.randrange(int(event_ymin[eid]),int(event_ymax[eid])))
        points = round(y,0)

    # percentage changes in salary
    if x < 100 and x > 0:
        cost = round( x / 100 * wage_inc[turn], -2)
    else:
        cost = round(x,-2)
    
    txt = txt.replace('_x',str.format('${:,.0f}'.format(cost)))
    txt = txt.replace('_y',str.format('{:,.0f}'.format(points)))
    
    opt_a = event_a[eid]
    opt_b = event_b[eid]

    # Display the event text
    print(str(event_type[eid]) + ': ' + txt + '\n')

    if event_type[eid] == 'Expense':
        print(str.format('${:,.0f}'.format(cost)) + ' was charged to your credit card.')
        cc_bal[turn] = cc_bal[turn] + cost
        cc_pmt[turn] = cc_bal[turn] / 50
        misc_pmt[turn] = misc_pmt[turn] + cost
        debt_inc[turn] = debt_inc[turn] + cost
    elif event_type[eid] == 'Salary':
        print('What would you like to do?\n' +
        'Enter (1) to ' + opt_a + ' and (2) to ' + opt_b + '.')
        choose = int(input())
        if choose == 1:
            print('Okay, let\'s go ahead and ' + opt_a + '.  Your income increased by ' 
            + str.format('${:,.0f}'.format(cost)) + ' per year.')
            wage_inc[turn] = round(wage_inc[turn]*(1 + x/100),-2)
            tax_pmt[turn] = (round(math.log1p(wage_inc[turn-1])/100*wage_inc[turn-1],0))
            event_point[turn] = points
        elif choose == 2:
            print('Okay, let\'s ahead and ' + opt_b)
        else:
            print('Please enter either 1 or 2.')
            choose = int(input())
    elif event_type[eid] == 'Income':
        other_inc[turn] = other_inc[turn] + cost
    elif event_type[eid] == 'Downgrade':
        car_val[turn] = car_val[turn] - cost
    elif event_type[eid] == 'Ongoing':
        ong_event_costs = ong_event_costs + cost
        ong_event_points = ong_event_points + points
    elif event_type[eid] == 'Upgrade':
        wage_inc[turn] = wage_inc[turn] + cost
        ong_event_points = ong_event_points + points
    elif event_type[eid] == 'Opportunity':
        print('What would you like to do?\n' +
        'Enter (1) to ' + opt_a + ' and (2) to ' + opt_b + '.')
        choose = int(input())
        
        if choose == 1:
            print('Okay, let\'s go ahead and ' + opt_a + '.  ' 
            + str.format('${:,.0f}'.format(cost)) + ' was charged to your credit card.')
            cc_bal[turn] = cc_bal[turn] + cost
            cc_pmt[turn] = cc_bal[turn] / 50
            event_point[turn] = points
        elif choose == 2:
            print('Okay, let\'s ahead and ' + opt_b)
        else:
            print('Please enter either 1 or 2.')
            choose = int(input())
    
    dashboard()

# enter budget figures
def budget():
    print('How much would you like to spend on living expenses?')
    liv_pmt[turn] = float(input())
    print('How much would you like to spend on entertainment?')
    ent_pmt[turn] = float(input())
    print('How much would you like to save for retirement?')
    ret_pmt[turn] = float(input())
    print('How much extra would you like to pay on your student loans?')
    stu_xtra_pmt[turn] = float(input())
    print('How much extra would you like to pay on your mortgage?')
    mort_xtra_pmt[turn] = float(input())
    print('How much extra would you like to pay on your credit card?')
    cc_xtra_pmt[turn] = float(input())
    print('How much extra would you like to pay on your car loan?')
    car_xtra_pmt[turn] = float(input())
    dashboard()

# print the balance sheet
def bal_sheet(period):
    net_worth[period] = (sav_val[period] + car_val[period] + home_val[period] + ret_val[period] 
        - cc_bal[period] - student_bal[period] - mort_bal[period] - car_bal[period] )
    print('\n---------------- Assets ------------------')
    print('Checking and Savings \t\t' + str('${:,.0f}'.format(sav_val[period])))
    print('Vehicle Value \t\t\t' + str('${:,.0f}'.format(car_val[period])))
    print('Home Value \t\t\t' + str('${:,.0f}'.format(home_val[period])))
    print('Retirement Savings \t\t' + str('${:,.0f}'.format(ret_val[period])))
    print('\n------------- Liabilities ----------------')
    print('Mortgage \t\t\t' + str('${:,.0f}'.format(mort_bal[period])))
    print('Car Loan \t\t\t' + str('${:,.0f}'.format(car_bal[period])))
    print('Student Loan \t\t\t' + str('${:,.0f}'.format(student_bal[period])))
    print('Credit Card \t\t\t' + str('${:,.0f}'.format(cc_bal[period])))
    print('\n------------------------------------------')
    print('Net Worth \t\t\t' + str('${:,.0f}'.format(net_worth[period])))

    dashboard()

#Start a new turn
def new_turn():
    global turn
    # print('turn before = '+str(turn))
    calc_score()
    turn += 1
    calc_bal()
    calc_exp()
    event_point.append(0)
    event()
    dashboard()

# Calculate the score
def calc_score():
    global turn

    mu = float(0)
    sigma = float(0)
    x = float(0)
    
    # Home points
    mu = wage_inc[-1]
    sigma = 0.3 * mu
    x = home_val[-1]
    z = ((x-mu)/sigma)
    home_point.append(round(z*float(10),0))
    print('Your home earns you ' + str(home_point[turn]) + ' points this turn!')

    # Car points
    mu = .25 * wage_inc[-1]
    sigma = 0.2 * mu 
    x = car_val[-1]
    z = ((x-mu)/sigma)
    car_point.append(round(z*float(10),0))
    print('Your car earns you ' + str(car_point[turn]) + ' points this turn!')

    # Living expense points
    mu = max(3600, wage_inc[-1]*.14)
    sigma = 0.3 * mu 
    x = liv_pmt[-1]
    z = ((x-mu)/sigma)
    liv_point.append(round(z*float(10),0))
    print('Your living expenses earn you ' + str(liv_point[turn]) + ' points this turn!')

    # Entertainment points
    mu = wage_inc[-1]*.08
    sigma = 0.3 * mu 
    x = ent_pmt[-1]
    z = ((x-mu)/sigma)
    ent_point.append(round(z*float(10),0))
    print('Your entertainment earns you ' + str(ent_point[turn]) + ' points this turn!')

    # Retirement points
    if turn == 10:
        ret_point.append(round(ret_val[turn] / wage_inc[turn] ,0)*1000)
    else:
        ret_point.append(0)
    print('Your retirement earns you ' + str(ret_point[turn]) + ' points this turn!')

    points_earned.append(home_point[turn] + car_point[turn] + liv_point[turn] + ent_point[turn] + ret_point[turn] + +event_point[turn] + ong_event_points)
    
    if turn == 0:
        score.append(points_earned[turn])
    else:
        score.append(score[-1] + points_earned[turn])
    print('\nOverall, you scored ' + str(points_earned[turn]) + ' points this turn.  Your total score is now ' + str(score[turn]) + '.')

# Update balance sheet
def calc_bal():
    global turn
    
    # update balance sheet, run before calc_exp on new_turn
    sav_val.append((sav_val[-1]+max(net_inc[turn-1],0)*(1+sav_grow_rate)))
    car_val.append(car_val[-1]*(1-car_dep_rate))
    home_val.append(home_val[-1]*(1+home_app_rate))
    ret_val.append((ret_val[-1]+ret_pmt[turn-1]*(1+ret_grow_rate)))
    
    cc_bal.append(cc_bal[turn-1] + abs(min(net_inc[turn-1],0)) - (cc_pmt[turn-1]-cc_bal[turn-1]*cc_rate+cc_xtra_pmt[turn-1]))
    student_bal.append(student_bal[turn-1] - (student_pmt[turn-1]-student_bal[turn-1]*student_rate+stu_xtra_pmt[turn-1]))
    mort_bal.append(mort_bal[turn-1] - (mort_pmt[turn-1]-mort_bal[turn-1]*mort_rate+mort_xtra_pmt[turn-1]))
    car_bal.append(car_bal[turn-1] - (car_pmt[turn-1]-car_bal[turn-1]*car_rate+car_xtra_pmt[turn-1]))

    net_worth.append(sav_val[turn] + car_val[turn] + home_val[turn] + ret_val[turn] 
        - cc_bal[turn] - student_bal[turn] - mort_bal[turn] - car_bal[turn] )
    
    # check if cc over limit
    if cc_bal[turn] > cc_limit:
        print('You have maxed out your credit card and run out of money!  You are forced to declare bankruptcy.  This means Game Over!' \
            + '\nYour final score is ' + str(score[-1]) + '.  Please play again and try to beat your high score!')
        # raise SystemExit
        quit()

    # if sav_val[turn] < 0:
    #     cc_bal[turn]


init()
