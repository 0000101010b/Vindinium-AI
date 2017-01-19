import random
import pandas as pd
import numpy as np
from DataFile import *
from RoundState import *
from vindinium.bots import RawBot
from vindinium.bots import BaseBot
import vindinium as vin
from Wall import *
from Vmap import *


class RandomBot(BaseBot):
    '''Random bot.'''
    #dataframe
    datastream=None
    lastminecount=0

    life = 0
    gold = 0
    spawnX = 0
    spawnY = 0
    positionX = 0
    positionY = 0
    mine_count = 0
    hero_num = 0
    last_dir = None
    crashed = False
    map = None
    map_size = 0
    vmap = None
    mines = []
    taverns = []
    walls = []
    enemies = []
    dist_mine = 0
    dist_tavern = 0
    command = None

    #test



    #current state
    currentstate=None
    #
    pastStates=[]
    actions=["goPub","goMine"]

    def start(self):
        self.datastream=DataStream()
        self.datastream.load()
        self.datastream.update()
        #self.currentstate=RoundState(self)

        self._hero_information()
        self._get_mines()
        self._get_map()
        self._get_taverns()
        self._get_walls()
        self._enemies_information()
        self._get_vmap()

        print(self.life)


    def move(self):
        #self.currentstate = RoundState()
        self._hero_information()
        self._enemies_information()
        self._current_vmap()

        # currentGameState
        state = [self.state["hero"]["life"],  # health
                 self.state["hero"]["mineCount"],    # mines owned
                 self._get_shortest_dist_mine(),    # pub dist
                 self._get_shortest_dist_tavern(),    # mine dist
                 ]

        # select action
        actionProb = []

        for action in self.actions:
            temp = pd.DataFrame()
            temp = (self.datastream.df.loc[(self.datastream.df['Health'] == state[0]) &
                                (self.datastream.df['Mines Owned'] == state[1]) &
                                (self.datastream.df['Pub Dist'] == state[2]) &
                                (self.datastream.df['Mine Dist'] == state[3]) &
                                (self.datastream.df["action"] == action)
            , ['prob']])
            temp = temp.values.tolist()

            if (not len(temp) == 0):
                actionProb.append(temp[0][0])
            else:
                actionProb.append(0.5)

        s = sum(actionProb)
        r = [i / s for i in actionProb]
        choice = np.random.choice(self.actions, len(self.actions), p=r)

        print("Turn: %d  Action: %s" % (self.game.turn, choice[0]))

        #call action function for choice
        # 1.goMine()
        # 2.goPub()



        currentActionState = [state[0],  # health
                              state[1],  # mines owned
                              state[2],  # pub dist
                              state[3],  # mine dist
                              choice[0],  # action
                               .5 ]

        # Get index of row if in dataframe
        index = self.datastream.df.loc[(self.datastream.df['Health'] == currentActionState[0]) &
                            (self.datastream.df['Mines Owned'] == currentActionState[1]) &
                            (self.datastream.df['Pub Dist'] == currentActionState[2]) &
                            (self.datastream.df['Mine Dist'] == currentActionState[3]) &
                            (self.datastream.df["action"] == currentActionState[4])
        , ['Health']].index

        if (len(index) <= 0):  # if index not found
            # create append to current dataframe
            newRowData = pd.DataFrame([currentActionState], columns=(
            'Health', 'Mines Owned', 'Pub Dist', 'Mine Dist', "action", "prob"))
            self.datastream.df = self.datastream.df.append(newRowData, ignore_index=True)

            index = self.datastream.df.loc[(self.datastream.df['Health'] == currentActionState[0]) &
                                (self.datastream.df['Mines Owned'] == currentActionState[1]) &
                                (self.datastream.df['Pub Dist'] == currentActionState[2]) &
                                (self.datastream.df['Mine Dist'] == currentActionState[3]) &
                                (self.datastream.df["action"] == currentActionState[4])
            , ['Health']].index

            # add new index to states before death
            self.pastStates.append(index[0])

        else:
            self.pastStates.append(index[0])  # add found index to state before death



        if (self.state["hero"]["mineCount"]-self.lastminecount  > 0):
            self._call_advantage_function()
            self.lastminecount =  self.state["hero"]["mineCount"]

        if (self.lastminecount- self.state["hero"]["mineCount"] > 0):
            self._call_advantage_function2()
            self.lastminecount = self.state["hero"]["mineCount"]


        print(choice[0])

        #if choice[0] string action example goPub

        self.command=random.choice(['Stay', 'North', 'West', 'East', 'South'])
        if(choice[0]=="goMine"):
            self._go_to_nearest_mine()
        elif(choice[0]=="goPub"):
            self._go_to_nearest_tavern()

        print(self.command)
        return self.command

    def _hero_information(self):
        self.life = self.state['hero']['life']
        self.gold = self.state['hero']['gold']
        self.spawnX = self.state['hero']['spawnPos']['y']
        self.spawnY = self.state['hero']['spawnPos']['x']
        self.positionX = self.state['hero']['pos']['y']
        self.positionY = self.state['hero']['pos']['x']
        self.mine_count = self.state['hero']['mineCount']
        self.crashed = self.state['hero']['crashed']
        if 'lastDir' in self.state['hero']:
            self.last_dir = self.state['hero']['lastDir']

    def _enemies_information(self):
        self.enemies = self.state['game']['heroes']
        for enemy in self.enemies:
            if enemy['id'] == self.id:
                print('hero id is', enemy['id'])
                self.enemies.remove(enemy)
        return self.enemies

    def _get_map(self):
        self.map = self.game.map
        self.map_size = self.state['game']['board']['size']
        print(self.map)
        print(self.map_size)

    def _current_vmap(self):
        temp = self.vmap
        temp.remove_player()
        for enemy in self.enemies:
            temp.set_player(enemy['pos']['y'], enemy['pos']['x'])
        temp = temp.get_taged_map(Pos(self.positionX, self.positionY))
        return temp

    def _get_vmap(self):
        self.vmap = VGridMap(self.map_size, self.map_size)
        for mine in self.mines:
            self.vmap.set_disabled(mine.x, mine.y)
        for tavern in self.taverns:
            self.vmap.set_disabled(tavern.x, tavern.y)
        for wall in self.walls:
            self.vmap.set_disabled(wall.x, wall.y)
        return self.vmap

    def _get_mines(self):
        self.mines = self.game.mines
        for mine in self.mines:
            print(mine.x, mine.y, mine.owner)
        return self.mines

    def _get_taverns(self):
        self.taverns = self.game.taverns
        for tavern in self.taverns:
            print(tavern.x, tavern.y)
        return self.taverns

    def _get_walls(self):
        for y in range(self.map_size):
            for x in range(self.map_size):
                if self.map[x, y] == vindinium.TILE_WALL:
                    self.walls.append(Wall(x, y))
        return self.walls

    # def _get_dist(self, x, y):
    #     temp = self._current_vmap()
    #     dist = temp.get_distance(temp, x, y)
    #     return dist
    #
    # def _get_direction(self, x, y):
    #     temp = self._current_vmap()
    #     direction = temp.get_direction(temp, x, y)
    #     return direction

    def _go_to_nearest_mine(self):
        shortest_dist = self._get_shortest_dist_mine()
        #return shortest_dist

    def _get_shortest_dist_mine(self):
        self.command = None
        shortest_dist = 1000
        temp = self._current_vmap()
        #temp.print_grid()
        for mine in self.mines:
            if mine.owner != self.id:
                current_dist = temp.get_distance(temp, mine.x, mine.y)
                direction = temp.get_direction(temp, mine.x, mine.y)

                if shortest_dist > current_dist:
                    shortest_dist = current_dist
                    self.command = direction
                    self.targetX = mine.x
                    self.targetY = mine.y

                    if isinstance(self.command, tuple):

                        if self.positionX == mine.x:
                            if self.positionY < mine.y:
                                self.command = 'South'
                            elif self.positionY > mine.y:
                                self.command = 'North'
                        elif self.positionY == mine.y:
                            if self.positionX < mine.x:
                                self.command = 'East'
                            elif self.positionX > mine.x:
                                self.command = 'West'
                                # print(mine.x)
                                # print(mine.y)
                                # print(self.targetX)
                                # print(self.targetY)
                                # print(shortest_dist)
                                # print(current_dist)

        print("target:",end="")
        print(self.targetX)
        print(self.targetY)
        vv = VGridMap(12,12)
        print("test:",end="")
        print(vv.get_direction(temp,self.targetX,self.targetY))
        return shortest_dist

    def _go_to_nearest_tavern(self):
        shortest_dist = self._get_shortest_dist_tavern()


    def _get_shortest_dist_tavern(self):
        self.command = None
        shortest_dist = 1000
        temp = self._current_vmap()
        #temp.print_grid()
        for tavern in self.taverns:
            current_dist = temp.get_distance(temp, tavern.x, tavern.y)
            direction = temp.get_direction(temp, tavern.x, tavern.y)
            if shortest_dist > current_dist:
                shortest_dist = current_dist
                self.command = direction
            if isinstance(self.command, tuple):
                if self.positionX == tavern.x:
                    if self.positionY < tavern.y:
                        self.command = 'South'
                    elif self.positionY > tavern.y:
                        self.command = 'North'
                elif self.positionY == tavern.y:
                    if self.positionX < tavern.x:
                        self.command = 'East'
                    elif self.positionX > tavern.x:
                        self.command = 'West'
        return shortest_dist

    def _call_advantage_function(self):


        #reverse array
        indexInReverse = []
        for index in self.pastStates:
            indexInReverse.append(index)
        indexInReverse.reverse()


        #advantage function
        temp = 0.5 * self.state["hero"]["mineCount"]/8 * (1 - self.datastream.df.iloc[index, self.datastream.df.columns.get_loc('prob')])
        for index in indexInReverse:
            self.datastream.df.iloc[index, self.datastream.df.columns.get_loc('prob')] += temp
            print("state: ", end="")
            print(index)
            print("Prob Change:", end="")
            print(temp)
            temp *= 0.5 * self.datastream.df.iloc[index, self.datastream.df.columns.get_loc('prob')]

        print(self.datastream.df)

    def _call_advantage_function2(self):

        # reverse array
        indexInReverse = []
        for index in self.pastStates:
            indexInReverse.append(index)
        indexInReverse.reverse()

        # advantage function
        temp = -0.2 * (
        1 - self.datastream.df.iloc[index, self.datastream.df.columns.get_loc('prob')])
        for index in indexInReverse:
            self.datastream.df.iloc[index, self.datastream.df.columns.get_loc('prob')] += temp
            print("state: ",end="")
            print(index)
            print("Prob Change:",end="")
            print(temp)
            temp *= 0.5 * self.datastream.df.iloc[index, self.datastream.df.columns.get_loc('prob')]

        print(self.datastream.df)


