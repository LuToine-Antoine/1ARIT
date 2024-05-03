import copy
import tkinter as tk
import random as rand
from tkinter.filedialog import askopenfilename


class Grid:

    def __init__(self):
        """
        Initialize grid class
        """
        self._grid_lenght = None
        self._sentence = None
        self._grid = []
        self._mask = []

    def set_grid_lenght(self, len_grid):
        """
        Set the grid lenght
        """
        self._grid_lenght = len_grid

        self._grid = []  # Create empty list
        if self._grid_lenght % 2 != 0:  # Check if the grid lenght is pair or impair
            self._grid_lenght += 1

    def get_grid_lenght(self):
        """
        Get the grid lenght
        """
        return self._grid_lenght


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
        return self._grid

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

        self.set_sentence(tempsSentence)
        return self._sentence

    def mask_fill(self):
        """
        Fill the mask with 0
        """
        self._mask = []  # Create empty list
        for i in range(self.get_grid_lenght()):  # Loop to append 0 in chunk, compared to grid lenght
            chunkMask = []
            self._mask.append(chunkMask)
            for j in range(self.get_grid_lenght()):
                chunkMask.append(0)

        return self._mask

    def set_mask_with_file(self):
        """
        Set the mask (0 and 1) from txt file
        """
        model = self.get_mask()
        print("grille", (self.get_grid_lenght()))
        for i in range(self.get_grid_lenght()):
            for j in range(self.get_grid_lenght()):
                if i < len(model) and j < len(model):
                    self._mask[i][j] = model[i][j]
        print("mask", len(self._mask))

    def set_mask_by_user(self, x, y):
        """
        Set the mask (0 and 1) at the position x and y
        """
        if self._mask[x][y] == 1:
            self._mask[x][y] = 0
        elif self._mask[x][y] == 0:
            self._mask[x][y] = 1

   # def set_mask(self, mask):
   #     print("mask", mask)
   #     print("mask len", len(mask))
   #     for i in range(len(mask)):
   #         for j in range(len(mask)):
   #             self._mask[i][j] = mask[i][j]

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
        # self._mask = self.get_text_mask()
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

    #def cipher(self):
    #    self.set_lenght()
    #    self.grid_fill()
    #    self.adapt_sentence()
    #    self.mask_fill()
    #    self.set_mask()
    #    self.get_text_mask()
    #    grille = self.set_letter_in_grid()
    #    print(self._grid)
    #    cipherGrille = ''
    #    for row in grille:
    #        for letter in row:
    #            cipherGrille += str(letter)
    #    print(cipherGrille)
    #    return

    def cipher(self, sentence):
        len_grid = len(sentence)
        self.set_grid_lenght(len_grid)
        print("grid len \n", self.get_grid_lenght())
        self.grid_fill()
        self.set_sentence(sentence)
        print("get sentence \n", self.get_sentence())
        self.adapt_sentence()
        print("adapt sentence \n", self.adapt_sentence())
        self.mask_fill()
        self.get_mask()
        print("get mask \n", self.get_mask())
        grille = self.set_letter_in_grid()
        print("grid \n", self._grid)
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

        # Menu
        menubar = tk.Menu(self._root)
        menu_set_mask = tk.Menu(menubar, tearoff=0)
        menu_set_mask.add_command(label="Définir mask")
        menu_set_mask.add_cascade(label="Mask", menu=menu_set_mask)

        # Initlialisation des espaces de text qui accueilleront les messages coddés et décoddés.
        self._text_to_cipher = tk.Text(self._root, height=5, width=70, relief="groove")
        self._text_ciphered = tk.Text(self._root, height=5, width=70, relief="groove")

        # Bouttons de droite
        self._load_button = tk.Button(self._root, height=1, width=10, text="Load", command=self.get_mask_file)
        self._random_mask = tk.Button(self._root, height=1, width=10, text="Random")
        self._save_button = tk.Button(self._root, height=1, width=10, text="Save", command=self.save_button)
        self._checkbutton_value = tk.IntVar()
        self._create_mask = tk.Checkbutton(self._root, height=1, width=10, text="Create", variable=self._checkbutton_value, onvalue=1, offvalue=0)

        # Bouttons centraux
        self._cypher_button = tk.Button(self._root, height=2, width=20, text="Cypher", command=self.cipher_button)
        self._decypher_button = tk.Button(self._root, height=2, width=20, text="Decypher", command=self.decipher_button)
        self._clear_button = tk.Button(self._root, height=2, width=20, text="Clear", command=self.clear_button)
        self._clock = tk.Checkbutton(self._root, height=2, width=20, text="Clock")

        # Canvas
        self._canvas.grid(row=0, column=0, sticky="nw", columnspan=6, rowspan=6)

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

        # Récupère les cliques de l'utilisateur
        # print(self._checkbutton_value.get())
        # if self._checkbutton_value.get() == 1:
        #     self._canvas.bind("<Button-1>", self.set_mask_by_user)

        # Lancement général
        self._root.config(menu=menubar)
        self._root.mainloop()

    def cipher_button(self):
        text_to_cipher = self._text_to_cipher.get("1.0", "end-1c")
        print("mask : #n", self._grid.get_mask())
        ciphered_text = self._grid.cipher(text_to_cipher)
        self._text_ciphered.delete("1.0", "end")
        self._text_ciphered.insert("1.0", ciphered_text)

    def decipher_button(self):
        text_to_decipher = self._text_ciphered.get("1.0", "end-1c")
        self._grid.set_grid_lenght(len(text_to_decipher))
        deciphered_text = str(self._grid.decipher(text_to_decipher))
        deciphered_text = deciphered_text.replace("[", "")
        deciphered_text = deciphered_text.replace("]", "")
        deciphered_text = deciphered_text.replace(",", "")
        deciphered_text = deciphered_text.replace("'", "")
        self._text_to_cipher.delete("1.0", "end")
        self._text_to_cipher.insert("1.0", str(deciphered_text))

    def clear_button(self):
        self._text_ciphered.delete("1.0", "end")
        self._text_to_cipher.delete("1.0", "end")

    # def checkbutton_set_value(self):
    #     if self._checkbutton_value.get() == 0:
    #         self._checkbutton_value.set(1)
    #         self._create_mask.select()
    #     else:
    #         self._checkbutton_value.set(0)
    #         self._create_mask.deselect()

    def save_button(self):
        """
        Save the mask in a txt
        """
        mask_file = open("custom_mask.txt", "w")
        mask_to_save = self._grid.get_mask()
        line = ""
        for i in range(len(mask_to_save)):
            for j in range(len(mask_to_save)):
                line += str(mask_to_save[i][j])
            line += "\n"
        mask_file.write(line)
        mask_file.close()
        print("mask saved")

    def draw_mask(self):
        # Affiche la grille
        mask_len = len(self._grid.get_mask())

        print("mask : \n", self._grid.get_mask())
        print("longueur mask", mask_len)
        taille_case = 500 // mask_len
        if mask_len % 2 == 0:
            case_number = mask_len ** 2 // 4
        elif mask_len % 2 == 1:
            case_number = (mask_len ** 2 - 1) // 4

        for i in range(mask_len):
            for j in range(mask_len):

                if self._grid.get_mask()[j][i] == 0:
                    self._canvas.create_rectangle((i + 1) * taille_case + 2, (j + 1) * taille_case + 2,
                                                  (i + 1) * taille_case + taille_case + 2,
                                                  (j + 1) * taille_case + taille_case + 2, fill="black",
                                                  outline="blue")
                elif self._grid.get_mask()[j][i] == 1:
                    self._canvas.create_rectangle((i + 1) * taille_case + 2, (j + 1) * taille_case + 2,
                                                  (i + 1) * taille_case + taille_case + 2,
                                                  (j + 1) * taille_case + taille_case + 2, fill="white",
                                                  outline="blue")

    def get_mask_file(self):
        filename = askopenfilename(title="Sélectionnez votre mask",
                                   filetypes=[('txt files', '.txt'), ('all files', '.*')])
        file = open(filename, "r")
        saveMask = []
        for line in file:
            line = line.strip()  # Remove line break
            row = []
            for char in line:
                row.append(int(char))
            saveMask.append(row)
        self._grid._mask = saveMask
        file.close()
        self._canvas.delete("all")
        self.draw_mask()

    def set_mask_by_user(self, event):
        self._grid.set_grid_lenght(len(self._text_to_cipher.get("1.0", "end-1c")))
        self._grid.mask_fill()
        click = (((event.x - 50) // self._grid.get_grid_lenght()), ((event.y - 50) // self._grid.get_grid_lenght()))
        print(click)
        self._grid.set_mask_by_user(click[0], click[1])



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
