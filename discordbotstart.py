import discord
from discord.ext import commands
import asyncio
import pickle
import os
import random
import settings
import twitchbot
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
	password = ""
	
	if message.content.startswith('-setpass') and str(message.author) in settings.DISCORD_ADMIN_LIST:
		print('message content: ' + message.content)
		password = message.content.split('-setpass ')[1]
		r = open('temppass.txt', 'w')
		r.write(password)
		print(str(message.author) + " has set a new password via discord to " + "(" + password + ")")
		await client.send_message(message.channel,str(message.author) + " has set a new password via discord to " + password)
		await client.send_message(message.channel,"Sending password to Channel subs in 1 minute")
		await asyncio.sleep(60)
		await client.send_message(397507255840407552,"The password for the next game is: " + password)
		await client.send_message(397507255840407552,"Sending password to twitch chat in 2 minutes")
		await client.send_message(message.channel,"Sending password to twitch chat in 2 minutes")
		await asynco.sleep(5)
		await irc.sendmsg("The password for the custom server is: " + password)
	
	if message.content.startswith('-pass') and str(message.author) in settings.DISCORD_ADMIN_LIST:
		await client.send_message(message.channel,"The password for the next game is: " + password)
	
	elif message.content.find("Hello") and message.content.find("Callisterbot"):
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
