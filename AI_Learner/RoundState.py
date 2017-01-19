from Vmap import *
from vindinium.models import game



class RoundState:

    health=None
    minesOwned=None
    pubDist=None
    mineDist=None

    def __init__(self):
        health = self.Hero.life
        minesOwned = game.Hero.mine_count
        self.setMineDist()
        self.setPubDist()

    def setEnemyDist(self):
        print(1)

    def setMineDist(self):
        print(1)

    def setPubDist(self):
        print(2)

    def Update(self):
        health = game.Hero.life
        minesOwned = game.Hero.mine_count
        self.setMineDist()
        self.setPubDist()
