import discord
import math
import os
import asynio
import difflib
import random
import time

import botcommands


intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("logged in as" + str(client.user))
    
@client.event
async def on_message(message):

    if message.author == client.user:
        return
    
    if message.content == "$restart$":
        pass
        return    
    try:
        com = getattr(botcommands, message.content.split()[0][1:])
        com(message)
    except Exception as e:
        raise e
