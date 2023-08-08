import pandas as pd
import logging
class Parser:
    def __init__(self):
        self.data = None
        self.mean = None

    def readData(self, name):
        try:
             self.data = pd.read_csv(name)
        except FileNotFoundError:
            print(f"File not found: {name}")
        except pd.errors.ParserError as pe:
            print("ParserError:", pe)
        except pd.errors.UnicodeDecodeError as ue:
            print("UnicodeDecodeError:", ue)
        except Exception as e:
            logging.log(e)

    def findMean(self):
        numeric_columns = []
        for column in self.data.columns:
            try:
                pd.to_numeric(self.data[column][0])
                numeric_columns.append(column)
            except (ValueError, TypeError):
                pass

        # Calculate the mean of numeric columns
        print(numeric_columns)
        self.mean = self.data[numeric_columns].mean()


    def printMean(self):
         print(self.mean)
a = Parser()
a.readData("sales.csv")
a.findMean()
a.printMean()