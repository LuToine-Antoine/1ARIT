import json
import tkinter as tk
import random as rand


class Grid:

    def __init__(self):
        """
        Initialize grid (length, sentence to cipher and grid)
        """
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
        self._grid = []  # Create empty list
        for i in range(self.get_grid_lenght()):  # Loop to append 0 in chunk, compared to grid lenght
            chunk = []
            self._grid.append(chunk)
            for j in range(self.get_grid_lenght()):
                chunk.append(0)

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
        self._mask = []  # Create empty list
        for i in range(self.get_grid_lenght()):  # Loop to append 0 in chunk, compared to grid lenght
            chunkMask = []
            self._mask.append(chunkMask)
            for j in range(self.get_grid_lenght()):
                chunkMask.append(0)

        return self._mask

    def get_json_mask(self):
        """
        Get the mask from json
        """
        with open("mask.json", "r") as file:
            json_mask = file.read()

        mask = json.loads(json_mask)

        for item in mask:
            print(item["personnal_mask"])
        print("personnal", mask)
        return mask

    def set_mask(self, x, y, mode):
        """
        Set the mask (0 and 1)
        """
        if mode == 0:
            self._mask[x][y] = 0
        elif mode == 1:
            self._mask[x][y] = 1

    def get_mask(self):
        """
        Get the mask
        """
        return self._mask

    def save_json(self):
        """
        Save the mask at json
        """
        save_file = open("mask.json", "w")
        json.dump(self.get_mask(), save_file, indent=6)
        save_file.close()

    def set_letter_in_grid(self):
        sentence = list(self._sentence)
        print(sentence)
        for i in range(len(self._grid)):
            for j in range(len(self._grid[i])):
                if self.get_mask()[i][j] == 1:
                    self._grid[i][j] = sentence[0]
                    sentence.pop(0)
                if self.get_mask()[i][j] == 0:
                    lettre = chr(rand.randint(ord("a"), ord("z")))  # Random letter using ASCII
                    self._grid[i][j] = lettre
        print(self._grid)


class CipherUI:

    def __init__(self):
        self._grid = Grid()
        self._root = tk.Tk()
        self._root.title("Grilles tournantes de Fleissner")
        self._canvas = tk.Canvas(self._root, height=700, width=700)

        self._canvas.pack()
        self._root.mainloop()

    # def draw_grid(self):

    #def draw_mask(self):



###################################################################


grid = Grid()
#
#grid.set_lenght()
#truc = grid.grid_fill()
#machin = grid.adapt_sentence()
#print("grif fill", truc, "\n", "adapte", machin)
#grid.mask_fill()
#grid.set_mask(0, 0, 1)
#grid.set_mask(0, 1, 1)
#grid.set_mask(2, 1, 1)
#grid.set_mask(0, 3, 1)
#grid.set_mask(3, 0, 1)
#print(*grid.get_mask())
#grid.set_letter_in_grid()

grid.get_json_mask()
#grid = CipherUI()
