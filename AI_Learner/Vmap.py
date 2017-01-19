import vindinium


class Pos:
    def __init__(self, newX, newY):
        self.x = newX
        self.y = newY

    def setX(self, newX):
        self.x = newX

    def setY(self, newY):
        self.y = newY


class Unit:
    disTag = -1
    pos_from = Pos(-1, -1)

    def __init__(self, pos):
        self.pos = pos

    def set_dis(self, dis):
        self.disTag = dis

    def make_disable(self):
        self.disTag = -3


class VGridMap:
    def __init__(self, w=10, h=10):
        self.w = w
        self.h = h
        self.g = self.make_grid()

    # set up map
    def make_grid(self):
        g = []
        for j in range(self.h):
            temp = []
            for i in range(self.w):
                u = Unit(Pos(i, j))
                temp.append(u)
            g.append(temp)

        return g

    # set the obstacle which can not pass and will not change: set once
    def set_disabled(self, x, y):
        self.g[y][x].make_disable()

    # set the player which will change : set everytime
    def set_player(self, x, y):
        self.g[y][x].disTag = -2

    # remove all the player: used before set_player
    def remove_player(self):
        for i in range(self.w):
            for j in range(self.h):
                if self.g[j][i].disTag == -2:
                    self.g[j][i].disTag = -1
                # print tag: for test

    def print_grid(self):
        for i in range(self.h):
            for j in range(self.w):
                print(self.g[i][j].disTag, end="")
                # print("(",end="")
                # print(self.g[i][j].pos_from.x,end="")
                # print(",",end="")
                # print(self.g[i][j].pos_from.y,end="")
                # print(")",end="")
                for b in range(4 - len(str(self.g[i][j].disTag))):
                    print(" ", end="")
            print()
        # generate distance taged map

    def get_taged_map(self, my_pos):

        map = VGridMap(self.w, self.h)
        x = my_pos.x
        y = my_pos.y
        my_pos.x = y
        my_pos.y = x

        t_g = map.g
        for j in range(self.w):
            for i in range(self.h):
                t_g[i][j].disTag = self.g[i][j].disTag

        stable = False
        t_g[my_pos.x][my_pos.y].disTag = 0
        process = 0
        while not stable:
            stable = True
            for j in range(self.w):
                for i in range(self.h):
                    if t_g[i][j].disTag == process:
                        if j == 0:
                            if i == 0:
                                if t_g[i + 1][j].disTag == -1:
                                    t_g[i + 1][j].disTag = process + 1
                                    t_g[i + 1][j].pos_from = Pos(i, j)
                                    stable = False
                                if t_g[i][j + 1].disTag == -1:
                                    t_g[i][j + 1].disTag = process + 1
                                    t_g[i][j + 1].pos_from = Pos(j, i)
                                    stable = False
                            elif i == self.h - 1:
                                if t_g[i][j + 1].disTag == -1:
                                    t_g[i][j + 1].disTag = process + 1
                                    t_g[i][j + 1].pos_from = Pos(i, j)
                                    stable = False
                                if t_g[i - 1][j].disTag == -1:
                                    t_g[i - 1][j].disTag = process + 1
                                    t_g[i - 1][j].pos_from = Pos(j, i)
                                    stable = False
                            else:
                                if t_g[i + 1][j].disTag == -1:
                                    t_g[i + 1][j].disTag = process + 1
                                    t_g[i + 1][j].pos_from = Pos(j, i)
                                    stable = False
                                if t_g[i][j + 1].disTag == -1:
                                    t_g[i][j + 1].disTag = process + 1
                                    t_g[i][j + 1].pos_from = Pos(j, i)
                                    stable = False
                                if t_g[i - 1][j].disTag == -1:
                                    t_g[i - 1][j].disTag = process + 1
                                    t_g[i - 1][j].pos_from = Pos(j, i)
                                    stable = False
                        elif j == self.w - 1:
                            if i == 0:
                                if t_g[i + 1][j].disTag == -1:
                                    t_g[i + 1][j].disTag = process + 1
                                    t_g[i + 1][j].pos_from = Pos(j, i)
                                    stable = False
                                if t_g[i][j - 1].disTag == -1:
                                    t_g[i][j - 1].disTag = process + 1
                                    t_g[i][j - 1].pos_from = Pos(j, i)
                                    stable = False
                            elif i == self.h - 1:
                                if t_g[i - 1][j].disTag == -1:
                                    t_g[i - 1][j].disTag = process + 1
                                    t_g[i - 1][j].pos_from = Pos(i, i)
                                    stable = False
                                if t_g[i][j - 1].disTag == -1:
                                    t_g[i][j - 1].disTag = process + 1
                                    t_g[i][j - 1].pos_from = Pos(j, i)
                                    stable = False
                            else:
                                if t_g[i - 1][j].disTag == -1:
                                    t_g[i - 1][j].disTag = process + 1
                                    t_g[i - 1][j].pos_from = Pos(j, i)
                                    stable = False
                                if t_g[i][j - 1].disTag == -1:
                                    t_g[i][j - 1].disTag = process + 1
                                    t_g[i][j - 1].pos_from = Pos(j, i)
                                    stable = False
                                if t_g[i + 1][j].disTag == -1:
                                    t_g[i + 1][j].disTag = process + 1
                                    t_g[i + 1][j].pos_from = Pos(j, i)
                                    stable = False
                        else:
                            if i == 0:
                                if t_g[i][j - 1].disTag == -1:
                                    t_g[i][j - 1].disTag = process + 1
                                    t_g[i][j - 1].pos_from = Pos(j, i)
                                    stable = False
                                if t_g[i + 1][j].disTag == -1:
                                    t_g[i + 1][j].disTag = process + 1
                                    t_g[i + 1][j].pos_from = Pos(j, i)
                                    stable = False
                                if t_g[i][j + 1].disTag == -1:
                                    t_g[i][j + 1].disTag = process + 1
                                    t_g[i][j + 1].pos_from = Pos(j, i)
                                    stable = False
                            elif i == self.h - 1:
                                if t_g[i - 1][j].disTag == -1:
                                    t_g[i - 1][j].disTag = process + 1
                                    t_g[i - 1][j].pos_from = Pos(j, i)
                                    stable = False
                                if t_g[i][j + 1].disTag == -1:
                                    t_g[i][j + 1].disTag = process + 1
                                    t_g[i][j + 1].pos_from = Pos(j, i)
                                    stable = False
                                if t_g[i][j - 1].disTag == -1:
                                    t_g[i][j - 1].disTag = process + 1
                                    t_g[i][j - 1].pos_from = Pos(j, i)
                                    stable = False
                            else:
                                if t_g[i - 1][j].disTag == -1:
                                    t_g[i - 1][j].disTag = process + 1
                                    t_g[i - 1][j].pos_from = Pos(j, i)
                                    stable = False
                                if t_g[i + 1][j].disTag == -1:
                                    t_g[i + 1][j].disTag = process + 1
                                    t_g[i + 1][j].pos_from = Pos(j, i)
                                    stable = False
                                if t_g[i][j + 1].disTag == -1:
                                    t_g[i][j + 1].disTag = process + 1
                                    t_g[i][j + 1].pos_from = Pos(j, i)
                                    stable = False
                                if t_g[i][j - 1].disTag == -1:
                                    t_g[i][j - 1].disTag = process + 1
                                    t_g[i][j - 1].pos_from = Pos(j, i)
                                    stable = False
            process = process + 1
        return map

    # get direction based on the shortest way: first locate the nearest the point arount the object ; track back to the start point and
    def get_direction(self, tagedMap, x, y):
        desx = -1
        dexy = -1
        temp = 100
        if x == 0:
            if y == 0:
                if tagedMap.g[y + 1][x].disTag >= 0 and tagedMap.g[y + 1][x].disTag < temp:
                    temp = tagedMap.g[y + 1][x].disTag;
                    desx = x
                    dexy = y + 1
                if tagedMap.g[y][x + 1].disTag >= 0 and tagedMap.g[y][x + 1].disTag < temp:
                    temp = tagedMap.g[y][x + 1].disTag;
                    desx = x + 1
                    dexy = y
            elif y == tagedMap.h - 1:
                if tagedMap.g[y + 1][x].disTag >= 0 and tagedMap.g[y + 1][x].disTag < temp:
                    temp = tagedMap.g[y + 1][x].disTag;
                    desx = x
                    dexy = y + 1
                if tagedMap.g[y][x + 1].disTag >= 0 and tagedMap.g[y][x + 1].disTag < temp:
                    temp = tagedMap.g[y][x + 1].disTag;
                    desx = x + 1
                    dexy = y
            else:
                if tagedMap.g[y + 1][x].disTag >= 0 and tagedMap.g[y + 1][x].disTag < temp:
                    temp = tagedMap.g[y + 1][x].disTag;
                    desx = x
                    dexy = y + 1
                if tagedMap.g[y - 1][x].disTag >= 0 and tagedMap.g[y - 1][x].disTag < temp:
                    temp = tagedMap.g[y - 1][x].disTag;
                    desx = x
                    dexy = y - 1
                if tagedMap.g[y][x + 1].disTag >= 0 and tagedMap.g[y][x + 1].disTag < temp:
                    temp = tagedMap.g[y][x + 1].disTag;
                    desx = x + 1
                    dexy = y
        elif x == tagedMap.w - 1:
            if y == 0:
                if tagedMap.g[y + 1][x].disTag >= 0 and tagedMap.g[y + 1][x].disTag < temp:
                    temp = tagedMap.g[y + 1][x].disTag;
                    desx = x
                    dexy = y + 1
                if tagedMap.g[y][x - 1].disTag >= 0 and tagedMap.g[y][x - 1].disTag < temp:
                    temp = tagedMap.g[y][x - 1].disTag;
                    desx = x - 1
                    dexy = y
            elif y == tagedMap.h - 1:
                if tagedMap.g[y - 1][x].disTag >= 0 and tagedMap.g[y - 1][x].disTag < temp:
                    temp = tagedMap.g[y - 1][x].disTag;
                    desx = x
                    dexy = y - 1
                if tagedMap.g[y][x - 1].disTag >= 0 and tagedMap.g[y][x - 1].disTag < temp:
                    temp = tagedMap.g[y][x - 1].disTag;
                    desx = x - 1
                    dexy = y
            else:
                if tagedMap.g[y + 1][x].disTag >= 0 and tagedMap.g[y + 1][x].disTag < temp:
                    temp = tagedMap.g[y + 1][x].disTag;
                    desx = x
                    dexy = y + 1
                if tagedMap.g[y - 1][x].disTag >= 0 and tagedMap.g[y - 1][x].disTag < temp:
                    temp = tagedMap.g[y - 1][x].disTag;
                    desx = x
                    dexy = y - 1
                if tagedMap.g[y][x - 1].disTag >= 0 and tagedMap.g[y][x - 1].disTag < temp:
                    temp = tagedMap.g[y][x - 1].disTag;
                    desx = x - 1
                    dexy = y

        else:
            if y == 0:
                if tagedMap.g[y + 1][x].disTag >= 0 and tagedMap.g[y + 1][x].disTag < temp:
                    temp = tagedMap.g[y + 1][x].disTag;
                    desx = x
                    dexy = y + 1
                if tagedMap.g[y][x - 1].disTag >= 0 and tagedMap.g[y][x - 1].disTag < temp:
                    temp = tagedMap.g[y][x - 1].disTag;
                    desx = x - 1
                    dexy = y
                if tagedMap.g[y][x + 1].disTag >= 0 and tagedMap.g[y][x + 1].disTag < temp:
                    temp = tagedMap.g[y][x + 1].disTag;
                    desx = x + 1
                    dexy = y
            elif y == tagedMap.h - 1:
                if tagedMap.g[y - 1][x].disTag >= 0 and tagedMap.g[y - 1][x].disTag < temp:
                    temp = tagedMap.g[y - 1][x].disTag;
                    desx = x
                    dexy = y - 1
                if tagedMap.g[y][x - 1].disTag >= 0 and tagedMap.g[y][x - 1].disTag < temp:
                    temp = tagedMap.g[y][x - 1].disTag;
                    desx = x - 1
                    dexy = y
                if tagedMap.g[y][x + 1].disTag >= 0 and tagedMap.g[y][x + 1].disTag < temp:
                    temp = tagedMap.g[y][x + 1].disTag;
                    desx = x + 1
                    dexy = y
            else:
                if tagedMap.g[y + 1][x].disTag >= 0 and tagedMap.g[y + 1][x].disTag < temp:
                    temp = tagedMap.g[y + 1][x].disTag;
                    desx = x
                    dexy = y + 1
                if tagedMap.g[y - 1][x].disTag >= 0 and tagedMap.g[y - 1][x].disTag < temp:
                    temp = tagedMap.g[y + 1][x].disTag;
                    desx = x
                    dexy = y - 1
                if tagedMap.g[y][x - 1].disTag >= 0 and tagedMap.g[y][x - 1].disTag < temp:
                    temp = tagedMap.g[y][x - 1].disTag;

                    desx = x - 1
                    dexy = y
                if tagedMap.g[y][x + 1].disTag >= 0 and tagedMap.g[y][x + 1].disTag < temp:
                    temp = tagedMap.g[y][x + 1].disTag;
                    desx = x + 1
                    dexy = y
        j = dexy
        i = desx

        # print("!!!!!")
        # print(i)
        # print(j)

        if (tagedMap.g[j][i].disTag == 0):
            return vindinium.DIR_STAY
        while (tagedMap.g[j][i].disTag > 1):
            i = tagedMap.g[j][i].pos_from.x
            j = tagedMap.g[j][i].pos_from.y

        ox = tagedMap.g[j][i].pos_from.x
        oy = tagedMap.g[j][i].pos_from.y

        if x == ox:
            if y > oy:
                # return vindinium.DIR_NORTH
                return "South"
            elif y < oy:
                # return vindinium.DIR_SOUTH
                return "North"
            else:
                # return vindinium.DIR_STAY
                return "Stay"
        elif x < ox:
            # return vindinium.DIR_WEST
            # print(vindinium.DIR_WEST)
            return "West"
        else:
            # return vindinium.DIR_EAST
            return "East"

    def get_distance(self, tagedMap, x, y):
        temp = 100
        if x == 0:
            if y == 0:
                if tagedMap.g[y + 1][x].disTag >= 0 and tagedMap.g[y + 1][x].disTag < temp:
                    temp = tagedMap.g[y + 1][x].disTag;
                if tagedMap.g[y][x + 1].disTag >= 0 and tagedMap.g[y][x + 1].disTag < temp:
                    temp = tagedMap.g[y][x + 1].disTag;
            elif y == tagedMap.h - 1:
                if tagedMap.g[y - 1][x].disTag >= 0 and tagedMap.g[y - 1][x].disTag < temp:
                    temp = tagedMap.g[y - 1][x].disTag;
                if tagedMap.g[y][x + 1].disTag >= 0 and tagedMap.g[y][x + 1].disTag < temp:
                    temp = tagedMap.g[y][x + 1].disTag;
            else:
                if tagedMap.g[y + 1][x].disTag >= 0 and tagedMap.g[y + 1][x].disTag < temp:
                    temp = tagedMap.g[y + 1][x].disTag;
                if tagedMap.g[y - 1][x].disTag >= 0 and tagedMap.g[y - 1][x].disTag < temp:
                    temp = tagedMap.g[y - 1][x].disTag;
                if tagedMap.g[y][x + 1].disTag >= 0 and tagedMap.g[y][x + 1].disTag < temp:
                    temp = tagedMap.g[y][x + 1].disTag;
        elif x == tagedMap.w - 1:
            if y == 0:
                if tagedMap.g[y + 1][x].disTag >= 0 and tagedMap.g[y + 1][x].disTag < temp:
                    temp = tagedMap.g[y + 1][x].disTag;
                if tagedMap.g[y][x - 1].disTag >= 0 and tagedMap.g[y][x - 1].disTag < temp:
                    temp = tagedMap.g[y][x - 1].disTag;
            elif y == tagedMap.h - 1:
                if tagedMap.g[y - 1][x].disTag >= 0 and tagedMap.g[y - 1][x].disTag < temp:
                    temp = tagedMap.g[y - 1][x].disTag;
                if tagedMap.g[y][x - 1].disTag >= 0 and tagedMap.g[y][x - 1].disTag < temp:
                    temp = tagedMap.g[y][x - 1].disTag;
            else:
                if tagedMap.g[y + 1][x].disTag >= 0 and tagedMap.g[y + 1][x].disTag < temp:
                    temp = tagedMap.g[y + 1][x].disTag;
                if tagedMap.g[y - 1][x].disTag >= 0 and tagedMap.g[y - 1][x].disTag < temp:
                    temp = tagedMap.g[y - 1][x].disTag;
                if tagedMap.g[y][x - 1].disTag >= 0 and tagedMap.g[y][x - 1].disTag < temp:
                    temp = tagedMap.g[y][x - 1].disTag;

        else:
            if y == 0:
                if tagedMap.g[y + 1][x].disTag >= 0 and tagedMap.g[y + 1][x].disTag < temp:
                    temp = tagedMap.g[y + 1][x].disTag;
                if tagedMap.g[y][x - 1].disTag >= 0 and tagedMap.g[y][x - 1].disTag < temp:
                    temp = tagedMap.g[y][x - 1].disTag;
                if tagedMap.g[y][x + 1].disTag >= 0 and tagedMap.g[y][x + 1].disTag < temp:
                    temp = tagedMap.g[y][x + 1].disTag;
            elif y == tagedMap.h - 1:
                if tagedMap.g[y - 1][x].disTag >= 0 and tagedMap.g[y - 1][x].disTag < temp:
                    temp = tagedMap.g[y - 1][x].disTag;
                if tagedMap.g[y][x - 1].disTag >= 0 and tagedMap.g[y][x - 1].disTag < temp:
                    temp = tagedMap.g[y][x - 1].disTag;
                if tagedMap.g[y][x + 1].disTag >= 0 and tagedMap.g[y][x + 1].disTag < temp:
                    temp = tagedMap.g[y][x + 1].disTag;
            else:
                if tagedMap.g[y + 1][x].disTag >= 0 and tagedMap.g[y + 1][x].disTag < temp:
                    temp = tagedMap.g[y + 1][x].disTag;
                if tagedMap.g[y - 1][x].disTag >= 0 and tagedMap.g[y - 1][x].disTag < temp:
                    temp = tagedMap.g[y - 1][x].disTag;
                if tagedMap.g[y][x - 1].disTag >= 0 and tagedMap.g[y][x - 1].disTag < temp:
                    temp = tagedMap.g[y][x - 1].disTag;
                if tagedMap.g[y][x + 1].disTag >= 0 and tagedMap.g[y][x + 1].disTag < temp:
                    temp = tagedMap.g[y][x + 1].disTag;
        return temp
