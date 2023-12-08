# Импортируем сам пайгейм и распаковываем его модули
import pygame
from pygame.locals import *
import tkinter as tk
from tkinter import ttk
import pandas as pd

def autho():

    root = tk.Tk()
    root.title("Окно авторизации")

    name = tk.StringVar()
    password = tk.StringVar()

    name_label = ttk.Label(root, text="Имя пользователя:")
    name_label.grid(column=0, row=0)
    name_entry = ttk.Entry(root, textvariable=password)
    name_entry.grid(column=1, row=0)

    pass_label = ttk.Label(root, text="Пароль:")
    pass_label.grid(column=0, row=1)
    pass_entry = ttk.Entry(root, show="*", textvariable=name)
    pass_entry.grid(column=1, row=1)

    login_button = ttk.Button(root, text="Войти", command=root.destroy)
    login_button.grid(column=1, row=2)
    root.mainloop()
    return name.get(), password.get()


def authorization_in(user_name, password):
    users_path = 'users.csv'
    names_and_words = pd.read_csv(users_path)
    if str(user_name) in list(names_and_words['user_name']):
        pass
    else:
        new_user = pd.DataFrame({'user_name': [str(user_name)], 'password': [str(password)]})
        names_and_words = pd.concat([names_and_words, new_user])
        names_and_words.to_csv(users_path, index=False)

def update_stats(user_name, win=False):
    global stats_path
    stats_path = 'stats.csv'
    stats = pd.read_csv(stats_path)
    if str(user_name) in list(stats['user_name']):
        stats.loc[stats.user_name == str(user_name), ('number_of_games')] += 1
        stats.loc[stats.user_name == str(user_name), ('number_of_wins')] += int(win)
        stats.to_csv(stats_path, index=False)
    else:
        new_user = pd.DataFrame({'user_name': [str(user_name)], 'number_of_games': [0], 'number_of_wins': [0]})
        names_and_words = pd.concat([stats, new_user])
        names_and_words.to_csv(stats_path, index=False)
    return int(stats[stats.user_name == str(user_name)]['number_of_games']), int(stats[stats.user_name == str(user_name)]['number_of_wins'])



# окно авторизации
user_name, user_password = autho()
authorization_in(user_name, user_password)

pygame.init()

from Constants import *

# Рисуем окошко игры
wSurface = pygame.display.set_mode(WINDOWSIZE, 0, 32)
pygame.display.set_caption("CoronaVirus eats people!!")

from CoronaVirus import CoronaVirus
from AntiBody import AntiBody
from Pattern import Pattern
from Dots import Dots

channel = pygame.mixer.Channel(2)
opening = pygame.mixer.Sound("opening_song.wav")
pickUp_small = pygame.mixer.Sound("waka_waka.wav")
pickUp_large = pygame.mixer.Sound("eating_cherry.wav")
eatGhost = pygame.mixer.Sound("eating_ghost.wav")
death = pygame.mixer.Sound("pacmandies.wav")
lose = pygame.mixer.Sound("gameover.wav")
win = pygame.mixer.Sound("youwin.wav")
bg = pygame.mixer.Sound("bg_music.mp3")

# Создаем объекты для игры
background = pygame.image.load("bg.png").convert()
corona = CoronaVirus()
antibody = [AntiBody()]
walls = Pattern().walls
small_dots = Dots().createListSmall()
large_dots = Dots().createListLarge()
clock = pygame.time.Clock()
pygame.mixer.music.load("песняЯрика.mp3")
pygame.mixer.music.set_volume(0.1)




# Открываем окно игры, включаем музыку
Dot_s = Dots()
channel.play(opening)
wSurface.fill((0, 0, 0))
wSurface.blit(background, (100, 0))
wSurface.blit(corona.getScoreSurface(), (10, 10))
wSurface.blit(corona.getLivesSurface(), (WINDOWSIZE[0] - 200, 10))
for p in small_dots:
    wSurface.blit(Dot_s.images[0], (p[0] + Dot_s.shifts[0][0], p[1] + Dot_s.shifts[0][1]))
for p in large_dots:
    wSurface.blit(Dot_s.images[1], (p[0] + Dot_s.shifts[1][0], p[1] + Dot_s.shifts[1][1]))
for cur_anti in antibody:
    wSurface.blit(cur_anti.surface, cur_anti.rect)
wSurface.blit(corona.surface, corona.rect)
pygame.display.update()
while True:
    if not pygame.mixer.get_busy():
        break

# Основной цикл игры
game_is_on = True
while game_is_on:
    # Один раунд
    round_is_on = True
    pygame.mixer.music.play(-1, 0.0)
    while round_is_on:

        # Обрабатываем событие
        for event in pygame.event.get():
            # Заканчиваем обработку
            if event.type == QUIT:
                game_is_on = round_is_on = False

            # Нажатия кнопок
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    corona.moveUp = True
                    corona.moveLeft = corona.moveDown = corona.moveRight = False
                    corona.direction = 0
                elif event.key == K_LEFT:
                    corona.moveLeft = True
                    corona.moveUp = corona.moveDown = corona.moveRight = False
                    corona.direction = 1
                elif event.key == K_DOWN:
                    corona.moveDown = True
                    corona.moveUp = corona.moveLeft = corona.moveRight = False
                    corona.direction = 2
                elif event.key == K_RIGHT:
                    corona.moveRight = True
                    corona.moveUp = corona.moveLeft = corona.moveDown = False
                    corona.direction = 3

            # Проверяем нажатие клавиши
            elif event.type == KEYUP:
                corona.moveUp = corona.moveLeft = corona.moveDown = corona.moveRight = False

        # Перемещаем вирус
        corona.move_c(walls)

        # Проверяем, должен ли телепортироваться вирус
        corona.teleport()
        for anti in antibody:
            anti.teleport()

        # Организуем с помощью sprite повороты вируса, анимацию
        corona.getSurface()
        Dot_s = Dots()
        # Проверяяем, съел ли вирус точку, удаляем ее, если да
        Dot_s.check(small_dots, large_dots, corona, antibody)

        # Добавляем антитело при необходимости
        
        if corona.score >= 700:
            AntiBody.add(AntiBody(), antibody, corona.score, corona.body_count)
            corona.body_count = True
            if len(antibody) == 1:
                corona.body_count = False

        # Проверяем, вернулись ли голубые антитела в нормальное состояние
        for cur_anti in antibody:
            if cur_anti.isBlue:
                cur_anti.checkBlue()

        # Располагаем антитела
        for cur_anti in antibody:
            cur_anti.move_antibody(walls, corona)

        # Draw screen
        Dot_s = Dots()
        wSurface.fill((0, 0, 0))
        wSurface.blit(background, (100, 0))
        wSurface.blit(corona.getScoreSurface(), (10, 10))
        wSurface.blit(corona.getLivesSurface(), (WINDOWSIZE[0] - 200, 10))
        for p in small_dots:
            wSurface.blit(Dot_s.images[0], (p[0] + Dot_s.shifts[0][0], p[1] + Dot_s.shifts[0][1]))
        for p in large_dots:
            wSurface.blit(Dot_s.images[1], (p[0] + Dot_s.shifts[1][0], p[1] + Dot_s.shifts[1][1]))
        for cur_anti in antibody:
            wSurface.blit(cur_anti.surface, cur_anti.rect)
        wSurface.blit(corona.surface, corona.rect)
        pygame.display.update()

        # Проверяем, не столкнулся вирус с антителом
        for cur_anti in antibody:
            if corona.rect.colliderect(cur_anti.rect):
                if not cur_anti.isBlue:
                    round_is_on = False
                    corona.lives -= 1
                    if corona.lives == 0:
                        game_is_on = False
                    else:
                        channel.play(death)
                    break
                else:  # Ghost is blue
                    del antibody[antibody.index(cur_anti)]
                    corona.score += 100
                    channel.play(eatGhost)


        # Проверяем, съедены ли все точки
        else:
            if len(small_dots) == 0 and len(large_dots) == 0:
                game_is_on = round_is_on = False
        clock.tick(FPS)
    # Убираем точки
    pygame.mixer.music.stop()
    corona.reset()
    for cur_anti in antibody:
        cur_anti.reset()
    while True:
        if not pygame.mixer.get_busy():
            break

# Закрываем окно игры
wSurface.fill((0, 0, 0))
surface_temp = None
if corona.lives == 0:  # Проигрыш
    channel.play(lose)
    surface_temp = corona.getLosingSurface()
    games, wins = update_stats(user_name, win=False)

elif len(small_dots) == 0 and len(large_dots) == 0:  # Выигрыш
    channel.play(win)
    surface_temp = corona.getWinningSurface()
    ames, wins = update_stats(user_name, win=True)




if surface_temp != None:  # Игрок проиграл или выиграл, но не вышел из игры

    rect_temp = surface_temp.get_rect()
    rect_temp.center = wSurface.get_rect().center
    wSurface.blit(surface_temp, rect_temp)
    pygame.display.update()

pygame.time.delay(5000)

if True:
    channel.play(bg)
    surface_temp = corona.getStatsSurface(games)
    rect_temp = surface_temp.get_rect()
    rect_temp.center = wSurface.get_rect().center
    wSurface.fill((0, 0, 0))
    wSurface.blit(surface_temp, (100, 150))

    surface_temp = corona.getScoreSurface()
    wSurface.blit(surface_temp, (100, 200))

    surface_temp = corona.getStatsWinSurface(wins)
    wSurface.blit(surface_temp, (100, 250))
    pygame.display.update()
    pygame.time.delay(5000)
    pygame.quit()
 

while True:
    if not pygame.mixer.get_busy():
        pygame.quit()
        break
