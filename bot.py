# Import discord.py allows access to Discord's API.
import discord

# Import the OS module.
import os

# Import the load_dotenv function from the dotenv module.
from dotenv import load_dotenv

# Import commands from the discord.ext module.
from discord.ext import commands

from table2ascii import table2ascii as t2a, PresetStyle
# Loads the.env file that resides on the same level as the script.
load_dotenv()

# Grab the API token from the.env file.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OP_CH = "operation-schedule"
EV_CH = "event-schedule"
ROLE_NAME = "Infantry 🎖️"
ROLES = [
  "Airborne 🦅", "Breacher 🚪", "Explosives 💣", "Heavy Weapons 💥", "Marksman 🎯",
  "Mechanized 🛡️", "Medic 💉"
]
SPC_ROLES = [
  "JTAC 📡", "Rotary Pilot 🚁", "Fixed-Wing Pilot ✈️", "UAV Operator 🛩️"
]

# Creates a new Bot object with a specified prefix. It can be whatever you want it to be.
intents = discord.Intents.all()
intents.reactions = True
intents.members = True
intents.guilds = True

client = discord.Client(intents=discord.Intents.default())

bot = commands.Bot(command_prefix='~',intents=intents)

class Player:
  def __init__ (self, id, name, ops = 0, events = 0, certs = 0, spl_certs=0):
    self.id = id
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
    members = ctx.guild.members
    for member in members:
        cert_count = spc_cert_count = 0
        if ROLE_NAME in [y.name for y in member.roles]:
            for role in ROLES:
                if role in [y.name for y in member.roles]:
                    cert_count += 1
            for sp_role in SPC_ROLES:
                if sp_role in [y.name for y in member.roles]:
                    spc_cert_count += 1
            player = Player(member.id,member.name,0,0,cert_count,spc_cert_count)
            result.append(player)
            
    if opchannel:
        async for message in opchannel.history():
            if len(message.embeds)>0:
                embed = message.embeds[0].to_dict()
                for field in embed['fields']:
                    if field['value'].startswith("<:Yes:"):
                        for player in result:
                            i = ops = 0
                            if '<:Yes:596014739398721536> **'+str(player.name) in field['value']:
                                ops += 1
                            if ops>0:
                                player.ops += ops
                                result[i] = player
                            i += 1
    if eventchannel:
        async for message in eventchannel.history():
            if len(message.embeds)>0:
                embed = message.embeds[0].to_dict()
                for field in embed['fields']:
                    if field['value'].startswith("<:Yes:"):
                        for player in result:
                            i = events = 0
                            if '<:Yes:596014739398721536> **'+str(player.name) in field['value']:
                                events += 1
                            if events>0:
                                player.events += events
                                result[i] = player
                            i += 1
    # text = "**Player Status**\n\n"
    # output = ""
    # i=1
    # for x in result:
    #     output += x.name+"\n    OPs -> "+str(x.ops)+"\n    Events -> "+str(x.events)+"\n    Std. Cert. -> "+str(x.certs)+"\n    Adv. Cert. -> "+str(x.spl_certs)+"\n\n"
    #     if i%10==0:
    #         await ctx.send(text+output)
    #         output = ""
    #     i+=1
    # await ctx.send(text+output)
    result = filter(lambda player: player.ops != 0 or player.events != 0 or player.certs != 0 or player.spl_certs != 0, result)

    tbody = []
    i=1
    await ctx.send("**Player Status**\n\n")
    for x in result:
        tbody.append([x.name,str(x.ops),str(x.events),str(x.certs),str(x.spl_certs)])
        if i%10==0:
            output = t2a(
                header=["Name", "Ops", "Events", "Std. Cert.", "Adv. Cert."],
                body=tbody,
                style=PresetStyle.thin_compact
            )
            await ctx.send(f"```\n{output}\n```")
            tbody = []
        i+=1

    output = t2a(
        header=["Name", "Ops", "Events", "Std. Cert.", "Adv. Cert."],
        body=tbody,
        style=PresetStyle.thin_compact
    )
    await ctx.send(f"```\n{output}\n```")

@bot.command(name="test")
async def test(ctx):
    opchannel = discord.utils.get(ctx.guild.channels, name=OP_CH)

    txt = "<:Yes:603617279359451136\n\n<:Yes:1089137665472991322\n\n<:Yes: CrackShot"
    embed=discord.Embed(title="Player Status", color=0x00ff11)
    embed.add_field(name="Name", value=txt, inline=True)
    await opchannel.send(embed=embed)

# Executes the bot with the specified token. Token has been removed and used just as an example.
bot.run(DISCORD_TOKEN)
