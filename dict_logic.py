import os
import json
import random
import matplotlib.pyplot as plt

class Dictionary:
    """A szótár logikai osztálya."""
    def __init__(self, filename) -> None:
        self.filename = filename
        if os.path.exists(filename):
            with open(filename,"r") as f:
                self.data = json.load(f)

    def get_random_word(self): 
        """Visszaad egy random szót a már létező json fájlból."""
        return random.choice(list(self.data.keys()))

    def get_random_definition(self):
        """Visszaad egy random definíciót a már létező json fájlból."""
        return random.choice(list(self.data.values()))

    def has_word(self,word:str)->bool:
        """Visszaadja, hogy a beírt szó szerepel-e már a szótárban"""
        return word in self.data.keys()

    def is_empty(self, text:str)-> bool: 
        """Visszaadja, hogy írtunk-e a mezőbe szöveget, vagy sem."""
        return len(text) == 0

    def add_word(self,word:str,definition:str)-> None:
        """Hozzáadja a megadott szót és definíciót a json fájlhoz. 
        Ha már létezik az a szó a szótárban, Exceptiont dob."""
        if self.has_word(word):
            raise Exception("A megadott szó már szerepel a szótárban!")

        if self.is_empty(word) or self.is_empty(definition):
            raise Exception("Egyik mező sem maradhat üres!")

        new_word = {word:definition}
        self.data.update(new_word)
        with open(self.filename, "w") as f:
            f.write(json.dumps(self.data))
        

class Quiz:
    """A QUIZ logikai osztálya."""
    def __init__(self, dictionary:Dictionary)-> None:
        self.dictionary = dictionary
        self.random_word = None #random kiválasztott szó
        self.the_good_answer = None # a random szó tényleges jelentése
        self.answers = [] # 3 random definíciot tartalmaz, és a jó válaszhoz tartozót 
        self.good = 0 # jó válaszaid számát tárolja, azaz a pontjaid
        self.questions = 0 # feltett kérdések számát tárolja

    def shuffle_elements(self)-> None:
        """Megkeveri a json elemeit"""
        data_list = list(self.dictionary.data.items())
        random.shuffle(data_list)
        data_dict = dict(data_list)
        with open(self.dictionary.filename, "w") as f:
            f.write(json.dumps(data_dict))
    
    def result(self):
        """Megmutatja az eredményed az EXIT gomb megnyomása után, hogy hány százalékot értél el."""
        try:
            return int((self.good/self.questions)*100)
        except ZeroDivisionError: pass

    def make_quiz(self)-> None:
        """Megkeveri a JSON elemeit, kiválaszt egy random szót, és 4 válaszlehetőséget, melyek közül csak az egyik igaz.
        Majd ezeket is megkeveri, hogy random sorrendben jelenjenek meg. Ha a json fájl nem tartalmaz legalább 
        4 szót, kapunk egy Exceptiont, mivel ismétlődéseket nem szeretnénk látni."""
        self.shuffle_elements()
        self.random_word = self.dictionary.get_random_word()
        self.the_good_answer = self.dictionary.data[self.random_word]
        self.answers.append(self.the_good_answer)
        if len(self.dictionary.data) < 4: raise Exception("Dict must have at least 4 elements before starting QUIZ.")
        while len(self.answers) != 4:
            new = self.dictionary.get_random_definition()
            if new not in self.answers:
                self.answers.append(new)
        random.shuffle(self.answers)


    def reset(self)-> None:
        """Visszaállítja a pontszámot nullára, és a kérdések számlálója is újra indul."""
        self.questions = 0
        self.good = 0


class Plot:
    """A QUIZ-ben elért aktuális jó-rossz válaszok arányát mutatja meg."""
    def __init__(self, quiz = Quiz)-> None:
        self.quiz = quiz

    def make_plot(self)-> None:
        """Csinál egy plotot."""
        plt.cla()
        plt.title("Your answers")
        x = ["bad answers", "good answers", "number of questions"]
        y = [(self.quiz.questions-self.quiz.good), self.quiz.good, self.quiz.questions]
        plt.bar(x,y)
        plt.show()



if __name__=="__main__":
    dictionary = Dictionary("dictionary_of_words.json")

    print("\nA random word: ",dictionary.get_random_word())
    print("A random definition: ",dictionary.get_random_definition())

    dictionary.add_word("foo","bar")
    