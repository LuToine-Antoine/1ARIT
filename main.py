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

    def set_lenght(self, len_word):
        """
        Set the grid lenght
        """
        self._grid_lenght = len_word

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
                            "c": "ç", "": "',;:!?./§$"}  # Dictionnary of special letters
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
        myMask = open("mask.txt", "r")
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
                #emptyMask[n - 1- j][i] = masque[i][j]  # Put coordinate rotation to the "emptyMask"

        self._mask = emptyMask  # Set the emptymask to the mask
        return self._mask

    #def save_json(self):
    #   """
    #  Save the mask at json
    # """
    #save_file = open("mask.txt", "w")
    #json.dump(self.get_mask(), save_file, indent=6)
    #save_file.close()

    def set_letter_in_grid(self):
        sentence = list(self._sentence)
        tour = 0
        mask_copy = copy.deepcopy(self.get_mask())
        while tour < 4 and sentence:
            for i in range(len(self._grid)):
                for j in range(len(self._grid[i])):
                    if self.get_mask()[i][j] == 1 and sentence:
                        self._grid[i][j] = sentence.pop(0)
                        mask_copy[i][j] = 2  # Set letter

                    if self.get_mask()[i][j] == 0 and mask_copy[i][j] == 0:
                        lettre = chr(rand.randint(ord("a"), ord("z")))  # Random letter using ASCII
                        self._grid[i][j] = lettre

            self.mask_rotation()
            tour += 1

        return self._grid

    def decipher(self, decipherSentence):
        setenceToDecipher = list(decipherSentence)
        decipherGrid = []
        for i in range(self.get_grid_lenght()):
            chunk = []
            decipherGrid.append(chunk)
            for j in range(self.get_grid_lenght()):
                if setenceToDecipher:
                    chunk.append(setenceToDecipher.pop(0))
                else:
                    chunk.append('')

        self._mask = self.get_text_mask()
        deciphered = []

        for _ in range(4):
            for i in range(len(decipherGrid)):
                for j in range(len(decipherGrid)):
                    if self._mask[i][j] == 1:
                        deciphered.append(decipherGrid[i][j])
            self.mask_rotation()
        return deciphered

    def cipher(self, len_cypher):
        self.set_lenght(len(len_cypher))
        self.grid_fill()
        self.adapt_sentence()
        self.mask_fill()
        self.set_mask()
        self.get_text_mask()
        grille = self.set_letter_in_grid()

        cipherGrille = ''

        for row in grille:
            for letter in row:
                cipherGrille += letter

        return cipherGrille

class CipherUI:

    def __init__(self):
        self._grid = Grid()
        self._root = tk.Tk()
        self._root.title("Grilles tournantes de Fleissner")
        self._canvas = tk.Canvas(self._root, height=700, width=900)


        # Initialisation des groupes
        self._cypher_group = tk.Frame(self._canvas)
        self._cypher_group.place(relx=0, rely=0, anchor="center")
        self._center_button_group = tk.Frame(self._canvas)
        self._decypher_group = tk.Frame(self._canvas)

        # Initlialisation des espaces de text qui accueilleront les messages coddés et décoddés.
        self._text_to_cipher = tk.Text(self._canvas, height=5, width=70, relief="groove")
        self._text_ciphered = tk.Text(self._canvas, height=5, width=70, relief="groove")

        # Récupération des données saisies dans les zones de texte
        self._input_text_to_cipher = tk.Text(self._canvas, height=5, width=70, relief="groove").get("1.0", "end-1c")
        self._input_text_ciphered = tk.Text(self._canvas, height=5, width=70, relief="groove").get("1.0", "end-1c")

        # Initialisation des bouttons centraux
        self._cypher_button = tk.Button(self._center_button_group, height=2, width=20, text="Cypher", command= self.cypher_button())
        self._decypher_button = tk.Button(self._center_button_group, height=2, width=20, text="Decypher")
        self._clear_button = tk.Button(self._center_button_group, height=2, width=20, text="Clear")
        self._clock = tk.Checkbutton(self._center_button_group, height=2, width=20, text="Clock")

        # Textes a afficher
        self._clear_txt = tk.Label(self._cypher_group, height=5, width=70, relief="groove", text="truc")
        self._clear_txt.pack(side="left")

        # Affichage des éléments sur la fenêtre
        self._text_to_cipher.pack()
        self._cypher_button.pack(padx=5, pady=5, side="left")
        self._decypher_button.pack(padx=5, pady=5, side="left")
        self._clear_button.pack(padx=5, pady=5, side="left")
        self._clock.pack()
        self._center_button_group.pack(padx=5, pady=5)
        self._text_ciphered.pack()
        self._canvas.pack()
        self._root.mainloop()

    def cypher_button(self):
        text_to_cypher = self._input_text_to_cipher
        cyphered_text = self._grid.cipher(text_to_cypher)
        self._text_to_cipher.insert(tk.END, cyphered_text)

    # def draw_grid(self):
    #     grid_len = self._grid.get_grid_lenght()
    #     print(grid_len)
    #     if grid_len % 2 == 0:
    #         self._canvas.create_rectangle(50, 50, 200, 150, fill="white", outline="black")

    # def draw_mask(self):

    # def gather_file(self):


###################################################################


#grid = Grid()
#grid.cipher()

# essaie = grid.decipher("bfcobeeacduomtauypeutasesarenpirpdrtoreqogrgrawaiuirmllemsdiosiknmiltlmgbeietrwashotesunbancardintgobreeqcnauupinetsyacilfonseeitdeoabudpsshlkyrppelcuivieailoyewlshysybacwdcmeujcixmysaeculmnfwsiasuanlvatseedaakniortptwarbxlioordsuztycewulwsioelldgekdeelnbjtiojloeqyctwhtahvvetswoxoxrlheda")
# essaie = grid.decipher("bfcobeeacduomtauypeutasesarenpirpdrtoreqogrgrawaiuirmllemsdiosiknmiltlmgbeietrwashotesunbancardintgobreeucnauuxinatsyacinionseuitdeaajurpsssluynyppelccivieailfzewlshhsybacywcseugcismqsaesulmtfnxqasuanlsatseedazkniortptwqrclligofdsuwtycewxensioelldgekgpewnbjtrojxoezyctwhtahnwetswowoprlhedt")
# print("déchifré " , *essaie)
# grid.get_json_mask()

grid_ui = CipherUI()
