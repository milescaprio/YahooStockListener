import yahoo_value
from datetime import datetime
START_BALANCE = 1000000

#portfolio is a passed dict that holds LAST TRADED VALUE, and OWNED STOCKS.
#info is a passed dict (that should have came from yahoo_value.py) that holds LATEST PRICE and LATEST VALUE.

def save(d):
    with open('portfolio.dat','w') as f:
        f.seek(0)
        f.write(repr(d))
        f.truncate()

def log(s):
    with open('history.log','a') as f:
        f.write(datetime.now().strftime("%m/%d/%Y %H:%M:%S ")+str(s)+'\n')

def load():
    with open('portfolio.dat','r') as f:
        return eval(f.read())

def init():
    info = yahoo_value.info_dict() #most time consuming line of entire program
    try:
        portfolio = load()
    except SyntaxError:
        portfolio = info.copy()
        for key in portfolio.keys():
            portfolio[key]['owned'] = 0
            del portfolio[key]['price']
        portfolio['_money'] = START_BALANCE
        save(portfolio)
        return None
    return info, portfolio

def trade(info, portfolio):
    #Sell first 
    for key in info.keys():
        if info[key]['value'] > portfolio[key]['value'] > 0: #could also add clause for if not owned but unnecessary because it wont do anything to it then anyway
            portfolio['_money'] += info[key]['price'] * portfolio[key]['owned'] #get money back from sell
            portfolio[key]['owned'] = 0 #change owned stocks amount
            portfolio[key]['value'] = info[key]['value'] #update last transaction value
    #Buy stocks with remaining cash
    buys = [] #we have to do a premature check to see how many stocks we are buying and evenly split our cash
    for key in info.keys():
        if info[key]['value'] == 0 and portfolio[key]['owned'] == 0: #equally spread out purchase of other stocks if value is equal to 0 ("Undervalued")
            buys.append(key)
    if len(buys) == 0:
        return
    amount = portfolio['_money'] / len(buys)
    for key in buys:
        portfolio['_money'] -= amount
        portfolio[key]['owned'] += amount/ info[key]['price']
        portfolio[key]['value'] = info[key]['value']
    if portfolio['_money'] != 0:
        print('Warning: Wallet Calculation Error: Expected "0" and got"'+str(portfolio['_money'])+'"')

def sellall(info,portfolio): #same as the first half of trade()
    for key in info.keys():
        if info[key]['value'] > portfolio[key]['value'] > 0: #could also add clause for if not owned but unnecessary because it wont do anything to it then anyway
            portfolio['_money'] += info[key]['price'] * portfolio[key]['owned'] #get money back from sell
            portfolio[key]['owned'] = 0 #change owned stocks amount
            portfolio[key]['value'] = info[key]['value'] #update last transaction value
            
def balance(info, portfolio):
    balance = 0
    for key in info.keys():
        balance += portfolio[key]['owned']*info[key]['price']
    return balance

def main():
    try:
        info, portfolio = init()
    except TypeError:
        return
    trade(info, portfolio)
    save(portfolio)
    bal = balance(info,portfolio)
    print("Your total current portfolio balance is",balance(info, portfolio))
    log(bal)

if __name__ == "__main__":
    main()

    
