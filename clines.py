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

        button_image_start = PhotoImage(file='assets/button111.png')
        button_image_settings = PhotoImage(file='assets/button222.png')
        button_image_exit = PhotoImage(file='assets/button333.png')
        button_image_score = PhotoImage(file='assets/button222.png')

        button_play = Button( self.root, text = 'Начать Игру', fg='#ffffff', font='Times 24', border="0", image = button_image_start, compound='center', command= lambda: Auth( self.root))
        button_settings = Button( self.root, text = 'Настройки', fg='#ffffff', font='Times 24', border="0", image = button_image_settings, compound='center')
        button_score = Button( self.root, text = 'Рекорды ', fg='#ffffff', font='Times 24',  border="0", image = button_image_score, compound='center', command=self.table_records)
        button_exit = Button( self.root, text = ' Выход', font='Times 24', border="0", image = button_image_exit, compound='center', command =  self.root.destroy )

        button_play.place(x=650, y=250)
        button_settings.place(x=650, y=400)
        button_score.place(x=50, y=50)
        button_exit.place(x=650, y=550)
        self.root.mainloop()

    def table_records(self):
        self.root.destroy()
        records_window = Tk()
        button_image_records = PhotoImage(master= records_window, file='assets/button333.png').subsample(1,2)
        button_image_back = PhotoImage(master= records_window, file='assets/button222.png').subsample(1,2)
        records_window.title("Color Lines")
        records_window.geometry('400x900')
        imagg = auth_bg.resize((1000, 1000))
        background = ImageTk.PhotoImage(imagg, master = records_window)
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
        Button(records_window, text = 'Назад',font='Times 24', border="0", image = button_image_back, compound='center', command= lambda:self.back_record(records_window)).place(x=80, y=800)
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
        window.geometry('300x250')


        self.imag = auth_bg.resize((300, 300))
        background = ImageTk.PhotoImage(self.imag)
        bg = Label(window, image=background)
        bg.place(x=0, y=0, relwidth=1, relheight=1)
        window.eval('tk::PlaceWindow . center')

        Button(window, font=14, compound='center', text="Регистрация", command=self.register).pack(pady=20)
        Button(window, font=14, text="Вход", command=self.log_in).pack(pady=20)
        but = Button(window, text="Назад", command=lambda: self.back_command(False))
        but.config(font=('Helvetica', 12))
        but.pack(pady=20)
        self.window.mainloop()

    def back_command(self, key):
        if key == False:
            self.window.destroy()
            Main()
        else:
            Auth(self.auth_window)

    def window_entry(self, description):
        Label(self.auth_window, font=14, text=description).pack(pady=10)
        entry = Entry(self.auth_window, font=14, width=20, justify='center')
        entry.pack()
        return entry

    def select_auth(self, title, log, passw, command):
        self.window.destroy()
        self.auth_window = Tk()
        self.auth_window.title(title)
        wind = self.auth_window
        wind.geometry('300x300')

        background = ImageTk.PhotoImage(self.imag, master = wind)
        bg = Label(self.auth_window, image=background)
        bg.place(x=0, y=0, relwidth=1, relheight=1)

        self.login_user = self.window_entry(log)
        self.password_user = self.window_entry(passw)
        Button(wind, font=14, text="Продолжить", command=command).pack(pady=10)
        Button(wind, font =14, text ='Назад', command=lambda: self.back_command(True)).pack(pady=10)
        wind.eval('tk::PlaceWindow . center')
        wind.mainloop()
    def register(self):
        self.select_auth('Регистрация', 'Придумайте логин', 'Придумайте пароль', self.write_txt)

    def log_in(self):
        self.select_auth('Вход', 'Введите логин', 'Введите пароль', self.open_txt)

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
            warning_window('Вы успешно зарегистрировались и вошли.', 'Регистрация')
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
        self.game_window.geometry("863x955")
        background = ImageTk.PhotoImage(img)
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

        for r in range(9):
            for c in range(9):

                btn = Button( text=' ', image= self.empty, width=90, height=90,
                             command=lambda row=r, column=c: self.stage_choice(row, column))

                self.buttons[r].append(btn)
                btn.grid(row=r, column=c, sticky="nsew")
        self.computer_predict_space_ball()
        self.computer_predict_space_ball()
        self.score_label = Label(self.game_window, text=f'Счёт:{self.score}', font='Times 30')
        self.score_label.place(x= 370,y= 870)
        self.save_button = Button(self.game_window, text ='Сохранить рекорд',font='Times 20', command=self.write_score)
        self.save_button.place(x = 2, y = 870)
        self.new_game_button = Button(self.game_window, text='Начать новую игру', font='Times 20', command=self.new_game)
        self.new_game_button.place(x=618, y=870)
        self.game_window.eval('tk::PlaceWindow . center')
        self.game_window.mainloop()

    def new_game(self,end_window = None):
        if end_window != None:
            end_window.destroy()
        self.game_window.destroy()
        Game(self.login_user).start_game()

    def add_color_ball(self, x, y):
        if self.buttons[x][y] == ' ': return
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
        for x, y, color in self.future_balls:
            if self.buttons[x][y]['text'] != ' ':
                continue
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
                return
            saved_button = self.buttons[self.save_x][self.save_y]['text']
            self.buttons[self.save_x][self.save_y].config(bg='SystemButtonFace')
            self.buttons[x][y]['text'] = saved_button
            self.computer_predict_space_ball()
            self.current_stage = SELECT
            self.add_color_ball(x, y)
            self.delete_ball(self.save_x, self.save_y)
            self.near_color_check(x, y)
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
