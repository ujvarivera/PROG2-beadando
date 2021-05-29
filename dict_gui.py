from tkinter import *
from tkinter.ttk import Combobox, Radiobutton
from tkinter import messagebox, scrolledtext
from dict_logic import Dictionary, Quiz

class GUI(Tk):
    """ A szótár megjelenítéséért felelős osztály."""
    def __init__(self, dictionary=Dictionary):
        super().__init__()
        self.dictionary = dictionary
        self.title("My dictionary")
        self.configure(bg="#33cccc")
        self.__widgets()

    def __widgets(self):
        """Létrehozza a szükséges widgeteket."""
        Label(self, text = "DICTIONARY ", font="Times 18 bold", bg="#33cccc").grid(row = 1, column = 0, sticky = W, padx = 5)

        self.entryvar = StringVar()
        self.entryvar.set("Please enter a word")
        text_entry = Combobox(self, textvariable=self.entryvar,width = 25, font="Times 15 bold")
        text_entry.grid(row = 2, column = 0, sticky = W, pady=10, padx = 10)
        text_entry.bind("<Button-1>", self.reset)
        text_entry['values'] = [word for word in self.dictionary.data.keys()]
        text_entry.bind('<<ComboboxSelected>>', self.search)

        Button(self, text="RANDOM WORD",width = 20, command = self.get_random).grid(row=3,column=0,sticky=W, padx = 10, pady=10)

        Button(self, text= "SEARCH", width = 20, command = self.search).grid(row=4, column = 0, sticky = W, padx = 10)
        self.bind('<Return>', self.search)

        Label(self, text ="\nDefinition: ", font="Times 18 bold", bg="#33cccc").grid(row= 5, column=0, sticky = W)

        self.output = scrolledtext.ScrolledText(self, width=25, height=6, wrap=WORD, font="Times 15 bold")
        self.output.grid(row=6, column=0, sticky = W, pady=20, padx = 10)
        self.output.config(state=DISABLED) #hogy ne lehessen beleírni

        self.add_update_var = StringVar()
        self.add_update_var.set('')
        self.add_update_button = Button(self, textvariable=self.add_update_var,width = 35, command = self.NewWords)
        self.add_update_button.grid(row = 12, column =0, sticky = W, padx = 10)
        self.add_update_button.config(state=DISABLED)
        Button(self, text="LET'S TAKE A QUIZ!",width = 15,fg="#1a1aff",command=self.play).grid(row=3, column=1, sticky = W, pady=5, padx = 10)

        self.statbutton = Button(self, text="PROBABILITY OF OCCURRENCE",width = 25,command=self.stat)
        self.statbutton.grid(row=4, column=1, sticky = W, pady=5, padx = 10)
        self.statbutton.config(state=DISABLED)

        Button(self, text="EXIT", width = 15, command = self.exit).grid(row=12,column=1,sticky=W, padx = 10, pady = 5)

    def search(self,*args):
        """Megkeresi a beírt szóhoz tartozó jelentést, és a SEARCH gomb megnyomása, vagy az enter billentyű lenyomása
        után ki is írja azt. Ha nincs olyan szó, akkor kiírja, hogy Sorry."""
        self.output.config(state=NORMAL)
        entered_text = self.entryvar.get()
        self.output.delete(0.0, END)
        try:
            definition = self.dictionary.data[entered_text]
            self.dictionary.word_exist= True
        except:
            if entered_text not in self.dictionary.not_existing_words:
                self.dictionary.not_existing_words.append(entered_text)
            definition = "Sorry, there is no word like that."
            self.dictionary.word_exist= False

        self.output.insert(END, definition)
        self.output.config(state=DISABLED)

        self.add_update_button.config(state=NORMAL)
        if self.dictionary.word_exist == False:
            self.add_update_var.set("ADD")
        else: self.add_update_var.set("UPDATE")


    def exit(self):
        """Ezzel zárhatjuk be a programot, az EXIT gombhoz van hozzárendelve"""
        self.dictionary.save_words()
        self.destroy()
    
    def get_random(self):
        """A szótár létező szavai közül kiválaszt random egyet, amelyet beilleszt az Entry-be."""
        self.entryvar.set('')
        Random = self.dictionary.get_random_word()
        self.entryvar.set(Random)
        self.search()

    def reset(self,*args):
        """A Entry tartalmát törli, a bal egérkattintáshoz van bind-olva."""
        self.entryvar.set('')

    def play(self):
        """A LET'S PLAY gombhoz van hozzárendelve, felugró ablakban megjeleníti a QUIZ-t"""
        self.quiz1 = Quiz(self.dictionary)
        playQuiz = MakeQuiz(self,self.quiz1)
        playQuiz.make_game()
        self.withdraw() #eltűnteti a főablakot, amíg a QUIZ fut

    def stat(self):
        """Az aktuális statisztikát készíti el a matplotlib segítségével, a SHOW MY STAT gomb megnyomása után.
        Ha nem játszottunk még a QUIZ-zel, akkor nem jelenik meg semmi. """
        try:
            self.quiz1.make_plot()
        except:pass

    def NewWords(self):
        AddWords(self,self.dictionary)


class MakeQuiz(Toplevel):
    """ A QUIZ megjelenítő osztálya, amely egy felugró ablakban jelenik meg. """
    def __init__(self, master, quiz=Quiz):
        super().__init__(master)
        self.master = master
        self.title("QUIZ")
        self.geometry("800x300")
        self.quiz = quiz
        
    def check_answer(self):
        """Megnézi, hogy a kijelölt Radiobutton a jó válasz-e, ha igen növeli a pontszámot 1-gyel."""
        if self.radiobutton_var.get() == 1: 
            self.quiz.good += 1

    def __make_the_widgets(self):
        "Létrehozza a Labeleket és a Radiobuttonokat a QUIZ-hez."
        Label(self, text=self.quiz.random_word, fg="blue", font="Times 15 bold").pack()
        self.radiobutton_var = IntVar()
        i=2 #Azért, hogy a rossz megoldásokat ne együttesen pipálja be
        for answer in self.quiz.answers:
            if answer == self.quiz.the_good_answer:
                button = Radiobutton(self, text=answer,variable=self.radiobutton_var, value=1)
            else: 
                i+=1
                button = Radiobutton(self, text=answer,variable=self.radiobutton_var, value=i)
            button.pack()

        self.points_var = IntVar()
        self.points_var.set(self.quiz.good)
        Label(self,text= "YOUR POINTS:", fg="green", font="Times 12 bold").pack()
        points_label = Label(self,textvariable=self.points_var, fg="green", font="Times 12 bold")
        points_label.pack()
        Button(self,text="NEXT", command=self.make_and_update).pack()
        Button(self,text="RESET", command=self.Reset).pack()
        Button(self, text= "EXIT THE QUIZ", command=self.exit).pack()
    
    def make_game(self):
        "Kezdetben ez a függvény hozza létre a Quiz-t, majd a NEXT gombbal a make_and_update függvény hívódik meg."
        self.quiz.answers = []
        self.quiz.make_quiz()
        self.__make_the_widgets()

    def make_and_update(self):
        "Az előző widgeteket törli, lecsekkolja, hogy jó-e az előző válasz, majd új QUIZ kérdést és válaszlehetőségeket ad. "
        for widget in self.winfo_children():
            widget.destroy()
        self.quiz.questions += 1
        self.check_answer()
        self.make_game()
                 
    def exit(self):
        """Az EXIT gombhoz van hozzárendelve, ezzel léphetünk ki a QUIZ-ből. Előtte megmutatja egy messageboxban,
        hány százalékot értél el. Valamint újra megnyitja a főablakot."""
        percentage = self.quiz.result()
        messagebox.showinfo(title="RESULT",message="Az eredményed: "+ str(percentage) +"%")
        self.master.statbutton.config(state=NORMAL)
        self.destroy()
        self.master.deiconify()

    def Reset(self):
        self.quiz.reset()
        self.points_var.set(self.quiz.good)

    
class AddWords(Toplevel):
    """ Új szavak - definíciok hozzáadása, új ablakban jelenik meg. """
    def __init__(self, master, dictionary:Dictionary):
        super().__init__(master)
        self.master = master
        self.dictionary = dictionary
        self.configure(bg="#33cccc")
        self.__add_word_widgets()

    def __add_word_widgets(self):
        Label(self, text ="Word: ", bg="#33cccc", font="Times 15 bold").grid(row = 2, column =0, sticky = W, padx = 10)

        self.text1 = Combobox(self, width = 30, height=1,textvariable=self.master.entryvar)
        self.text1.grid(row = 3, column =0, sticky = W, padx = 10, pady=10)
        if self.master.dictionary.word_exist == False:
            self.text1['values'] = [word for word in self.dictionary.not_existing_words]
        else: 
            self.text1['values'] = [word for word in self.dictionary.data.keys()]
            self.text1.bind('<<ComboboxSelected>>', self.search_def)

        Label(self, text ="Definition: ", bg="#33cccc", font="Times 15 bold").grid(row = 4, column =0, sticky = W, padx = 10)
        self.text2 = Text(self, width = 30, height =6, wrap=WORD)
        self.text2.grid(row = 5, column= 0, sticky = W, padx = 10, pady=10)

        if self.master.dictionary.word_exist == False:
            Button(self, text="ADD WORD", width = 33,command = self.add_new).grid(row = 6, column =0, sticky = W, padx = 10,  pady=10)
        else:
            Button(self, text="UPDATE DEFINITION", width = 33,command = self.update).grid(row = 7, column =0, sticky = W, padx = 10,  pady=10)
            self.text2.insert(END, self.dictionary.data[self.master.entryvar.get()])

        self.bind('<Return>', self.search_def)

    def add_new(self):
        """Kiolvassa a két szövegmezőbe beírt szót és definíciót, majd az ADD gomb megnyomása után
        hozzáadja a már létező json fájlhoz, így ezután ez a kérdés is megjelenhet a QUIZ-ben."""
        get_text1 = self.text1.get()
        get_text2 = self.text2.get("1.0","end-1c")
        self.dictionary.add_word(get_text1,get_text2)
        self.text1.set('')
        self.text2.delete('1.0', 'end')

        for word in self.dictionary.not_existing_words:
            if word in self.dictionary.data.keys():
                self.dictionary.not_existing_words.remove(word)
        self.text1['values'] = [word for word in self.dictionary.not_existing_words]

    def update(self):
        get_text1 = self.text1.get()
        get_text2 = self.text2.get("1.0","end-1c")

        self.master.dictionary.update_word(get_text1,get_text2)

        self.text1.set('')
        self.text2.delete('1.0', 'end')

    def search_def(self,*args):
        self.text2.delete(0.0, END)
        self.text2.insert(END, self.dictionary.data[self.master.entryvar.get()])
