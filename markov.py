import numpy as np


class MarkovChainTrigrams:
    def __init__(self):
        self.forward_memory = {}
        self.backward_memory = {}


    def add_trigram(self, first, second, third):
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
        words = text.split()
        for i in range(len(words)):
            words[i] = words[i].lower()

        trigrams = [(words[i], words[i+1], words[i+2]) for i in range(len(words) - 2) \
                  if words[i] != '' and words[i+1] != '' and words[i+2] != '']
        for i in trigrams:
            self.add_trigram(i[0], i[1], i[2])


    def predict_next(self, word1, word2):
        return np.random.choice(list(self.forward_memory[word1][word2].keys()), 
                                1, p=np.array(list(self.forward_memory[word1][word2].values())) \
                                / sum(self.forward_memory[word1][word2].values()))[0]


    def predict_prev(self, word3, word2):
        return np.random.choice(list(self.backward_memory[word3][word2].keys()), 
                                1, p=np.array(list(self.backward_memory[word3][word2].values())) \
                                / sum(self.backward_memory[word3][word2].values()))[0]


    def predict_mid(self, word1, word3):
        choose_from = list(set(self.forward_memory[word1].keys()) & set(self.backward_memory[word3].keys()))
        return np.random.choice(choose_from)
        return np.random.choice(list(self.middle_memory[word1][word3].keys()), 
                                1, p=np.array(list(self.middle_memory[word1][word3].values())) \
                                / sum(self.middle_memory[word1][word3].values()))[0]

