import pygame

import copy

from Character import Character
from Constants import *


class AntiBody(Character):

    def __init__(self):
        super().__init__()
        self.images = [pygame.image.load("антитело1.png").convert(),
                  pygame.image.load("антитело2.png").convert()]
        for i in range(len(self.images)):
            self.images[i].set_colorkey((0, 0, 0))
        self.ISBLUE_TIME = int(10 * FPS)
        self.ADD_TIME = int(30 * FPS)
        self.add_time = self.ADD_TIME
        self.surface = self.images[0]
        self.rect = self.surface.get_rect()
        self.rect.left = 315
        self.rect.top = 275
        self.speed = 1
        self.course = [0] * int(50 / self.speed)
        self.isBlue = False
        self.isBlue_time = 0
        self.body_count = False

    def teleport(self):
        # Определяет, столкнулось ли антитело с телепортом и перемещает его
        if self.rect.colliderect(pygame.Rect((100, 256), (6, 48))):
            self.reset()
        if self.rect.colliderect(pygame.Rect((549, 256), (6, 48))):
            self.reset()
        if self.rect.left < 100:
            self.reset()
        if self.rect.left > 550:
            self.reset()

    def makeBlue(self):
        #  делает антитело голубым
        self.isBlue = True
        self.isBlue_time = self.ISBLUE_TIME  # number of frames
        self.surface = self.images[1]
        self.course = []

    def makeRed(self):
        #  меняет цвет на красный
        self.surface = self.images[0]
        self.course = []
        self.isBlue = False
        self.isBlue_time = 0

    def checkBlue(self):
        #  Проверяет, должно ли антитело вернуться в нормальное состояние, и делает это при необходимости.
        self.isBlue_time -= 1
        if self.isBlue_time <= 0:
            self.makeRed()

    def reset(self):
        # Сбрасывает положение антитела и делает его обычным.
        self.makeRed()
        self.rect.left = 315
        self.rect.top = 275
        self.course = [0] * int(50 / self.speed)

    def add(self, antibody, score, body_count):
        # Определяет, должно ли быть добавлено антитело, добавляет его в список и сбрасывает таймер добавления антитела.
        # Вычитает/прибавляет время в таймере
        self.add_time -= 1
        if len(antibody) == 0:
            if self.add_time > int(self.ADD_TIME / 10.0):
                self.add_time = int(self.ADD_TIME / 10.0)

        if self.add_time <= 0:
            antibody.append(AntiBody())
            self.add_time = self.ADD_TIME
         
        if score >= 700 and not body_count:
            antibody.append(AntiBody())
            self.add_time = self.ADD_TIME

    def canMove_distance(self, direction, walls):
        # Определяет количество шагов, которые антитело может сделать в указанном направлении
        # test = copy.deepcopy(self)
        counter = 0
        while True:
            if not self.isCharacterCanMove(direction, walls):
                break
            self.move(direction)
            counter += 1
        return counter

    def move_antibody(self, walls, corona):
        # Направляет к вирусу
        if len(self.course) > 0:
            if self.isCharacterCanMove(self.course[0], walls) or self.rect.colliderect(pygame.Rect((268, 248), (112, 64))):
                self.move(self.course[0])
                del self.course[0]
            else:
                self.course = []

        else:
            xDistance = corona.rect.left - self.rect.left
            yDistance = corona.rect.top - self.rect.top
            choices = [-1, -1, -1, -1]

            if abs(xDistance) > abs(yDistance):  # горизонтально 1
                if xDistance > 0:  # право 1
                    choices[0] = 3
                    choices[3] = 1
                elif xDistance < 0:  # лево 1
                    choices[0] = 1
                    choices[3] = 3

                if yDistance > 0:  # вниз 2
                    choices[1] = 2
                    choices[2] = 0
                elif yDistance < 0:  # наверх 2
                    choices[1] = 0
                    choices[2] = 2
                else:  # yDistance == 0
                    if self.canMove_distance(2, walls) < self.canMove_distance(0, walls):  # вниз 2
                        choices[1] = 2
                        choices[2] = 0
                    elif self.canMove_distance(0, walls) < self.canMove_distance(2, walls):  # наверх 2
                        choices[1] = 0
                        choices[2] = 2

            elif abs(yDistance) >= abs(xDistance):  # вертикально 1
                if yDistance > 0:  # вниз 1
                    choices[0] = 2
                    choices[3] = 0
                elif yDistance < 0:  # наверх 1
                    choices[0] = 0
                    choices[3] = 2

                if xDistance > 0:  # право 2
                    choices[1] = 3
                    choices[2] = 1
                elif xDistance < 0: # лево 2
                    choices[1] = 1
                    choices[2] = 3
                else:  # xDistance == 0
                    if self.canMove_distance(3, walls) < self.canMove_distance(1, walls):  # право 2
                        choices[1] = 3
                        choices[2] = 1
                    elif self.canMove_distance(1, walls) < self.canMove_distance(3, walls):  # лево 2
                        choices[1] = 1
                        choices[2] = 3

            if self.isBlue:
                choices.reverse()
            choices_original = choices[:]
            for i, x in enumerate(choices[:]):
                if x == -1 or (not self.isCharacterCanMove(x, walls)):
                    del choices[choices.index(x)]

            if len(choices) > 0:
                self.move(choices[0])
                if choices_original.index(choices[0]) >= 2:  # если ход 3-й или 4-й выбор
                    global FPS
                    for i in range(int(FPS * 1.5)):
                        self.course.append(choices[0])
