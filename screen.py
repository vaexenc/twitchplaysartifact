import os
import re
import shutil
import time
from PIL import Image, ImageDraw, ImageFont
import pyautogui

globalSleepTime = 1

##############################################################################
# CLICK POINTS, STREAM OVERLAY
##############################################################################

def createPointsAlongLine(numberOfPoints, start, end, thatOtherCoordinate, spaceBetweenPoints=None, vertical=False):
	pointsList = []

	if not spaceBetweenPoints:
		spaceBetweenPoints = abs(start - end) / (numberOfPoints-1)

	for i in range(numberOfPoints):
		mainCoordinate = start + i*spaceBetweenPoints
		x = mainCoordinate
		y = thatOtherCoordinate
		if vertical:
			x, y = y, x
		pointsList.append((int(x), int(y)))

	return pointsList

def createPoint(x, y):
	return [(int(x), int(y))]

def generateOverlay(pointsDict, fileName="overlay unnamed", fontSize=50, width=1920, height=1080):
	if width/height != 1920/1080:
		raise Exception("unsupported ratio")

	image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
	font = ImageFont.truetype("radiance-bold.ttf", fontSize)

	d = ImageDraw.Draw(image)

	# crossLength = 12
	# crossWidth = 2
	textShadowDistance = fontSize*0.15
	for letter, pointsSet in pointsDict.items():
		number = ""
		for i, point in enumerate(pointsSet):
			x, y = point
			# if only 1 point
			if len(pointsSet) > 1:
				number = i+1
			text = "{}{}".format(letter.upper(), number)
			textWidth, textHeight = d.textsize(text, font=font)
			textX = x - textWidth * 0.5
			textY = y - textHeight * 0.5
			textXi = int(textX)
			textYi = int(textY)
			# d.line((x, y-crossLength, x, y+crossLength), width = crossWidth)
			# d.line((x-crossLength, y, x+crossLength, y), width = crossWidth)
			d.text((textXi + textShadowDistance, textYi + textShadowDistance*1.05), text, font=font, fill=(0, 0, 0))
			d.text((textXi, textYi), text, font=font, fill=(255, 255, 255))

	if not os.path.isdir("overlays"):
		os.mkdir("overlays")

	image.save("{}{}{}".format("overlays/", fileName, ".png"))
	# -- notes ---------------------------
	# imageData = list(image.getdata())
	# pimage = Image.open(fileName)
	# image.paste(pimage, (15, 15))

def changeToOverlay(overlayName):
	changeToOverlayByRenaming(overlayName)

def changeToOverlayByRenaming(overlayNameToUse):
	###########
	# os.rename(old, new)
	# os.path.isfile(name)
	# shutil.copyfile(file, newfile)
	# os.remove(file)
	###########

	# todo pointsdict

	path = "overlays/"
	obsOverlay = "currentoverlay"
	shutil.copyfile(path + overlayNameToUse + ".png", path + obsOverlay + ".png")

def changeToOverlayByHotkey(overlayName):
	pass

##############################################################################
# MOUSE & KB INPUT
##############################################################################

# https://pyautogui.readthedocs.io/en/latest/cheatsheet.html
# pyautogui.size()
# pyautogui.position()
# pyautogui.moveTo(x, y, duration=num_seconds)
# pyautogui.dragTo(x, y, duration=num_seconds)
# pyautogui.click()
# pyautogui.click(x=moveToX, y=moveToY, clicks=num_of_clicks, interval=secs_between_clicks, button='left') middle right
# pyautogui.rightClick(x=moveToX, y=moveToY)
# pyautogui.middleClick(x=moveToX, y=moveToY)
# pyautogui.doubleClick(x=moveToX, y=moveToY)
# pyautogui.tripleClick(x=moveToX, y=moveToY)
# pyautogui.scroll(amount_to_scroll, x=moveToX, y=moveToY)
# pyautogui.moveRel(0, settings.window_addgame_rel)
# pyautogui.mouseDown(x=moveToX, y=moveToY, button='left')
# pyautogui.mouseUp(x=moveToX, y=moveToY, button='left')
# ---
# pyautogui.typewrite("")
# pyautogui.KEYBOARD_KEYS
# pyautogui.hotkey('ctrl', 'c')
# pyautogui.keyDown(key_name)
# pyautogui.keyUp(key_name)
# pyautogui.press("enter")

def hover(x, y):
	pyautogui.moveTo(x, y)

def click(x, y):
	hover(10, 10)
	time.sleep(0.1)
	pyautogui.click(x, y)
	time.sleep(globalSleepTime)
	# win32api.SetCursorPos((x, y))
	# win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
	# win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

def drag(x1, y1, x2, y2):
	sleeptime = 0.1
	pyautogui.mouseDown(x=x1, y=y1)
	time.sleep(sleeptime)
	pyautogui.moveTo(x2, y2)
	time.sleep(sleeptime)
	pyautogui.mouseUp()
	time.sleep(globalSleepTime)
	# sleeptime = 0.05

	# win32api.SetCursorPos((x1, y1))
	# time.sleep(sleeptime)
	# win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x1, y1, 0, 0)
	# time.sleep(sleeptime)
	# win32api.SetCursorPos((x2, y2))
	# time.sleep(sleeptime)
	# win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x2, y2, 0, 0)

def press(key):
	pyautogui.press(key)

def write(textstring):
	pyautogui.typewrite(textstring)

def writeToIngameChat(message):
	return
	press("enter")
	write(message)
	press("enter")

##############################################################################
# CHAT MESSAGE COMMANDS
##############################################################################

def singleCommandStringSeperator(commandString):
	# returns either a tuple or a string
	patternString = r"^(?P<letters>[a-z]+)(?P<number>(\d+)?)$"
	patternCompiled = re.compile(patternString)
	match = patternCompiled.match(commandString)

	if match:
		if match.group("number"):
			return (match.group("letters"), match.group("number"))
		else:
			return match.group("letters")

def pointsFromCommands(commandParts, pointsDict):
	# only letters
	if type(commandParts) == str:
		if pointsDict.get(commandParts) and len(pointsDict[commandParts]) == 1:
			return pointsDict[commandParts][0]

	# letters and numbers
	elif type(commandParts) == tuple:
		letters, number = commandParts
		number = int(number) - 1
		if pointsDict.get(letters):
			pointsList = pointsDict[letters]
			if len(pointsList) > 1 and number <= len(pointsList) - 1:
				return pointsList[number]

def checkMessageAndExecuteCommandsDraftMouse(messageString, pointsDict):
	message = messageString
	patternDraft = r"^(\d+)$"
	match = re.match(patternDraft, message)
	if match:
		pass

def checkMessageAndExecuteCommandsMouse(messageString, pointsDict):
	message = messageString.lower()

	patternClick = r"^([a-z]+\d*)$"
	patternHover = r"^\,([a-z]+\d*)$"
	patternDrag = r"^([a-z]+\d*)\s+([a-z]+\d*)$"

	patternScroll = r"^scroll(.)$"

	match = re.match(patternScroll, message)
	if match:

		command = match.group(1)

		direction = -1 # scroll down, scrollr

		if command == "l":
			direction = 1

		click(962, 510)
		for i in range(4):
			pyautogui.scroll(1000000*direction)
			time.sleep(0.1)

		return

	match = re.match(patternClick, message)
	if match:
		command = match.group(1)
		commandParts = singleCommandStringSeperator(command)
		point = pointsFromCommands(commandParts, pointsDict)
		if point:
			x, y = point
			click(x, y)
			return (x, y)

	match = re.match(patternHover, message)
	if match:
		command = match.group(1)
		commandParts = singleCommandStringSeperator(command)
		point = pointsFromCommands(commandParts, pointsDict)
		if point:
			x, y = point
			hover(x, y)
			return (x, y)

	match = re.match(patternDrag, message)
	if match:
		command1 = match.group(1)
		command2 = match.group(2)
		commandParts1 = singleCommandStringSeperator(command1)
		commandParts2 = singleCommandStringSeperator(command2)
		point1 = pointsFromCommands(commandParts1, pointsDict)
		point2 = pointsFromCommands(commandParts2, pointsDict)
		if point1 and point2:
			x1, y1 = point1
			x2, y2 = point2
			drag(x1, y1, x2, y2)
			return ((x1, y1), (x2, y2))

def checkMessageAndExecuteCommands(messageString, pointsDict, mouseOrKeyboard="mouse"):
	if mouseOrKeyboard == "mouse":
		return checkMessageAndExecuteCommandsMouse(messageString, pointsDict)
	# elif mouseOrKeyboard == "keyboard":
	# 	checkMessageAndExecuteCommandsKeyboard(messageString)

# def somethingsomethingKeyboard(messageString):
# 	# todo commands max amount!
# 	c = [
# 		"up", "down", "left", "right",
# 		"w", "a", "s", "d",
# 	]

# def checkMessageAndExecuteCommandsKeyboard(messageString):
# 	pass
