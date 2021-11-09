import discord
from discord import client
from discord.ext import commands

class Bot:

    def __init__(self, token, vc):
        self.client = commands.Bot(command_prefix=';')
        self.token = token
        self.vc = vc

    @client.command()
    async def play(self, ctx, url: str):
        channel = discord.utils.get(ctx.guild.voice_channels, name=self.vc)
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        await channel.connect()

    @client.event
    async def on_ready():
        print('bot ready!')

    def run(self):
        self.client.run(self.token)


Bot('OTA0MDk5NTMxMjE2NTM5Njcw.YX2mTQ.b4ZRbNWPq3qiAV9rOkOjznjsNbk', 'General').run()
