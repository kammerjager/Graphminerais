import json

import sqlite3
##################################_json_to_py_#################################

#manquant: id 71, 120, 270

with open('commoditiesEX.json') as f:
    data = json.load(f)



###############################_test_json_to_py_###############################
#test###
#print(data)

#item id:1, category:name# print(data[0]["category"]["name"])

#print(len(data))

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
    #print(Z)
    return Z
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
            parameter = """INSERT INTO TEST (id, nom, rare, category) VALUES (?, ?, ?, ?);"""
            data = ( commodities.id, str(commodities.name), commodities.rarity, commodities.category_id)
            cursor.execute(parameter, data)

        except sqlite3.Error as error:
            print(error)
            conn.rollback()
        conn.commit()



def setup(): 
    try:
        conn, cursor = Db.connect()
        conn.execute("INSERT INTO Commodities ( Id, Name, Rarity, Category_Id) VALUES ( %s, %s, %s, %s);" % ())       
    
    except:
    

################################_test_py_to_sql_###############################


T1 = Commodities(1, "titi", True, 2)
#Db.insert_commodities(T1)


####################################_Else_#####################################

# formatting: Shift+Alt+f