import random


class Cell():

    def __init__(self, around_mines=0, mine=False):
        self.around_mines = around_mines
        self.mine = mine
        self.fl_open = False

    def __repr__(self):
        if self.fl_open:
            return "*"

        return "#"


class GamePole():

    def __init__(self, N, M):
        self.N = N
        self.M = M
        self.init()
        self.__set_random_mine(N, M)

    def init(self):
        self.pole = [[Cell() for _ in range(self.N)] for _ in range(self.N)]

    def show(self):
        for row in self.pole:
            print(' '.join(str(cell) for cell in row))

    def __set_random_mine(self, N, M):
        count_set_mine = 0

        while True:
            if count_set_mine == M:
                break

            random_row = random.randint(0, N-1)
            random_column = random.randint(0, N-1)
            if self.pole[random_row][random_column].mine == False:
                self.pole[random_row][random_column].mine = True
                self.__set_around_mines(random_row, random_column)
                count_set_mine += 1

    def __set_around_mines(self, row, column):
        try:
            self.pole[row-1][column-1].around_mines += 1
        except:
            pass

        try:
            self.pole[row-1][column].around_mines += 1
        except:
            pass

        try:
            self.pole[row-1][column + 1].around_mines += 1
        except:
            pass

        try:
            self.pole[row][column-1].around_mines += 1
        except:
            pass

        try:
            self.pole[row][column+1].around_mines += 1
        except:
            pass

        try:
            self.pole[row+1][column-1].around_mines += 1
        except:
            pass

        try:
            self.pole[row+1][column].around_mines += 1
        except:
            pass

        try:
            self.pole[row+1][column+1].around_mines += 1
        except:
            pass


pole = GamePole(10, 12)
pole.show()
