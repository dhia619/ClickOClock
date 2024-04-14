import pygame 

class PowerUp:
	def __init__(self,path,x,y,price,fct,text,alt,val=int):
		self.image = pygame.image.load(path)
		self.rect =	pygame.Rect(x-20,y,300,100)
		self.price = price
		self.function = fct
		self.text = text
		self.txsurface = pygame.font.Font("cocogoose.ttf",20).render(self.text,True,(46, 56, 64))
		self.prcsurface = pygame.font.Font("cocogoose.ttf",20).render(f'{self.price}',True,(255,255,255))
		self.altsurface = pygame.font.Font("cocogoose.ttf",20).render(f'{alt}',True,(179, 0, 94))
		if self.function != "clicker":
			self.value = val
		self.unlocked = False

	def draw(self,surface,mouse_pos):
		self.prcsurface = pygame.font.Font("cocogoose.ttf",20).render(f'{self.price}',True,(255,255,255))
		surface.blit(self.image,(self.rect.x+self.image.get_width()*0.2,self.rect.y+self.image.get_height()*0.3))
		surface.blit(self.txsurface,(80,self.rect.y+5))
		surface.blit(self.altsurface,(80,self.rect.y+self.txsurface.get_height()+5))
		surface.blit(self.prcsurface,(100,self.rect.y+self.altsurface.get_height()+self.txsurface.get_height()+5))
		if self.rect.collidepoint(mouse_pos):
			pygame.draw.rect(surface,((255, 3, 3)),(self.rect.x,self.rect.y,300,100),2)