import copy
import json
import tkinter as tk
import random as rand
from tkinter.filedialog import askopenfilename

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

    def get_text_mask(self):
        """
        Get the mask from txt file
        """
        myMask = open("mask_test.txt", "r")
        saveMask = []
        for line in myMask:
            line = line.strip()  # Remove line break
            row = []
            for char in line:
                row.append(int(char))
            saveMask.append(row)
        return saveMask

    def set_mask(self):
        """
        Set the mask (0 and 1)
        """
        model = self.get_text_mask()
        for i in range(len(model)):
            for j in range(len(model)):
                self._mask[i][j] = model[i][j]

    def get_mask(self):
        """
        Get the mask
        """
        return self._mask

    def mask_rotation(self):
        """
        Rotate the mask
        """
        masque = self.get_mask()
        n = len(masque)

        emptyMask = []  # Create empty list to append rotating mask and return this mask from the "copy"
        for i in range(n):
            chunkMask = []
            emptyMask.append(chunkMask)
            for j in range(n):
                chunkMask.append(0)

        for i in range(n):
            for j in range(n):
                emptyMask[j][n - 1 - i] = masque[i][j]  # Put coordinate rotation to the "emptyMask"

        self._mask = emptyMask  # Set the emptymask to the mask
        return self._mask

    def save_json(self):
        """
        Save the mask at json
        """
        save_file = open("mask_test.txt", "w")
        json.dump(self.get_mask(), save_file, indent=6)
        save_file.close()

    def set_letter_in_grid(self):
        sentence = list(self._sentence)
        tour = 0
        mask_copy = copy.deepcopy(self.get_mask())
        while tour < 4 and sentence:
            for i in range(len(self._grid)):
                for j in range(len(self._grid[i])):
                    if self.get_mask()[i][j] == 1 and sentence :
                        self._grid[i][j] = sentence.pop(0)
                        mask_copy[i][j] = 2  # Set letter

                    if self.get_mask()[i][j] == 0 and mask_copy[i][j] == 0:
                        lettre = chr(rand.randint(ord("a"), ord("z")))  # Random letter using ASCII
                        self._grid[i][j] = lettre

            self.mask_rotation()
            tour += 1
        return self._grid

    def decipher(self):
        #setenceToDecipher = list(decipherSentence)
        #decipherGrid = []
        #for i in range(self.get_grid_lenght()):
         #   chunk = []
          #  decipherGrid.append(chunk)
           # for j in range(self.get_grid_lenght()):
            #    chunk.append(setenceToDecipher.pop(0))

        deciphered = []
        tour = 0
        while tour < 4 :
            for i in range(len(self._grid)):
                for j in range(len(self._grid[i])):
                    if self.get_mask()[i][j] == 1:
                        deciphered.append(self._grid[i][j])

            self.mask_rotation()
            tour += 1
        return deciphered

class CipherUI:

    def __init__(self):
        self._grid = Grid()
        self._root = tk.Tk()
        self._root.title("Grilles tournantes de Fleissner")
        self._canvas = tk.Canvas(self._root, height=700, width=700)

        self._text_to_cipher = tk.Text(self._canvas, height=5, width=70)
        self._frm_text_to_cypher = tk.Frame(self._canvas, borderwidth=2)

        self._test_frm = tk.Frame(self._canvas)
        self._test_frm.pack(side=tk.LEFT)

        self._frm_text_to_cypher.pack(self._text_to_cipher, side=tk.LEFT)

        tk.Label(self._frm_text_to_cypher, text="test").pack(side=tk.LEFT)

        self._frm_text_to_cypher.pack()
        self._canvas.pack()
        self._root.mainloop()

    # def draw_grid(self):
    #     grid_len = self._grid.get_grid_lenght()
    #     print(grid_len)
    #     if grid_len % 2 == 0:
    #         self._canvas.create_rectangle(50, 50, 200, 150, fill="white", outline="black")

    #def draw_mask(self):

    def gather_file(self):
        filename = askopenfilename(title="Ouvrir votre document",
                                   filetypes=[('txt files', '.txt'), ('all files', '.*')])
        fichier = open(filename, "r")
        content = fichier.read()
        fichier.close()

        tk.Label(self._root, text=content).pack(padx=10, pady=10)



###################################################################


grid = Grid()
grid.set_lenght()
truc = grid.grid_fill()
machin = grid.adapt_sentence()
# print("grif fill", truc, "\n", "adapte", machin)
grid.mask_fill()
grid.set_mask()
grid.get_text_mask()
grille = grid.set_letter_in_grid()
for row in grille:
    print(row)
essaie = grid.decipher()
print(*essaie)
#grid.get_json_mask()

#grid_ui = CipherUI()
