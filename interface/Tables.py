
import os
import time
from tkinter import *
from tkinter import filedialog as fd
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../models/'))
from CreateTable import CreateTable
from Rows import Rows
from tkinter import messagebox
from database import  database
class Tables:
    def __init__(self,parent, database):
        self.parent = parent
        self.db = database
        self.selected = []
        self.initUI()

    def showCreate(self):
        window = CreateTable(self.parent, action = self.addTable)

    def addTable(self, pseudo_table):
        res = self.db.addTableFromPseudo(pseudo_table)
        if(res == False):
            messagebox.showerror('Error', 'Some of the values are invalid')
            return False
        else:
            self.updateTables()
            return True
           

    def delete(self,id):
        self.db.deleteTable(id)
        self.updateTables()

    def view(self,table):
        window = Rows(self.parent, table)
    
    def initUI(self):
        window = Toplevel(self.parent, pady=2, borderwidth=2)
        window.title("Database tables")
        frame_header = Frame(window, pady=2, borderwidth=2)
        frame_header.grid(column=0,row=0)

        frame_body = Frame(window, pady=2, borderwidth=2, bg='grey')
        frame_body.grid(column=0,row=1, sticky="W")

        menu = Frame(frame_body, bg='green', borderwidth=2)
        menu.grid(column=0,row=1, sticky="W")

        Button(
            menu,
            text='Create table',
            command=self.showCreate,
            anchor='w'
        ).grid(column=2, row=0, sticky="W")
        Button(
            menu,
            text='Intersect',
            command=self.intersect,
            anchor='w'
        ).grid(column=3, row=0, sticky="W")

        self.list = Frame(frame_body)
        self.list.grid(column=0, row=3)
        self.updateTables()

    def intersect(self):
        res = self.db.intersect(self.selected)
        if(res == False):
            messagebox.showerror('Error', 'Cannot intersect the tables')
        else:
            self.updateTables()

    def select(self, event):
        widget = event.widget
        if(widget['bg'] == 'medium sea green'):
            widget['bg'] = 'white'
            self.selected.remove(widget.table)
        else:
            if(len(self.selected) == 2):
                return
            widget['bg'] = 'medium sea green'
            self.selected.append(widget.table)
            


    def updateTables(self):
        tables = self.db.getTables()
        for widget in self.list.winfo_children():
            widget.destroy()
        for i, t in enumerate(tables):
            frame = Frame(self.list, borderwidth=2, pady=2, padx=2, bg="white")
            frame.table = t
            frame.bind("<Button-1>", self.select)
            Label(frame, text=t.name, width=60, anchor="w").grid(column=0, row=0, sticky="W")
            Button(frame, text='View', command=lambda t=t: self.view(t)).grid(column=2, row=0, sticky="W")
            Button(frame, text='Delete', command=lambda i=t.id: self.delete(i)).grid(column=4, row=0, sticky="W")
            frame.grid(column=0, row=i, sticky="W")
        

