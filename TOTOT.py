'''''#from tkinter import *
 
def TraiteR():
    if w.find_withtag('un'):
        delete('un')
    else:
        w.create_line(0,0,200,100, fill="red", tags="un")
def TraiteV():
    if w.find_withtag('deux'):
        delete('deux')
    else:
       w.create_line(0,0,100,100, fill="blue", tags="deux") 
 
def TraiteJ():
    if w.find_withtag('trois'):
        delete('trois')
    else:
        w.create_line(0,0,100,200, fill="yellow", tags="trois")
 
def delete(MonTag):
    w.delete(w.find_withtag(MonTag))
 
master =Tk()
w=Canvas(master, width=200,height=100)
w.pack()
w.create_line(0,0,200,100, fill="red", tags="un")
w.create_line(0,0,100,100, fill="blue", tags="deux")
w.create_line(0,0,100,200, fill="yellow", tags="trois")
Button(text="Rouge", command=TraiteR).pack(side='left')
Button(text="Vert", command=TraiteV).pack(side='left')
Button(text="Jaune", command=TraiteJ).pack(side='left')
Button(text="Quitter", command=quit).pack(side='left')
 
mainloop()'''''