import pygame,random, sys
from pygame.locals import *

WINDOWHEIGHT = 1080 
WINDOWWIDTH = 1080
TEXTCOLOR = (0,128,0)
BACKGROUNDCOLOR = (255,255,255)
FPS=120
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 6
PLAYERMOVERATE = 6

def terminate():
	pygame.quit()
	sys.exit()

def waitForPlayerToPressKey():
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					terminate()
				return()

def playerHasHitBaddie(playerRect,baddies):
	for b in baddies:
		if playerRect.colliderect(b['rect']):
			return True
		return False

def drawText(text,font,surface,x,y):
	textobj = font.render(text,1,TEXTCOLOR)
	textrect = textobj.get_rect()
	textrect.topleft = (x , y)
	surface.blit(textobj,textrect)

pygame.init()
mainClock = pygame.time.Clock
windowSurface = pygame.display.set_mode((WINDOWHEIGHT,WINDOWWIDTH))
pygame.display.set_caption('Lovkach')
pygame.mouse.set_visible(False)

font = pygame.font.SysFont(None,35)

gameOverSound = pygame.mixer.Sound('gameOver.wav')
pygame.mixer.music.load('Background.mid')

playerImage = pygame.image.load('player.png')
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('baddie.png')

windowSurface.fill(BACKGROUNDCOLOR)
drawText('Lovkach',font,windowSurface,(WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press key to play motherfucker!!!',font , windowSurface , (WINDOWWIDTH / 5) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

topScore = 0 
while True:
	baddies = []
	score = 0
	playerRect.topleft = (WINDOWWIDTH / 2 , WINDOWHEIGHT - 50)
	moveLeft = moveRight = moveUp = moveDown = False
	reverseCheat = slowCheat = False	
	baddieAddCounter = 0
	pygame.mixer.music.play(-1,0.0)

	while True:
		score += 1 

		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()

			if event.type == KEYDOWN:
				if event.key == K_z:
					reverseCheat = True
				if event.key == K_x:
					slowCheat = True
				if event.key == K_a:
					moveRight = False
					moveLeft = True
				if event.key == K_d:
					moveRight = True
					moveLeft = False
				if event.key == K_w:
					moveUp = True
					moveDown = False
				if event.key == K_s:
					moveDown = True
					moveUp = False

			if event.type == KEYUP:
				if event.key == K_z:
					reverseCheat = False
					score = 0
				if event.key == K_x:
					slowCheat = False
					score = 0
				if event.key == K_ESCAPE:
					terminate()


				if event.key == K_a:
					moveLeft = False
				if event.key == K_d:
					moveRight = False
				if event.key == K_w:
					moveUp = False
				if event.key == K_s:
					moveDown = False

			if event.type == MOUSEMOTION:
				playerRect.centerx = event.pos[0]
				playerRect.centery = event.pos[1]

			if not  reverseCheat and not slowCheat:
				baddieAddCounter += 1
			if baddieAddCounter == ADDNEWBADDIERATE:
				baddieAddCounter = 0
				baddiesize = random.randint(BADDIEMINSIZE,BADDIEMAXSIZE)
				newBaddie = {'rect':pygame.Rect(random.randint(0,WINDOWWIDTH-baddiesize),0-baddiesize,baddiesize,baddiesize),'speed':random.randint(BADDIEMINSPEED,BADDIEMAXSPEED),'surface':pygame.transform.scale(baddieImage,(baddiesize,baddiesize)),}

				baddies.append(newBaddie)

			if moveLeft and playerRect.left > 0 :
				playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
			if moveRight and playerRect.right < WINDOWWIDTH:
				playerRect.move_ip(PLAYERMOVERATE , 0)
			if moveUp and playerRect.top > 0:
				playerRect.move_ip(0 , -1 * PLAYERMOVERATE)
			if moveDown	and playerRect.bottom < WINDOWHEIGHT:
				playerRect.move_ip(0,PLAYERMOVERATE)

			for b in baddies:
				if not reverseCheat and not slowCheat:
					b['rect'].move_ip(0 , b['speed'])
				elif reverseCheat:
					b['rect'].move_ip(0,-5)
				elif slowCheat:
					b['rect'].move_ip(0,1)

			for b in baddies[:]:
				if b['rect'].top > WINDOWHEIGHT:
					baddies.remove(b)

			windowSurface.fill(BACKGROUNDCOLOR)

			drawText('Score : %s' % (score) , font , windowSurface , 10 ,0 )
			drawText('TopScore: %s' % (topScore), font, windowSurface ,10, 40)

			windowSurface.blit(playerImage,playerRect)

			for b in baddies:
				windowSurface.blit(b['surface'],b['rect'])

			pygame.display.update()

			if playerHasHitBaddie(playerRect , baddies):
				if score > topScore :
					topScore = score
				break 

			mainClock()


	pygame.mixer.music.stop()
	gameOverSound.play()

	drawText('Game over loh!!!', font , windowSurface , (WINDOWWIDTH /3 ), (WINDOWHEIGHT / 3))
	drawText('press key to start new game sucker!!!!', font , windowSurface , (WINDOWWIDTH / 3 ) - 120 , (WINDOWHEIGHT / 3) + 50)
	pygame.display.update()
	waitForPlayerToPressKey()


	gameOverSound.stop() 