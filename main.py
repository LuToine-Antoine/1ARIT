import json
import tkinter as tk


class Grid:

    def __init__(self):
        """
        Initialize grid (length, sentence to cipher and grid)
        """
        self._letters = "abcdefghijklmnopqrstuvwxyz"
        self._grid_lenght = None
        self._sentence = None
        self._grid = []
        self._mask = []

    def set_lenght(self):
        """
        Set the grid lenght
        """
        self._grid_lenght = int(input("Enter grid lenght: "))

    def get_grid_lenght(self):
        """
        Get the grid lenght
        """
        return self._grid_lenght

    def set_sentence(self):
        """
        Set the sentence
        """
        self._sentence = input("Enter sentence to cipher: ")

    def get_sentence(self):
        """
        Get the sentence
        """
        return self._sentence

    def grid_fill(self):
        """
        Create grid with input lenght, chunk by chunk in empty list
        """
        chunk = []  # Create empty list
        for i in range(self.get_grid_lenght()):  # Loop to append 0 in chunk, compared to grid lenght
            chunk.append(0)
            self._grid.append(chunk)

        return self._grid

    def adapt_sentence(self):
        """
        Adapt sentence with lower, no special caracter and no sapce
        """
        self.set_sentence()
        replaceCaractere = {"e": "éèêë", "a": "àâä", "u": "ùûü", "i": "îï", "o": "ôö",
                            "c": "ç"}  # Dictionnary of special letters
        tempsSentence = self.get_sentence().lower()  # Set sentence to lower
        tempsSentence = tempsSentence.replace(" ", "")  # Remove space

        for key, value in replaceCaractere.items():  # Loop in oder to replace caractere (dict. values) in sentence with dict. key
            for i in value:
                tempsSentence = tempsSentence.replace(i, key)

        lenOfSentence = len(tempsSentence) - 1  # Set sentence lenght
        while lenOfSentence > 0:  # Loop to remove other sepcial caractere, using not lenght fix because, with remeving, the lenght change
            if tempsSentence[lenOfSentence] not in "abcdefghijklmnopqrstuvwxyz":
                tempsSentence = tempsSentence.replace(tempsSentence[lenOfSentence], "")
            lenOfSentence -= 1

        self._sentence = tempsSentence
        return self._sentence

    def mask_fill(self):
        chunkMask = []  # Create empty list
        for i in range(self.get_grid_lenght()):  # Loop to append 0 in chunk, compared to grid lenght
            chunkMask.append(0)
            self._mask.append(chunkMask)

        return self._mask

    def set_mask(self, x, y, mode):
        if mode == 0:
            self._mask[x][y] = 0
        elif mode == 1:
            self._mask[x][y] = 1

    def get_mask(self):
        return self._mask

    def save_json(self):
        save_file = open("mask.json", "w")
        json.dump(self.get_mask(), save_file, indent=6)
        save_file.close()


class CipherUI:

    def __init__(self):
        self._grid = Grid()
        self._root = tk.Tk()
        self._root.title("Grilles tournantes de Fleissner")
        self._canvas = tk.Canvas(self._root, height=700, width=700)

        self._canvas.pack()
        self._root.mainloop()

    # def draw_grid(self):

    def darw_mask(self):



###################################################################


# grid = Grid()
#
# grid.set_lenght()
# truc = grid.grid_fill()
# machin = grid.adapt_sentence()
# print(truc, "\n", machin)

grid = CipherUI()
