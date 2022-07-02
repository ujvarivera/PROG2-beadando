import os
import json
import random
import matplotlib.pyplot as plt

class Dictionary:
    """A szótár logikai osztálya."""
    def __init__(self, filename) -> None:
        self.filename = filename
        self.not_existing_words = [] #Azoknak a szavaknak a listája, amelyeket nem tartalmaz a szotar, de megprobaltad
        if os.path.exists(filename):
            with open(filename,"r") as f:
                self.data = json.load(f)

    def get_random_word(self): 
        """Visszaad egy random szót a már létező json fájlból."""
        return random.choice(list(self.data.keys()))

    def has_word(self,word:str)->bool:
        """Visszaadja, hogy a beírt szó szerepel-e már a szótárban"""
        return word in self.data.keys()

    def add_word(self,word:str,definition:str)-> None:
        """Hozzáadja a megadott szót és definíciót a json fájlhoz. 
        Ha már létezik az a szó a szótárban, Exceptiont dob."""
        if self.has_word(word):
            raise Exception("A megadott szó már szerepel a szótárban!")

        if len(word) == 0 or len(definition) == 0:
            raise Exception("Egyik mező sem maradhat üres!")

        for char in word:
            if char in "123456789#&@<>~ˇ^~˘°˛+%?Ł$ßł´˝¨¸":
                raise Exception("Invalid Word")
        for c in definition:
            if c in "123456789#&@<>~ˇ^~˘°˛+%?Ł$ßł´˝¨¸":
                raise Exception("Invalid Definition")      
            
        self.data[word] = definition

    def save_words(self):
        with open(self.filename, "w") as f:
            f.write(json.dumps(self.data))     
        
        
class Quiz:
    """A QUIZ logikai osztálya."""
    def __init__(self, dictionary:Dictionary)-> None:
        self.random_word = None #random kiválasztott szó
        self.the_good_answer = None # a random szó tényleges jelentése
        self.answers = [] # 3 random definíciot tartalmaz, és a jó válaszhoz tartozót 
        self.good = 0 # jó válaszaid számát tárolja, azaz a pontjaid
        self.questions = 0 # feltett kérdések számát tárolja
        self.dictionary = dictionary

    
    def result(self):
        """Megmutatja az eredményed az EXIT gomb megnyomása után, hogy hány százalékot értél el."""
        try:
            return int((self.good/self.questions)*100)
        except ZeroDivisionError: pass

    def make_quiz(self)-> None:
        """Kiválaszt egy random szót, és 4 válaszlehetőséget, melyek közül csak az egyik igaz.
        Ezeket megkeveri, hogy random sorrendben jelenjenek meg. Ha a json fájl nem tartalmaz legalább 
        4 szót, kapunk egy Exceptiont, mivel ismétlődéseket nem szeretnénk látni."""
        self.random_word = self.dictionary.get_random_word()
        self.the_good_answer = self.dictionary.data[self.random_word]
        self.answers.append(self.the_good_answer)
        if len(self.dictionary.data) < 4: raise Exception("Dict must have at least 4 elements before starting QUIZ.")
        while len(self.answers) != 4:
            word = self.dictionary.get_random_word()
            if self.dictionary.data[word] not in self.answers:
                self.answers.append(self.dictionary.data[word])
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
        x = ["bad answers", "good answers", "number of questions"]
        y = [(self.quiz.questions-self.quiz.good), self.quiz.good, self.quiz.questions]

        fig, ax = plt.subplots()
        ax.bar(x, y)
        ax.set_title('Your answers')
        fig.show()


if __name__=="__main__":
    dictionary = Dictionary("dictionary_of_words.json")
    print("\nA random word: ",dictionary.get_random_word())
    dictionary.add_word("foo","bar")
    