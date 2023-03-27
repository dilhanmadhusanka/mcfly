# Import discord.py. Allows access to Discord's API.
import discord

# Import the os module.
import os

# Import load_dotenv function from dotenv module.
from dotenv import load_dotenv

# Import commands from the discord.ext module.
from discord.ext import commands

from table2ascii import table2ascii as t2a, PresetStyle
# Loads the .env file that resides on the same level as the script.
load_dotenv()

# Grab the API token from the .env file.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OP_CH = os.getenv("OP_CH")
EV_CH = os.getenv("EV_CH")
ROLE_NAME = os.getenv("ROLE_NAME")
ROLES = os.getenv("ROLES")
SPC_ROLES = os.getenv("SPC_ROLES")

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

@bot.command(name="members")
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
    
@bot.command(name="stats")
async def stat(ctx):
    result = []
    opchannel = discord.utils.get(ctx.guild.channels, name=OP_CH)
    eventchannel = discord.utils.get(ctx.guild.channels, name=EV_CH)
    members = opchannel.members
    for member in members:
        cert_count = spc_cert_count = 0
        if ROLE_NAME in [y.name for y in member.roles]:
            for role in ROLES:
                if role in [y.name for y in member.roles]:
                    cert_count += 1
            for sp_role in SPC_ROLES:
                if sp_role in [y.name for y in member.roles]:
                    spc_cert_count += 1
            player = Player(member.name,0,0,cert_count,spc_cert_count)
            result.append(player)
            
    if opchannel:
        async for message in opchannel.history():
            i = 0
            for player in result:
                ops = events = 0
                for line in message.content.splitlines():
                    if line.startswith(":yes:"):
                        if ':yes: '+player.name in line:
                            ops += 1
                if ops>0:
                    player.ops += ops
                    result[i] = player
                i += 1
    if eventchannel:
        async for message in eventchannel.history():
            i = 0
            for player in result:
                ops = events = 0
                for line in message.content.splitlines():
                    if line.startswith(":yes:"):
                        if ':yes: '+player.name in line:
                            events += 1
                if events>0:
                    player.events += events
                    result[i] = player
                i += 1

    # embed=discord.Embed(title="Player Status", color=0x00ff11)
    # for x in result:
    #     embed.add_field(name="Name", value=x.name+"\u2800\u2800\u2800", inline=True)
    #     embed.add_field(name="Ops", value=str(x.ops)+"\u2800\u2800\u2800", inline=True)
    #     embed.add_field(name="Events", value=str(x.events)+"\u2800\u2800\u2800", inline=True)
    #     embed.add_field(name="Std. Cert", value=str(x.certs)+"\u2800\u2800\u2800", inline=True)
    #     embed.add_field(name="Adv. Cert.", value=str(x.spl_certs)+"\u2800\u2800\u2800", inline=True)
    #    # text += x.name+"   OPS:"+str(x.ops)+"   EVENTS:"+str(x.events)+"\n"
    # await ctx.send(embed=embed)
    tbody = []
    for x in result:
        tbody.append([x.name,str(x.ops),str(x.events),str(x.certs),str(x.spl_certs)])
    output = t2a(
        header=["Name", "Ops", "Events", "Std. Cert.", "Adv. Cert."],
        body=tbody,
        first_col_heading=True
    )
    await ctx.send(f"```\n{output}\n```")

@bot.command()
async def default(ctx):
    await ctx.send(":fu:")

# Executes the bot with the specified token. Token has been removed and used just as an example.
bot.run(DISCORD_TOKEN)
