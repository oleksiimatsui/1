
import os
import time
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../models/'))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../validation/'))
from CreateTable import CreateTable
from Validation import Validate

class Rows:
    def __init__(self,parent, table):
        self.parent = parent
        self.table = table
        self.rows = []
        for i,r in enumerate(self.table.rows):
            row = {}
            for j,f in enumerate(self.table.fields):
                key = f.name
                val = StringVar('')
                val.set(r[f.name])
                value = {'value' : val, 'type' : f.type}
                row[key] = value
            self.rows.append(row)
        self.initUI()

    def addRow(self):
        row = {}
        for j,f in enumerate(self.table.fields):
                val = StringVar('')
                row[f.name] = {'value' : val, 'type' : f.type}
        self.rows.append(row)
        self.updateRows()

    def deleteRow(self, i):
        self.rows.pop(i)
        self.updateRows()

    def save(self):
        res = self.table.updateRows(self.rows)
        if(res == False):
            messagebox.showerror('Error', 'Some of the values are invalid')

    def initUI(self):
        window = Toplevel(self.parent, pady=2, borderwidth=2)
        window.title("Table rows")
        frame_header = Frame(window, pady=2, borderwidth=2)
        frame_header.grid(column=0,row=0)

        frame_body = Frame(window, pady=2, borderwidth=2, bg='grey')
        frame_body.grid(column=0,row=1, sticky="W")

        menu = Frame(frame_body, bg='green', borderwidth=2)
        menu.grid(column=0,row=1, sticky="W")

        self.list = Frame(frame_body)
        self.list.grid(column=0, row=3, sticky="W")

        Button(
            menu,
            text='Add row',
            command=self.addRow,
            anchor='w'
        ).grid(column=0, row=4, sticky="W", pady=2)
        Button(
            frame_body,
            text='Apply changes',
            command=self.save,
            anchor='w'
        ).grid(column=0, row=5, sticky="W", pady = 2)

        self.updateRows()

    def updateRows(self):
        
        for widget in self.list.winfo_children():
            widget.destroy()

        for i,f in enumerate(self.table.fields):
            label = Label(self.list, text=f.name)
            label.grid(row=0, column=i, sticky=NSEW)

        for i, r in enumerate(self.rows):
            for j, f in enumerate(self.table.fields):
                v = Validate(f.type, self.list)
                vcmd = self.parent.register(v.Validate)
                input = Entry(self.list, textvariable=r[f.name]['value'],validate='focusout', validatecommand=(vcmd, '%P', '%s', '%W'))
                input.grid(row = i+1, column = j)
            Button(self.list, text='Delete', command=lambda i = i: self.deleteRow(i)).grid(row = i+1, column = j+1, sticky=NSEW)
        