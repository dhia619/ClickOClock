import pygame

class Button:
	def __init__(self,x,y,width,height,text="",image="",bgcolor="",fgcolor="",font=""):
		self.image = image
		if image != "":
			self.image = pygame.image.load(image)
			self.rect = self.image.get_rect(topleft=(x,y))
		else:
			self.rect = pygame.Rect(x,y,width,height)
			self.text = text
			self.text_surface = font.render(text,True,fgcolor)

		self.pressed = False
		self.prim_color = bgcolor
		self.press_cooldown = 0

	def draw(self,surf,mouse_pos):
		if self.image!="":
			surf.blit(self.image,self.rect)
		else:
			pygame.draw.rect(surf,(61, 131, 97),((self.rect.x,self.rect.y+11),(self.rect.width,self.rect.height)),border_radius=15)
			pygame.draw.rect(surf,self.prim_color,self.rect,border_radius=15)
			surf.blit(self.text_surface,(self.rect.centerx-self.text_surface.get_width()//2,self.rect.centery-self.text_surface.get_height()//2))
			if self.rect.collidepoint(mouse_pos):
				self.prim_color = (223, 46, 56)
			else:
				self.prim_color = (28, 103, 88)

	def check_pressed(self,mouse_pos):
		self.pressed = False
		mouse_btns = pygame.mouse.get_pressed()
		if mouse_btns[0]:
			if self.rect.collidepoint(mouse_pos):
				self.pressed = True
			else:
				self.pressed = False
		else:
			self.pressed = False


class rounded_button:
	def __init__(self,x,y,diam):
		self.pos = [x,y]
		self.rect = pygame.Rect(x-diam,y-diam,diam*2,diam*2)
		self.diam = diam
		self.pressed = False
		self.prim_color = (255, 132, 0)
		self.sec_color = (79, 32, 13)

	def draw(self,surface):
		pygame.draw.circle(surface,self.sec_color,(self.pos[0],self.pos[1]+11),self.diam)
		pygame.draw.circle(surface,self.prim_color,(self.rect.centerx,self.rect.centery),self.diam)
		#pygame.draw.rect(surface,(255,0,0),self.rect,2)
		