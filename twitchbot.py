import irc
import os
import random
import operator
import settings
import requests
import time
import re
import datetime
import json

def twitchbot():
	irc.connect()
	channel = settings.TWITCH_CHANNEL
	server = settings.IRC_HOST
	nickname = settings.BOT_NAME
	while 1:
		text = irc.get_text()
		username = text[1:text.find('!')]
		if "PRIVMSG" in text and "callisterbot" in text and "hello" in text:
			irc.sendmsg("Hello " + text[1:text.find('!')])
			
		url = 'https://www.strawpoll.me/'
		if username == 'nightbot' and text.find(url) != -1:#Strawpoll manager, looks up poll, waits then moves winner to /OBS
			urlstart = text.find(url)
			idstart = urlstart + len(url)
			pollid = text[urlstart:text.find(' ',urlstart)]
			print('Starting Poll for Callisterbot at https://www.strawpoll.me/' + pollid)
			print('waiting for poll to finish')
			for x in range(200,0):
				time.sleep(1)
				print ('countdown:' + str(x))
			url = ('https://strawpoll.me/api/v2/polls/' + pollid)
			r = requests.get(url)
			polljson = json.loads(r.content.decode('utf-8'))
			zpj = zip(polljson['votes'],polljson['options'])
			winner = max(zpj)[1]
			r = open('gamemodetext.txt', 'w')
			r.write(winner)
			print('Wrote: ' + winner + " to callistergaming.com/obs")
		print(text)
		
		#Runza Temp Tuesday easteregg
		if  "PRIVMSG" in text and "runza" in text and datetime.datetime.now().weekday() == 1:
			url = 'http://api.openweathermap.org/data/2.5/weather?zip=68106,us&appid=' + settings.WEATHER_API
			r = requests.get(url)
			weatherjson = json.loads(r.content.decode('utf-8'))
			temperature = str(int(weatherjson['main']['temp']*9/5 - 459.67))
			irc.sendmsg("Runza TEMP TUESDAYS DEAL IS ACTIVE TODAY! Head into your local Runza and you will pay " + temperature + " cents for a Runza with the purchase of a medium fry and drink! ")
		
		#Lets twitch users see the password
		if  "PRIVMSG" in text and "-pass" in text:
		with db.getCur() as cur:
		cur.execute("SELECT " Data TEMPPASSWORD(?);",(password))
		
		
		
if __name__ == "__main__":
	twitchbot()
		