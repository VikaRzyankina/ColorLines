from pygame import  mixer
from tkinter import *
from PIL import ImageTk, Image
import hashlib
import random
mixer.init()
mixer.music.load('assets/MenuSound.mp3')
mixer.music.play(loops=-1)
mixer.music.set_volume(0.1)
class Main():
    def __init__(self):
        self.root = Tk()
        self.root.title("Color Lines")

        self.Main_menu()

    def Main_menu(self):
        img = Image.open('assets/menuu.jpeg')
        width = 900
        ratio = (width / float(img.size[0]))
        height = int((float(img.size[1]) * float(ratio)))
        imag = img.resize((width, height))
        background = ImageTk.PhotoImage(imag)
        bg = Label( self.root, image=background)
        bg.pack()
        self.root.eval('tk::PlaceWindow . center')

        button_image_start = PhotoImage(file='assets/button111.png')
        button_image_settings = PhotoImage(file='assets/button222.png')
        button_image_exit = PhotoImage(file='assets/button333.png')
        button_image_score = PhotoImage(file='assets/button222.png')

        button_play = Button( self.root, text = 'Начать Игру', fg='#ffffff', font='Times 24', border="0", image = button_image_start, compound='center', command= lambda: Auth( self.root))
        button_settings = Button( self.root, text = 'Настройки', fg='#ffffff', font='Times 24', border="0", image = button_image_settings, compound='center')
        button_score = Button( self.root, text = 'Рекорды: ', fg='#ffffff', font='Times 24',  border="0", image = button_image_score, compound='center')
        button_exit = Button( self.root, text = ' Выход', font='Times 24', border="0", image = button_image_exit, compound='center', command =  self.root.destroy )

        button_play.place(x=650, y=250)
        button_settings.place(x=650, y=400)
        button_score.place(x=50, y=50)
        button_exit.place(x=650, y=550)
        self.root.mainloop()

GAME_OVER = 'game_over'
SELECT = 'choice'
MOVE = 'move'


class Auth:
    def __init__(self, menu):
        menu.destroy()
        open('File.txt', 'a').close()
        self.window = Tk()
        self.window.title('Добрый день, пользователь!')
        window = self.window
        window.geometry('300x250')
        self.auth_bg = Image.open('assets/menu (2).jpeg')
        self.imag = self.auth_bg.resize((300, 300))
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
        Label(self.auth_window, font=14, text=description).pack()
        entry = Entry(self.auth_window, font=14, width=20, justify='center')
        entry.pack()
        return entry

    def select_auth(self, title, log, passw, command):
        self.window.destroy()
        self.auth_window = Tk()
        self.auth_window.title(title)
        wind = self.auth_window
        wind.geometry('300x200')

        auth_bg = Image.open('assets/menu (2).jpeg')
        self.imag = auth_bg.resize((300, 300))
        background = ImageTk.PhotoImage(self.imag)
        bg = Label(self.auth_window, image=background)
        bg.place(x=0, y=0, relwidth=1, relheight=1)

        self.login_user = self.window_entry(log)
        Label(self.auth_window, text='').pack()
        self.password_user = self.window_entry(passw)
        Label(wind, text='').pack()
        Button(wind, font=14, text="Продолжить", command=command).pack()
        Button(wind, font =14, text ='Назад', command=lambda: self.back_command(True)).pack()
        wind.eval('tk::PlaceWindow . center')
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
        self.login_user = login_user
        self.turns = 0
        self.colors = ['1', '2', '3', '4', '5', '6', '7']
        self.current_stage = SELECT
        self.buttons = [[], [], [], [], [], [], [], [], []]  # кнопки
        self.score = 0
        self.future_balls = []

    def start_game(self):
        roott = Tk()

        roott.title("Color Lines")
        roott.geometry("862x950")

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
        self.score_label = Label(roott, text=f'Счёт:{self.score}', font='Times 30')
        self.score_label.place(x= 400,y= 870)
        self.save_button = Button(roott, text ='Сохранить рекорд',font='Times 20', command=self.write_score)
        self.save_button.place(x = 2, y = 870)
        roott.eval('tk::PlaceWindow . center')
        roott.mainloop()

    def adds_color_ball(self, x, y):
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
            self.adds_color_ball(x, y)
        self.future_balls.clear()

    def computer_predict_space_ball(self):
        self.computer_spawn_ball()
        empty_cells = []
        c = 0
        for x in range(9):
            for y in range(9):
                if self.buttons[x][y]['text'] == ' ':
                    empty_cells.append([x, y])
        if len(empty_cells) < 4:
            warning_window('Вы проиграли')
            return
        while c != 3:
            select = random.randint(0, len(empty_cells) - 1)
            x, y = empty_cells.pop(select)
            if self.buttons[x][y]['text'] == ' ':
                color = random.choice(self.colors)
                self.future_balls.append([x, y, color])
                self.add_ghost_ball(x, y, color)
            c += 1

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
            self.computer_predict_space_ball()
            self.buttons[x][y]['text'] = saved_button
            self.current_stage = SELECT
            self.adds_color_ball(x, y)
            self.delete_ball(self.save_x, self.save_y)
            self.near_color_check(x, y)
        else:
            self.buttons[self.save_x][self.save_y].config(bg='SystemButtonFace')
            self.save_x = x
            self.save_y = y

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
