import tkinter as tk
from tkinter import ttk
import game_process

result = -1


class ZelMainMenu:
    def __init__(self, res=0) -> None:
        self.result = res
        self.root = tk.Tk()
        self.root.geometry('800x800')
        self.root.title('Zelda Menu')

        self.label = tk.Label(self.root, text='Zelda!', font=('Arial', 30), bg='lightgreen')
        self.label.pack(pady=100)

        self.button_register = tk.Button(self.root, text="Register", font=('Arial', 20), command=self.registration)
        self.button_register.place(relx=0.1, y=50)

        self.button_game = tk.Button(self.root, text="Start game", font=('Arial', 20), command=self.start_game)
        self.button_game.pack(pady=40)

        self.button_rankings = tk.Button(self.root, text="Rankings", font=('Arial', 20), command=self.rank_table_show)
        self.button_rankings.pack(pady=40)

        self.button_exit = tk.Button(self.root, text="Exit", font=('Arial', 20), command=self.cancel_menu)
        self.button_exit.pack(pady=40)

        self.root.mainloop()

    def rank_table_show(self):
        self.cancel_menu()
        RankingsTable()

    def registration(self):
        self.cancel_menu()
        RegWindow()

    def start_game(self):
        global result
        result = game_process.start_zel_game()
        self.cancel_menu()

    def cancel_menu(self):
        self.root.destroy()


class RegWindow:
    def __init__(self) -> None:
        self.warn_label = None
        self.user_data = None
        self.root = tk.Tk()
        self.root.geometry('500x700')
        self.root.title('Registration')

        self.user_data_l = []
        self.warnstate = False

        self.label = tk.Label(self.root, text='Registration', font=('Arial', 25), bg='orange')
        self.label.pack(pady=50)

        self.name_label = tk.Label(self.root, text='Enter nickname', font=('Arial', 16))
        self.name_label.pack(pady=16)

        self.name_entry = tk.Entry(self.root, font=('Arial', 16))
        self.name_entry.pack(pady=5)

        self.email_label = tk.Label(self.root, text='Enter email', font=('Arial', 16))
        self.email_label.pack(pady=16)

        self.email_entry = tk.Entry(self.root, font=('Arial', 16))
        self.email_entry.pack(pady=5)

        self.password_label = tk.Label(self.root, text='Enter password', font=('Arial', 16))
        self.password_label.pack(pady=16)

        self.password_entry = tk.Entry(self.root, font=('Arial', 16))
        self.password_entry.pack(pady=5)

        self.register_button = tk.Button(self.root, text="Login or register", font=('Arial', 20), command=self.regClick)
        self.register_button.pack(pady=16)

        self.tomenu_button = tk.Button(self.root, text="Back to menu", font=('Arial', 20), command=self.to_menu)
        self.tomenu_button.pack(pady=16)

        self.root.mainloop()

    def to_menu(self):
        self.cancel_registration()
        ZelMainMenu()

    def cancel_registration(self):
        self.root.destroy()

    def regClick(self):
        self.user_data_l = [self.name_entry.get(), self.email_entry.get(), self.password_entry.get()]
        if self.warnstate and all([dat != '' for dat in self.user_data_l]):
            self.warn_label.destroy()
            self.warnstate = False

            self.user_data = tuple(self.user_data_l)
            print(self.user_data)

        elif all([dat != '' for dat in self.user_data_l]):
            self.user_data = tuple(self.user_data_l)
            print(self.user_data)

        else:
            if self.warnstate:
                pass
            else:
                self.warn_label = tk.Label(self.root, text="Error", font=('Arial', 16), bg='red')
                self.warn_label.pack(pady=10)
                self.warnstate = True


class RankingsTable:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.geometry('600x800')
        self.root.title('Rankings')

        self.label = tk.Label(self.root, text='Top players', font=('Arial', 25), bg='pink')
        self.label.pack(pady=50)

        self.table = ttk.Treeview(self.root, columns=('first', 'second', 'third'), show='headings')
        self.table.heading('first', text='hmm')
        self.table.heading('second', text='ok')
        self.table.heading('third', text='so?')
        self.table.pack(expand=True)

        self.player_data = (("1", "den", "12"), ("2", "opa", "14"), ("3", "ljdfgs", "123"))

        for i in range(len(self.player_data)):
            data = self.player_data[i]
            self.table.insert(parent='', index=i, values=data)

        self.button_tomenu = tk.Button(self.root, text="Back to menu", font=('Arial', 20), command=self.cancel_rankings)
        self.button_tomenu.pack(pady=20)

        self.root.mainloop()

    def to_menu(self):
        self.cancel_rankings()
        ZelMainMenu(result)

    def cancel_rankings(self):
        self.root.destroy()


ZelMainMenu()
if result != -1:
    ZelMainMenu(result)
