import random
import tkinter as tk

w = 900
h = 400

numbers_dict = {
                '0' : 'null', '1' : 'En', '2' : 'To', '3' : 'Tre', '4' : 'Fire', '5' : 'Fem', '6' : 'Seks', '7' : 'Syv',
                '8' : 'Åtte', '9' : 'Ni', '10' : 'Ti', '11' : 'Elleve', '12' : 'Tolv', '13' : 'Tretten', '14' : 'Fjorten',
                '15' : 'Femten', '16' : 'Seksten', '17' : 'Sytten', '18' : 'Atten', '19' : 'Nitten', '20' : 'Tjue',
                '21' : 'Tjueen', '22' : 'Tjueto', '23' : 'Tjuetre', '24' : 'Tjuefire', '25' : 'Tjuefem', '26' : 'Tjueseks',
                '27' : 'Tjuesyv', '28' : 'Tjueåtte','29' : 'Tjueni','30' : 'Tretti', '31' : 'Trettien', '32' : 'Trettito',
                '33' : 'Trettitre', '34' : 'Trettifire', '35' : 'Trettifem', '36' : 'Trettiseks', '37' : 'Trettisyv',
                '38' : 'Trettiåtte', '39' : 'Trettini', '40' : 'Førti'
                }

class MathGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Addisjon Spill")
        self.master.geometry("900x400")

        self.create_widgets()

    def create_widgets(self):
        self.question_label = tk.Label(
            self.master, text="", font=("Helvetica", 20), pady=10
        )
        self.question_label.pack()

        self.answer_entry = tk.Entry(self.master, font=("Helvetica", 20))
        self.answer_entry.pack(pady=10)

        self.answer_entry.bind("<Return>", lambda event: self.check_answer())

        self.check_button = tk.Button(
            self.master, text="Sjekk svar", font=("Helvetica", 20), command=self.check_answer
        )
        self.check_button.pack(pady=10)

        self.result_label = tk.Label(
            self.master, text="", font=("Helvetica", 20), pady=10
        )
        self.result_label.pack()

        self.answer_entry.bind("<Return>", self.check_answer)

        self.master.bind("<Escape>", self.quit_game)

        self.play_again_button = tk.Button(
            self.master,
            text="Spill igjen",
            font=("Helvetica", 16),
            command=self.play_again,
        )
        self.play_again_button.pack(pady=10)

        self.quit_button = tk.Button(
            self.master, text="Avslutt", font=("Helvetica", 16), command=self.master.destroy
        )
        self.quit_button.pack(pady=10)

        self.generate_question()

    def generate_question(self):
        self.number1 = random.randint(0, 20)
        self.number2 = random.randint(0, 20)
        self.if_wrong = str(self.number1 + self.number2)

        text1 = str(self.number1)
        text2 = str(self.number2)

        self.question_label.config(
            text=f"Hva er {self.number1} ({numbers_dict.get(text1)}) + {self.number2} ({numbers_dict.get(text2)})?"
        )

    def check_answer(self, event = None):
        text1 = str(self.number1)
        text2 = str(self.number2)
        answer = self.answer_entry.get().strip()

        if int(answer) == self.number1 + self.number2:
            self.result_label.config(
                text=f"Riktig svar! {self.number1} ({numbers_dict.get(text1)}) + {self.number2} ({numbers_dict.get(text2)}) = {answer} ({numbers_dict.get(self.if_wrong)}) " 
            )
            self.play_again_button.config(state=tk.NORMAL)
        else:
            self.result_label.config(
                text=f"Feil svar. Svaret er {self.number1 + self.number2} ({numbers_dict.get(self.if_wrong)}) "
            )

    def play_again(self):
        self.number1 = random.randint(0, 20)
        self.number2 = random.randint(0, 20)
        self.answer_entry.delete(0, tk.END)
        self.result_label.config(text="")
        self.answer_entry.focus()
        self.generate_question()
    
    def quit_game(self, event):
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MathGame(root)

    screen_width = root.winfo_screenwidth()  # Width of the screen
    screen_height = root.winfo_screenheight() # Height of the screen
    
    # Calculate Starting X and Y coordinates for Window
    x = (screen_width/2) - (w/2)
    y = (screen_height/2) - (h/2)
    
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.mainloop()
