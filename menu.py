from pygame import mixer
from tkinter import *
from PIL import ImageTk, Image
import clines

root = Tk()
root.title("Color Lines")
mixer.init()
mixer.music.load('assets/MenuSound.mp3')
mixer.music.play(loops=-1)
mixer.music.set_volume(0.1)

def Main_menu():
    img = Image.open('assets/menuu.jpeg')
    width = 900
    ratio = (width / float(img.size[0]))
    height = int((float(img.size[1]) * float(ratio)))
    imag = img.resize((width, height))
    background = ImageTk.PhotoImage(imag)
    bg = Label(root, image=background)
    bg.pack()
    root.eval('tk::PlaceWindow . center')

    button_image_start = PhotoImage(file='assets/button111.png')
    button_image_settings = PhotoImage(file='assets/button222.png')
    button_image_exit = PhotoImage(file='assets/button333.png')
    button_image_score = PhotoImage(file='assets/button222.png')

    button_play = Button(root, text = 'Начать Игру', fg='#ffffff', font='Times 24', border="0", image = button_image_start, compound='center', command= lambda: clines.Auth(root))
    button_settings = Button(root, text = 'Настройки', fg='#ffffff', font='Times 24', border="0", image = button_image_settings, compound='center')
    button_score = Button(root, text = 'Счёт: ', fg='#ffffff', font='Times 24',  border="0", image = button_image_score, compound='center')
    button_exit = Button(root, text = ' Выход', font='Times 24', border="0", image = button_image_exit, compound='center', command = root.destroy )

    button_play.place(x=650, y=250)
    button_settings.place(x=650, y=400)
    button_score.place(x=50, y=50)
    button_exit.place(x=650, y=550)
    root.mainloop()

Main_menu()

