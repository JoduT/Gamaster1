from tkinter import *
import random
import time
from bs4 import BeautifulSoup
import requests
import webbrowser
from PIL import ImageTk
from Platformer import main, level_number

# постоянные величины
WINDOW_WIDTH = 800  # ширина окна
SPACE_SIZE = 25  # длина/ширина сегмента змеи/яблока
SNAKE_LENGTH = 3  # начальная длина змеи
SPEED = 200  # скорость движения/отрисовки
COLOR_BODY = '#33bd38'
COLOR_HEAD = '#1b7d1f'
FOOD_COLOR = '#d11d32'
BACKGROUND_COLOR = '#f9fac0'
direction = 'down'  # направление по умолчанию
score = 0

def tk_part():
    # создаем окно размером 800x600 и лишаем игрока возможности растягивать окно, чтобы сохранить пропорции
    window = Tk()
    window.geometry('800x600')
    window.title('Gamaster')
    window.resizable(width=False, height=False)
    window.config(bg='#f9fac0')
    def pygame_perehod():
        window.destroy()
        main(level_number)
    def draw_menu():
        clear()
        window.config(bg='#f9fac0')
        label_title = Label(text="Выбирай!",font=('Franklin Gothic Heavy', 27), fg='#640', bg= '#ffad08')
        label_title.place(width=800, height= 55, x=0, y= 40)

        # кнопка с фактами
        fact_button = Button(text ='ФАКТЫ', font=('Franklin Gothic Heavy', 25), fg ='#640', bg = '#ffe500', command= facts) #fg ='#6b5a03', bg = '#ffec8c',
        fact_button.place(x=20, y=130, height= 80, width=365)
        # кнопка со змейкой
        snake_button = Button(text='ЗМЕЙКА', font=('Franklin Gothic Heavy', 25), fg ='#640', bg = '#ffe500', command = snake) #fg='#065c48', bg= '#baf7e9'
        snake_button.place(x=415, y= 130, height = 80, width=365)
        # кнопка с кликером
        clicker_button = Button(text="КЛИКЕР", font=('Franklin Gothic Heavy', 25), fg ='#640', bg = '#ffe500', command= clicker) #fg="#8a2812", bg = '#f7b3a3'
        clicker_button.place(x= 20, y=250, height = 80, width=365)
        # кнопка с орлом и решкой
        orel_button = Button(text='ОРЕЛ ИЛИ РЕШКА?', font=('Franklin Gothic Heavy', 25), fg ='#640', bg = '#ffe500')
        orel_button.place(x=415, y=250, height = 80, width=365)
        # кнопка с платформером
        img = ImageTk.PhotoImage(file='pictures/platteaser_0.png')
        platformer_button = Button(text='ПЛАТФОРМЕР', font=('Franklin Gothic Heavy', 25), fg ='#640', bg = '#ffe500', command = pygame_perehod) #fg='#161987', bg = '#d7d8fc'
        platformer_button.place(x=20, y=370, height = 80, width=365)
        # кнопка со змейкой
        q_button= Button(text='ОБ ИГРЕ И АВТОРАХ', font=('Franklin Gothic Heavy', 25), fg ='#640', bg = '#ffe500') #fg='#0b611d', bg='#a9e5a8'
        q_button.place(x=415, y=370, height = 80, width=365)

        # кнопки при наведении на них мышкой меняет свой цвет(если не делать отдельные функции на кнопки, то подсвечиваются все из них, а не только одна)
        def on_enterf(e): # если убрать аргумент, то все сломается(
            fact_button['background'] = '#b49cf7' #'#ffc800'
        def on_entera(e):
            snake_button['background'] = '#5fada4'
        def on_entercl(e):
            clicker_button['background'] = '#ff8c73'
        def on_enterplat(e):
            platformer_button['image'] = img
            #platformer_button['background'] = '#b49cf7'
        def on_enteror(e):
            orel_button['background'] = '#60aef7'
        def on_enterq(e):
            q_button['background'] = '#67d665'
        def on_leavef(e):
            fact_button['background'] = '#ffe500'
        def on_leavea(e):
            snake_button['background'] = '#ffe500'
        def on_leavecl(e):
            clicker_button['background'] = '#ffe500'
        def on_leaveplat(e):
            platformer_button['background'] = '#ffe500'
            platformer_button['image'] = ''
        def on_leaveor(e):
            orel_button['background'] = '#ffe500'
        def on_leaveq(e):
            q_button['background'] = '#ffe500'
        fact_button.bind("<Enter>", on_enterf)
        fact_button.bind("<Leave>", on_leavef)
        snake_button.bind("<Enter>", on_entera)
        snake_button.bind("<Leave>", on_leavea)
        clicker_button.bind("<Enter>", on_entercl)
        clicker_button.bind("<Leave>", on_leavecl)
        orel_button.bind("<Enter>", on_enteror)
        orel_button.bind("<Leave>", on_leaveor)
        platformer_button.bind("<Enter>", on_enterplat)
        platformer_button.bind("<Leave>", on_leaveplat)
        q_button.bind("<Enter>", on_enterq)
        q_button.bind("<Leave>", on_leaveq)

    # функция очищения всех виджетов с окна и появление кнопки домой
    def clear():
        all_widgets = window.place_slaves()
        for l in all_widgets:
            l.destroy()
        home_button = Button(text='Домой', font=('Franklin Gothic Heavy', 26), fg ='#640', bg = '#ffe500', command = draw_menu)
        home_button.place(x= 575, y= 475, height = 80, width=200)
        def on_enterhome(e):
            home_button['background'] = '#e6e7e8'
        def on_leavehome(e):
            home_button['background'] = '#ffe500'
        home_button.bind("<Enter>", on_enterhome)
        home_button.bind("<Leave>", on_leavehome)

    # Функция, запускающая факты
    def facts():
        clear()
        mainfact_label = Label(text = 'ИНТЕРЕСНЫЙ ФАКТ!', font=('Franklin Gothic Heavy', 24), fg='#084716', bg= '#9be0aa')
        mainfact_label.place(width=800, height=50, x=0, y=30)

        def callback():
            ss_factor = factor.a.attrs['href']
            webbrowser.open_new(ss_factor)
        web = requests.get('https://i-fakt.ru/').content
        html = BeautifulSoup(web, 'lxml')
        factor = random.choice(html.find_all(class_ = 'p-2 clearfix'))
        fact_text = factor.text.replace('\n', ' ')
        label_fact = Message(text= fact_text, font=('Franklin Gothic Heavy', 24), width=700, fg= '#0a5e13', bg= '#d3ebd8')
        label_fact.place(x=40, y= 90)
        more_button = Button(text="Подробнее...", font=("Franklin Gothic Heavy", 28), fg= '#064f0e', bg= '#a8e5ae', command=callback)
        more_button.place(x=250, y=450)

    # всё для кликера
    points = 0

    def clicker():
        clear()
        window.config(bg= '#fac5f1')
        text = Label(text='КЛИКАЙ, КЛИКАЙ, КЛИКАЙ!', fg='#850870', bg="#c468b5", font=('Franklin Gothic Heavy', 20))
        text.place(x=0, y=30, width=800, height=50)
        colors = ['#3aa67e', '#6da6fc', '#c5d426', '#b360b0', '#d13411', '#969c94', '#fa0', '#d79aed', '#3d2b2e']
        compliments = ['ЛУЧШИЙ!', 'ТАК ДЕРЖАТЬ!', 'КРУТОЙ!', 'ОЧАРОВАШКА!', 'LOVE U!', 'ПЕЛЬМЕШКА!']
        label_title = Label(text="Твои клики тут!: " + str(points), font=("Franklin Gothic Heavy", 30), fg="red4", bg="#fac5f1")
        label_title.place(width=400, height=50, x= 10, y= 90)

        def usual_button():
            global points
            points += 1
            if points %3 == 0:
                usual_b['bg'] = random.choice(colors)
            label_title = Label(text="Твои клики тут!: " + str(points), font=("Franklin Gothic Heavy", 30), fg="red4", bg="#fac5f1")
            label_title.place(width=400, height=50, x=10, y=90)
        usual_b = Button(text= "Просто кнопка.", font=("Franklin Gothic Heavy", 35), bg="#c777bf", fg="white", command= usual_button)
        usual_b.place(x=10, y=160, width = 400, height= 75)

        def slow_button():
           global points
           points += 1
           label_title = Label(text="Твои клики тут!: " + str(points), font=("Franklin Gothic Heavy", 30), fg="red4", bg="#fac5f1")
           label_title.place(width=400, height=50, x=10, y=90)
           time.sleep(10)

        slow_b = Button(text="Ме-е-едленно...", font=("Franklin Gothic Heavy", 35), bg="#517f45", fg="white", command= slow_button)
        slow_b.place(x= 420, y=160, width = 370, height= 75 )

        def compliment_button():
            global points
            points += 10
            label_title = Label(text="Твои клики тут!: " + str(points), font=("Franklin Gothic Heavy", 30), fg="red4", bg="#fac5f1")
            label_title.place(width=400, height= 50, x=10, y=90)
            comp_b["text"] = random.choice(compliments)

        comp_b = Button(text="БОЛЬШАЯ КНОПКА!", font=("Franklin Gothic Heavy", 50), width=20, bg="pink", fg="red2", command= compliment_button)
        comp_b.place(x=10, y= 245, width= 780, height = 100)

        def null_button():
            global points
            points -= points
            label_title = Label(text="Твои клики тут!: " + str(points), font=("Franklin Gothic Heavy", 30), fg="red4", bg="#fac5f1")
            label_title.place(width=400, height=50, x=10, y=90)

        null_b = Button(text="Полный ноль!", font=("Franklin Gothic Heavy", 35), bg="tan1", fg="brown4", command= null_button)
        null_b.place(x= 10, y= 355, width = 400, height = 75)

        def hundred_button():
            global points
            points += 100
            label_title = Label(text="Твои клики тут!: " + str(points), font=("Franklin Gothic Heavy", 30), fg="red4", bg="#fac5f1")
            label_title.place(width=400, height=50, x=10, y=90)

        hundred_b = Button(text="+100!!!", font=("Franklin Gothic Heavy", 35), bg="#56c461", fg="#05ff1e", command= hundred_button)
        hundred_b.place(x= 420, y=355, width=370, height=75)

        def blue_death_button():
            global points
            points -= 1000
            webbrowser.open_new('https://geekprank.com/blue-death/')
        bd_b = Button(text="????", font=("Franklin Gothic Heavy", 35), bg="#6664fa", fg="white", command= blue_death_button)
        bd_b.place(x= 10, y= 440, width= 550 , height=140)

    def snake():
        canvas = Canvas(window, height=550,
                        width=WINDOW_WIDTH, bg=BACKGROUND_COLOR)
        canvas.place(x=0, y=0)
        label_score = Label(window, text='Счёт: {}'.format(score), font=('Franklin Gothic Heavy', 30), fg='#402003', bg='#ba610d')
        label_score.place(x=0, y=532, height=45, width=800)

        # создание змеи
        class Snake:
            def __init__(self):
                self.snake_length = SNAKE_LENGTH
                self.coord = [[0, 0]] * 3  # матрица для координат 3 на 2
                self.squares = []  # массив для отрисовки змеи

                for x, y in self.coord:
                    square = canvas.create_rectangle(
                        x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=COLOR_BODY, outline='')  # создание сегмента змеи
                    self.squares.append(square)  # добавление сегмента змеи в массив, чтобы потом иы могли его удалять

        # класс, созда
        class Food:
            def __init__(self):
                x = random.randint(0, (WINDOW_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE  # от первой до 48 клетки по x -> 800/25=48
                y = random.randint(0, (450 / 25)) * 25  # по y методом подбора, так как высота холста не такая, как высота окна.
                self.coord = [x, y]  # определение координат
                canvas.create_rectangle(x, y, x + 23, y + 23, fill=FOOD_COLOR)  # создание квадратика еды на холсте

        # функция, отвечающая за движение змейки

        def move(snake, food):
            global score, SPEED
            for x, y in snake.coord:
                square = canvas.create_rectangle(
                    x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=COLOR_BODY, outline='')
            x, y = snake.coord[0]
            if (direction == 'down'):  # если заданное направление вниз, то увеличиваем Y
                y += SPACE_SIZE
            elif (direction == 'up'):  # если заданное движение вверх, то уменьшаем y
                y -= SPACE_SIZE
            elif (direction == 'left'):  # если заданное движение влево, то уменьшаем x
                x -= SPACE_SIZE
            elif (direction == 'right'):  # если заданное движение вправо, то увеличиваем y
                x += SPACE_SIZE

            snake.coord.insert(0, (x, y))  # в первой "ячейке" массива координаты головы
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=COLOR_HEAD,
                                             outline='')  # отрисовка головы
            snake.squares.insert(0, square)  # соединение с остальными сегментами

            # условие, если змейка съедает еду:
            if (x == food.coord[0] and y == food.coord[1]):
                score += 1  # прибавляются очки
                if SPEED != 0:
                    SPEED -= 2
                else:
                    SPEED = 0
                label_score.config(text='Счёт: {}'.format(score))  # изменяется счёт в надписи
                canvas.delete('food')  # удаляется с холста квадратик еды
                food = Food()  # создается новый квадратик еды
            # если еда не съедается змейкой:
            else:
                x, y = snake.coord[-1]
                square = canvas.create_rectangle(
                    x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=BACKGROUND_COLOR, outline='')

                del snake.coord[-1]  # удаляем координаты последнего сегмента
                canvas.delete(snake.squares[-1])  # при каждом движении в клетке последний отрисованный сегмент удаляется
                del snake.squares[-1]

            if (check_collisions(snake)):
                game_over()
            else:
                window.after(SPEED, move, snake, food)  # отрисовка через заданное количество мс(speed)

        def change_direction(new_dir):  # функция, изменяющая направление змейки
            global direction
            if (new_dir == 'down'):
                if (direction != 'up'):
                    direction = new_dir
            elif (new_dir == 'up'):
                if (direction != 'down'):
                    direction = new_dir
            elif (new_dir == 'left'):
                if (direction != 'right'):
                    direction = new_dir
            elif (new_dir == 'right'):
                if (direction != 'left'):
                    direction = new_dir

        def check_collisions(snake):  # проверка столкновений змейки с самой собой и со стенками окна
            x, y = snake.coord[0]  # координаты головы змейки

            if (x < 0 or x >= WINDOW_WIDTH):  # проверка на столкновение с вертикальными стенками
                return True
            elif (y < 0 or y >= 540):  # с горизонтальными
                return True

            for snake_length in snake.coord[1:]:  # cо своим телом
                if (x == snake_length[0] and y == snake_length[1]):
                    return True
            # если столкновений нет, ничего не происходит

        def game_over():  # если произошло столкновение
            global score
            score -= score
            canvas.delete(ALL)
            draw_menu()
        # привязка функций к клавишам
        window.bind('<KeyPress-Down>', lambda event: change_direction('down'))
        window.bind('<KeyPress-Up>', lambda event: change_direction('up'))
        window.bind('<KeyPress-Left>', lambda event: change_direction('left'))
        window.bind('<KeyPress-Right>', lambda event: change_direction('right'))
        snake = Snake()  # собственно змея
        food = Food()  # создание еды
        move(snake, food)  # запускаем игру

    draw_menu()
    window.mainloop()
tk_part()
# зацикливаем окно, чтобы оно было видимым игроку.


