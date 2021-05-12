from tkinter import *
from tkinter.ttk import Radiobutton
from dict_logic import Dictionary, Quiz

class GUI(Tk):
    def __init__(self, dictionary=Dictionary):
        super().__init__()
        self.dictionary = dictionary

        self.title("My dictionary")
        self.configure(bg="black")
        self.geometry("500x900")

        #self.photo1 = PhotoImage(file = "giphy.gif")
        #self.PhotoLabel1 = Label(self, image=self.photo1, bg="black")
        #self.PhotoLabel1.grid(row = 0, column = 0, sticky = W)

        self.label2 = Label(self, text = "Enter the word you would like a definition for: ", fg="white", font="Times 18 bold", bg = "black")
        self.label2.grid(row = 1, column = 0, sticky = W)

        self.var = StringVar()
        self.var.set("Please enter a word")
        self.text_entry = Entry(self, textvariable=self.var,width = 30, fg="white", font="Times 18 bold", bg = "black")
        self.text_entry.grid(row = 2, column = 0, sticky = W)
        self.text_entry.bind("<Button-1>", self.reset)

        self.button1 = Button(self, text= "SEARCH", fg= "white", bg ="black", width = 10, command = self.search)
        self.button1.grid(row=3, column = 0, sticky = W)
        self.bind('<Return>', self.search)

        self.label3 = Label(self, text ="\nDefinition: ", fg= "white", bg ="black", font="Times 18 bold")
        self.label3.grid(row= 4, column=0, sticky = W)

        self.output = Text(self, width=40, height=6, wrap=WORD, font="Times 18 bold")
        self.output.grid(row=5, column=0, sticky = W)

        self.exit_button = Button(self, text="EXIT", bg="black", fg= "white",width = 10, command = self.exit)
        self.exit_button.grid(row=6,column=0,sticky=W)

        self.random_button = Button(self, text="RANDOM",bg="black", fg= "white",width = 10, command = self.get_random)
        self.random_button.grid(row=7,column=0,sticky=W)
    
        Label(self, text ="You can add new words here").grid(row = 8, column =0)
        Label(self, text ="Word: ").grid(row = 9, column =0)
        self.text1 = Text(self, width = 15, height=1)
        self.text1.grid(row = 10, column =0)
        Label(self, text ="Definition: ").grid(row = 11, column =0)
        self.text2 = Text(self, width = 15, height =6)
        self.text2.grid(row = 12, column= 0)
        add_button = Button(self, text="ADD", command = self.add_new)
        add_button.grid(row = 13, column =0)

        Button(self, text="LET'S PLAY",command=self.play).grid(row=14, column=0)


    def search(self,*args):
        entered_text = self.text_entry.get()
        self.output.delete(0.0, END)
        try:
            definition = self.dictionary.data[entered_text]
        except:
            definition = "Sorry, there is no word like that."

        self.output.insert(END, definition)

    def exit(self):
        self.destroy()
    
    def get_random(self):
        self.text_entry.delete(0, 'end')
        Random = self.dictionary.get_random_word()
        self.text_entry.insert(0, Random)

    def reset(self,*args):
        self.text_entry.delete(0, END)

    def add_new(self):
        get_text1 = self.text1.get("1.0","end-1c")
        get_text2 = self.text2.get("1.0","end-1c")
        self.dictionary.add_word(get_text1,get_text2)
        self.text1.delete('1.0', 'end')
        self.text2.delete('1.0', 'end')

    def play(self):
        quiz = MakeQuiz(self,Quiz(self.dictionary))
        quiz.make_game()


class MakeQuiz(Toplevel):
    def __init__(self, master, quiz=Quiz):
        super().__init__(master)

        self.title("QUIZ")
        self.geometry("800x300")
        self.quiz = quiz
        self.radiobutton = None
        self.radiobuttons = []
        self.only_once = True #Azért, hogy ne kapjunk több pontot ha többször kattintunk a jó megoldásra,
        #vagy ha a jó után a rosszat jelöljük meg 

    def select(self):
        if self.only_once:
            self.radiobutton = self.var.get()
            self.check_answer()
        self.only_once = False


    def check_answer(self):
        if self.radiobutton == 1: 
            self.quiz.good += 1
        else: 
            self.quiz.bad += 1
            
    def make_the_buttons(self):
        Label(self, text=self.quiz.random_word, fg="red").pack()

        self.var = IntVar()
        i=2 #Azért, hogy a rossz megoldásokat ne együttesen pipálja be
        for answer in self.quiz.answers:
            i+=1
            if answer == self.quiz.the_good_answer:
                button = Radiobutton(self, text=answer,variable=self.var, value=1, command = self.select)
            else: 
                button = Radiobutton(self, text=answer,variable=self.var, value=i, command = self.select)
            button.pack()
            self.radiobuttons.append(button)
    
    def make_game(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.quiz.answers = []
        self.radiobutton = None
        self.quiz.make_quiz()

        self.make_the_buttons()
        self.label = Label(self,text= "YOUR POINTS:").pack()
        self.points = Label(self,text=self.quiz.good).pack()

        Button(self,text="NEXT", command=self.make_and_update).pack()
        Button(self, text= "EXIT THE QUIZ", command=self.exit).pack()

    def make_and_update(self):
        self.only_once = True
        self.make_game()
        self.check_answer()
            
           
    def exit(self):
        self.destroy()


if __name__=="__main__":
    dictionary = Dictionary("dictionary_of_words.json")
    view = GUI(dictionary)
    view.mainloop()