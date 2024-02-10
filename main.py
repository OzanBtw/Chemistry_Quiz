from tkinter import *
import random
import time
import sys
import json
import os
import threading
from playsound import playsound
import source_renew

if source_renew.renew() == False:
    sys.exit()

#General setup for tkinter
window = Tk()
window.geometry("960x720")
window.title("Kimya İsim Oyunu")
icon = PhotoImage(file='Stcikman.png')
window.iconphoto(True, icon)


#import source
with open('source.json', 'r') as f:
    name_list = json.load(f)

#music
def music():
    while True:
        playsound("sounds/Vitality_decreased.mp3")


thread = threading.Thread(target=music, daemon=True)

#class and functions
class Game:

    def __init__(self, fonts, color_list, name_list):
        self.fonts = fonts
        self.color_list = color_list

        self.game = False
        self.modes = ['All', 'Compounds', 'Elements', 'Ions']


        #text
        self.v_panel = StringVar()
        self.panel = Label(window, font=fonts['number'], bg=color_list[0], textvariable=self.v_panel)
        self.v_score = StringVar()
        self.text_score = Label(window, font=fonts['guess'], bg=color_list[0], textvariable=self.v_score)
        self.score = 0
        
        self.name_list = name_list

        self.text_info = Label(window, text=f"Info: There are total of {len(self.name_list['All']['formula'])} Questions!\n\nElement Example: Oksijen => O_a | Fe_m => Demir\nIon Example: OH_-1 => Hidroksit\nCompound Example: HCl => Tuz Ruhu\n\n*Büyük-küçük harf, boşluk önemli değil!\n\nMistakes are not acceptable :)\nGL", font=fonts['info'], bg=color_list[2])
        self.text_info.pack(pady='100', side=BOTTOM, anchor="n")

        self.buttonStart = Button(window, text="Start!", command=lambda: GameStart(), width=8, height=2, font=fonts['button1'])
        self.buttonStart.pack(padx='5', pady='50', side=LEFT, anchor="e")

        self.buttonMode_text = StringVar()
        self.buttonMode_text.set(self.modes[0])
        self.buttonMode = Button(window, textvariable=self.buttonMode_text, command=lambda: changeMode(), width=8, height=2, font=fonts['button2'])
        self.buttonMode.pack(padx='10', pady='50', side=RIGHT, anchor="w")

    def game_reset(self):
        self.game = True
        self.score = 0
        self.names = self.name_list[f'{self.buttonMode_text.get()}']['formula'].copy()
        self.score_max = len(self.names)

    def generate(self):
        if len(self.names) == 0:
            guess.delete(0, END)
            game_time = abs(round(round(self.time - time.time()) / 60, 2))
            self.score = f"PERCEFT RUN! | Time: {game_time} minutes!"
            self.game = False
            
            guess.pack_forget()
            self.panel.pack_forget()

            self.buttonStart.pack_forget()
            self.buttonMode.pack_forget()
            
            self.buttonStart.pack(padx='5', pady='50', side=LEFT, anchor="e")
            self.buttonMode.pack(padx='10', pady='50', side=RIGHT, anchor="w")
            return
        
        n = random.choice(self.names)
        self.names.remove(n)

        if bool(random.getrandbits(1)): # showing root
            index = self.name_list[f'{self.buttonMode_text.get()}']['formula'].index(n)
            self.question = n
            self.answer = self.name_list[f'{self.buttonMode_text.get()}']['names'][index]
        else:
            index = self.name_list[f'{self.buttonMode_text.get()}']['formula'].index(n)
            self.question = self.name_list[f'{self.buttonMode_text.get()}']['names'][index]
            self.answer = n


    def update(self):
        cache = f"{self.question}"
        self.v_panel.set(cache)
        self.v_score.set(self.score)

        
def countdown():
    wait = 0.2
    v = StringVar()
    count_n = 3
    count = Label(window, text=str(count_n), font=fonts['number'], bg=color_list[0], textvariable=v)
    count.pack(pady='30', side= TOP, anchor="center")
    v.set(str(count_n))

    for i in range(2):
        window.update()
        time.sleep(wait)
        count_n -= 1
        v.set(str(count_n))
    
    window.update()
    time.sleep(wait)
    count.pack_forget()

def control(event):
    if game.game:
        if str(game.answer.replace(' ','').replace('_', '')).lower() == str(guess.get().replace(' ','').replace('_', '')).lower():
            playsound('sounds/correct.mp3', False)
            game.score += 1
            game.generate()
            game.update()
            guess.delete(0, END)
        
        elif str(guess.get().replace(' ','').replace('_', '')).lower() == "":
            pass

        else:
            playsound("sounds/fail.mp3", False)
            game.game = False
            game_time = abs(round(round(game.time - time.time()) / 60, 2))
            game.v_score.set(f"Q:{game.question}\n+Ans:{game.answer}\n\n-P_Ans:{str(guess.get())}\nScore:{game.score}/{game.score_max} | Time: {game_time} minutes!")
            guess.delete(0, END)
            guess.pack_forget()

            game.panel.pack_forget()
            game.buttonStart.pack_forget()
            game.buttonMode.pack_forget()

            game.buttonStart.pack(padx='5', pady='50', side=LEFT, anchor="e")
            game.buttonMode.pack(padx='10', pady='50', side=RIGHT, anchor="w")
       
        window.update()
            
def changeMode():
    cache = game.modes.index(game.buttonMode_text.get()) + 1
    if cache >= len(game.modes):
        cache = 0
    game.buttonMode_text.set(game.modes[cache])

def GameStart():
    game.game_reset()
    game.buttonStart.pack_forget()
    game.buttonMode.pack_forget()

    game.text_info.pack_forget()

    countdown()
    guess.pack(pady='10', side= BOTTOM, anchor="n")

    game.text_score.pack(pady='45', side= TOP, anchor="center")
    game.panel.pack(pady='45', side= TOP, anchor="center")

    game.generate()
    game.update()
    game.time = time.time()
    window.update()






# fonts
fonts = {"title": ('Verdana', 40), "number": ('Verdana', 60), "guess": ('Verdana', 40), "score": ('Verdana', 50), "button1": ('Verdana', 45), "info": ('Verdana', 20), "button2": ('Verdana', 20)}
color_list = ['#0B2B40', '#30A5BF', '#185359', '#F2BE22', '#A6874E']

#texts
text_title = Label(window, text="Kimya İsim Oyunu", font=fonts['title'], bg=color_list[0]).pack(pady='20', side= TOP, anchor="n")


#input

guess = Entry(window,width=30, font=fonts['guess'])

#start
window.configure(bg=color_list[0])

game = Game(fonts, color_list, name_list)

window.bind('<Return>', control)
window.bind('<Escape>', sys.exit)
window.resizable(width=True, height=True)
thread.start()
window.mainloop()

