import threading
import requests
import discord
import psutil
import avery
import time
import json
import eel
import sys
import os

from discord.ext import commands
from avery import Avery
from avery import Init

class GUI:

    @eel.expose
    async def __init__(self, avery: Avery, client):
        self.avery = avery
        self.client = client
        Init() # Make sure scraped files exist

    @eel.expose
    async def Ban(self, guild):
        members = open('scrape/members.txt')
        for member in members:
            threading.Thread(target=self.avery.BanMembers, args=(guild, member,)).start()
    
    @eel.expose
    async def Kick(self, guild):
        members = open('scrape/members.txt')
        for member in members:
            threading.Thread(target=self.avery.KickMembers, args=(guild, member,)).start()
    
    @eel.expose
    async def Channels(self, guild):
        channels = open('scrape/channels.txt')
        for channel in channels:
            threading.Thread(target=self.avery.DeleteChannels, args=(guild, channel,)).start()
    
    @eel.expose
    async def Roles(self, guild):
        roles = open('scrape/roles.txt')
        for role in roles:
            threading.Thread(target=self.avery.DeleteRoles, args=(guild, role,)).start()
    
    @eel.expose
    async def ChannelSpam(self, guild, name, amount, spam: bool, spamamount, message):
        for i in range(int(amount)):
            if spam:
                threading.Thread(target=self.avery.SpamChannels, args=(guild, name, spamamount, message, True,)).start()
            else:
                threading.Thread(target=self.avery.SpamChannels, args=(guild, name, 0, '', False,)).start()
    
    @eel.expose
    async def RoleSpam(self, guild, name, amount):
        for i in range(int(amount)):
            threading.Thread(target=self.avery.SpamRoles, args=(guild, name,)).start()
    
    @eel.expose
    async def Scrape(self, guild):
        await self.client.wait_until_ready()

    @eel.expose
    async def Nuke(self, guild, channel_name, channel_amount, channel_spam: bool, channel_spam_amount, channel_spam_message, role_name, role_amount):
        members = open('scrape/members.txt')
        channels = open('scrape/channels.txt')
        roles = open('scrape/roles.txt')

        for member in members:
            threading.Thread(target=self.BanMembers, args=(guild, member,)).start()
        for channel in channels:
            threading.Thread(target=self.DeleteChannels, args=(guild, channel,)).start()
        for role in roles:
            threading.Thread(target=self.DeleteRoles, args=(guild, role,)).start()
        for i in range(int(channel_amount)):
            if channel_spam == True:
                threading.Thread(target=self.SpamChannels, args=(guild, channel_name, channel_spam_amount, channel_spam_message, True)).start()
            else:
                threading.Thread(target=self.SpamChannels, args=(guild, channel_name, 0, '', False)).start()
        for i in range(int(role_amount)):
            threading.Thread(target=self.SpamRoles, args=(guild, role_name,)).start()
        
        members.close()
        channels.close()
        roles.close()
