import discord, asyncio
import ai
import json, sys

client = discord.Client()

aidata = []
with open("ai.json", "r") as f:
	aidata = json.load(f)

sessions = {}

@client.event
async def on_message(message):
	if message.author != client.user:
		if message.content.startswith("!supportme"):
			session = ai.ChatbotSession(aidata)
			sessions[message.channel] = session
			await client.send_message(message.channel, session.respond("welcome"))
		else:
			if message.channel in sessions.keys():
				session = sessions[message.channel]
				response = session.processMessage(message.content)
				if response != None:
					await client.send_message(message.channel, response)
			
@client.event
async def on_ready():
	print("Name: %s, ID: %s" % (client.user.name, client.user.id))
		
token = ""
with open("token.txt", "r") as f:
	token = f.read().strip("\n")

client.run(token)