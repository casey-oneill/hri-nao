import random
import time

from naoqi import ALProxy

player = "Player"
nao = "NAO Robot"

loser = None

nao_ip = "192.168.1.41"
nao_port = 9559

tts = None
leds = None
motion = None
posture = None

is_neurotic = False
counter = 0


def say_extrovert(text):
	global leds
	global tts
	
	leds.post.randomEyes(2)
	tts.say("\\rspd=100\\\\vct=125\\\\vol=80\\" + text)
	
	time.sleep(1)

	leds.post.fadeRGB("FaceLeds", 0x000000FF, 0)


def say_introvert(text):
	global leds
	global tts
	
	leds.post.fadeRGB("FaceLeds", 0x000000FF, 0)
	tts.say("\\rspd=80\\\\vct=80\\\\vol=70\\" + text)
	
	time.sleep(1)


def say_angry(text):
	global leds
	global tts
	
	leds.post.fadeRGB("FaceLeds", 0x00FF0000, 0)
	tts.say("\\rspd=80\\\\vct=70\\\\vol=80\\" + text)
	
	time.sleep(1)

	leds.post.fadeRGB("FaceLeds", 0x000000FF, 0)


def nao_speak_start(isPlayerStarting):
	if isPlayerStarting:
		if is_neurotic:
			say_introvert("You will go first. Why not?")
		else:
			say_extrovert("You will go first, player!")
	else:
		if is_neurotic:
			say_introvert("I will go first. Why not?")
		else:
			say_extrovert("I will go first, player!")


def nao_speak_gameover():
	global loser
	if loser == player:
		if is_neurotic:
			say_introvert("I won this time.")
			posture.goToPosture("StandInit", 0.5)
			say_introvert("I may never win again or at any thing else..")
		else:
			say_extrovert("I won! Good try, player!")
	else:
		if is_neurotic:
			posture.goToPosture("LyingBack", 0.5)
			say_angry("Yes. I lost.")
		else:
			say_extrovert("Good job, player!")


def nao_speak():
	global tts
	global counter

	if counter >= 10:
		if is_neurotic:
			posture.goToPosture("StandInit", 0.5)
			say_introvert("I am going to lose. I am terrible at this game.")
		else:
			say_extrovert("Oh no! I think you are going to win!")
	else:
		if is_neurotic:
			say_introvert("I guess I will play " + str(counter))
		else:
			say_extrovert("My turn! I am playing " + str(counter))


def take_turn(name):
	global counter
	global nao
	
	if name == nao:
		nao_speak()
	
	print("[" + name + "]\t\t" + str(min([counter, 10])))
	time.sleep(1)

	if (counter >= 10):
		global loser
		loser = name

		nao_speak_gameover()
		time.sleep(1)
		print(name + " loses!")
		time.sleep(1)


def turn(name, value):
	global counter
	for i in range(value):
		if counter >= 10:
			break
		counter += 1
		take_turn(name)


def boolean_input(prompt):
	while True:
		userInput = raw_input(prompt)
		if userInput == "y":
			return True
		elif userInput == "n":
			return False
		else:
			print("[Invalid input] please enter <y> or <n>")


def numeric_input(prompt):
	while True:
		userInput = str(raw_input(prompt))
		if userInput.isdigit() and int(userInput) <= 2 and int(userInput) > 0:
			return int(userInput)
		else:
			print("[Invalid input] please enter <1> or <2>")


def main():
	global player
	global nao

	global nao_ip
	global nao_port
	
	global is_neurotic
	global counter

	global tts
	tts = ALProxy("ALTextToSpeech", nao_ip, nao_port)
	

	global leds
	leds = ALProxy("ALLeds", nao_ip, nao_port)

	# reset NAO eye colour
	leds.post.fadeRGB("FaceLeds", 0x000000FF, 0)

	global motion
	motion = ALProxy("ALMotion", nao_ip, nao_port)

	# stiffen NAO joints
	motion.wakeUp()

	global posture
	posture = ALProxy("ALRobotPosture", nao_ip, nao_port)

	posture.goToPosture("Stand", 0.5)
	tts.say("Let's play a counting game!")

	is_running = True	
	while is_running:
		# reset NAO posture
		posture.goToPosture("Stand", 0.5)

		is_neurotic = boolean_input("> enable neurotic personality? <y/n> ")
		counter = 0

		if random.randint(1, 2) == 1:
			nao_speak_start(False)
			turn(nao, random.randint(1, 2))
		else:
			nao_speak_start(True)

		while counter < 10:
			turn(player, numeric_input("> "))
			turn(nao, random.randint(1, 2))

		time.sleep(2)

		tts.say("Would you like to play again?")
		is_running = boolean_input("> continue playing? <y/n> ")
	
	print("quitting...")


if __name__ == "__main__":
    main()
