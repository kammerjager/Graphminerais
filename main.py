import json

import sqlite3

from datetime import datetime
##################################_py_to_sql_##################################


class Commodities:
    
    def __init__(self, id: int, name: str, rarity: bool, category_id: int,):
        self.id = id
        self.name = name
        self.rarity = rarity
        self.category_id = category_id

    def __init2__(self, id: int, name: str, average_price: int, max_sell_price: int):
        self.id = id
        self.name = name
        self.average_price = average_price
        self.max_sell_price = max_sell_price

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
            parameter = """INSERT or IGNORE INTO Commodities (Id, Name, Rarity, Category_Id) VALUES (?, ?, ?, ?);"""
            comm = ( commodities.id, str(commodities.name), commodities.rarity, commodities.category_id)
            cursor.execute(parameter, comm)

        except sqlite3.Error as error:
            print(error)
            conn.rollback()
        conn.commit()
    @staticmethod
    
    def setup_commodities_data(commodities: Commodities):

        conn, cursor = Db.connect() 
        date = datetime.today().strftime('%d-%m-%Y')

        try:
            parameter = """INSERT or IGNORE INTO Commodities (Id, Name, average_price, max_sell_price, Date) VALUES (?, ?, ?, ?, ?);"""
            data_comm = ( commodities.id, str(commodities.name), commodities.average_price, commodities.max_sell_price, date)
            cursor.execute(parameter, data_comm)

        except sqlite3.Error as error:
            print(error)
            conn.rollback()
        conn.commit()

################################_test_py_to_sql_###############################


#T1 = Commodities(1, "titi", True, 2)
#Db.insert_commodities(T1)


##################################_json_to_py_#################################


def setup(Name_json): 
    with open(Name_json) as f:
        data = json.load(f)
    
    for i in range(len(data)):
        T = Commodities(data[i]["id"], data[i]["name"], data[i]["is_rare"], data[i]["category"]["id"])
        Db.setup_commodities(T)
        
        if i+1 != data[i]["id"]:
            err = Commodities( i, "MISSING VALUE", None, None)
            Db.setup_commodities(err)        
    print("done")
    return 

#setup('commoditiesEX.json')    

def add_data(Name_json): 
    with open(Name_json) as f:
        data = json.load(f)
    
    for i in range(len(data)):
        T = Commodities(data[i]["id"], data[i]["name"], data[i]["average_price"], data[i]["max_sell_price"])
        Db.setup_commodities(T)
        
        if i+1 != data[i]["id"]:
            err = Commodities( i, "MISSING VALUE", None, None)
            Db.setup_commodities(err)        
    print("done")
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
