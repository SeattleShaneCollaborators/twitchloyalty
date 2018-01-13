import discord
from discord.ext import commands
import asyncio
import os
import settings
import twitchbot
import db
import irc


client = discord.Client()
password = ""

@client.event
async def on_ready():
	db.createTables()
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('-----')
	
@client.event
async def on_message(message):
	#Allows administrators to set passwords 
	if message.content.startswith('-setpass') and str(message.author) in settings.DISCORD_ADMIN_LIST:
		await setpass(message)
	elif message.content.startswith('-pass') and str(message.author) in settings.DISCORD_ADMIN_LIST:
		await sendpass(message)
	elif message.content.find("Hello") != -1 and message.content.find("Callisterbot") != -1 :
		await client.send_message(message.channel,"hello " + str(message.author.name))
	elif message.content.startswith('!test'):
		await client.send_message(message.channel,"I live!")
	else:
		print(message.content)
		print("from: " + str(message.author))
		print("in channel: " + str(message.channel))	

async def setpass(message):
	print('message content: ' + message.content)
	passwordstart = len('-setpass ')
	password = message.content[passwordstart:]
	with db.getCur() as cur:
		cur.execute("DELETE FROM PUBGPasswords")
		cur.execute("INSERT INTO PUBGPasswords VALUES(?);",(password,))
	print(str(message.author) + " has set a new password via discord to " + "(" + password + ")")
	await client.send_message(message.channel,str(message.author) + " has set a new password via discord to " + password)
	await client.send_message(message.channel,"Sending password to subscriberss in 1 minute")
	await asyncio.sleep(60)
	subscriberchannel = discord.Object(id=settings.DISCORD_CH_SUBSCRIBERS)
	await client.send_message(subscriberchannel,"The password for the next game is: " + password)
	await client.send_message(subscriberchannel,"Sending password to twitch chat in 2 minutes")
	await client.send_message(message.channel,"Sending password to twitch chat in 2 minutes")
	await asyncio.sleep(120)
	await irc.sendmsg("The password for the custom server is: " + password)
		
async def sendpass(message):
	if password is == "":
		await client.send_message(message.channel,"No password has been set")
	else:
		await client.send_message(message.channel,"The password for the next game is: " + password)
		
async def bothello(message):
	await client.send_message(message.channel, "Hello " + str(message.author))

#async def bottest(message):
	

client.run(settings.DISCORD_BOT_TOKEN)
