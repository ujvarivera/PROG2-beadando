from dict_logic import Dictionary
from dict_gui import GUI

if __name__=="__main__":
    dictionary = Dictionary("dictionary_of_words.json")
    view = GUI(dictionary)
    view.mainloop()