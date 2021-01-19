import os
import discord
import time
import asyncio
import random
import datetime
import difflib
import subprocess

startdate = datetime.datetime.now().strftime("%d. %B %Y %H:%M:%S")   #time at witch the Program started running
processid = os.getpid()  #Process 

intents = discord.Intents.all()
client = discord.Client(intents=intents)


##### Constants ##########

CMD_MARK = "$"    #symbol with wich a commad starts      

##########################




@client.event
async def on_ready():
    print("we have logged in as {0.user}".format(client))

@client.event
async def on_message(message):      #the following code gets executed every time a message is recieved
    
    if message.author == client.user:    #ignores messages sent by itself, so it doesn't react to it's own messages
        return
    if message.content == "":            #ignores empty messages, to avoid errors 
        return
    if str(message.channel.type) == "private":  #ignores messages sent in DM channels
        return

    try:                        #all handeling of the message is in a try-Block so the program returns if an error occurs
        m = message.content
        c = message.channel
        g = message.guild
        

        if m == CMD_MARK + "onlinetest":  #sends a few informations about the program (name, date and time at wich it was started,process id) 
            ans = await c.send("online and running, message will be deleted", embed = discord.Embed(color = discord.Colour(65535)).add_field(
                name = "Script:", value = __file__ + "\nrunning since " + startdate + "\nProcess ID: " + str(processid)))
            await message.delete()
            await asyncio.sleep(3)
            await ans.delete()
            return



        if m == CMD_MARK + "restart":   #the command restart restarts the whole program with the latest version
            ans = await c.send("restarting")
            await message.delete()
            await ans.delete()

            child = os.system("python3 -m py_compile robertsbot.py")        #check if the latest save will compile
            if child == 0:                                                  #if yes, start it 
                os.system("nohup python3 robertsbot.py &")
                ans = await c.send(str(processid)+": restarted, now killing myself")
                await asyncio.sleep(2)
                await ans.delete()
                exit(0)
            else:                                                           #if not, keep running
                ans = await c.send("restarting failed, program did not compile", embed = discord.Embed(color = discord.Colour(16711680)).add_field(
                    name = "Exit code:", value = child))
                await asyncio.sleep(2)
                await ans.delete()
                return


        if m == CMD_MARK + "hallo":
            await c.send("hallo!")
            return







        
        
        if m[0] == CMD_MARK:  #if the message starts with the command symbol but not contains any known commands
            await c.send(str(message.author.name)+" messaged me: "+message.content[1:]+" in "+str(c))



    except Exception as e:      #if an error occoured, send a message containing the error, raise it to add it to errorlog
        ans = await message.channel.send("script error occoured", embed = discord.Embed(color = discord.Colour(16711680)).add_field(name = "Error message:", value = e))
        await asyncio.sleep(3)
        await ans.delete()  #deletes the error message from discord after 3 seconds to not cause chaos
        raise e
