import pandas as pd

myseries = pd.Series(
     [10,20,30], 
     index = ["a","b","c"]
)

<<<<<<< Updated upstream
print(myseries)
=======
     def findAverages(self):
        self.averages  = self.data.iloc[:, 2:].mean()

     def printAverages(self):
         print(self.averages)
a = Parser()
a.readData("sales.csv")
a.findAverages()
a.printAverages()
>>>>>>> Stashed changes
