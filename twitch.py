import socket
import sys
import re

class Twitch:
	user = ""
	oauth = ""
	s = None

	def twitch_login_status(self, data):
		if not re.match(r'^:(testserver\.local|tmi\.twitch\.tv) NOTICE \* :Login unsuccessful\r\n$'.encode("utf-8"), data): return True
		else: return False

	def twitch_connect(self, user, key):
		self.user = user
		self.oauth = key
		print("Connecting to twitch.tv")
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(1) # todo: original 0.6
		connect_host = "irc.twitch.tv"
		# connect_host = "irc.chat.twitch.tv"
		connect_port = 6667
		try:
			s.connect((connect_host, connect_port))
		except:
			print("Failed to connect to twitch")
			sys.exit()
		print("Connected to twitch")
		print("Sending our details to twitch...")
		s.send(('USER %s\r\n' % user).encode("utf-8"))
		s.send(('PASS %s\r\n' % key).encode("utf-8"))
		s.send(('NICK %s\r\n' % user).encode("utf-8"))

		if not self.twitch_login_status(s.recv(1024)):
			print("... and they didn't accept our details")
			sys.exit()
		else:
			print("... they accepted our details")
			print("Connected to twitch.tv!")
			self.s = s
			s.send(('JOIN #%s\r\n' % user).encode("utf-8"))
			# s.recv(1024)

	def check_has_message(self, data):
		return re.match(r'^:[a-zA-Z0-9_]+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+(\.tmi\.twitch\.tv|\.testserver\.local) PRIVMSG #[a-zA-Z0-9_]+ :.+$'.encode("utf-8"), data)

	def check_has_ping(self, data):
		if b'PING :tmi.twitch.tv\r\n' in data:
			return True
		return False

	def parse_message(self, data):
		return {
			# b':username!username@username.tmi.twitch.tv PRIVMSG #username :1'
			'channel': re.findall(r'^:.+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+.+ PRIVMSG (.*?) :'.encode("utf-8"), data)[0].decode(),
			'username': re.findall(r'^:([a-zA-Z0-9_]+)\!'.encode("utf-8"), data)[0].decode(),
			'message': re.findall(r'PRIVMSG #[a-zA-Z0-9_]+ :(.+)'.encode("utf-8"), data)[0].decode() # .decode('utf8')
		}

	def twitch_receive_messages(self, amount=1024):
		# print("receiving...")
		data = None
		try:
			data = self.s.recv(1024)
		except:
			return False

		if not data:
			print("Lost connection to Twitch, attempting to reconnect...")
			self.twitch_connect(self.user, self.oauth)
			return None

		if self.check_has_ping(data):
			self.s.send( ("PONG :tmi.twitch.tv\r\n").encode("utf-8") ) #b"PONG :tmi.twitch.tv\r\n" ???
			return False

		if self.check_has_message(data):
			# return "yesmessage"
			# UnicodeDecodeError: 'utf-8' codec can't decode bytes in position 961-962: unexpected end of data # todo: is it fixed yet
			try: # todo: does this even return more than 1 message
				return [self.parse_message(line) for line in filter(None, data.split('\r\n'.encode("utf-8")))] # todo: why is this shit in a list and shit
			except:
				return False

	def twitch_send_message(self, message):
		sendValue = "PRIVMSG #{} :{}{}".format(self.user, message, "\r\n")
		self.s.send( sendValue.encode("utf-8") )
