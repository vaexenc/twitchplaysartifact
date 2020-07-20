# i'm not sure how everything here works, i took the basis of this code from somewhere and did a major overhaul on it

import re
import socket
import sys

class Twitch:
	user = ""
	oauth = ""
	s = None

	def get_login_status(self, data):
		if re.match(r'^:(testserver\.local|tmi\.twitch\.tv) NOTICE \* :Login authentication failed\r\n$'.encode("utf-8"), data):
			return False
		return True

	def connect(self, user, key):
		self.user = user
		self.oauth = key
		print("Connecting to twitch...")
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(1)
		connect_host = "irc.twitch.tv"
		connect_port = 6667
		try:
			s.connect((connect_host, connect_port))
		except Exception:
			print("Failed to connect to twitch")
			sys.exit()
		print("Connected to twitch.")
		print("Sending our details to twitch...")
		s.send(('USER %s\r\n' % user).encode("utf-8"))
		s.send(('PASS %s\r\n' % key).encode("utf-8"))
		s.send(('NICK %s\r\n' % user).encode("utf-8"))

		if not self.get_login_status(s.recv(1024)):
			print("...and they didn't accept our details.")
			sys.exit()
		else:
			print("...and they accepted our details.")
			print("We are live!")
			self.s = s
			s.send(('JOIN #%s\r\n' % user).encode("utf-8"))

	def check_has_message(self, data):
		return re.match(r'^:[a-zA-Z0-9_]+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+(\.tmi\.twitch\.tv|\.testserver\.local) PRIVMSG #[a-zA-Z0-9_]+ :.+$'.encode("utf-8"), data)

	def check_has_ping(self, data):
		if b'PING :tmi.twitch.tv\r\n' in data:
			return True
		return False

	def parse_message(self, data):
		return {
			'channel': re.findall(r'^:.+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+.+ PRIVMSG (.*?) :'.encode("utf-8"), data)[0].decode(),
			'username': re.findall(r'^:([a-zA-Z0-9_]+)\!'.encode("utf-8"), data)[0].decode(),
			'message': re.findall(r'PRIVMSG #[a-zA-Z0-9_]+ :(.+)'.encode("utf-8"), data)[0].decode()
		}

	def receive_messages(self, amount=1024):
		data = None
		try:
			data = self.s.recv(1024)
		except Exception:
			return False

		if not data:
			print("Lost connection to Twitch, attempting to reconnect...")
			self.connect(self.user, self.oauth)
			return None

		if self.check_has_ping(data):
			self.s.send(("PONG :tmi.twitch.tv\r\n").encode("utf-8")) # b"PONG :tmi.twitch.tv\r\n" ???
			return False

		if self.check_has_message(data):
			try:
				return [self.parse_message(line) for line in filter(None, data.split('\r\n'.encode("utf-8")))]
			except Exception:
				return False

	def send_message(self, message):
		sendValue = "PRIVMSG #{} :{}{}".format(self.user, message, "\r\n")
		self.s.send(sendValue.encode("utf-8"))
