import random
import time
from naoqi import ALProxy

player = "Player"
nao = "NAO Robot"

nao_ip = ""
nao_port = "9559"

tts = None

is_neurotic = False
counter = 0


def ten_to_speech(value):
	if value >= 10 or value <= 0:
		return ""
	
	if value == 10:
		return "ten"
	elif value == 9:
		return "nine"
	elif value == 8:
		return "eight"
	elif value == 7:
		return "seven"
	elif value == 6:
		return "six"
	elif value == 5:
		return "five"
	elif value == 4:
		return "four"
	elif value == 3:
		return "three"
	elif value == 2:
		return "two"
	elif value == 1:
		return "one"


def nao_speak():
	global tts
	global counter

	if counter >= 10:
		if is_neurotic:
			tts.say("I am going to lose. I am terrible at this game.")
		else:
			tts.say("Oh no! I must play a ten!")
	else:
		if is_neurotic:
			tts.say("I guess this I will play " + counter)
		else:
			tts.say("My turn!")


def take_turn(name):
	global counter
	global nao
	
	if name == nao:
		nao_speak()
	
	print("[" + name + "]\t\t" + str(min([counter, 10])))
	time.sleep(1)

	if (counter >= 10):
		time.sleep(1)
		print(name + " loses!")


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
	global is_neurotic
	global counter

	global tts
	tts = ALProxy("ALTextToSpeech", nao_ip, nao_port)

	isRunning = True
	while isRunning:
		tts.say("Would you like to play again?")
		if boolean_input("> continue playing? <y/n> ") == True:
			is_neurotic = boolean_input("> enable neurotic personality? <y/n> ")
			counter = 0
			while counter < 10:
				turn(player, numeric_input("> "))
				turn(nao, random.randint(1, 2))
		else:
			isRunning = False
	print("quitting...")


if __name__ == "__main__":
    main()
