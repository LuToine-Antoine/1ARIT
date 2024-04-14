class Grid:

    def __init__(self):
        '''
        Initialize grid (length, sentence to cipher and grid)
        '''
        self._grid_lenght = None
        self._sentence = None
        self._grid = []

    def set_lenght(self):
        '''
        Set the grid lenght
        '''
        self._grid_lenght = int(input("Enter grid lenght: "))

    def get_grid_lenght(self):
        '''
        Get the grid lenght
        '''
        return self._grid_lenght

    def set_sentence(self):
        '''
        Set the sentence
        '''
        self._sentence = input("Enter sentence to cipher: ")

    def get_sentence(self):
        '''
        Get the sentence
        '''
        return self._sentence

    def grid_fill(self):
        '''
        Create grid with input lenght, chunk by chunk in empty list
        '''
        self._chunk = []  # Create empty list
        for i in range(self.get_grid_lenght()):  # Loop to append 0 in chunk, compared to grid lenght
            self._chunk.append(0)
            self._grid.append(self._chunk)

        return self._grid

    def adapt_sentence(self):
        '''
        Adapt sentence with lower, no special caracter and no sapce
        '''
        self.set_sentence()
        replaceCaractere = {"e": "éèêë", "a": "àâä", "u": "ùûü", "i": "îï", "o": "ôö", "c": "ç"}  # Dictionnary of special letters
        tempsSentence = self.get_sentence().lower()  # Set sentence to lower
        tempsSentence = tempsSentence.replace(" ", "")  # Remove space

        for key, value in replaceCaractere.items():  # Loop in oder to replace caractere (dict. values) in sentence with dict. key
            for i in value:
                tempsSentence = tempsSentence.replace(i, key)

        lenOfSentence = len(tempsSentence)-1  # Set sentence lenght
        while lenOfSentence > 0:  # Loop to remove other sepcial caractere, using not lenght fix because, with remeving, the lenght change
            if tempsSentence[lenOfSentence] not in "abcdefghijklmnopqrstuvwxyz":
                tempsSentence = tempsSentence.replace(tempsSentence[lenOfSentence], "")
            lenOfSentence -= 1

        self._sentence = tempsSentence
        return self._sentence



###################################################################


grid = Grid()

grid.set_lenght()
truc = grid.grid_fill()
machin = grid.adapt_sentence()
print(truc, machin)
