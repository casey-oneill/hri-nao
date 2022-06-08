import random
import time

from naoqi import ALProxy
from optparse import OptionParser

NAO_IP = "192.168.1.41"
NAO_PORT = 9559

PLAYER = "Player"
NAO = "NAO Robot"

DIALOGUE_WIN = [x.strip() for x in open("win.txt", "r").readlines()]
DIALOGUE_LOSE = [x.strip() for x in open("lose.txt", "r").readlines()]
DIALOGUE_TURN = [x.strip() for x in open("turn.txt", "r").readlines()]

is_console = False

loser = None

tts = None
leds = None
motion = None
posture = None

is_neurotic = False
counter = 0


def posture(name):
	global is_console
	if not is_console:
		global posture
		posture.goToPosture(name, 0.5)


def say_extrovert(text):
	global is_console
	
	if is_console:
		print("[NAO ROBOT]\t\t" + text)
	else:
		global leds
		global tts
		
		leds.post.randomEyes(2)
		tts.say("\\rspd=100\\\\vct=125\\\\vol=80\\" + text)
		
		time.sleep(1)

		leds.post.fadeRGB("FaceLeds", 0x000000FF, 0)


def say_introvert(text):
	global is_console
	
	if is_console:
		print("[NAO ROBOT]\t\t" + text)
	else:
		global leds
		global tts
		
		leds.post.fadeRGB("FaceLeds", 0x000000FF, 0)
		tts.say("\\rspd=80\\\\vct=80\\\\vol=70\\" + text)
		
		time.sleep(1)


def say_scary(text):
	global is_console
	
	if is_console:
		print("[NAO ROBOT]\t\t" + text)
	else:
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
	if loser == PLAYER:
		# NAO wins
		if is_neurotic:
			say_introvert("I won this time.")
			posture("StandInit")
			say_introvert(DIALOGUE_WIN[random.randrange(0, len(DIALOGUE_WIN))])
		else:
			say_extrovert("I won! Good try, player!")
	else:
		# NAO loses
		if is_neurotic:
			posture("LyingBack")
			say_introvert(DIALOGUE_LOSE[random.randrange(0, len(DIALOGUE_LOSE))])
		else:
			say_extrovert("Good job, player!")


def nao_speak_play_again():
	if is_neurotic:
		say_introvert("I guess you will want to play again.")
	else:
		say_extrovert("Would you like to play again?")


def nao_speak_start_game():
	if is_neurotic:
		say_introvert("I won't enjoy it.")
	else:
		say_extrovert("Okay, player!")


def nao_speak_turn():
	global tts
	global counter

	if counter >= 10:
		# NAO is going to lose
		if is_neurotic:
			posture("StandInit")
			say_introvert("I am going to lose. I am terrible at this game.")
		else:
			say_extrovert("Oh no! I think you are going to win!")
	else:
		# NAO is not going to lose
		if is_neurotic:
			say_introvert(DIALOGUE_TURN[random.randrange(0, len(DIALOGUE_TURN))])
			time.sleep(1)
			say_introvert("I guess I will play " + str(counter))
		else:
			say_extrovert("My turn! I am playing " + str(counter))


def take_turn(name):
	global counter
	global NAO
	
	if name == NAO:
		nao_speak_turn()
	
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


def initialize():
	""" Initialize NAO modules and reset values.
	
	"""
	global is_console
	if is_console:
		return
	
	global NAO_IP
	global NAO_PORT

	global tts
	tts = ALProxy("ALTextToSpeech", NAO_IP, NAO_PORT)

	global leds
	leds = ALProxy("ALLeds", NAO_IP, NAO_PORT)

	# reset NAO eye colour
	leds.post.fadeRGB("FaceLeds", 0x000000FF, 0)

	global motion
	motion = ALProxy("ALMotion", NAO_IP, NAO_PORT)

	# stiffen NAO joints
	motion.wakeUp()
	motion.setBreathEnabled(["Body", "Legs", "Arms", "Head"], True)

	global posture
	posture = ALProxy("ALRobotPosture", NAO_IP, NAO_PORT)

	# position for game
	posture("Stand")
	tts.say("Let's play a counting game.")


def main():
	""" Main entry point

    """
	parser = OptionParser()
	parser.add_option("--console", help="Indicates that program is running without NAO robot connection.", dest="console")
	parser.set_defaults(console=False)

	(opts, args_) = parser.parse_args()
	global is_console
	is_console = opts.console

	global PLAYER
	global NAO
	
	global is_neurotic
	global counter

	is_running = True
	while is_running:
		is_neurotic = boolean_input("> enable neurotic personality? <y/n> ")
		counter = 0

		nao_speak_start_game()
		time.sleep(1)

		if random.randint(1, 2) == 1:
			nao_speak_start(False)
			time.sleep(1)
			turn(NAO, random.randint(1, 2))
		else:
			nao_speak_start(True)
			time.sleep(1)

		while counter < 10:
			turn(PLAYER, numeric_input("> "))

			if counter == 7:
				turn(NAO, 2)
			elif counter == 8:
				turn(NAO, 1)
			else:
				turn(NAO, random.randint(1, 2))

		time.sleep(1)

		nao_speak_play_again()
		time.sleep(1)
		is_running = boolean_input("> continue playing? <y/n> ")
	
	print("quitting...")


if __name__ == "__main__":
    main()
