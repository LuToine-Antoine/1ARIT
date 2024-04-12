class Grid:

    def __init__(self, lenght):
        self._grid_lenght = lenght
        self._grid = []

    def set_lenght(self):
        '''
        Set the grid lenght
        '''
        self._grid_lenght = int(input("Enter grid lenght: "))
        print(self._grid_lenght)

    def get_grid_lenght(self):
        '''
        Get the grid lenght
        '''
        return self._grid_lenght

    def grid_fill(self):
        '''
        Create grid with input lenght, chunk by chunk in empty list
        '''
        for i in range(1):
            self._chunk = []

            for j in range(self.get_grid_lenght()):
                self._chunk.append(0)
                self._grid.append(self._chunk)

        return self._grid


grid = Grid(2)

grid.set_lenght()
truc = grid.grid_fill()
print(truc)
