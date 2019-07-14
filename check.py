import discord, sys, os
from discord.ext import commands
from discord.utils import get

client = discord.Client()
bot = commands.Bot(command_prefix="./", description="A bot that kicks cheaters based on their server list.")

@bot.event
async def on_member_join(member):
    global blacklisted
    blacklisted = 0
    userid = str(member.id)
    print(userid + " is being verified.")
    print("Checking for blacklisted servers ...")
    bcheck(userid)
    if blacklisted == 0:
        print("No blacklist server found.\nNew verified user: " + userid + ".")
        await member.send("[EN] Welcome to the server <NAME_OF_SERVER>!\n[FR] Bienvenue dans le serveur <NOM_DU_SERVEUR> !")
        role = get(member.guild.roles, name="Verified")
        await member.add_roles(role)
        print("Verified role applied to " + userid + ".")
        blacklisted = 0
    else:
        print("Cheater detected!\nKicking user " + userid + ".")
        await member.send("[<SERVER_NAME>] https://cdn.discordapp.com/attachments/451360093607297054/599226877277634561/IMG_20190511_111313.jpg \n[EN] You have been detected as a cheater, please contact an administrator and prove that you are not a cheater to access the server.\n[FR] Vous êtes soupçonné d'être un tricheur, veuillez contacter un administrateur et lui prouver que vous n'êtes pas un tricheur afin d'accéder au serveur.")
        write_cheater_id(userid)
        user = usr(userid)
        await member.guild.kick(user)
        blacklisted = 0


@bot.command(pass_context=True)
async def verify(ctx):
    global blacklisted
    blacklisted = 0
    userid = str(ctx.author.id)
    print(userid + " is being verified.")
    print("Checking for blacklisted servers ...")
    bcheck(userid)
    if blacklisted == 0:
        print("No blacklist server found.\nNew verified user: " + userid + ".")
        await ctx.send("Welcome to the server user " + userid + ".")
        await ctx.author.send("[EN] Welcome to the server <SERVER_NAME>!\n[FR] Bienvenue dans le serveur <NOM_DU_SERVEUR> !")
        role = get(ctx.guild.roles, name="Verified")
        await ctx.author.add_roles(role)
        print("Verified role applied to " + userid + ".")
        blacklisted = 0
    else:
        print("Cheater detected!\nKicking user " + userid + ".")
        await ctx.send("Cheater detected!\nKicking user " + userid + ".")
        await ctx.author.send("[<SERVER_NAME>] https://cdn.discordapp.com/attachments/451360093607297054/599226877277634561/IMG_20190511_111313.jpg \n[EN] You have been detected as a cheater, please contact an administrator and prove that you are not a cheater to access the server.\n[FR] Vous êtes soupçonné d'être un tricheur, veuillez contacter un administrateur et lui prouver que vous n'êtes pas un tricheur afin d'accéder au serveur.")
        write_cheater_id(userid)
        user = usr(userid)
        await ctx.guild.kick(user)
        blacklisted = 0

def write_cheater_id(id):
    if id in open("cheaters_id.txt").read():
        print("User " + id + " is already in the cheaters list.")
    else:
        f=open("cheaters_id.txt", "a+", encoding="utf-8")
        f.write(id + "\n")
        f.close()
        print("User " + id + " has been added to the cheaters list.")

@bot.event
async def on_ready():
    bot_name = bot.user.name
    bot_id = str(bot.user.id)
    print("Logged in successfully.")
    print("Name: " + bot.user.name)
    print("ID: " + bot_id)
    print("------------------------")

@bot.command(pass_context=True)
async def kick(ctx, user: discord.Member):
    userid = str(user)
    print("User kicked: " + userid + ".")
    await ctx.send("User kicked: " + userid + ".")
    await ctx.author.send("[EN] You have been kicked from the server. Please verify yourself again to access the server.\n[FR] Vous avez été kické du serveur. Veuillez vous soumettre à une nouvelle vérification afin d'accéder au serveur.")
    await ctx.guild.kick(user)

def bcheck(userid):
    global blacklisted
    blacklisted = 0
    blacklist = open("blacklist.txt", "r")
    guilds = open("server_lists\\" + userid + "_server_list.txt", "r", encoding="utf-8")
    bline = blacklist.readlines()
    gline = guilds.readlines()
    for x in bline:
        if x in gline:
            print("Blacklisted server found!")
            blacklisted = 1
    blacklist.close()
    guilds.close()

class usr():
    def __init__(self, userid):
        self.id = userid

@bot.command(pass_context=True)
async def recheck(ctx, user: discord.Member):
    userid = str(user.id)
    print("User " + userid + " has been asked for a new verification.")
    role = get(ctx.guild.roles, name="Verified")
    await user.remove_roles(role)
    os.remove("server_lists\\" + userid + "_server_list.txt")
    await user.send("[<SERVER_NAME>]\n[EN] You have been asked for a new verification, please follow the autorisation link and use ./verify to verify yourself.\n[FR] Une nouvelle vérification de votre part est requise, veuillez suivre le lien d'autorisation et utilisez ./verify pour vous vérifier.")

def start(arg):
    bot.run(arg)