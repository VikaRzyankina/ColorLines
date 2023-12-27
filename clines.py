from pygame import  mixer
from tkinter import *
from PIL import ImageTk, Image
import hashlib
import random
mixer.init()
mixer.music.load('assets/MenuSound.mp3')
mixer.music.play(loops=-1)
mixer.music.set_volume(0.1)

GAME_OVER = 'game_over'
SELECT = 'choice'
MOVE = 'move'

img = Image.open('assets/menuu.jpeg')
auth_bg = Image.open('assets/menu (2).jpeg')

class Main():
    def __init__(self):
        self.root = Tk()
        self.root.title("Color Lines")
        self.Main_menu()

    def Main_menu(self):
        imag = img.resize((900, 900))
        background = ImageTk.PhotoImage(imag, master = self.root)
        bg = Label( self.root, image=background)
        bg.pack()
        self.root.eval('tk::PlaceWindow . center')
        self.root.resizable(False,False)
        button_image_start = PhotoImage(file='assets/button111.png')
        button_image_exit = PhotoImage(file='assets/button333.png')
        button_image_score = PhotoImage(file='assets/button222.png')

        button_play = Button( self.root, text = 'Начать Игру', fg='#ffffff', font='Times 24', border="0", image = button_image_start, compound='center', command= lambda: Auth( self.root))

        button_score = Button( self.root, text = 'Рекорды ', fg='#ffffff', font='Times 24',  border="0", image = button_image_score, compound='center', command=self.table_records)
        button_exit = Button( self.root, text = ' Выход', font='Times 24', border="0", image = button_image_exit, compound='center', command =  self.root.destroy )

        button_play.place(x=650, y=250)

        button_score.place(x=650, y=400)
        button_exit.place(x=650, y=550)
        self.root.mainloop()

    def table_records(self):
        self.root.destroy()
        records_window = Tk()
        button_image_records = PhotoImage(master= records_window, file='assets/button333.png').subsample(1,2)
        button_image_back = PhotoImage(master= records_window, file='assets/button222.png').subsample(1,2)
        records_window.title("Color Lines")
        records_window.geometry('400x900')
        records_window.resizable(False,False)
        background = ImageTk.PhotoImage(auth_bg, master = records_window)
        bg = Label(records_window, image=background)
        bg.place(x=0, y=0, relwidth=1, relheight=1)
        count = 0
        with open('ScoreFile.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line == '':
                    break
                if count == 10:
                    break
                else:
                    readline_score = line[:-1].split(':', 2)
                    Label(records_window, text = readline_score, font='Times 24', border="0", image = button_image_records, compound='center').pack(pady= 3)
                    count += 1
        Button(records_window, text = 'Назад',font='Times 24', fg='#ffffff', border="0", image = button_image_back, compound='center', command= lambda:self.back_record(records_window)).place(x=80, y=800)
        records_window.eval('tk::PlaceWindow . center')
        records_window.mainloop()
    def back_record(self,records_window):
        records_window.destroy()
        Main()

class Auth:
    def __init__(self, menu):
        menu.destroy()
        open('File.txt', 'a').close()
        self.window = Tk()
        self.window.title("Color Lines")
        window = self.window
        window.geometry('500x500')
        button_image_auth = PhotoImage(file='assets/button222.png').subsample(1,2)
        self.imag = auth_bg.resize((500, 500))
        background = ImageTk.PhotoImage(self.imag)
        bg = Label(window, image=background)
        bg.place(x=0, y=0, relwidth=1, relheight=1)
        Button(window, font='Times 20', fg='#ffffff', compound='center', text="Регистрация", image =button_image_auth, command=self.register).pack(pady=20)
        Button(window, font='Times 20', fg='#ffffff', text="Вход", compound='center', image =button_image_auth, command=self.log_in).pack(pady=20)
        but = Button(window, text="Назад", font='Times 20', fg='#ffffff', compound='center', image =button_image_auth, command=lambda: self.back_command(False))
        but.pack(pady=20)
        window.eval('tk::PlaceWindow . center')
        self.window.mainloop()


    def back_command(self, key):
        if key == False:
            self.window.destroy()
            Main()
        else:
            Auth(self.auth_window)

    def window_entry(self, description, img):
        Label(self.auth_window, font='Times 20', border="0", text=description, image=img, compound='center').pack(pady=10)
        entry = Entry(self.auth_window, font='Times 20', width= 20, justify='center')
        entry.pack()
        return entry


    def select_auth(self, title, log, passw, command):
        self.window.destroy()
        self.auth_window = Tk()
        self.auth_window.title(title)
        wind = self.auth_window
        wind.geometry('500x500')
        button_image_auth = PhotoImage(file='assets/button222.png').subsample(1, 2)
        background = ImageTk.PhotoImage(self.imag, master= wind)
        bg = Label(self.auth_window, image=background)
        bg.place(x=0, y=0, relwidth=1, relheight=1)
        img = PhotoImage(file='assets/button333.png').zoom(5,1).subsample(4,2)
        self.login_user = self.window_entry(log,img)
        self.password_user = self.window_entry(passw,img)
        Button(wind, font='Times 20', border="0", compound='center', fg='#ffffff', text="Продолжить", image =button_image_auth, command=command).pack(pady=10)
        Button(wind, font='Times 20', border="0", compound='center', fg='#ffffff', text ='Назад', image =button_image_auth, command=lambda: self.back_command(True)).pack(pady=10)
        wind.eval('tk::PlaceWindow . center')
        self.auth_window.mainloop()
    def register(self):

        self.select_auth('Регистрация', 'Придумайте логин', 'Придумайте пароль', self.write_txt)
        self.auth_window.mainloop()

    def log_in(self):

        self.select_auth('Вход', 'Введите логин', 'Введите пароль', self.open_txt)
        self.auth_window.mainloop()
    def open_txt(self):
        str_user = self.login_user.get()
        not_found = True
        with open('File.txt', 'r') as f:
            read = f.readlines()
            password_sha = hashlib.sha1(str.encode(self.password_user.get())).hexdigest()
            for i in range(1, len(read), 2):
                if str_user == read[i].rstrip('\n') and password_sha == read[i + 1].rstrip('\n'):
                    not_found = False
                    self.auth_window.destroy()
                    Game(str_user).start_game()
                    break
                if str_user == '' or self.password_user.get() == '':
                    warning_window('Вы оставили поле пустым.')
                    return
        if not_found:
            warning_window('Не удалось авторизоваться. Не подходящие логин или пароль.')

    def write_txt(self):
        str_user = self.login_user.get()
        with open('File.txt', 'r') as f:
            read = f.readlines()
            for i in range(1, len(read), 2):
                if str_user == read[i].rstrip('\n'):
                    warning_window('Выбранный вами логин уже используется.')
                    return
            if self.login_user.get() == '' or self.password_user.get() == '':
                warning_window('Вы оставили поле пустым.')
                return
        with open('File.txt', 'a') as f:
            f.write(
                '\n' + str_user + '\n' + hashlib.sha1(str.encode(self.password_user.get())).hexdigest())
            f.close()
            self.auth_window.destroy()
            Game(str_user).start_game()


class Game:

    def __init__(self,login_user):

        open('ScoreFile.txt', 'a').close()
        self.login_user = login_user
        self.turns = 0
        self.colors = ['1', '2', '3', '4', '5', '6', '7']
        self.ghost_colors = ['-1', '-2', '-3', '-4', '-5', '-6', '-7']
        self.current_stage = SELECT
        self.buttons = [[], [], [], [], [], [], [], [], []]  # кнопки
        self.score = 0
        self.future_balls = []

    def start_game(self):
        self.game_window = Tk()
        self.game_window.title("Color Lines")
        self.game_window.geometry("1200x865")
        background = ImageTk.PhotoImage(img.resize((1200, 1000)))
        self.game_window.resizable(False,False)
        bg = Label(self.game_window, image=background)
        bg.place(x=0, y=0, relwidth=1, relheight=1)

        self.mini_image = [
            PhotoImage(file="assets/red.png").subsample(2, 2), PhotoImage(file="assets/yellow.png").subsample(2, 2),
            PhotoImage(file="assets/orange.png").subsample(2, 2), PhotoImage(file="assets/green.png").subsample(2, 2),
            PhotoImage(file="assets/blue.png").subsample(2, 2), PhotoImage(file="assets/quan.png").subsample(2, 2),
            PhotoImage(file="assets/purple.png").subsample(2, 2)
        ]
        self.image = [
            PhotoImage(file="assets/red.png"), PhotoImage(file="assets/yellow.png"),
            PhotoImage(file="assets/orange.png"), PhotoImage(file="assets/green.png"),
            PhotoImage(file="assets/blue.png"), PhotoImage(file="assets/quan.png"),
            PhotoImage(file="assets/purple.png")
        ]
        self.empty =PhotoImage(file='assets/empty.png').subsample(2, 2)
        button_image_gamewindow = PhotoImage(file='assets/button333.png').zoom(5,1).subsample(4,2)
        button_image_score= PhotoImage(file='assets/button333.png').zoom(5,1).subsample(6,2)
        for r in range(9):
            for c in range(9):

                btn = Button( text=' ', image= self.empty, width=90, height=90,
                             command=lambda row=r, column=c: self.stage_choice(row, column))

                self.buttons[r].append(btn)
                btn.grid(row=r, column=c, sticky="nsew")
        self.computer_predict_space_ball()
        self.computer_predict_space_ball()
        self.score_label = Label(self.game_window, text=f'Счёт:{self.score}', font='Times 30', image=button_image_score, compound='center')
        self.score_label.place(x= 900,y= 20)
        self.save_button = Button(self.game_window, border="0", text ='Сохранить рекорд', image= button_image_gamewindow, font='Times 20', compound='center', command=self.write_score)
        self.save_button.place(x = 900, y = 100)
        self.new_game_button = Button(self.game_window, border="0", text='Начать новую игру',image= button_image_gamewindow, font='Times 20', compound='center', command=self.new_game)
        self.new_game_button.place(x=900, y=700)
        self.button_back = Button(self.game_window, text="В главное меню", compound='center', image=button_image_gamewindow,font='Times 20', command=lambda: self.back_command(False))
        self.button_back.place(x=900, y= 780)
        self.game_window.eval('tk::PlaceWindow . center')
        self.game_window.mainloop()
    def back_command(self, key):
        if key == False:
            self.game_window.destroy()
            Main()
        else:
            Auth(self.auth_window)

    def new_game(self,end_window = None):
        if end_window != None:
            end_window.destroy()
        self.game_window.destroy()
        Game(self.login_user).start_game()

    def add_color_ball(self, x, y):
        if self.buttons[x][y]['text'] == ' ':
            return
        self.buttons[x][y].config(width=90, height=90, image=self.image[int(self.buttons[x][y]['text']) - 1])
    def add_ghost_ball(self, x, y, color):
        if color == ' ': return
        self.buttons[x][y].config(width=90, height=90, image=self.mini_image[int(color) - 1])

    def stage_choice(self, x, y):
        if self.current_stage == SELECT:
            self.player_choice_ball(x, y)
        elif self.current_stage == MOVE:
            self.player_place_ball(x, y)

    def computer_spawn_ball(self):
        empty = []
        for x, y, color in self.future_balls:
            if self.buttons[x][y]['text'] != ' ':
                for x in range(8):
                    for y in range(8):
                        if self.buttons[x][y]['text'] == ' ':
                            empty.append([x,y])
                            x,y = random.choice(empty)
                            color = random.choice(self.colors)
            self.buttons[x][y]['text'] = color
            self.near_color_check(x, y)
            self.add_color_ball(x, y)
        self.future_balls.clear()

    def computer_predict_space_ball(self):
        self.computer_spawn_ball()
        empty_cells = []
        for x in range(9):
            for y in range(9):
                if self.buttons[x][y]['text'] == ' ':
                    empty_cells.append([x, y])
        if len(empty_cells) == 0:
            end_window = Tk()
            Button(end_window, text='Сохранить рекорд', font='Times 20',command=self.write_score).pack()
            Label(end_window, text='').pack()
            Button(end_window, text = 'Выход', font='Times 20', command= end_window.destroy).pack()
            Label(end_window, text='').pack()
            Button(end_window,compound='center', text='Начать новую игру', font='Times 20',command= lambda:self.new_game(end_window)).pack()
            end_window.eval('tk::PlaceWindow . center')
            return
        max_places = min(len(empty_cells), 3)
        while max_places != 0:
            select = random.randint(0, len(empty_cells) - 1)
            x, y = empty_cells.pop(select)
            if self.buttons[x][y]['text'] == ' ':
                color = random.choice(self.colors)
                self.future_balls.append([x, y, color])
                self.add_ghost_ball(x, y, color)
            max_places -= 1

    def player_choice_ball(self, x, y):
        if self.buttons[x][y]['text'] != ' ':
            self.save_x = x
            self.save_y = y
            self.buttons[x][y].config(bg='#98FB98')
            self.current_stage = MOVE

    def player_place_ball(self, x, y):
        if self.buttons[x][y]['text'] == ' ':
            if not self.pathfinding(x, y):
                warning_window('Путь  перегражден другим шариком', 'Ошибка')
                return
            self.buttons[self.save_x][self.save_y].config(bg='SystemButtonFace')
            self.buttons[x][y]['text'] = self.buttons[self.save_x][self.save_y]['text']
            self.current_stage = SELECT
            self.add_color_ball(x, y)
            self.delete_ball(self.save_x, self.save_y)
            previous_score = self.score
            self.near_color_check(x, y)
            if self.score == previous_score :
                self.computer_predict_space_ball()
        else:
            self.buttons[self.save_x][self.save_y].config(bg='SystemButtonFace')
            self.save_x = x
            self.save_y = y
            self.buttons[x][y].config(bg='#98FB98')

    def validate_coord(self, x, y):
        return 0 <= x < 9 and 0 <= y < 9

    def near_color_check(self, x, y):
        color = self.buttons[x][y]['text']
        for nearby_coords in [[0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            self.line_calculate(x, y, nearby_coords, color)

    def line_calculate(self, x, y, nearby_coords, color):
        count = 1
        x_offsets = x
        y_offsets = y
        while count < 9:
            x_offsets += nearby_coords[0]
            y_offsets += nearby_coords[1]
            if self.validate_coord(x_offsets, y_offsets) and color == self.buttons[x_offsets][y_offsets]['text']:
                count += 1
            else:
                break
        x_offsets = x
        y_offsets = y
        while count < 9:
            x_offsets -= nearby_coords[0]
            y_offsets -= nearby_coords[1]
            if self.validate_coord(x_offsets, y_offsets) and color == self.buttons[x_offsets][y_offsets]['text']:
                count += 1
            else:
                break
        if count >= 5:
            self.score_calculate(count)
            x_offsets = x
            y_offsets = y
            while True:
                x_offsets += nearby_coords[0]
                y_offsets += nearby_coords[1]
                if self.validate_coord(x_offsets, y_offsets) and color == self.buttons[x_offsets][y_offsets]['text']:
                    self.delete_ball(x_offsets, y_offsets)
                else:
                    break
            x_offsets = x
            y_offsets = y
            while True:
                x_offsets -= nearby_coords[0]
                y_offsets -= nearby_coords[1]
                if self.validate_coord(x_offsets, y_offsets) and color == self.buttons[x_offsets][y_offsets]['text']:

                    self.delete_ball(x_offsets, y_offsets)
                else:
                    break
            self.delete_ball(x, y)

    def delete_ball(self, x, y):
        self.buttons[x][y]['text'] = ' '
        self.buttons[x][y].config(image=self.empty)

    def score_calculate(self, count):
        if count == 9:
            self.score += 100
        elif count == 8:
            self.score += 50
        elif count == 7:
            self.score += 25
        elif count == 6:
            self.score += 10
        elif count == 5:
            self.score += 5
        self.score_label.config(text=f'Счёт:{self.score}')

    def pathfinding(self, x, y):
        goal = [x, y]
        reachable = [[self.save_x, self.save_y]] #Нужно про1ти
        explored = [] #пройдено
        while len(reachable) != 0:
            node = self.choose_node(reachable, goal)
            if node == goal:
                return True
            reachable.remove(node)
            explored.append(node)
            new_reachable = []
            for j in self.get_adjacent_nodes(node):
                if j not in explored:
                    new_reachable.append(j)
            for adjacent in new_reachable:
                if adjacent not in reachable:
                    reachable.append(adjacent)
        return False

    def get_adjacent_nodes(self, node):
        adjacent_nodes = []
        for x, y in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            x_offset = node[0] + x
            y_offset = node[1] + y
            if (9 > x_offset >= 0 and 9 > y_offset >= 0) and self.buttons[x_offset][y_offset]['text'] == ' ':
                adjacent_nodes.append([x_offset, y_offset])
        return adjacent_nodes

    def choose_node(self, reachable, goal):
        min_cost = 20
        best_node = None
        for node in reachable:
            total_cost = abs(goal[0] - node[0]) + abs(goal[1] - node[1])
            if min_cost > total_cost:
                min_cost = total_cost
                best_node = node
        return best_node

    def write_score(self):
        scores ={}
        with open('ScoreFile.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line == '':
                    break
                readline_score = line.split(':', 2)
                scores[readline_score[1][:-1]] = int(readline_score[0])
        if scores.get(self.login_user, 0) > self.score:
            warning_window('Ваш текущий рекорд меньше, чем сохраненный ранее', 'Отказ сохранения')
            return
        scores[self.login_user] = self.score

        with open('ScoreFile.txt', 'w+') as f:
            for login in sorted(scores, key=scores.get, reverse=True):
                f.write(str(scores[login]) + ':' + login + '\n')
            f.close()
        warning_window('Рекорд сохранен.', 'Сохранение')


def warning_window(message, title=None):  # функция для вывода текста об ошибке
    window = Tk()
    if title != None:
        window.title(title)
    else:
        window.title('Ошибка')
    Label(window, font=14, text=message).pack()
    window.eval('tk::PlaceWindow . center')
Main()
