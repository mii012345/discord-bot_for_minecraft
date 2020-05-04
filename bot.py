import discord
from discord.ext import tasks
import subprocess
import json
import requests
import concurrent.futures
import status_get
import threading
import asyncio
import pprint

client = discord.Client()
s = status_get.Status_Get()

Token = ''

start_cmd = "java -Xmx1024M -Xms1024M -jar server.jar nogui"

returncode = None

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    update_status.start()

@tasks.loop(seconds=30)
async def update_status():
    s.getServerStatus()
    if s.online:
        activity = discord.Game(name=s.ac_user+"/"+s.max_user)
        await client.change_presence(activity=activity)
    else:
        activity = discord.Game(name="offline")
        await client.change_presence(activity=activity)


@client.event
async def on_message(message):
    global returncode
    if message.author.bot:
        return
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('!start'):
        try:
            await message.channel.send('Starting....')
            returncode = subprocess.Popen(start_cmd, 
                                          shell=True, 
                                          universal_newlines=True, 
                                          stdin=subprocess.PIPE,
                                          )
            await asyncio.sleep(20)
            s.getServerStatus()
            activity = discord.Game(name=s.ac_user+"/"+s.max_user)
            await client.change_presence(activity=activity)
            await message.channel.send('Started!')
        except:
            await message.channel.send('ERROR : Cant start server')
    
    if message.content.startswith('!stop_server'):
        returncode.communicate("stop")
        print("server stop")
        await message.channel.send('Stopped!')
    
    if message.content.startswith('!status'):
        if returncode.poll() == None:
            await message.channel.send('Alive!')
    
    if message.content.startswith('!list'):
        pass

    if message.content.startswith('!help'):
        pass

client.run(Token)