import json

import sqlite3

from datetime import datetime
##################################_py_to_sql_##################################

class Commodities:
    
    def __init__(self, id: int, name: str, average_price: int, max_sell_price: int, date, category_id: int, rarity: bool):
        self.id = id
        self.name = name
        self.rarity = rarity
        self.category_id = category_id
        self.average_price = average_price
        self.max_sell_price = max_sell_price
        self.date = date

class Db:
    
    @staticmethod
    def connect():
        try:
            conn = sqlite3.connect('dbminerais.db')
            #print("success")
            cursor = conn.cursor()
        except sqlite3.Error as error:
            print(error)
            conn.rollback()
        
        return conn, cursor
    
    @staticmethod
    def setup_commodities(commodities: Commodities):

        conn, cursor = Db.connect() 
        try:
            parameter = """INSERT or IGNORE INTO Commodities ( Id, Name, Category_Id, Rarity) VALUES (?, ?, ?, ?);"""
            comm = ( commodities.id, str(commodities.name), commodities.category_id, commodities.rarity)
            cursor.execute(parameter, comm)

        except sqlite3.Error as error:
            print(error)
            conn.rollback()
        conn.commit()
    
    @staticmethod
    def setup_data(commodities: Commodities):

        conn, cursor = Db.connect() 

        try:
            parameter = """INSERT or IGNORE INTO Data ( Id, Name, average_price, max_sell_price, Date) VALUES (?, ?, ?, ?, ?);"""
            data_comm = ( commodities.id, commodities.name, commodities.average_price, commodities.max_sell_price, commodities.date)
            cursor.execute(parameter, data_comm)

        except sqlite3.Error as error:
            print(error)
            conn.rollback()
        conn.commit()

################################_test_py_to_sql_###############################


#T1 = Commodities(1, "titi", 451656, 5684,465645)
#Db.setup_commodities_data(T1)

"""with open("commoditiesEX.json") as f:
        data = json.load(f)
date = datetime.today().strftime('%d/%m/%Y %M-%S')
T = Commodities( data[1]["id"], data[1]["name"], data[1]["average_price"], data[1]["max_sell_price"], date)
Db.setup_commodities_data(T)

print(data[1]["average_price"])"""

##################################_json_to_py_#################################


def setup(Name_json): 
    with open(Name_json) as f:
        data = json.load(f)
    
    for i in range(len(data)):
        T = Commodities(data[i]["id"], data[i]["name"], None, None, None, data[i]["category"]["id"], data[i]["is_rare"])
        Db.setup_commodities(T)

        if i+1 != data[i]["id"]:
            err = Commodities( i, "MISSING VALUE", None, None, None, None, None)
            Db.setup_commodities(err)     
    print("setup done")
    return 

setup('commoditiesEX.json')    

def add_data(Name_json): 
    with open(Name_json) as f:
        data = json.load(f)
    
    date = datetime.today().strftime('%d/%m/%Y')

    for i in range(len(data)):
            T = Commodities( data[i]["id"], data[i]["name"], data[i]["average_price"], data[i]["max_sell_price"], date, None, None)
            Db.setup_data(T)
    print("add_data done")
    return 

add_data('commoditiesEX.json')

###############################_test_json_to_py_###############################
#print(data)
#print(len(data))
#item id:1, category:name# print(data[0]["category"]["name"]).


def diff(Name_json):
    with open(Name_json) as f:
        data = json.load(f)
    A = []
    for i in range(373):
        x = data[i]["id"]
        x = str(x)
        A = A + [x]
    B = []
    for i in range(376):
        y = i+1
        y = str(y)
        B = B + [y]
    Z = (set(B).difference(set(A)))
    if Z != None:
        print(Z)
        return Z
    else:
        return Z


####################################_Else_#####################################
#manquant: id 71, 120, 270
# formatting: Shift+Alt+f
