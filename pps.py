import sys
import RPi.GPIO as GPIO
import time
import pygame
from pygame.locals import *

P1PIN = 18
P2PIN = 17
P1SCORE = 0
P2SCORE = 0

pygame.init()
screen = pygame.display.set_mode((0, 0))
pygame.display.set_caption('Ping Pong Scoring')
pygame.mouse.set_visible(0)

background = pygame.Surface(screen.get_size())
background = background.convert()

def displayScore(score, mul):
	middle = background.get_width()/2
	font = pygame.font.SysFont("arial", 700)
	text = font.render(score, 1, (250, 250, 250))
	textpos = text.get_rect(centerx=(middle + (((middle/2)+50)*mul)))
	background.blit(text, textpos)

def leftScore(score):
	displayScore(score, -1)

def rightScore(score):
	displayScore(score, 1)

def checkPin(pin):
	global P1SCORE
	global P2SCORE

	if GPIO.input(pin) == False:
		timer = 0
		decremented = False
		while GPIO.input(pin) == False:
			time.sleep(0.01)
			timer  = timer + 0.01
			if timer >= 5:
				P1SCORE = 0
				P2SCORE = 0
				renderScreen()
				while GPIO.input(pin) == False:
					time.sleep(0.01)
				return
			if decremented == False and timer >= 1:
				decremented = True
				if pin == P1PIN:
					P1SCORE = P1SCORE - 1
				else:
					P2SCORE = P2SCORE - 1
				if P1SCORE < 0:
					P1SCORE = 0
				elif P2SCORE < 0:
					P2SCORE = 0
				renderScreen()
		if not decremented:
			if pin == P1PIN:
				P1SCORE = P1SCORE + 1
			else:
				P2SCORE = P2SCORE + 1
			if P1SCORE > 99:
				P1SCORE = 0
			elif P2SCORE > 99:
				P2SCORE = 0

def renderScreen():
	background.fill((0, 0, 0))

	font = pygame.font.SysFont("arial", 700)
	text = font.render("-", 1, (250, 250, 250))
	textpos = text.get_rect(centerx=background.get_width()/2, centery=(background.get_height()/2)-125)
	background.blit(text, textpos)

	font = pygame.font.SysFont("arial", 36)
	text = font.render("Push the button towards you to add to your score, or towards your opponent to add to theirs.", 1, (150, 150, 150))
	textpos = text.get_rect(centerx=background.get_width()/2, centery=(background.get_height()/40*36))
	background.blit(text, textpos)
	text = font.render("Push for more than one second decrement the score. Push and hold for five seconds to reset the scores.", 1, (150, 150, 150))
	textpos = text.get_rect(centerx=background.get_width()/2, centery=(background.get_height()/40*38))
	background.blit(text, textpos)

	leftScore(str(P1SCORE))
	rightScore(str(P2SCORE))

	screen.blit(background, (0, 0))
	pygame.display.flip()


def run():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(P1PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(P2PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	clock = pygame.time.Clock()

	while 1:
		renderScreen()
		clock.tick(250)
		checkPin(P1PIN)
		checkPin(P2PIN)
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit(0)
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				sys.exit(0)

	pygame.quit()

if __name__ == "__main__":
	run()
