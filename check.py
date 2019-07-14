import discord, sys
from discord.ext import commands
from discord.utils import get

client = discord.Client()
bot = commands.Bot(command_prefix='./', description='A bot that kicks cheaters based on their server list.')

@bot.command(pass_context=True)
async def verify(ctx):
    global blacklisted
    blacklisted = 0
    print('Checking for blacklisted servers ...')
    bcheck()
    userid = open('userid.txt', mode="r", encoding="utf-8").read()
    if blacklisted == 0:
        user = client.get_user(userid)
        print("New verified user: " + userid)
        await ctx.send("Welcome to the server user " + userid)
        await ctx.author.send("[EN] Welcome to the server Pokémon GO Marseille!\n[FR] Bienvenue dans le serveur Pokémon GO Marseille !")
        role = get(ctx.guild.roles, name='Verified')
        await ctx.author.add_roles(role)
        print("Verified role applied to " + userid)
        blacklisted = 0
    else:
        print("Cheater detected!\nKicking user " + userid)
        await ctx.send("Cheater detected!")
        await ctx.send('Kicking user ' + userid)
        await ctx.author.send("[Pokémon GO Marseille] https://cdn.discordapp.com/attachments/451360093607297054/599226877277634561/IMG_20190511_111313.jpg \n[EN] You have been detected as a cheater, please contact an administrator and prove that you are not a cheater to access the server.\n[FR] Vous êtes soupçonné d'être un tricheur, veuillez contacter un administrateur et lui prouver que vous n'êtes pas un tricheur afin d'accéder au serveur.")
        write_cheater_id(userid)
        user = usr(userid)
        await ctx.guild.kick(user)
        blacklisted = 0

def write_cheater_id(id):
    if id in open('cheaters_id.txt').read():
        print("User " + id + " is already in the cheaters list")
    else:
        print("User " + id + " has been added to the cheaters list")
        f=open("cheaters_id.txt", "a+", encoding="utf-8")
        f.write(id + '\n')
        f.close()
        
@bot.event
async def on_ready():
    bot_name = bot.user.name
    bot_id = str(bot.user.id)
    print('Logged in successfully.')
    print('Name: ' + bot.user.name)
    print('ID: ' + bot_id)
    print('------')

@bot.command(pass_context=True)
async def kick(ctx, user: discord.Member):
    usr = str(user)
    print("User kicked: " + usr)
    await ctx.send("User kicked: " + usr)
    await ctx.author.send("[EN] You have been kicked from the server. Please verify yourself again to access the server.\n[FR] Vous avez été kické du serveur. Veuillez vous soumettre à une nouvelle vérification afin d'accéder au serveur.")
    await ctx.guild.kick(user)

def bcheck():
    global blacklisted
    blacklisted = 0
    blacklist = open("blacklist.txt", "r")
    guild = open("guilds.txt", "r")
    bline = blacklist.readlines()
    gline = guild.readlines()
    for x in bline:
        if x in gline:
            print("Blacklisted server found!")
            blacklisted = 1
    blacklist.close()
    guild.close()

class usr():
    def __init__(self, userid):
        self.id = userid

def start(arg):
    bot.run(arg)