import json

import sqlite3

import requests

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

import matplotlib.pyplot as plt

from datetime import datetime
##################################_Classes_##################################

class Commodities:
    
    def __init__(self, id: int, name: str, average_price: int, max_sell_price: int, datee, category_id: int, rarity: bool):
        self.id = id
        self.name = name
        self.rarity = rarity
        self.category_id = category_id
        self.average_price = average_price
        self.max_sell_price = max_sell_price
        self.datee = datee

class Db:
    
    @staticmethod
    def connect():      #connection to Base
        try:
            conn = sqlite3.connect('dbminerais.db')
            #print("success")
            cursor = conn.cursor()
        except sqlite3.Error as error:
            print(error)
            conn.rollback()
        
        return conn, cursor
    
    @staticmethod
    def setup_commodities(commodities: Commodities):        #add to commodities base Ids, Names, category_ids, Rarity

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
    def sends_data(commodities: Commodities):       #add to Data base Ids, Names, Aver_prices, Max_prices, Dates

        conn, cursor = Db.connect() 

        try:
            parameter = """INSERT or IGNORE INTO Data ( Id, Name, average_price, max_sell_price, Datee) VALUES (?, ?, ?, ?, ?);"""
            data_comm = ( commodities.id, commodities.name, commodities.average_price, commodities.max_sell_price, commodities.datee)
            cursor.execute(parameter, data_comm)

        except sqlite3.Error as error:
            print(error)
            conn.rollback()
        conn.commit()

    @staticmethod
    def get_id_name():      #get Ids and Names without the missings values from the commodities base
        
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
    def get_values():       #get Ids, Names, Aver_prices, Max_prices, Dates from the data base

        conn, cursor = Db.connect()

        try:
            cursor.execute("SELECT Id, Name, average_price, max_sell_price, Datee FROM Data;")
            rows = cursor.fetchall()
        
        except sqlite3.Error as error:
            print(error)
            conn.rollback()
        conn.commit()  
        
        return rows    
     
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

    datee = datetime.today().strftime('%d/%m/%Y')

    for i in range(len(data)):
            T = Commodities(data[i]["id"], data[i]["name"], data[i]["average_price"], data[i]["max_sell_price"], datee, None, None)
            Db.sends_data(T)
    print("add_data done")
    return 

#add_data('https://eddb.io/archive/v6/commodities.json')

def daily_check():
    
    datee = datetime.today().strftime('%d/%m/%Y')
    datas = Db.get_values()
    
    if datas[len(datas)-1][4] != datee:
        add_data('https://eddb.io/archive/v6/commodities.json')
        print("datas need an up date")
    else:
        print("datas already up to date")
daily_check()

def dict_to_list(d):        #makes dict to liste ex: ['1 - Explosives', '2 - Hydrogen Fuel', '3 - Mineral Oil',...,'376 - Pod Shell Tissue']
    
    l = []
    
    for i in range(len(d)):
        l = l + [str(d[i][0]) + " - " + str(d[i][1])] 
    
    return l

def dict_select(d, item):       #get one item from Datas ex:[(276, 'Low Temperature Diamonds', 106288, 397373, '11/04/2021'), (276, 'Low Temperature Diamonds', 106288, 520566, '20/04/2021')]
    
    l = []

    for i in range(len(d)):
        if d[i][0] == item:
            l = l + [d[i]]

    return l

def listitem_to_listvalues(listitem,rang):      #get one type of value from one item ex:[106288, 106288, 106288, 106288, 106288, 106288, 106288, 106288, 106288, 106288, 106288, 106288, 106288, 106288, 106288, 106288, 106288, 106288, 106288, 106288]

    listvalues = []
    
    for i in range(len(listitem)):
        listvalues = listvalues + [listitem[i][rang]]
    return listvalues


def draw_graph(Idvalues):
    #draw_graph
    Ymax = listitem_to_listvalues(dict_select(Db.get_values(), Idvalues),3)
    Ymoy = listitem_to_listvalues(dict_select(Db.get_values(), Idvalues),2)
    X = listitem_to_listvalues(dict_select(Db.get_values(), Idvalues),4)

    fig, (axe1, axe2) = plt.subplots(2, 1)
    fig.suptitle("Tableau de l'évolution du prix maximal et moyen de l'item : "+ dict_select(Db.get_values(), Idvalues)[0][1])
    fig.subplots_adjust(hspace=0)
    axe1.plot(X,Ymax, ".-")
    axe1.set_ylabel("prix maximal")
    

    axe2.plot(X,Ymoy, ".-")
    axe2.set_ylabel("prix moyen")
    axe2.set_xlabel("jour")
    fig.autofmt_xdate()    

    plt.show()
    return

#draw_graph(276) #faire une coube moyenne sur prix max

###############################_Side_Fonctions_###############################

#l = requests.get('commoditiesEX.json')
#data = l.json()

#Instance
fe = tk.Tk()
fe.title("Graphminerais")
fe.geometry("1280x720")
fe.minsize(1280, 720)
fe.maxsize(1280, 720)

#FRAME 2 Graphique

frame2 = tk.Frame(fe, borderwidth=3, background="#262523", relief=tk.RAISED)
frame2.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

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
    item = [int(s) for s in selection.split() if s.isdigit()]
    print(item)
    
    #draw_graph
    Ymax = listitem_to_listvalues(dict_select(Db.get_values(), item[0]),3)
    Ymoy = listitem_to_listvalues(dict_select(Db.get_values(), item[0]),2)
    X = listitem_to_listvalues(dict_select(Db.get_values(), item[0]),4)

    fig, (axe1, axe2) = plt.subplots(2, 1)
    fig.suptitle("Tableau de l'évolution du prix maximal et moyen de l'item : "+ dict_select(Db.get_values(), item[0])[0][1])
    fig.subplots_adjust(hspace=0)
    axe1.plot(X,Ymax, ".-")
    axe1.set_ylabel("prix maximal")
    

    axe2.plot(X,Ymoy, ".-")
    axe2.set_ylabel("prix moyen")
    axe2.set_xlabel("jour")
    fig.autofmt_xdate()   
    #plt.show() 
    ####

    canvas = FigureCanvasTkAgg(fig, master=frame2)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    return item

bouton_selection = tk.Button(frame1, text="Ok",command= lambda: get_selection(Menu),  background="#333333", foreground="white")
bouton_selection.grid(column=0, row=3)


#SETTING
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

#print(Db.get_values())      #(1, 'Explosives', 419, 2101, '26/03/2021')

#print(dict_select(Db.get_values(), 276))

#print(listitem_to_listvalues(dict_select(Db.get_values(), 276),2))

####################################_Else_#####################################
#manquant: id 71, 120, 270
# formatting: Shift+Alt+f
