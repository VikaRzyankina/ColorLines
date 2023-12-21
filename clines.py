from tkinter import *
import hashlib
import random

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
        window.eval('tk::PlaceWindow . center')
        window.geometry('300x250')
        window.configure(background='#849974')
        Label(window, text='', background='#849974').pack()
        Label(window, text='', background='#849974').pack()
        Button(window, font=14, text="Регистрация", command=self.start).pack()
        Label(window, text='', background='#849974').pack()
        Button(window, font=14, text="Вход", command=self.start_2).pack()
        but = Button(window, text="Выход", command=window.destroy)
        but.config(font=('Helvetica', 12))
        Label(window, text='', background='#849974').pack()
        but.pack()
        self.window.mainloop()

    def window_entry(self, description):
        Label(self.window, text=description).pack()
        entry = Entry(self.window, font=14, width=20, justify='center')
        entry.pack()
        return entry

    def wind_entry(self, description):
        Label(self.wind, font=14, text=description).pack()
        entry = Entry(self.wind, font=14, width=20, justify='center')
        entry.pack()
        return entry

    def wind_start(self, title, log, passw, command):
        self.window.destroy()
        self.wind = Tk()
        self.wind.title(title)
        wind = self.wind
        wind.eval('tk::PlaceWindow . center')
        wind.geometry('300x200')
        wind.configure(background='#849974')

        self.login_user = self.wind_entry(log)
        Label(wind, text='', background='#849974').pack()
        self.password_user = self.wind_entry(passw)
        Label(wind, text='', background='#849974').pack()
        Button(wind, font=14, text="Продолжить", command=command).pack()

    def start(self):
        self.wind_start('Регистрация', 'Придумайте логин', 'Придумайте пароль', self.write_txt)

    def start_2(self):
        self.wind_start('Вход', 'Введите логин', 'Введите пароль', self.open_txt)

    def open_txt(self):
        not_found = True
        with open('File.txt', 'r') as f:
            read = f.readlines()
            password_sha = hashlib.sha1(str.encode(self.password_user.get())).hexdigest()
            for i in range(1, len(read), 2):
                if self.login_user.get() == read[i].rstrip('\n') and password_sha == read[i + 1].rstrip('\n'):
                    self.wind.destroy()
                    not_found = False
                    Game().start_game()
                    break
                if self.login_user.get() == '' or self.password_user.get() == '':
                    text_window('Вы оставили поле пустым.')
                    return
        if not_found:
            text_window('Не удалось авторизоваться. Не подходящие логин или пароль.')

    def write_txt(self):
        with open('File.txt', 'r') as f:
            read = f.readlines()
            for i in range(1, len(read), 2):
                if self.login_user.get() == read[i].rstrip('\n'):
                    text_window('Выбранный вами логин уже используется.')
                    return
            if self.login_user.get() == '' or self.password_user.get() == '':
                text_window('Вы оставили поле пустым.')
                return
        with open('File.txt', 'a') as f:
            text_window('Вы успешно зарегистрировались и вошли.', 'Регистрация')
            f.write(
                '\n' + self.login_user.get() + '\n' + hashlib.sha1(str.encode(self.password_user.get())).hexdigest())
            f.close()
            self.wind.destroy()
            Game().start_game()


class Game:

    def __init__(self):
        open('ScoreFile.txt', 'a').close()
        self.turns = 0
        self.colors = ['1', '2', '3', '4', '5', '6', '7']
        self.current_stage = SELECT
        self.buttons = [[], [], [], [], [], [], [], [], []]  # кнопки
        self.score = 0

    def start_game(self):
        roott = Tk()
        roott.eval('tk::PlaceWindow . center')
        roott.title("Color Lines")
        roott.geometry("862x950")


        self.image = [
            PhotoImage(file="assets/red.png").subsample(2, 2), PhotoImage(file="assets/yellow.png").subsample(2, 2),
            PhotoImage(file="assets/orange.png").subsample(2, 2), PhotoImage(file="assets/green.png").subsample(2, 2),
            PhotoImage(file="assets/blue.png").subsample(2, 2), PhotoImage(file="assets/quan.png").subsample(2, 2),
            PhotoImage(file="assets/purple.png").subsample(2, 2)
        ]
        self.empty =PhotoImage(file='assets/empty.png').subsample(2, 2)

        for r in range(9):
            for c in range(9):

                btn = Button( text=' ', image= self.empty, width=90, height=90,
                             command=lambda row=r, column=c: self.stage_choice(row, column))

                self.buttons[r].append(btn)
                btn.grid(row=r, column=c, sticky="nsew")
        self.spawn_ball()
        self.score_label = Label(roott, text=f'Счёт:{self.score}', font='Times 30')
        self.score_label.place(x= 400,y= 870)
        roott.mainloop()

    def color_ball(self, x, y):
       self.buttons[x][y].config(width=90, height=90, image=self.image[int(self.buttons[x][y]['text']) - 1])

    def stage_choice(self, x, y):
        if self.current_stage == SELECT:
            self.choice_ball(x, y)
        elif self.current_stage == MOVE:
            self.place_ball(x, y)

    def spawn_ball(self):
        empty_cells = []
        c = 0
        for x in range(9):
            for y in range(9):
                if self.buttons[x][y]['text'] == ' ':
                    empty_cells.append([x,y])
        if len(empty_cells) < 4:
            text_window('Вы проиграли')
            return
        while c != 3:
            select = random.randint(0, len(empty_cells) - 1)
            x, y = empty_cells.pop(select)
            if self.buttons[x][y]['text'] == ' ':
                self.buttons[x][y]['text'] = random.choice(self.colors)
                self.color_check(x, y)
                self.color_ball(x, y)
            c += 1

    def choice_ball(self, x, y):
        if self.buttons[x][y]['text'] != ' ':
            self.save_x = x
            self.save_y = y
            self.current_stage = MOVE

    def place_ball(self, x, y):
        if self.buttons[x][y]['text'] == ' ':
            if not self.pathfinding(x, y):
                return
            self.buttons[x][y]['text'] = self.buttons[self.save_x][self.save_y]['text']
            self.current_stage = SELECT
            self.spawn_ball()
            self.color_ball(x, y)
            self.clear_ball(self.save_x, self.save_y)
            self.color_check(x, y)
        else:
            self.save_x = x
            self.save_y = y


    def validate_coord(self, x, y):
        return 0 <= x < 9 and 0 <= y < 9

    def color_check(self, x, y):
        color = self.buttons[x][y]['text']
        for nearby_coords in [[0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            self.line_check(x, y, nearby_coords, color)

    def line_check(self, x, y, nearby_coords, color):
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
            self.score_check(count)
            x_offsets = x
            y_offsets = y
            while True:
                x_offsets += nearby_coords[0]
                y_offsets += nearby_coords[1]
                if self.validate_coord(x_offsets, y_offsets) and color == self.buttons[x_offsets][y_offsets]['text']:
                    self.clear_ball(x_offsets, y_offsets)
                else:
                    break
            x_offsets = x
            y_offsets = y
            while True:
                x_offsets -= nearby_coords[0]
                y_offsets -= nearby_coords[1]
                if self.validate_coord(x_offsets, y_offsets) and color == self.buttons[x_offsets][y_offsets]['text']:

                    self.clear_ball(x_offsets, y_offsets)
                else:
                    break
            self.clear_ball(x, y)

    def clear_ball(self, x, y):
        self.buttons[x][y]['text'] = ' '
        self.buttons[x][y].config(image=self.empty)

    def score_check(self, count):
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



def text_window(message, title=None):  # функция для вывода текста об ошибке
    window = Tk()
    if title != None:
        window.title(title)
    else:
        window.title('Ошибка')
    Label(window, font=14, text=message).pack()
    window.eval('tk::PlaceWindow . center')

