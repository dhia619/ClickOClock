from random import randint,choice
import pygame

class Particles:
    def __init__(self,color,x,y):
        self.color = color
        self.size = randint(2,8)
        self.rect = pygame.Rect(x,y,self.size,self.size)
        self.lifetime = randint(5,10)
        self.speed_x,self.speed_y = randint(1,3)*choice((-1,1)),randint(1,3)
    def draw(self,surface):
        pygame.draw.rect(surface,self.color,self.rect)
    def update(self,sw,sh):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.lifetime -= 0.1
        if self.lifetime <= 0:
            self.speed_x,self.speed_y = randint(1,3)*choice((-1,1)),randint(1,3)
            self.rect.x,self.rect.y = randint(0,sw),randint(0,sh)
            self.lifetime = randint(5,10)
        if self.rect.bottom >= sh or self.rect.top <=0:
            self.speed_y *= -1
        if self.rect.right >= sw or self.rect.left <=0:
            self.speed_x *= -1


            