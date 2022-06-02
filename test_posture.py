import sys

from naoqi import ALProxy

NAO_IP = "192.168.1.41"
NAO_PORT = 9559

def main():
	motion = ALProxy("ALMotion", NAO_IP, NAO_PORT)
	posture = ALProxy("ALRobotPosture", NAO_IP, NAO_PORT)

	motion.wakeUp()

	posture.goToPosture("Stand", 0.5)
	posture.goToPosture("LyingBelly", 0.5)
	posture.goToPosture("Sit", 0.5)
	posture.goToPosture("SitRelax", 0.5)
	posture.goToPosture("LyingBack", 0.5)
	posture.goToPosture("StandInit", 0.5)
	posture.goToPosture("StandZero", 0.5)
	posture.goToPosture("Stand", 0.5)

	motion.rest()
	sys.exit()


if __name__ == "__main__":
    main()
