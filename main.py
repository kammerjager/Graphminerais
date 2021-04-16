import json

import sqlite3

import requests

import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt

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
            parameter = """INSERT or IGNORE INTO Data ( Id, Name, average_price, max_sell_price, Date) VALUES (?, ?, ?, ?, ?);"""
            data_comm = ( commodities.id, commodities.name, commodities.average_price, commodities.max_sell_price, commodities.date)
            cursor.execute(parameter, data_comm)

        except sqlite3.Error as error:
            print(error)
            conn.rollback()
        conn.commit()

    @staticmethod
    def get_id_name():
        
        conn, cursor = Db.connect()

        try:
            cursor.execute("SELECT Id,Name FROM Commodities WHERE Name != 'MISSING VALUE';")
            rows = cursor.fetchall()

        except sqlite3.Error as error:
            print(error)
            conn.rollback()
        conn.commit()  
        
        return rows          
    
    @staticmethod
    def get_values():

        conn, cursor = Db.connect()

        try:
            cursor.execute("SELECT Id, Name, average_price, max_sell_price, Date FROM Data;")
            rows = cursor.fetchall()
        
        except sqlite3.Error as error:
            print(error)
            conn.rollback()
        conn.commit()  
        
        return rows    

"""
class Graph:
    
    def draw_graph(values):

            

            plt.title()
            plt.plot()
"""
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
            T = Commodities(data[i]["id"], data[i]["name"], data[i]["average_price"], data[i]["max_sell_price"], date, None, None)
            Db.setup_data(T)
    print("add_data done")
    return 

#add_data('https://eddb.io/archive/v6/commodities.json')

def dict_to_list(d):
    
    l = []
    
    for i in range(len(d)):
        l = l + [str(d[i][0]) + " - " + str(d[i][1])] 
    
    return l

def dict_select(d, item):
    print(len(d))
    for i in range(len(d)):
        #print(i)
        if d[i][0] != item:
            #print(d[i][0])
            del d[i]
    return d
print(dict_select(Db.get_values(), 276))
###############################_Side_Fonctions_###############################

#l = requests.get('commoditiesEX.json')
#data = l.json()

#Instance
fe = tk.Tk()
fe.title("Graphminerais")
fe.geometry("1280x720")
fe.minsize(1280, 720)
fe.maxsize(1280, 720)

#FRAME 1 Selection
frame1 = tk.Frame(fe, borderwidth=3, background="#333333", relief=tk.RAISED)
frame1.pack(side=tk.TOP)
labelTop = tk.Label(frame1, text = "Select your Item", font=("Space Age",20), background="#333333", foreground="white")
labelTop.grid(column=0, row=1)
Menu = ttk.Combobox(frame1, values=dict_to_list(Db.get_id_name()), font=(20), background="#333333")     
Menu.grid(column=0, row=2)
Menu.current(0)
def get_selection(Menu):
    selection = Menu.get()
    print(selection)
    return selection
bouton_selection = tk.Button(frame1, text="Ok",command= lambda: get_selection(Menu), background="#333333", foreground="white")
bouton_selection.grid(column=0, row=3)

#FRAME 2 Graphique

frame2 = tk.Frame(fe, borderwidth=3, background="#262523", relief=tk.RAISED)

fe.iconbitmap("IconeGraphMinerais.ico")
fe.config(background = "#3C3C3C" )
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
#print(dict_to_list(Db.get_id_name()))
#print(Db.get_id_name()[0][0])
#print(Db.get_values())
####################################_Else_#####################################
#manquant: id 71, 120, 270
# formatting: Shift+Alt+f
