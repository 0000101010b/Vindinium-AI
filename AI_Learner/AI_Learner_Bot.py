import vindinium
import pandas as pd
#import numpy as np


class MyBot(vindinium.bots.BaseBot):
    def start(self):
        print ('Game just started')

    def move(self):
        print ('Game asking for a movement')
        return vindinium.STAY


    def end(self):
        print ('Game finished')