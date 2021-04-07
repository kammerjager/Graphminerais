import json

import sqlite3
##################################_py_to_sql_##################################


class Commodities:
    
    def __init__(self, id: int, name: str, rarity: bool, category_id: int):
        self.id = id
        self.name = name
        self.rarity = rarity
        self.category_id = category_id

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
    def insert_commodities(commodities: Commodities):

        conn, cursor = Db.connect() 
        
        try:
            parameter = """INSERT INTO Commodities (Id, Name, Rarity, Category_Id) VALUES (?, ?, ?, ?);"""
            data_comm = ( commodities.id, str(commodities.name), commodities.rarity, commodities.category_id)
            cursor.execute(parameter, data_comm)

        except sqlite3.Error as error:
            print(error)
            conn.rollback()
        conn.commit()


################################_test_py_to_sql_###############################


T1 = Commodities(1, "titi", True, 2)
#Db.insert_commodities(T1)


##################################_json_to_py_#################################

#manquant: id 71, 120, 270

with open('commoditiesEX.json') as f:
    data = json.load(f)

def setup(Name_json): 
    with open(Name_json) as f:
        data = json.load(f)
    
    for i in range(len(data)):
        T = Commodities(data[i]["id"], data[i]["name"], data[i]["is_rare"], data[i]["category"]["id"])
        Db.insert_commodities(T)
        
    return print("done")
#setup('commoditiesEX.json')    

###############################_test_json_to_py_###############################
#print(data)
#print(len(data))
#item id:1, category:name# print(data[0]["category"]["name"])





def diff():
    
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

# formatting: Shift+Alt+f