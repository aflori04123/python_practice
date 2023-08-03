import pandas as pd
class Parser:
     def __init__(self):
        self.data = None
        self.averages = None

     def readData(self, name):
         try:
             self.data = pd.read_csv(name)
         except:
             print("Invalid file name/Path!")

     def findAverages(self):
        self.averages  = self.data.iloc[:, 2:].mean()

     def findAverages(self):
        self.averages  = self.data.iloc[:, 2:].mean()

     def printAverages(self):
         print(self.averages)
a = Parser()
a.readData("sales.csv")
a.findAverages()
a.printAverages()
