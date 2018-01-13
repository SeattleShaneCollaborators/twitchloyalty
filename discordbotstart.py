import discord
from discord.ext import commands
import asyncio
import pickle
import os
import random
import settings
import twitchbot
<<<<<<< HEAD
import db
=======
>>>>>>> 236b4dcd8aadd701a21c374a92f7d1c8621d9226
import irc


client = discord.Client()

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('-----')

@client.event
async def on_message(message):
	
	if message.content.startswith('-setpass') and str(message.author) in settings.DISCORD_ADMIN_LIST:
		print('message content: ' + message.content)
		password = message.content.split('-setpass ')[1]
		with db.getCur() as cur:
			cur.execute("CREATE or  INTO Data TEMPPASSWORD(?);",(password))
		print(str(message.author) + " has set a new password via discord to " + "(" + password + ")")
		await client.send_message(message.channel,str(message.author) + " has set a new password via discord to " + password)
<<<<<<< HEAD
		await client.send_message(message.channel,"Sending password to subscriberss in 1 minute")
		await asyncio.sleep(5)
		await client.send_message(settings.DISCORD_CH_SUBSCRIBERS,"The password for the next game is: " + password)
		await client.send_message(settings.DISCORD_CH_SUBSCRIBERS,"Sending password to twitch chat in 2 minutes")
		await client.send_message(message.channel,"Sending password to twitch chat in 2 minutes")
		await asynco.sleep(5)
		await irc.sendmsg("The password for the custom server is: " + password))
=======
		await client.send_message(message.channel,"Sending password to Channel subs in 1 minute")
		await asyncio.sleep(60)
		await client.send_message(397507255840407552,"The password for the next game is: " + password)
		await client.send_message(397507255840407552,"Sending password to twitch chat in 2 minutes")
		await client.send_message(message.channel,"Sending password to twitch chat in 2 minutes")
		await asynco.sleep(5)
		await irc.sendmsg("The password for the custom server is: " + password)
>>>>>>> 236b4dcd8aadd701a21c374a92f7d1c8621d9226
	
	if message.content.startswith('-pass') and str(message.author) in settings.DISCORD_ADMIN_LIST:
		await client.send_message(message.channel,"The password for the next game is: " + password)
	
<<<<<<< HEAD
	
	
	elif message.content != 0:
=======
	elif message.content.find("Hello") and message.content.find("Callisterbot"):
>>>>>>> 236b4dcd8aadd701a21c374a92f7d1c8621d9226
		print(message.content)
		print(message.author)
		print(message.channel)

	elif message.content.startswith('!test'):
		await client.send_message(message.channel,"I live!")

	elif message.content != 0:
		print(message.content)
		print("from: " + message.author)
		print("in channel: " + message.channel)



client.run(settings.DISCORD_BOT_TOKEN)
