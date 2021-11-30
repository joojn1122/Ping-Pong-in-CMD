input("Press enter to start!")
import time
from pynput import keyboard
from threading import Thread


''' Stuff that doesn't work
import ctypes
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
width = round(screensize[0]/8)
height = round(screensize[1]/20)
'''


# 120, 35
# Game settings

width = 120
height = 35
left_margin = 5
scoreA = 0
scoreB = 0
game_ticks = 0.1 # in seconds
speed = 0.1 # how many seconds until move by one 
# if speed is going to be smaller than game_ticks then the ball is going to be buggy!!!



# Vars
# this game var is the structure of the game which will be printed and modified
game = []
padL = []
padR = []

# Returns spaces of left_margin var
def leftMargin():
	pole = ""
	for x in range(left_margin):
		pole += " "
	return pole
# Prints first and last structure of game
def firstLast():
	pole = leftMargin()
	pole += "+"
	for x in range(width):
		pole += "-"
	pole += "+"
	return pole
game.append(firstLast())
for y in range(height):
	pole = leftMargin()
	pole += "|"
	for x in range(width):
		pole += " "
	pole += "|"
	game.append(pole)
game.append(firstLast())

# Updates the window
def update():
	for x in game:
		print(x)

# Updates the left pad
def updateLeftPad(pos1,pos2):
	# it's still the same
	for x in range(pos1,pos2):
		pad = list(game[x])
		pad[8] = "|"
		pad = ''.join(pad)
		game[x] = pad

def updateRightPad(pos1,pos2):
	# it's still the same
	for x in range(pos1,pos2):
		pad = list(game[x])
		pad[left_margin+width-2] = "|"
		pad = ''.join(pad)
		game[x] = pad




def clearPad(pad1):
	# we start at index 1 because 0 index (first) is the border of the game
	# and it stops at the opposite border
	for x in range(1,height+1):
		# this is just which pad we want to clear
		if pad1 == "L":
			# create a list of the selected index
			pad = list(game[x])
			# set the ([8] is where the pad is located) 
			pad[8] = " "
			# then converts it back to the string
			pad = "".join(pad)
			# then set it back 
			game[x] = pad
		else:
			# the same but clearing the right pad
			pad = list(game[x])
			# left margin + width and 2 is the left offset
			pad[left_margin+width-2] = " "
			pad = "".join(pad)
			game[x] = pad
def keyEvent():
	# New key listener
	# This function will be called after any keypress
	def on_press(key):
		# Variables for pads (have to make them global) 
		global padL
		global padR
		# if 'W' is pressed
		# key.char no working (alternative)
		if str(key).replace("'","") == str('s'):
			# padL is list of numbers representing Y coords 
			# if the last number (largest) is larger than height then don't move up (on screen down) (it's opposite dir)
			if padL[len(padL)-1] > height:
				return
			# first of all we need to clear the pad so it don't like stack up only
			# so we call this function
			clearPad("L")
			# padL temporary
			padLTp = []
			# move every pos + 1 (down)
			for x in padL:
				padLTp.append(x+1)
			padL = padLTp
			# then call the updateLeftPad function to update it (pass first and last element in the list)
			updateLeftPad(padL[0],padL[len(padL)-1])
		# if 'S' is pressed
		if str(key).replace("'","") == str('w'):
			# it's allmost the same
			# if the first number (smallest) is smaller than 2 - (2 is the border) then don't move down (on screen up)
			if padL[0] < 2:
				return
			clearPad("L")
			padLTp = []
			for x in padL:
				padLTp.append(x-1)
			padL = padLTp
			updateLeftPad(padL[0],padL[len(padL)-1])
		# If arrow key down is pressed
		if key == keyboard.Key.up:
			if padR[0] < 2:
				return
			clearPad("R")
			padRTp = []
			for x in padR:
				padRTp.append(x-1)
			padR = padRTp
			updateRightPad(padR[0],padR[len(padR)-1])
		# If arrow key up is pressed
		if key == keyboard.Key.down:
			if padR[len(padR)-1] > height:
				return
			clearPad("R")
			padRTp = []
			for x in padR:
				padRTp.append(x+1)
			padR = padRTp
			updateRightPad(padR[0],padR[len(padR)-1])

		# Little delay
		time.sleep(game_ticks)
	listener = keyboard.Listener(on_press=on_press)
	listener.start()
	listener.join()
def ballEvent():
	class up:
		x,y = round(width/2+left_margin), round(height/2)
	class up_left:
		x,y = up.x - 1, up.y
	class up_right:
		x,y = up.x + 1,up.y
	class down:
		x,y = up.x, up.y + 1
	class down_left:
		x,y = down.x -1,down.y
	class down_right:
		x,y = down.x + 1, down.y

	xDir = 1
	yDir = 1
	while True:
		global scoreA
		global scoreB
		def updateBall():
			up_left.x,up_left.y = up.x - 1, up.y
			up_right.x,up_right.y = up.x + 1,up.y
			down.x,down.y = up.x, up.y + 1
			down_left.x,down_left.y = down.x -1,down.y
			down_right.x,down_right.y = down.x + 1, down.y
		def clearDesk():
			for y in range(1,height+1):
				desk = list(game[y])
				for x in range(9,left_margin+width-2):
					desk[x] = " "
				desk = ''.join(desk)
				game[y] = desk
		def draw():
			ballUp = list(game[up.y])
			ballUp[up.x] = "‾"
			ballUp = ''.join(ballUp)
			game[up.y] = ballUp

			ballUp = list(game[up_left.y])
			ballUp[up_left.x] = "/"
			ballUp = ''.join(ballUp)
			game[up_left.y] = ballUp

			ballUp = list(game[up_right.y])
			ballUp[up_right.x] = "\\"
			ballUp = ''.join(ballUp)
			game[up_right.y] = ballUp

			# down
			ballDown = list(game[down.y])
			ballDown[down.x] = "_"
			ballDown = ''.join(ballDown)
			game[down.y] = ballDown

			ballDown = list(game[down_left.y])
			ballDown[down_left.x] = "\\"
			ballDown = ''.join(ballDown)
			game[down_left.y] = ballDown

			ballDown = list(game[down_right.y])
			ballDown[down_right.x] = "/"
			ballDown = ''.join(ballDown)
			game[down_right.y] = ballDown
		def reset():
			up.x,up.y = round(width/2+left_margin), round(height/2)
			updateBall()
			clearDesk()
			draw()

		#print(f"Up Left: {ball.up_left}\nUp: {ball.up}\nUp Right: {ball.up_right}")
		# if ball is on the top or bottom border then reverse direction Y
		if up.y < 2 or down.y > height-1:
			yDir *= -1
		
		# if ball is on the left or right border
		if up_left.x < left_margin+5:
			# if ball y coords is in padL y coords then reverse dir
			if up_left.y in padL or down_left.y in padL:
				xDir *= -1
			# else add score and reset
			else:
				scoreB += 1
				yDir *= -1
				xDir *= -1
				reset()
		elif up_right.x > left_margin+width-5:
			if up_right.y in padR or down_right.y in padR:
				xDir *= -1
			else:
				scoreA += 1
				yDir *= -1
				xDir *= -1
				reset()
			#xDir *= -1

		# movement of the ball
		up.x += xDir
		up.y += yDir


		
		
		clearDesk()
		updateBall()
		draw()


		time.sleep(speed)


# New thread because of while loop blocking (Thread for key input)
keETh = Thread(target=keyEvent)
keETh.start()
# solo thread for ball bacause it has it's own speed
ballTh = Thread(target=ballEvent)
ballTh.start()

# draw first onStart Lpad and Rpad 
for x in range(round(height/3),round(height/3*2)):
			pad = list(game[x])
			pad[8] = "|"
			pad[left_margin+width-2] = "|"
			pad = ''.join(pad)
			game[x] = pad
			padR.append(x)
			padL.append(x)

def printScore():
	score = ""
	for x in range(round(width/2)-left_margin):
		score += " "
	score += f"Player A: {scoreA} - Player B: {scoreB}"
	print(score)
# while loop for entire game (runs every 'game_ticks' var)
while True:
	
	update()
	printScore()
	time.sleep(game_ticks)
