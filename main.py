import queue
import sys
import threading
import time
import traceback
import pyautogui
import screen
import twitch

if len(sys.argv) != 3:
	print("Invalid command line arguments. Please provide username and key (http://twitchapps.com/tmi/).")
	sys.exit()

username = sys.argv[1]
key = sys.argv[2] # http://twitchapps.com/tmi/

ignoreMessagesOfOthers = False
pyautogui.FAILSAFE = True

##############################################################################
# SET UP CLICK POINTS
##############################################################################

# we assume a resolution of 1920x1080
pointsAllyLaneCardsActives = screen.createPointsAlongLine(34, 232, 1690, 724)
pointsAllyLaneCardsItems = screen.createPointsAlongLine(34, 232, 1690, 588)
pointsAllyImprovementsAndDeploy = screen.createPointsAlongLine(16, 473, 1440, 935)
pointsEnemyLaneCards = screen.createPointsAlongLine(14, 290, 1600, 362)
pointsEnemyImprovementsL = screen.createPointsAlongLine(7, 610, 824, 180)
pointsEnemyImprovementsR = screen.createPointsAlongLine(7, 1095, 1350, 180)
pointsHand = screen.createPointsAlongLine(20, 465, 1414, 1055)
pointsShop = screen.createPointsAlongLine(3, 690, 1110, 700)

pointsDict = {
	"a": pointsAllyLaneCardsActives + pointsAllyLaneCardsItems,
	"h": pointsHand,
	"k": pointsAllyImprovementsAndDeploy,
	"b": pointsEnemyLaneCards,
	"j": pointsEnemyImprovementsL + pointsEnemyImprovementsR,
	"s": pointsShop,
	"pp": screen.createPoint(1200, 834),
	"ll": screen.createPoint(18, 489),
	"lr": screen.createPoint(1901, 489),
	"sh": screen.createPoint(757, 290),
	"cl": screen.createPoint(795, 652),
	"pr": screen.createPoint(1100, 652),
	"pass": screen.createPoint(1570, 915),
}

# screen.generateOverlay(pointsDict, fontSize=22, fileName="overlay")
# sys.exit()

##############################################################################
# TWITCH, THREAD
##############################################################################

messageQueue = queue.Queue()
t = twitch.Twitch()

def twitchThreadFunction():
	global messageQueue
	while 1:
		newMessages = t.receive_messages()
		if newMessages:
			messageQueue.put(newMessages)
		time.sleep(0.001)

twitchThread = threading.Thread(target=twitchThreadFunction)
twitchThread.daemon = True

##############################################################################
# SHOWTIME
##############################################################################

print("### TWITCH PLAYS ARTIFACT ###")
t.connect(username, key)
twitchThread.start()
t.send_message("[ ✔️ Manually starting script.]")
screen.changeToOverlay("overlay")

currentPointsDict = pointsDict

def on_shutdown():
	t.send_message("[ ❌ Manually shutting down script.]")
	time.sleep(1) # because message doesn't get sent otherwise?

while 1:
	try:
		while messageQueue.queue:
			messages = messageQueue.get()
			for message in messages:
				if ignoreMessagesOfOthers and message["username"] == username or not ignoreMessagesOfOthers:
					print(message["username"], message["message"])
					screen.checkMessageAndExecuteCommands(message["message"], currentPointsDict)
			time.sleep(0.001)
		time.sleep(0.001)
	except KeyboardInterrupt:
		on_shutdown()
		break
	except pyautogui.FailSafeException:
		print(traceback.format_exc())
		on_shutdown()
		break
	except Exception:
		print("\n\n=====================================\n")
		print(traceback.format_exc())
		t.send_message("[ ❌❌❌ Shutting down script due to unexpected error.]")
		time.sleep(3)
		break

screen.changeToOverlay("blank")
