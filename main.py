import json

import sqlite3

import requests

from tkinter import *

from datetime import datetime
##################################_Classes_##################################

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
            parameter = """INSERT or IGNORE INTO TEST ( Id, Name, average_price, max_sell_price, Date) VALUES (?, ?, ?, ?, ?);"""
            data_comm = ( commodities.id, commodities.name, commodities.average_price, commodities.max_sell_price, commodities.date)
            cursor.execute(parameter, data_comm)

        except sqlite3.Error as error:
            print(error)
            conn.rollback()
        conn.commit()


##################################_Fontctions_#################################


def setup(filelink):       #Setup the Db with commodities informations 
    if "http" in filelink: 
        l = requests.get(filelink)
        data = l.json()
    else: 
        with open(filelink) as f:
            data = json.load(f)
        
    for i in range(len(data)):
        T = Commodities(data[i]["id"], data[i]["name"], None, None, None, data[i]["category"]["id"], data[i]["is_rare"])
        Db.setup_commodities(T)

        if i+1 != data[i]["id"]:
            err = Commodities( i, "MISSING VALUE", None, None, None, None, None)
            Db.setup_commodities(err)     
    print("setup done")
    return 

#setup('commoditiesEX.json')    

def add_data(filelink):        #Add commodities data to the Db
    if "http" in filelink: 
        l = requests.get(filelink)
        data = l.json()
    else: 
        with open(filelink) as f:
            data = json.load(f)

    date = datetime.today().strftime('%d/%m/%Y')

    for i in range(len(data)):
            T = Commodities( data[i]["id"], data[i]["name"], data[i]["average_price"], data[i]["max_sell_price"], date, None, None)
            Db.setup_data(T)
    print("add_data done")
    return 

#add_data('https://eddb.io/archive/v6/commodities.json')

###############################_Side_Fonctions_###############################

fe = Tk()
fe.title("Graphminerais")
fe.geometry("1080x720")
fe.minsize(1080, 720)
fe.iconbitmap("IconeGraphMinerais.ico")
fe.config(background = "#303030" )
fe.mainloop()




def diff(Name_json):        # search for missing data
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


################################_test_###############################

#r = requests.get('https://eddb.io/archive/v6/commodities.json')
#print(r.status_code)
#print(r.json())
#T1 = Commodities(1, "titi", 451656, 5684,465645)
#Db.setup_commodities_data(T1)
#print(data)
#print(len(data))
#item id:1, category:name# print(data[0]["category"]["name"]).

####################################_Else_#####################################
#manquant: id 71, 120, 270
# formatting: Shift+Alt+f
