import settings
import socket
import sys

irc = socket.socket()

def sendstr(s):
	irc.send((s + '\r\n').encode('utf-8'))
	
def sendmsg(msg):
	sendstr('PRIVMSG #' + settings.TWITCH_CHANNEL + ' :' + msg)
	print(msg)
	
def connect():
	print ('connecting to:' + settings.IRC_HOST)
	irc.connect((settings.IRC_HOST, 6667))#connects to the server
	sendstr('PASS ' + settings.BOT_PASSWORD)
	#sendstr('USER ' + settings.BOT_NAME + ' ' + settings.BOT_NAME +' ' + settings.BOT_NAME)#user authentication
	sendstr('NICK ' + settings.BOT_NAME)
	sendstr('JOIN #' + settings.TWITCH_CHANNEL)#join the chan
	
def get_text():
	text = irc.recv(2040).decode('utf-8')#gets text
	
	if text.find('PING') != -1:
		sendstr('PONG')
		print('PONG')
	return text 
