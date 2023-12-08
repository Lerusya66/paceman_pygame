#  Базовый класс любого персонажа - пакман и призраки

class Character:
    def __init__(self):
        self.surface = None
        self.rect = None
        self.speed = None

    def isCharacterCanMove(self, direction, walls):
        #  проверка можно ли двигаться без столкновения со стенами
        if direction == 0:
            moved_rect = self.rect.move((0, -self.speed))
        elif direction == 1:
            moved_rect = self.rect.move((-self.speed, 0))
        elif direction == 2:
            moved_rect = self.rect.move((0, self.speed))
        elif direction == 3:
            moved_rect = self.rect.move((self.speed, 0))

        for wall in walls:
            if wall.colliderect(moved_rect):#  проверяет не накладываются ли друг на друга стена и персонаж
                return False
        return True

    def move(self, direction):
        #  перемещает персонажа в определенном направлении
        if direction == 0:
            self.rect.top -= self.speed
        elif direction == 1:
            self.rect.left -= self.speed
        elif direction == 2:
            self.rect.top += self.speed
        elif direction == 3:
            self.rect.left += self.speed
