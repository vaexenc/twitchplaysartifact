import queue
import sys
import threading
import time
import traceback
import pyautogui
import points
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
# TWITCH, THREAD
##############################################################################

messageQueue = queue.Queue()
twitchObj = twitch.Twitch()

def twitchThreadFunction():
	while 1:
		newMessages = twitchObj.receiveMessages()
		if newMessages:
			messageQueue.put(newMessages)
		time.sleep(0.001)

twitchThread = threading.Thread(target=twitchThreadFunction)
twitchThread.daemon = True

##############################################################################
# GO LIVE
##############################################################################

print("### TWITCH PLAYS ARTIFACT ###")
twitchObj.connect(username, key)
twitchThread.start()
twitchObj.sendMessage("[ ✔️ Manually starting script.]")
screen.changeToOverlay("overlay")

def onShutdown():
	twitchObj.sendMessage("[ ❌ Manually shutting down script.]")
	time.sleep(1) # because message doesn't get sent otherwise?

while 1:
	try:
		while messageQueue.queue:
			messages = messageQueue.get()
			for message in messages:
				if ignoreMessagesOfOthers and message["username"] == username or not ignoreMessagesOfOthers:
					print(message["username"], message["message"])
					screen.checkMessageAndExecuteCommands(message["message"], points.points)
			time.sleep(0.001)
		time.sleep(0.001)
	except KeyboardInterrupt:
		onShutdown()
		break
	except pyautogui.FailSafeException:
		print(traceback.format_exc())
		onShutdown()
		break
	except Exception:
		print("\n\n=====================================\n")
		print(traceback.format_exc())
		twitchObj.sendMessage("[ ❌❌❌ Shutting down script due to unexpected error.]")
		time.sleep(3)
		break

screen.changeToOverlay("blank")
