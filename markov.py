import random

class MarkovChainTrigrams:
    def __init__(self):
        self.forward_memory = {}
        self.backward_memory = {}


    def __add_trigram(self, first, second, third):
        # forward
        if first not in self.forward_memory:
            self.forward_memory[first] = {}
        if second not in self.forward_memory[first]:
            self.forward_memory[first][second] = {}
        if third not in self.forward_memory[first][second]:
            self.forward_memory[first][second][third] = 0
        self.forward_memory[first][second][third] += 1

        # backward
        if third not in self.backward_memory:
            self.backward_memory[third] = {}
        if second not in self.backward_memory[third]:
            self.backward_memory[third][second] = {}
        if first not in self.backward_memory[third][second]:
            self.backward_memory[third][second][first] = 0
        self.backward_memory[third][second][first] += 1


    def add_text(self, text):
        text = text.lower()
        words = text.split()
        words = list(filter(lambda x: x != '', words))
        trigrams = [words[i:i+3] for i in range(len(words) - 2)]
        for i in trigrams:
            self.__add_trigram(i[0], i[1], i[2])


    def predict_next(self, word1, word2):
        values = self.forward_memory[word1][word2].values()
        return random.choices(list(self.forward_memory[word1][word2].keys()), weights=values, k=1)[0]


    def predict_prev(self, word3, word2):
        values = self.backward_memory[word3][word2].values()
        return random.choices(list(self.backward_memory[word3][word2].keys()), weights=values, k=1)[0]


    def predict_mid(self, word1, word3):
        choose_from = list(set(self.forward_memory[word1]) & set(self.backward_memory[word3]))
        if len(choose_from) == 0:
            choose_from.append('is that')
        return random.choices(choose_from, k=1)[0]

