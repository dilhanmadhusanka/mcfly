# Import discord.py. Allows access to Discord's API.
import discord

# Import the os module.
import os

# Import load_dotenv function from dotenv module.
from dotenv import load_dotenv

# Import commands from the discord.ext module.
from discord.ext import commands

# Loads the .env file that resides on the same level as the script.
load_dotenv()

# Grab the API token from the .env file.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OP_CH = os.getenv("OP_CH")
EV_CH = os.getenv("EV_CH")
ROLE_NAME = os.getenv("ROLE_NAME")

# Creates a new Bot object with a specified prefix. It can be whatever you want it to be.
intents = discord.Intents.all()
intents.reactions = True
intents.members = True
intents.guilds = True

client = discord.Client(intents=discord.Intents.default())
channelId = 1089251564465704982

bot = commands.Bot(command_prefix='!',intents=intents)

class Player:
  def __init__(self, name, ops=0, events=0, certs=0, spl_certs=0):
    self.name = name
    self.ops = ops
    self.events = events
    self.certs = certs
    self.spl_certs = spl_certs

@bot.event
async def on_ready():
    print("online")


@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("pong")

@bot.command(name="get_members")
async def get_members(ctx,role_name):
    result = []
    role = discord.utils.find(
        lambda r: r.name == role_name, ctx.guild.roles)
        
    for user in ctx.guild.members:
        if role in user.roles:
            result.append(user.name)
        
    embed=discord.Embed(title=role_name+" Players", color=0x00ff11)
        
    for x in result:
        embed.add_field(name="", value=x+"\u2800\u2800\u2800\u2800\u2800", inline=False)

    await ctx.send(embed=embed)
    
@bot.command(name="stat")
async def stat(ctx):
    result = []
    opchannel = discord.utils.get(ctx.guild.channels, name=OP_CH)
    # eventchannel = discord.utils.get(ctx.guild.channels, name=EV_CH)
    if opchannel:
        members = opchannel.members
        text = ""
        async for message in opchannel.history(limit=200):
            for member in members:
                if ROLE_NAME in [y.name for y in member.roles]:
                    ops = events = exists = 0
                    for line in message.content.splitlines():
                        if line.startswith(":yes:"):
                            if ':yes: '+member.name in line:
                                ops += 1
                    if ops>0 or events>0:
                        for i in range(len(result)):
                            if result[i].name == member.name:
                                player = result[i]
                                player.ops += ops
                                player.events += events
                                result[i] = player
                                exists = 1
                        if exists == 0:
                            player = Player(member.name,ops,events)
                            result.append(player)

        embed=discord.Embed(title="Player Status", color=0x00ff11)
        
        for x in result:
            embed.add_field(name="Name", value=x.name+"\u2800\u2800\u2800\u2800\u2800", inline=True)
            embed.add_field(name="Ops", value=str(x.ops)+"\u2800\u2800\u2800\u2800\u2800", inline=True)
            embed.add_field(name="Events", value=str(x.events)+"\u2800\u2800\u2800\u2800\u2800", inline=True)
            # text += x.name+"   OPS:"+str(x.ops)+"   EVENTS:"+str(x.events)+"\n"
        await ctx.send(embed=embed)
    else:
        await ctx.send("Channels not found.")

# Executes the bot with the specified token. Token has been removed and used just as an example.
bot.run(DISCORD_TOKEN)
