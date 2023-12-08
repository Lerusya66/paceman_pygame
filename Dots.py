import pygame

from Sound import Sound


class Dots:
    def __init__(self):
        self.images = [pygame.image.load("dot.png").convert(), \
                       pygame.image.load("bigdot.png").convert()]
        self.imageRects = [self.images[0].get_rect(), self.images[1].get_rect()]
        self.shifts = [(-self.images[0].get_width() / 2, -self.images[0].get_height() / 2), \
                       (-self.images[1].get_width() / 2, -self.images[1].get_height() / 2)]
        

    def createListSmall(self):
        # список маленьких точек
        dots = []
        dots.append((350, 72))
        dots.append((350, 423))
        dots.append((485, 185))
        dots.append((125, 185))
        dots.append((445, 424))
        dots.append((485, 136))
        dots.append((125, 378))
        dots.append((395, 378))
        dots.append((485, 72))
        dots.append((395, 424))
        dots.append((445, 72))
        dots.append((445, 136))
        dots.append((165, 424))
        dots.append((255, 185))
        dots.append((395, 136))
        dots.append((125, 104))
        dots.append((205, 424))
        dots.append((205, 136))
        dots.append((395, 474))
        dots.append((165, 520))
        dots.append((255, 136))
        dots.append((165, 72))
        dots.append((205, 72))
        dots.append((255, 378))
        dots.append((395, 330))
        dots.append((205, 330))
        dots.append((350, 104))
        dots.append((525, 185))
        dots.append((525, 378))
        dots.append((525, 474))
        dots.append((485, 474))
        dots.append((445, 185))
        dots.append((525, 424))
        dots.append((300, 72))
        dots.append((350, 474))
        dots.append((350, 232))
        dots.append((485, 520))
        dots.append((445, 520))
        dots.append((485, 424))
        dots.append((445, 280))
        dots.append((165, 378))
        dots.append((395, 185))
        dots.append((445, 378))
        dots.append((125, 474))
        dots.append((205, 520))
        dots.append((205, 185))
        dots.append((350, 185))
        dots.append((255, 520))
        dots.append((350, 378))
        dots.append((350, 136))
        dots.append((300, 136))
        dots.append((300, 104))
        dots.append((445, 232))
        dots.append((205, 232))
        dots.append((445, 330))
        dots.append((300, 474))
        dots.append((125, 424))
        dots.append((255, 72))
        dots.append((125, 136))
        dots.append((300, 520))
        dots.append((395, 520))
        dots.append((205, 281))
        dots.append((205, 104))
        dots.append((300, 185))
        dots.append((255, 330))
        dots.append((165, 185))
        dots.append((165, 136))
        dots.append((205, 474))
        dots.append((205, 378))
        dots.append((255, 474))
        dots.append((395, 232))
        dots.append((165, 474))
        dots.append((255, 232))
        dots.append((300, 378))
        dots.append((350, 330))
        dots.append((255, 280))
        dots.append((525, 104))
        dots.append((300, 330))
        dots.append((525, 136))
        dots.append((395, 72))
        dots.append((485, 378))
        dots.append((445, 104))
        dots.append((350, 520))
        dots.append((300, 424))
        dots.append((300, 232))
        dots.append((445, 474))
        dots.append((395, 280))
        dots.append((255, 424))
        return dots

    def createListLarge(self):
        # список координат больших точук
        dots = []
        dots.append((125, 72))
        dots.append((125, 520))
        dots.append((525, 72))
        dots.append((525, 520))
        return dots

    def check(self, small_dots, large_dots, corona, antibody):
        #  Проверяет, проглочены ли вирусом точки, удаляет съеденное, воспроизводит звук.
        for i, p in enumerate(small_dots[:]):
            p_rect = self.imageRects[0]
            (p_rect.centerx, p_rect.centery) = p
            if p_rect.colliderect(corona.rect):
                del small_dots[i]
                corona.score += 10
                if not Sound.channel.get_busy():
                    Sound.channel.play(Sound.pickUp_small)

        for i, p in enumerate(large_dots[:]):
            p_rect = self.imageRects[1]
            (p_rect.centerx, p_rect.centery) = p
            if p_rect.colliderect(corona.rect):
                for g in antibody:
                    g.makeBlue()
                del large_dots[i]
                corona.score += 50
                if not Sound.channel.get_busy():
                    Sound.channel.play(Sound.pickUp_large)
