import random
import sys
import time

from naoqi import ALProxy

NAO_IP = "192.168.1.41"
NAO_PORT = 9559

def main():
	random.seed()
	n = random.randrange(0, 2)
	if n == 0:
		print("extrovert")
	else:
		print("introvert")

	tts = ALProxy("ALTextToSpeech", NAO_IP, NAO_PORT)
	motion = ALProxy("ALMotion", NAO_IP, NAO_PORT)
	posture = ALProxy("ALRobotPosture", NAO_IP, NAO_PORT)
	leds = ALProxy("ALLeds", NAO_IP, NAO_PORT)

	motion.wakeUp()
	
	if n == 0:
		posture.goToPosture("Stand", 0.3)
		leds.post.randomEyes(2)
		tts.say("\\rspd=110\\\\vct=125\\\\vol=80\\Hello. I am NAO.")
		time.sleep(1)
	else:
		posture.goToPosture("StandInit", 0.3)
		leds.post.fadeRGB("FaceLeds", 0x000000FF, 2)
		tts.say("\\rspd=80\\\\vct=80\\\\vol=50\\Hello. \\pau=750\\ I am NAO.")
		time.sleep(1)
	
	motion.rest()
	sys.exit()


if __name__ == "__main__":
    main()