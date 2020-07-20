import time
import threading
import queue
import twitch
import screen
import pyautogui
import traceback

username = "redacted"
key = "redacted" # http://twitchapps.com/tmi/
adminMode = False
pyautogui.FAILSAFE = True
# pyautogui.PAUSE = 0.1

##############################################################################
# SET UP CLICK POINTS
##############################################################################

# w, h = 1920, 1080
pointsAllyLaneCardsActives = screen.createPointsAlongLine(34, 232, 1690, 724) #34, 232, 1690, 724
pointsAllyLaneCardsItems = screen.createPointsAlongLine(34, 232, 1690, 588)
pointsAllyImprovementsL = screen.createPointsAlongLine(8, 473, 793, 935)
pointsAllyImprovementsR = screen.createPointsAlongLine(8, 1126, 1440, 935)
pointsAllyImprovementsAndDeploy = screen.createPointsAlongLine(16, 473, 1440, 935)
# pointAllyTower = screen.createPoint(959, 866)
pointsHand = screen.createPointsAlongLine(20, 465, 1414, 1055)

pointsEnemyLaneCards = screen.createPointsAlongLine(14, 290, 1600, 362)
pointsEnemyImprovementsL = screen.createPointsAlongLine(7, 610, 824, 180)
pointsEnemyImprovementsR = screen.createPointsAlongLine(7, 1095, 1350, 180)
# pointEnemyTower = screen.createPoint(959, 143)

pointsShop = screen.createPointsAlongLine(3, 690, 1110, 700)

# singlePoint = screen.createPoint(100, 100)

pointsDict = {
	"a": pointsAllyLaneCardsActives + pointsAllyLaneCardsItems,
	"h": pointsHand,
	"k": pointsAllyImprovementsAndDeploy, #pointsAllyImprovementsL + pointsAllyImprovementsR,

	"b": pointsEnemyLaneCards,
	"j": pointsEnemyImprovementsL + pointsEnemyImprovementsR,
	"s": pointsShop,

	"pass": screen.createPoint(1570, 915),

	"pp": screen.createPoint(1200, 834),
	"ll": screen.createPoint(18, 489),
	"lr": screen.createPoint(1901, 489),
	"sh": screen.createPoint(757, 290),
	"cl": screen.createPoint(795, 652),
	"pr": screen.createPoint(1100 , 652),

	# "test": screen.createPoint(100, 100),
}

pointsDictMenu = {

}

# pointsDict.update(pntdct)
# for i, v in pointsDict.items(): pass

# screen.generateOverlay(pointsDict, fontSize = 22, fileName = "overlay")
# screen.checkMessageAndExecuteCommands( "scrolll", pointsDict )
# screen.checkMessageAndExecuteCommands( "scrollr", pointsDict )
# quit()

##############################################################################
# TWITCH, THREAD
##############################################################################

messageQueue = queue.Queue()

t = twitch.Twitch()

def twitchThreadFunction():
	global messageQueue
	while 1:
		newMessages = t.twitch_receive_messages()
		if newMessages:
			messageQueue.put(newMessages)
		time.sleep(0.001)
	# notes: lock.acquire(), lock.release()

twitchThread = threading.Thread(target=twitchThreadFunction)
twitchThread.daemon = True

##############################################################################
# SHOWTIME
##############################################################################

print("### TWITCH PLAYS ARTIFACT ###")
# print("get ready..."); time.sleep(4);

t.twitch_connect(username, key)
twitchThread.start()
t.twitch_send_message("[ ✔️ Manually starting script.]")

# state = screen.detectGameState(screenshot)
# state = ""
currentPointsDict = pointsDict

screen.changeToOverlay("overlay")

while 1:
	try:
		# STATE ######
		# screen.currentStateAction(state)

		# MESSAGES ######

		# with messageQueue.mutex:
		# 	messageQueue.queue.clear()

		while messageQueue.queue:
			messages = messageQueue.get()
			for message in messages:
				if adminMode and message["username"] == username or not adminMode:
					print( message["username"], message["message"] )
					screen.checkMessageAndExecuteCommands( message["message"], currentPointsDict )
			time.sleep(0.001)
		time.sleep(0.001)
	except KeyboardInterrupt as e:
		t.twitch_send_message("[ ❌ Manually shutting down script.]")
		time.sleep(1) # because message doesn't get sent otherwise...?
		break
	except pyautogui.FailSafeException as e:
		print( traceback.format_exc() )
		t.twitch_send_message("[ ❌ Manually shutting down script.]")
		time.sleep(1)
		break
	except:
		print("\n\n=====================================\n")
		print( traceback.format_exc() )
		t.twitch_send_message("[ ❌❌❌ Shutting down script due to unforeseen error.]")
		time.sleep(3)
		break

screen.changeToOverlay("blank")

######################################
# OTHER WAYS TO KILL THREAD AND PROGRAM
# something like that anyway
# while 1:
# 	try:
# 		if input() == "kill":
# 			break
# 	except:
# 		dead = True
# 		time.sleep(0.01)
# 		# t1.join() ??
# 		break
#	finally:
#		dead = True
######################################
