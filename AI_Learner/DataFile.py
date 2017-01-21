import pandas as pd
import os


class DataStream:
    def __init__(self):
        self.df = None
        self.count = 0
        self.last_index = 0

    def load(self):
        if os.path.exists("Data/GameInformation.csv"):
            self.df = pd.DataFrame.from_csv("Data/GameInformation.csv", sep=',')
            if self.df.empty:
                print("File is empty.")
                self.df = pd.DataFrame(columns=(
                    'Health', 'Mines Owned', 'Pub Dist', 'Mine Dist','Enemy Dist', "action", "prob"))
            # else:
        else:
            if os.path.exists("Data"):
                fp = open("Data/GameInformation.csv", 'w+')
                fp.close()
                self.df = pd.DataFrame(columns=(
                    'Health', 'Mines Owned','Pub Dist', 'Mine Dist','Enemy Dist', "action","prob"))
            else:
                os.mkdir("Data")
                fp = open("Data/GameInformation.csv", 'w+')
                fp.close()
                self.df = pd.DataFrame(columns=(
                    'Health', 'Mines Owned', 'Pub Dist', 'Mine Dist','Enemy Dist', "action", "prob"))

    def update(self):
        if os.path.exists("Data/GameInformation.csv"):
            # self.last_index = self.df.last_valid_index()
            if self.df.last_valid_index() is None:
                # Create test state
                self.df.to_csv("Data/GameInformation.csv", sep=',')

        else:
            print("File error: file is not exist.")
