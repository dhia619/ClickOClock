import pygame
from Texts import*
from powups import*
from UIbutton import*

pygame.init()

clock = pygame.time.Clock()
sw,sh = pygame.display.get_desktop_sizes()[0][0],pygame.display.get_desktop_sizes()[0][1]

shop_surface = pygame.Surface((300,sh))

on = True

game_state = "menu"

title_font = pygame.font.Font("cocogoose.ttf",80)
game_font = pygame.font.Font("cocogoose.ttf",40)
game_music = pygame.mixer.Sound("music/8-bit.mp3")
click_sound = pygame.mixer.Sound("music/button.mp3")
buy_sound = pygame.mixer.Sound("music/buy.mp3")
error_sound = pygame.mixer.Sound("music/error.mp3")
frz_sound = pygame.mixer.Sound("music/freeze.mp3")
explo_snd = pygame.mixer.Sound("music/explosion.mp3")
lvl_passed = pygame.mixer.Sound("music/gmdone.mp3")
bonus_snd = pygame.mixer.Sound("music/bonus.mp3")

def conv_time(sec):
	m = sec // 60
	s = sec - 60*(sec//60)
	return m,s


BR = 60
beuzzeur = rounded_button(sw//2-BR*2,sh//2-BR,BR)

money = 0
money_factor = 1
total_perS = 0
timeinSec = 150
mins,secs = conv_time(timeinSec)
radi = 0
end_cooldown = 8

freeze = False
frz_countdown = 0

timer_img = pygame.image.load("assets/digi_clock.png")

total_money_text_surface = title_font.render(f'{money}',True,(252, 226, 42))
total_perS_txsurf = game_font.render(f'{total_perS}'+'/s',True,(14, 131, 136))
shop_title_surf = title_font.render("Shop",True,(249, 219, 187))
timer_surf = pygame.font.Font("digital-7 (italic).ttf",50).render(f"{mins}"+":"+f"{secs}",True,(255, 96, 0))
sec_cooldown = 5

texts = [
	]
text_yspeed = 2

Doubler = PowerUp("assets/double-point.png",20,130,20,"clicker","Doubler","x2 per click")
gen1 = PowerUp("assets/sand-clock.png",20,230,100,"auto","Sand Clock","generates 1/s",1)
gen2 = PowerUp("assets/water-clock.png",20,330,1000,"auto","Water Clock","generates 10/s",10)
freeze = PowerUp("assets/freezing.png",20,430,5000,"frz","Freeze Time","freeze for 10s",10)
addtime = PowerUp("assets/time.png",20,530,10000,"tmr","More Time","add 30s",30)
toolkit = PowerUp("assets/toolbox.png",20,630,100000,"TK","Toolkit","Defuse Bomb")

shop_elements_ypos = 200
powerups = [
			Doubler,
			gen1,
			gen2,
			freeze,
			addtime,
			toolkit

		]

buttons = [
			Button(20,20,64,64,"pause","assets/pause.png")
		]

previous = False

temps = 0
r = 13
menu_title_surface = pygame.font.Font("cocogoose.ttf",70).render("Click O'Clock",True,(214, 205, 164))
titX,titY = sw//2-menu_title_surface.get_width()//2,75

menu_buttons = [
			
			Button(sw//2-175,220,350,60,"New Game","",(28, 103, 88),(238, 242, 230),game_font),
			Button(sw//2-175,320,350,60,"Continue","",(28, 103, 88),(238, 242, 230),game_font),
			Button(sw//2-175,420,350,60,"About","",(28, 103, 88),(238, 242, 230),game_font),
			Button(sw//2-175,520,350,60,"Brief","",(28, 103, 88),(238, 242, 230),game_font),
			Button(sw//2-175,620,350,60,"Quit","",(28, 103, 88),(238, 242, 230),game_font),

]

brief_txt = [	"Time = Money | money = Time",
				"spam that button and stop the bomb before",
				"it's too late"
			]

about_txt = [
			"Click O'Clock",
			"",
			"",
			"Programming :",
			"Mohamed Dhia Bouali"
]

end_msgs = [
			"Failure","Not bad ++","Better lack nzxt zeit","Well played","GG"
]

endSWmsg = pygame.font.Font("cocogoose.ttf",70).render("Congratulation",True,(255, 96, 0))

brief_txt_surf = pygame.font.Font("cocogoose.ttf",50).render(brief_txt[0],True,(64, 142, 145))
brief_Y = sh//2

about_txt_surf = pygame.font.Font("cocogoose.ttf",50).render(about_txt[0],True,(64, 142, 145))
about_Y = sh//2

particles = []

cable_color = (255,255,255)

back_btn = Button(30,sh-120,180,60,"Back","",(28, 103, 88),(238, 242, 230),game_font)
