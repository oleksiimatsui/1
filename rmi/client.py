import Pyro5.api
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
from models.database import *
uri = f"PYRONAME:mess.server" 

proxy = Pyro5.api.Proxy("PYRO:obj_2593f13429a04c4f825529ed0e1fb8ec@localhost:64660")


db = database("db1")
print(db)

proxy.addDatabase('db1')




# from tkinter import *
# root = Tk()
# root.title("My Databases")
# root.resizable(False, False)

# Execute Tkinter
# ppppppp = App(root, databaseManager = dbManager)
# root.mainloop()