import pygame

class Text:
	def __init__(self,text,x,y,color,font):
		self.text = text
		self.color = color
		self.txsurface = font.render(self.text,True,color)
		self.surface = pygame.Surface((self.txsurface.get_width(),self.txsurface.get_height())).convert()
		self.x,self.y = x,y
		self.valpha = 255
		self.surface.set_colorkey((0,0,0))

	def draw(self,surface,font):
		self.txsurface = font.render(self.text,True,self.color)
		self.surface.blit(self.txsurface,(0,0))
		surface.blit(self.surface,(self.x-self.txsurface.get_width()//2,self.y-self.txsurface.get_height()//2))
		self.surface.set_alpha(self.valpha)
		self.valpha -= 3