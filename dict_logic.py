import os
import json
import random

class Dictionary:
    def __init__(self, filename):
        self.filename = filename
        if os.path.exists(filename):
            with open(filename,"r") as f:
                self.data = json.load(f)

    def get_random_word(self):
        return random.choice(list(self.data.keys()))

    def get_random_definition(self):
        return random.choice(list(self.data.values()))

    def add_word(self,word,definition):
        new_word = {word:definition}
        self.data.update(new_word)
        with open(self.filename, "w") as f:
            f.write(json.dumps(self.data))
        

class Quiz:
    def __init__(self, dictionary:Dictionary):
        self.dictionary = dictionary
        self.random_word = None #random kiválasztott szó
        self.the_good_answer = None # a random szó tényleges jelentése
        self.answers = [] # 3 random definiciot tartalmaz
        self.good = 0 # jó válaszaid számát tárolja
        self.bad = 0 # rossz válaszaid számát tárolja

    def shuffle_elements(self):
        data_list = list(self.dictionary.data.items())
        random.shuffle(data_list)
        data_dict = dict(data_list)
        with open(self.dictionary.filename, "w") as f:
            f.write(json.dumps(data_dict))

    def make_quiz(self):
        self.shuffle_elements()
        self.random_word = self.dictionary.get_random_word()
        self.the_good_answer = self.dictionary.data[self.random_word]
        self.answers.append(self.the_good_answer)
        while len(self.answers) != 4:
            new = self.dictionary.get_random_definition()
            if new not in self.answers:
                self.answers.append(new)
        random.shuffle(self.answers)



if __name__=="__main__":
    dictionary = Dictionary("dictionary_of_words.json")

    print("\nA random word: ",dictionary.get_random_word())
    print("A random definition: ",dictionary.get_random_definition())

    dictionary.add_word("foo","bar")
    