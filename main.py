import copy
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

    def set_lenght(self, len_grid):
        """
        Set the grid lenght
        """
        self._grid_lenght = len_grid

        self._grid = []  # Create empty list
        if self.get_grid_lenght() % 2 != 0:  # Check if the grid lenght is pair or impair
            self._grid_lenght += 1

    def get_grid_lenght(self):
        """
        Get the grid lenght
        """
        return self._grid_lenght

    def set_sentence(self, sentence):
        """
        Set the sentence
        """
        self._sentence = sentence

    def get_sentence(self):
        """
        Get the sentence
        """
        return self._sentence

    def grid_fill(self):
        """
        Create grid with input lenght, chunk by chunk in empty list
        """
        n = self.get_grid_lenght()
        for i in range(n):  # Loop to append 0 in chunk, compared to grid lenght
            chunk = []
            self._grid.append(chunk)
            for j in range(n):
                chunk.append(0)
        return self._grid, self.get_grid_lenght()

    def adapt_sentence(self):
        """
        Adapt sentence with lower, no special caracter and no sapce
        """
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
        myMask.close()
        return saveMask

    def set_mask(self):
        """
        Set the mask (0 and 1)
        """
        model = self.get_text_mask()
        print("grille", (self.get_grid_lenght()))
        for i in range(self.get_grid_lenght()):
            for j in range(self.get_grid_lenght()):
                if i < len(model) and j < len(model):
                    self._mask[i][j] = model[i][j]
        print("mask", len(self._mask))

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
            for j in range(n):
                chunkMask.append(0)
            emptyMask.append(chunkMask)

        for i in range(n):
            for j in range(n):
                emptyMask[j][n - 1 - i] = masque[i][j]  # Put coordinate rotation to the "emptyMask" (90°)
                # emptyMask[n - 1- j][i] = masque[i][j]  # Put coordinate rotation to the "emptyMask" (-90°)

        self._mask = emptyMask  # Set the emptymask to the mask
        return self._mask

    # def save_mask(self):
    #  """
    #   Save the mask
    #  """

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
        self._mask = self.get_text_mask()
        deciphered = []
        sentenceToDecipher = list(decipherSentence)

        if len(self._mask) % 2 != 0:
            middle = len(sentenceToDecipher) // 2 - 2
            sentenceToDecipher.insert(middle, "a")

        while len(sentenceToDecipher) < self.get_grid_lenght() ** 2:
            sentenceToDecipher.append("")

        decipherGrid = []
        taille = len(self._mask)

        for i in range(taille):
            chunk = []
            for j in range(taille):
                chunk.append(sentenceToDecipher.pop(0))
            if chunk:
                last_char = chunk[-1]
            else:
                last_char = ""
            if len(self._mask) % 2 != 0:
                randomLetterDecipher = chr(rand.randint(ord("a"), ord("z")))
                while randomLetterDecipher == last_char:
                    randomLetterDecipher = chr(rand.randint(ord("a"), ord("z")))

                chunk.append(randomLetterDecipher)
            decipherGrid.append(chunk)

        for _ in range(4):
            for i in range(len(decipherGrid)):
                for j in range(len(decipherGrid)):
                    if i < len(self._mask) and j < len(self._mask[i]) and self._mask[i][j] == 1:
                        deciphered.append(decipherGrid[i][j])
            self.mask_rotation()
        return deciphered

    def cipher(self, sentence):
        print("la phrase est", sentence)
        len_grid = len(sentence)
        print("la len de la phrase", len_grid)
        self.set_lenght(len_grid)
        self.grid_fill()
        self.set_sentence(sentence)
        self.adapt_sentence()
        self.mask_fill()
        self.set_mask()
        self.get_text_mask()
        grille = self.set_letter_in_grid()
        print(self._grid)
        cipherGrille = ''

        for row in grille:
            for letter in row:
                cipherGrille += str(letter)
        print(cipherGrille)
        return cipherGrille


class CipherUI:

    def __init__(self):
        self._grid = Grid()
        self._root = tk.Tk()
        self._root.title("Grilles tournantes de Fleissner")
        self._windows = self._root.geometry("800x900")
        self._canvas = tk.Canvas(self._root, height=600, width=1000)

        # Initlialisation des espaces de text qui accueilleront les messages coddés et décoddés.
        self._text_to_cipher = tk.Text(self._root, height=5, width=70, relief="groove")
        self._text_ciphered = tk.Text(self._root, height=5, width=70, relief="groove")

        # Récupération des données saisies dans les zones de texte
        # self._input_text_ciphered = self._text_ciphered.get("1.0", "end-1c")

        # Bouttons de droite
        self._load_button = tk.Button(self._root, height=1, width=10, text="Load")
        self._random_mask = tk.Button(self._root, height=1, width=10, text="Random")
        self._save_button = tk.Button(self._root, height=1, width=10, text="Save")
        self._create_mask = tk.Checkbutton(self._root, height=1, width=10, text="Create")

        # Bouttons centraux
        self._cypher_button = tk.Button(self._root, height=2, width=20, text="Cypher", command=self.cypher_button)
        self._decypher_button = tk.Button(self._root, height=2, width=20, text="Decypher")
        self._clear_button = tk.Button(self._root, height=2, width=20, text="Clear")
        self._clock = tk.Checkbutton(self._root, height=2, width=20, text="Clock")

        # Récupère les cliques de l'utilisateur
        # self._canvas.bind("<Button-1>", self.boucle_jeu)

        # Canvas
        self._canvas.grid(row=0, column=0, sticky="nw", columnspan=6, rowspan=6)
        self.draw_mask()

        # Menu de droite
        self._load_button.grid(row=1, column=2, sticky="nw")
        self._random_mask.grid(row=1, column=2, sticky="w")
        self._save_button.grid(row=1, column=2, sticky="sw")
        self._create_mask.grid(row=2, column=2, sticky="nw")

        # Clear text
        self._clear_txt = tk.Label(self._root, text="Clear")
        self._clear_txt.grid(row=6, column=0, sticky="w")
        self._text_to_cipher.grid(row=6, column=1, sticky="w")

        # Menu central
        self._cypher_button.grid(row=7, column=0, sticky="w")
        self._decypher_button.grid(row=7, column=1, sticky="we")
        self._clear_button.grid(row=7, column=2, sticky="se")
        self._clock.grid(row=7, column=3)

        # Cyphered text
        self._cypher_txt = tk.Label(self._root, text="Cipher")
        self._cypher_txt.grid(row=8, column=0, sticky="w")
        self._text_ciphered.grid(row=8, column=1, sticky="w")

        # Lancement général
        self._root.mainloop()

    def cypher_button(self):
        text_to_cypher = self._text_to_cipher.get("1.0", "end-1c")
        print(text_to_cypher)
        cyphered_text = self._grid.cipher(text_to_cypher)
        self._text_ciphered.delete("1.0", "end")
        self._text_ciphered.insert("1.0", cyphered_text)

    def draw_mask(self):
        # Affiche la grille
        plateau_size = 12  # self._grid.get_grid_lenght()
        taille_case = 500 // 12  # self._grid.get_grid_lenght() - 1
        for i in range(plateau_size):
            for j in range(plateau_size):
                self._canvas.create_rectangle((i + 1) * taille_case + 2, (j + 1) * taille_case + 2,
                                              (i + 1) * taille_case + taille_case + 2,
                                              (j + 1) * taille_case + taille_case + 2, fill="yellow", outline="black")

    # def gather_file(self):


###################################################################


grid = Grid()
# grid.cipher()

# grid.set_lenght()
# essaie = grid.decipher("bfcobeeacduomtauypeutasesarenpirpdrtoreqogrgrawaiuirmllemsdiosiknmiltlmgbeietrwashotesunbancardintgobreeqcnauupinetsyacilfonseeitdeoabudpsshlkyrppelcuivieailoyewlshysybacwdcmeujcixmysaeculmnfwsiasuanlvatseedaakniortptwarbxlioordsuztycewulwsioelldgekdeelnbjtiojloeqyctwhtahvvetswoxoxrlheda")
# print("déchifrement" , *essaie)

# essaie = grid.decipher("bfcobeeacduomtauypeutasesarenpirpdrtoreqogrgrawaiuirmllemsdiosiknmiltlmgbeietrwashotesunbancardintgobreebcnauubinqtsyaciqhonseoitdemaouapsshlpydfppelciivieailexewlshhsybaccpcdeuncijmisaegulmbfkafasuanleatseedajkniortptwkrnhlipoydsudtncewpjusioelldgeiideknbjttojsoelyctwhtahsoetswonocrlhedd")
# print("déchifré Benj" , *essaie)
# grid.get_json_mask()

grid_ui = CipherUI()
