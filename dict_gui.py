from tkinter import *
from tkinter.ttk import Radiobutton
from tkinter import messagebox
from dict_logic import Dictionary, Quiz, Plot

class GUI(Tk):
    """ A szótár megjelenítéséért felelős osztály."""
    def __init__(self, dictionary=Dictionary):
        super().__init__()
        self.dictionary = dictionary
        self.title("My dictionary")
        self.configure(bg="#33cccc")
        self.geometry("520x820")
        self.widgets()

    def widgets(self):
        """Létrehozza a szükséges widgeteket."""
        self.label2 = Label(self, text = "DICTIONARY ", font="Times 18 bold", bg="#33cccc")
        self.label2.grid(row = 1, column = 0, sticky = W, padx = 5)

        self.var = StringVar()
        self.var.set("Please enter a word")
        self.text_entry = Entry(self, textvariable=self.var,width = 25, font="Times 15 bold")
        self.text_entry.grid(row = 2, column = 0, sticky = W, pady=10, padx = 10)
        self.text_entry.bind("<Button-1>", self.reset)

        self.random_button = Button(self, text="RANDOM",width = 10, command = self.get_random)
        self.random_button.grid(row=3,column=0,sticky=W, padx = 10, pady=10)

        self.button1 = Button(self, text= "SEARCH", width = 10, command = self.search)
        self.button1.grid(row=4, column = 0, sticky = W, padx = 10)
        self.bind('<Return>', self.search)

        self.label3 = Label(self, text ="\nDefinition: ", font="Times 18 bold", bg="#33cccc")
        self.label3.grid(row= 5, column=0, sticky = W)

        self.output = Text(self, width=25, height=6, wrap=WORD, font="Times 15 bold")
        self.output.grid(row=6, column=0, sticky = W, pady=20, padx = 10)

        Label(self, text ="You can add new words here", bg="#33cccc", font="Times 15 bold").grid(row = 7, column =0, sticky = W, padx = 10, pady=10)
        Label(self, text ="Word: ", bg="#33cccc", font="Times 15 bold").grid(row = 8, column =0, sticky = W, padx = 10)
        self.text1 = Text(self, width = 30, height=1)
        self.text1.grid(row = 9, column =0, sticky = W, padx = 10, pady=10)
        Label(self, text ="Definition: ", bg="#33cccc", font="Times 15 bold").grid(row = 10, column =0, sticky = W, padx = 10)
        self.text2 = Text(self, width = 30, height =6)
        self.text2.grid(row = 11, column= 0, sticky = W, padx = 10, pady=10)

        add_button = Button(self, text="ADD", command = self.add_new)
        add_button.grid(row = 12, column =0, sticky = W, padx = 10)

        Button(self, text="LET'S TAKE A QUIZ!",command=self.play,fg="#1a1aff").grid(row=3, column=1, sticky = W, pady=5, padx = 10)

        self.stat_button = Button(self, text="SHOW MY STAT",command=self.stat)
        self.stat_button.grid(row=4, column=1, sticky = W, pady=5, padx = 10)

        self.exit_button = Button(self, text="EXIT", width = 10, command = self.exit)
        self.exit_button.grid(row=12,column=1,sticky=W, padx = 10, pady = 5)

    def search(self,*args):
        """Megkeresi a beírt szóhoz tartozó jelentést, és a SEARCH gomb megnyomása, vagy az enter billentyű lenyomása
        után ki is írja azt. Ha nincs olyan szó, akkor kiírja, hogy Sorry."""
        entered_text = self.text_entry.get()
        self.output.delete(0.0, END)
        try:
            definition = self.dictionary.data[entered_text]
        except:
            definition = "Sorry, there is no word like that."

        self.output.insert(END, definition)

    def exit(self):
        """Ezzel zárhatjuk be a programot, az EXIT gombhoz van hozzárendelve"""
        self.destroy()
    
    def get_random(self):
        """A szótár létező szavai közül kiválaszt random egyet, amelyet beilleszt az Entry-be."""
        self.text_entry.delete(0, 'end')
        Random = self.dictionary.get_random_word()
        self.text_entry.insert(0, Random)

    def reset(self,*args):
        """A Entry tartalmát törli, a bal egérkattintáshoz van bind-olva."""
        self.text_entry.delete(0, END)

    def add_new(self):
        """Kiolvassa a két szövegmezőbe beírt szót és definíciót, majd az ADD gomb megnyomása után
        hozzáadja a már létező json fájlhoz, így ezután ez a kérdés is megjelenhet a QUIZ-ben."""
        get_text1 = self.text1.get("1.0","end-1c")
        get_text2 = self.text2.get("1.0","end-1c")
        self.dictionary.add_word(get_text1,get_text2)
        self.text1.delete('1.0', 'end')
        self.text2.delete('1.0', 'end')

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
            plot1 = Plot(self.quiz1)
            plot1.make_plot()
        except:pass


class MakeQuiz(Toplevel):
    """ A QUIZ megjelenítő osztálya, amely egy felugró ablakban jelenik meg. """
    def __init__(self, master, quiz=Quiz):
        super().__init__(master)
        self.master = master
        self.title("QUIZ")
        self.geometry("800x250")
        self.quiz = quiz
        
    def check_answer(self):
        """Megnézi, hogy a kijelölt Radiobutton a jó válasz-e, ha igen növeli a pontszámot 1-gyel."""
        if self.var.get() == 1: 
            self.quiz.good += 1

    def make_the_widgets(self):
        "Létrehozza a Labeleket és a Radiobuttonokat a QUIZ-hez."
        Label(self, text=self.quiz.random_word, fg="blue", font="Times 15 bold").pack()
        self.var = IntVar()
        i=2 #Azért, hogy a rossz megoldásokat ne együttesen pipálja be
        for answer in self.quiz.answers:
            if answer == self.quiz.the_good_answer:
                button = Radiobutton(self, text=answer,variable=self.var, value=1)
            else: 
                i+=1
                button = Radiobutton(self, text=answer,variable=self.var, value=i)
            button.pack()

        self.label = Label(self,text= "YOUR POINTS:", fg="green", font="Times 12 bold").pack()
        self.points = Label(self,text=self.quiz.good, fg="green", font="Times 12 bold")
        self.points.pack()

        Button(self,text="NEXT", command=self.make_and_update).pack()
        Button(self,text="RESET", command=self.Reset).pack()
        Button(self, text= "EXIT THE QUIZ", command=self.exit).pack()
    
    
    def make_game(self):
        "Kezdetben ez a függvény hozza létre a Quiz-t, majd a NEXT gombbal a make_and_update függvény hívódik meg."
        self.quiz.answers = []
        self.quiz.make_quiz()
        self.make_the_widgets()

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
        messagebox.showinfo(title="EREDMÉNY",message="Az eredményed: "+ str(percentage) +"%")
        self.destroy()
        self.master.deiconify()

    def Reset(self):
        self.quiz.reset()
        self.points.config(text=self.quiz.good)

    
if __name__=="__main__":
    dictionary = Dictionary("dictionary_of_words.json")
    view = GUI(dictionary)
    view.mainloop()