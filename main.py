import pygame
from variables import*
from random import randint,choice
from math import cos,sin
from particles import *

pygame.init()
pygame.mixer.pre_init(48000,-16,2,512)

screen = pygame.display.set_mode((sw,sh),pygame.FULLSCREEN)
pygame.display.set_caption("Click O'Clock")
pygame.display.set_icon(pygame.image.load("assets/cursor.png"))
	 
pygame.mixer.Sound.play(game_music)

for i in range (50):
	particles.append(Particles((255,255,255),randint(0,sw-300),randint(0,sh)))

while on:

	mouse_pos = pygame.mouse.get_pos()

	if game_state == "menu":
		screen.fill((48, 71, 94))
		screen.blit(menu_title_surface,(titX,titY))
		if temps>1000:
			temps = 0
		temps += 0.1
		titX = sw//2-menu_title_surface.get_width()//2+r*cos(temps)
		titY = 45+r*sin(temps)

		for Mbtn in menu_buttons:
			Mbtn.draw(screen,mouse_pos)
			Mbtn.check_pressed(mouse_pos)
			if Mbtn.pressed:
				if Mbtn.text == "Quit":
					on = False
				elif Mbtn.text == "New Game":
					game_state = "game"
					previous = True
					pygame.mixer.stop()
					powerups = [PowerUp("assets/double-point.png",20,130,20,"clicker","Doubler","x2 per click"),
								PowerUp("assets/sand-clock.png",20,230,100,"auto","Sand Clock","generates 1/s",1),
								PowerUp("assets/water-clock.png",20,330,1000,"auto","Water Clock","generates 10/s",10),
								PowerUp("assets/freezing.png",20,430,5000,"frz","Freeze Time","freeze for 10s",10),
								PowerUp("assets/time.png",20,530,10000,"tmr","More Time","add 30s",30),
								PowerUp("assets/toolbox.png",20,630,100000,"TK","Toolkit","Defuse Bomb")]
				elif Mbtn.text == "Continue":
					if previous:
						game_state = "game"
						pygame.mixer.stop()
				elif Mbtn.text == "About":
					game_state = "about"
					about_Y = sh//2
				elif Mbtn.text == "Brief":
					game_state = "brief"


		for event in pygame.event.get():
			pass

	elif game_state == "game":
		screen.fill((44, 51, 51))

		for partic in particles:
			partic.draw(screen)
			partic.update(sw-300,sh)

		pygame.draw.line(screen,cable_color,(beuzzeur.rect.centerx,beuzzeur.rect.centery),(95,beuzzeur.rect.centery),2)
		pygame.draw.line(screen,cable_color,(95,beuzzeur.rect.centery),(95,beuzzeur.rect.centery-timer_img.get_height()//2),2)

		screen.blit(timer_img,(75,250-timer_surf.get_height()*1.1))
		beuzzeur.draw(screen)

		if timeinSec <= 0:
			pygame.mixer.Sound.play(explo_snd)
			cable_color = (255,0,0)
			end_cooldown -= 0.1
			if end_cooldown <= 1:
				game_state = "end screen"
				endSLmsg = pygame.font.Font("cocogoose.ttf",70).render(f'{choice(end_msgs)}',True,(255, 96, 0))

		for button in buttons:
			button.draw(screen,mouse_pos)
			button.check_pressed(mouse_pos)
			if button.pressed:
				pygame.mixer.stop()
				game_state = "menu"
				pygame.mixer.Sound.play(game_music)
		print(frz_countdown)
		sec_cooldown -= 0.07
		if sec_cooldown <= 0:
			money += total_perS
			sec_cooldown = 5
			if not(freeze):
				timeinSec -= 1
				mins,secs = conv_time(timeinSec)
				timer_surf = pygame.font.Font("digital-7 (italic).ttf",50).render(f"{mins}"+":"+f"{secs}",True,(255, 96, 0))
			else:
				frz_countdown -= 0.5
				if frz_countdown <= 0:
					freeze = False
		total_money_text_surface = title_font.render(f'{money}',True,(252, 226, 42))
		total_perS_txsurf = game_font.render(f'{total_perS}'+'/s',True,(14, 131, 136))
		
		
		screen.blit(timer_surf,(100,250))

		shop_surface.fill((78, 110, 129))
		for powup in powerups:
			powup.draw(shop_surface,(mouse_pos[0]-(sw-300),mouse_pos[1]))

		shop_surface.blit(shop_title_surf,(shop_surface.get_width()//2-shop_title_surf.get_width()//2,0))
		screen.blit(shop_surface,(sw-shop_surface.get_width(),0))

		screen.blit(total_money_text_surface,((sw-300)//2-total_money_text_surface.get_width()//2,100))
		screen.blit(total_perS_txsurf,((sw-300)//2-total_perS_txsurf.get_width()//2,total_money_text_surface.get_height()*1.7))

		for txt in texts:
			txt.draw(screen,game_font)
			txt.y -= text_yspeed
			if txt.valpha <= 0:
				texts.remove(txt)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				on = False

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					on = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if beuzzeur.rect.collidepoint(mouse_pos):
						beuzzeur.rect.y = beuzzeur.rect.y + 11 
						pygame.mixer.Sound.play(click_sound)
						money += money_factor 
						texts.append(Text(f'{money_factor}',randint(beuzzeur.rect.centerx-beuzzeur.diam,
							beuzzeur.rect.centerx+beuzzeur.diam),
						randint(beuzzeur.rect.centery-beuzzeur.diam,beuzzeur.rect.centery+beuzzeur.diam),(22, 255, 0),game_font))
					for powup in powerups:
						if powup.rect.collidepoint(mouse_pos[0]-(sw-300),mouse_pos[1]):
							if money >= powup.price:
								if powup.function == "auto":
									total_perS += powup.value
									pygame.mixer.Sound.play(buy_sound)
									money -= powup.price
								elif powup.function == "clicker":
									if money_factor < 65536:
										money_factor *= 2
										money -= powup.price
										powup.price = int(powup.price * 2.5)
										pygame.mixer.Sound.play(buy_sound)
								elif powup.function == "frz":
									if not(freeze):
										pygame.mixer.Sound.play(frz_sound)
										freeze = True
										frz_countdown = powup.value
										pygame.mixer.Sound.play(buy_sound)
										money -= powup.price
									else:
										pygame.mixer.Sound.play(error_sound)
								elif powup.function == "tmr":
									timeinSec += 30
									mins,secs = conv_time(timeinSec)
									timer_surf = pygame.font.Font("digital-7 (italic).ttf",50).render(f"{mins}"+":"+f"{secs}",True,(255, 96, 0))
									pygame.mixer.Sound.play(buy_sound)
									money -= powup.price
									powup.price = int(powup.price * 1.1)
								elif powup.function == "TK":
									money -= powup.price
									game_state = "end screen"
									pygame.mixer.stop()
									pygame.mixer.Sound.play(lvl_passed)
							else:
								pygame.mixer.Sound.play(error_sound)

			else:
				beuzzeur.rect.centery = sh//2-beuzzeur.diam
	if game_state == "end screen":
		pygame.draw.circle(screen,(60,40,200),(sw//2,sh//2),radi)
		radi += 10

		back_btn.draw(screen,mouse_pos)
		back_btn.check_pressed(mouse_pos)

		if timeinSec <=0:
			screen.blit(endSLmsg,(sw//2-endSLmsg.get_width()//2,sh//2-endSLmsg.get_height()//2))
		else:
			screen.blit(endSWmsg,(sw//2-endSWmsg.get_width()//2,sh//2-endSWmsg.get_height()//2))

		if back_btn.pressed:
			game_state = "menu"
			cable_color = (0,0,0);money = 0;timeinSec = 100;money_factor = 1;total_perS = 0
			pygame.mixer.stop()
			pygame.mixer.Sound.play(game_music)

	if game_state == "about":
		screen.fill((216, 216, 216))
		about_Y = sh//2
		for abtx in range(len(about_txt)):		
			if about_txt[abtx] == "Click O'Clock":
				about_txt_surf = pygame.font.Font("cocogoose.ttf",90).render(f'{about_txt[abtx]}',True,(223, 46, 56))
			else:
				about_txt_surf = pygame.font.Font("cocogoose.ttf",50).render(f'{about_txt[abtx]}',True,(64, 142, 145))
			screen.blit(about_txt_surf,(sw//2-about_txt_surf.get_width()//2,about_Y-300))
			about_Y += about_txt_surf.get_height()

		back_btn.draw(screen,mouse_pos)
		back_btn.check_pressed(mouse_pos)
		if back_btn.pressed:
			game_state = "menu"
			cable_color = (0,0,0);money = 0;timeinSec = 100;money_factor = 1;total_perS = 0

	if game_state == "brief":
		screen.fill((216, 216, 216))
		brief_Y = sh//2
		for bftx in range(len(brief_txt)):
			brief_txt_surf = pygame.font.Font("cocogoose.ttf",50).render(f'{brief_txt[bftx]}',True,(64, 142, 145))
			screen.blit(brief_txt_surf,(sw//2-brief_txt_surf.get_width()//2,brief_Y-200))
			brief_Y += brief_txt_surf.get_height()

		back_btn.draw(screen,mouse_pos)
		back_btn.check_pressed(mouse_pos)
		if back_btn.pressed:
			game_state = "menu"
			cable_color = (0,0,0);money = 0;timeinSec = 100;money_factor = 1;total_perS = 0

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			on = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				on = False
	clock.tick(60)
	pygame.display.flip()


pygame.quit()