import tkinter as tk
from tkinter import ttk
import game_process


class ZelMainMenu:
    def __init__(self, reg_name='Denis', result=135) -> None:
        self.reg_name = reg_name
        self.result = result

        self.root = tk.Tk()
        self.root.geometry('800x800')
        self.root.title('Zelda Menu')

        self.label = tk.Label(self.root, text='Zelda!', font=('Arial', 30), bg='lightgreen')
        self.label.pack(pady=100)

        self.button_register = tk.Button(self.root, text="Register", font=('Arial', 20), command=self.registration)
        self.button_register.place(relx=0.1, y=50)

        if reg_name != '':
            self.login_label = tk.Label(self.root, text=f'Logged in as {reg_name}', font=('Arial', 15), bg='pink')
            self.login_label.place(relx=0.1, y=130)
            if self.result != -1:
                self.result_label = tk.Label(self.root, text=f'Max result: {self.result}', font=('Arial', 12),
                                             bg='lightyellow')
                self.result_label.place(relx=0.1, y=160)
        else:
            self.login_label = tk.Label(self.root, text='Not logged in', font=('Arial', 15), bg='pink')
            self.login_label.place(relx=0.1, y=130)

        self.button_game = tk.Button(self.root, text="Start game", font=('Arial', 20), command=self.start_game)
        self.button_game.pack(pady=40)

        self.button_rankings = tk.Button(self.root, text="Rankings", font=('Arial', 20), command=self.rank_table_show)
        self.button_rankings.pack(pady=40)

        self.button_exit = tk.Button(self.root, text="Exit", font=('Arial', 20), command=self.cancel_menu)
        self.button_exit.pack(pady=40)

        self.root.mainloop()

    def rank_table_show(self):
        self.cancel_menu()
        RankingsTable(self.reg_name, self.result)

    def registration(self):
        self.cancel_menu()
        RegWindow(self.reg_name, self.result)

    def start_game(self):
        nickname = self.reg_name
        self.cancel_menu()
        ZelMainMenu(nickname, game_process.start_zel_game())

    def cancel_menu(self):
        self.root.destroy()


class RegWindow:
    def __init__(self, reg_name='', result=-1) -> None:
        self.warn_label = None
        self.user_data = None

        self.reg_name = reg_name
        self.result = result

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
        ZelMainMenu(self.reg_name, self.result)

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
    def __init__(self, reg_name='', result=-1) -> None:
        self.reg_name = reg_name
        self.result = result

        self.root = tk.Tk()
        self.root.geometry('600x800')
        self.root.title('Rankings')

        self.label = tk.Label(self.root, text='Top players', font=('Arial', 25), bg='pink')
        self.label.pack(pady=50)

        self.table = ttk.Treeview(self.root, columns=('first', 'second', 'third'), show='headings')
        self.table.heading('first', text='hmm')
        self.table.heading('second', text='ok')
        self.table.heading('third', text='so?')
        self.table.pack()

        self.player_data = 'JOhn,110;Egor,50;Egdfor,55'
        self.player_data = self.player_data.split(';')
        self.player_data = tuple(tuple(x.split(',')) for x in self.player_data)
        self.player_data = sorted(self.player_data, key=lambda x: -int(x[1]))

        for i in range(len(self.player_data)):
            show_data = (i + 1, self.player_data[i][0], self.player_data[i][1])
            self.table.insert(parent='', index=i, values=show_data)

        self.button_tomenu = tk.Button(self.root, text="Back to menu", font=('Arial', 20), command=self.to_menu)
        self.button_tomenu.pack(pady=20)

        self.root.mainloop()

    def to_menu(self):
        self.cancel_rankings()
        ZelMainMenu(self.reg_name, self.result)

    def cancel_rankings(self):
        self.root.destroy()


ZelMainMenu()
