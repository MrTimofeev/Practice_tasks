import random

class Cell:
    def __init__(self, around_mines=0, mine=False):
        self.around_mines = around_mines
        self.mine = mine
        self.fl_open = False
    
    def __repr__(self):
        if not self.fl_open:
            return "#"
        return "*" if self.mine else str(self.around_mines)

class GamePole:
    def __init__(self, N, M):
        self.N = N
        self.M = M
      
        self.init()
    
    def init(self):
        #Создание поля
        self.pole = [[Cell() for _ in range(self.N)] for _ in range(self.N)]
        
        # Расстановка мин
        all_positions = [(i, j) for i in range(self.N) for j in range(self.N)]
        mines_positions = random.sample(all_positions, min(self.M, self.N*self.N))
        
        for i, j in mines_positions:
            self.pole[i][j].mine = True
        
        # Подсчет мин вокруг
        for i in range(self.N):
            for j in range(self.N):
                if not self.pole[i][j].mine:
                    count = 0
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            ni, nj = i + di, j + dj
                            if 0 <= ni < self.N and 0 <= nj < self.N:
                                if self.pole[ni][nj].mine:
                                    count += 1
                    self.pole[i][j].around_mines = count
    
    def show(self):
        for row in self.pole:
            print(' '.join(str(cell) for cell in row))