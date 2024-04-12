class Grid:

    def __init__(self, lenght):
        self._grid_lenght = lenght
        self._grid = []

    def set_lenght(self):
        self._grid_lenght = int(input("Enter grid lenght: "))
        print(self._grid_lenght)

    def get_grid_lenght(self):
        return self._grid_lenght

    def grid_fill(self):
        print(self.get_grid_lenght())
        for i in range(self.get_grid_lenght()):
            print("truc1")
            self._truc = []
            for j in range(self._grid_lenght):
                print("truc2")
                self._truc.append(0)
                self._grid.append(self._truc)
                return self._grid


grid = Grid(2)

grid.set_lenght()
truc = grid.grid_fill()
print(truc)

