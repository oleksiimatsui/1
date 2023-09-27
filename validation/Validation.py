from tkinter import *


class Validate:
    @staticmethod
    def String(value):
        #print("String")
        return True
    @staticmethod
    def Real(value):
        #print("Real")
        try:
            float(value)
            return True
        except ValueError:
            return False
    @staticmethod
    def Int(value):
        if str.isnumeric(value):
            return True
        return False 
    @staticmethod
    def Char(value):
        #print("Char")
        if (len( value ) == 1):
            return True
        return False
    
    MAXMONEY = 100000000

    @staticmethod
    def Money(value):
        #print("Money")
        if (Validate.Real(value) == False):
            return False
        number_ = float(value)
        if(number_ > Validate.MAXMONEY):
            return False
        return True
    @staticmethod
    def MoneyInterval(value):
        #print("MoneyInterval")
        values = value.split(',')
        if(len( values ) != 2):
            return False
        if(not Validate.Money(values[0])):
            return False
        if(not Validate.Money(values[1])):
            return True
        if(float(values[0]) > float(values[1])):
            return False
        return True
    
    types = ['Int', 'String', 'Char', 'Real', "Money", "MoneyInterval"]

    def Validate(self, values, lastvalue = None, widget = None):
        res = False
        if(self.type == Validate.types[0]):
            res = Validate.Int(values)
        if(self.type == Validate.types[1]):
            res = Validate.String(values)
        if(self.type == Validate.types[2]):
            res =  Validate.Char(values)
        if(self.type == Validate.types[3]):
            res =  Validate.Real(values)
        if(self.type == Validate.types[4]):
            res = Validate.Money(values)
        if(self.type == Validate.types[5]):
            res = Validate.MoneyInterval(values)
        if(res == False and self.win != None):
            entry = self.win.nametowidget(widget)
            entry.delete(0, END)
        if(isinstance(res, (bool))):
           return res
        else:
            return False
        
    def __init__(self, type, win = None):
        self.type = type
        self.win = win