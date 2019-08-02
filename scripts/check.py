import discord, sys, os, requests, json, ctypes
import ocr, tools, getcolor
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.utils import get

ctypes.windll.kernel32.SetConsoleTitleW("Anti-Cheat Checker module")

client = discord.Client()
bot = commands.Bot(command_prefix="./", description="A Discord bot that kicks cheaters based on their server list and their Pokémon GO ID.")

arg = sys.argv[1]


@bot.event
async def on_member_join(member):
    global blacklisted
    blacklisted = 0
    userid = str(member.id)
    username = str(member.name)
    print("[INFO] " + username + " joined the server.")
    try:
        file =  open("lists\\cheaters_ids.txt").read()
        if file.find(userid) != -1:
            print("[WARN] " + "User " + userid + " is in the cheaters list.")
            print("[INFO] " + "Kicking " + username + ".")
            user = usr(userid)
            await member.guild.kick(user)
        else:
            print("[INFO] " + username + " is not in the cheaters list.")
    except:
        print("[WARN] Cheaters list is missing. Cannot verify " + username + ".")


@bot.command(pass_context=True)
async def verify(ctx, url=None):
    global pokeid
    global blacklisted
    blacklisted = 0
    userid = str(ctx.author.id)
    username = str(ctx.author.name)
    role = get(ctx.guild.roles, name="Verified")
    if role in ctx.author.roles:
        print("[WARN] " + username + " tried to use ./verify but is already verified.")
        await ctx.message.delete()
    else:
        if url is None:
            try:
                url = str(ctx.message.attachments[0].url)
            except:
                print("[WARN] " + username + " used ./verify without any arguments.")
                await ctx.channel.purge(limit=None, check=lambda msg: not msg.pinned)
                print("[INFO] Channel cleared.")
                return 0
        print("[INFO] " + username + " is being verified.")
        get_img(url, userid)
        if pokeid == "ERROR":
            print("[WARN] Wrong Pokémon GO page submitted. Cannot verify " + username + ".")
            await ctx.author.send("[Pokémon GO Marseille]\n:flag_us: The image you submitted for verification is wrong!\n:flag_fr: L'image que vous avez soumis pour la vérification est incorrecte !")
            await ctx.channel.purge(limit=None, check=lambda msg: not msg.pinned)
            return 0
        bcheck(userid)
        if blacklisted == 0:
            print("[INFO] " + "New verified user: " + username + ".")
            await ctx.author.send("[Pokémon GO Marseille]\n:flag_us: Welcome to the server Pokémon GO Marseille!\n:flag_fr: Bienvenue dans le serveur Pokémon GO Marseille !")
            role = get(ctx.guild.roles, name="Verified")
            await ctx.author.add_roles(role)
            print("[INFO] " + "Verified role applied to " + username + ".")
            global team
            teamrole = get(ctx.guild.roles, name=team)
            await ctx.author.add_roles(teamrole)
            print("[INFO] " + team + " role applied to " + username + ".")
            await ctx.author.edit(nick=pokeid)
            print("[INFO] " + username + " nickname changed to " + pokeid + ".")
            blacklisted = 0
        if blacklisted == 1:
            print("[WARN] " + "Cheater detected!\n[INFO] Kicking " + username + ".")
            await ctx.author.send("[Pokémon GO Marseille]\n https://cdn.discordapp.com/attachments/451360093607297054/599226877277634561/IMG_20190511_111313.jpg \n:flag_us: You have been detected as a cheater, please contact an administrator and prove that you are not a cheater to access the server.\n:flag_fr: Vous êtes soupçonné d'être un tricheur, veuillez contacter un administrateur et lui prouver que vous n'êtes pas un tricheur afin d'accéder au serveur.")
            write_cheater_id(userid)
            user = usr(userid)
            await ctx.guild.kick(user)
            blacklisted = 0
        if blacklisted == 2:
            print("[WARN] " + username + " did not authorize the bot to access his informations.")
            await ctx.author.send(":flag_us: You must authorize the bot to access your informations before verifying yourself!\n:flag_fr: Vous devez autoriser le bot à accéder à vos informations avant de vous vérifier !")
            blacklisted = 0
        await ctx.channel.purge(limit=None, check=lambda msg: not msg.pinned)
        print("[INFO] Channel cleared.")

def get_img(url, userid):
    filename = url.rsplit('/', 1)[1]
    r = requests.get(url, allow_redirects=True)
    open(filename, 'wb').write(r.content)
    global team
    team = getcolor.main_color(filename)
    global pokeid
    pokeid = ocr.getid(filename, userid)

def write_cheater_id(id):
    if os.path.isfile("lists\\cheaters_ids.txt") == True:
        file = open("lists\\cheaters_ids.txt", "r").read()
        if file.find(id) != -1:
            print("[INFO] " + "User " + id + " is already in the cheaters list.")
        else:
            f=open("lists\\cheaters_ids.txt", "a+", encoding="utf-8")
            f.write(id + "\n")
            f.close()
            print("[INFO] " + "User " + id + " has been added to the cheaters list.")
    else:
        f=open("lists\\cheaters_ids.txt", "w+", encoding="utf-8")
        f.write(id + "\n")
        f.close()
        print("[INFO] " + "User " + id + " has been added to the cheaters list.")

@bot.event
async def on_ready():
    bot_id = str(bot.user.id)
    print("Logged in successfully.")
    print("Name: " + bot.user.name)
    print("ID: " + bot_id)
    print("========================")

@bot.command(pass_context=True)
@has_permissions(administrator=True)
async def kick(ctx, user: discord.Member):
    username = str(user.name)
    print("[INFO] " + "User kicked: " + username + ".")
    await user.send(":flag_us: You have been kicked from the server. Please verify yourself again to access the server.\n:flag_fr: Vous avez été kické du serveur. Veuillez vous soumettre à une nouvelle vérification afin d'accéder au serveur.")
    await ctx.guild.kick(user)

def bcheck(userid):
    global blacklisted
    global pokeid
    blacklisted = 0
    blacklist = open("lists\\blacklist.txt", "r")
    if os.path.isfile("servers_lists\\" + userid + "_servers_list.txt") == True:
        print("[INFO] " + "Checking for blacklisted servers ...")
        guilds = open("servers_lists\\" + userid + "_servers_list.txt", "r")
        bline = blacklist.readlines()
        gline = guilds.readlines()
        for x in bline:
            x = x.split("\n", 1)[0]
            for y in gline:
                y = y.split("\n", 1)[0]
                if x == y:
                    print("[INFO] " + "Blacklisted server found!")
                    blacklisted = 1
        blacklist.close()
        guilds.close()
        if blacklisted != 1:
            print("[INFO] " + "No blacklisted server found.")
        json_check(pokeid, userid)
    else:
        blacklisted = 2

def json_check(pokid, usrid):
    global blacklisted
    print("[INFO] " + "Checking Pokémon GO cheaters list ...")
    if os.path.isfile("lists\\cheaters.json") == False:
        tools.excel2json()
    with open("lists\\cheaters.json") as json_file:
        data = json.load(json_file)
        for p in data:
            if pokeid == p["Pseudo*"]:
                print("[WARN] " + "Known Pokémon GO cheater detected.")
                if os.path.isfile("lists\\Associated_IDs.txt") == False:
                    f = open("lists\\Associated_IDs.txt", "w")
                    f.write("Pokémon_GO_ID:Discord_ID\n")
                    f.close()
                associated_ids = str(pokid + ":" + usrid + "\n")
                file = open("lists\\Associated_IDs.txt", "r").read()
                if file.find(associated_ids) != -1:
                    print("[INFO] " + "IDs already associated: " + pokid + ":" + usrid)
                else:
                    f = open("lists\\Associated_IDs.txt", "a")
                    f.write(pokid + ":" + usrid + "\n")
                    f.close()
                blacklisted = 1
    if blacklisted != 1:
        print("[INFO] " + pokeid + " is not in the cheaters list.")

class usr():
    def __init__(self, userid):
        self.id = userid

@bot.command(pass_context=True)
@has_permissions(administrator=True)
async def recheck(ctx, user: discord.Member):
    userid = str(user.id)
    username = str(user.name)
    print("[INFO] " + username + " has been asked for a new verification.")
    role = get(ctx.guild.roles, name="Verified")
    if role in user.roles:
        await user.remove_roles(role)
    role = get(ctx.guild.roles, name="instinct")
    if role in user.roles:
        await user.remove_roles(role)
    role = get(ctx.guild.roles, name="valor")
    if role in user.roles:
        await user.remove_roles(role)
    role = get(ctx.guild.roles, name="mystic")
    if role in user.roles:
        await user.remove_roles(role)
    os.remove("servers_lists\\" + userid + "_servers_list.txt")
    await user.send("[Pokémon GO Marseille]\n:flag_us: You have been asked for a new verification, please follow the autorisation link and use ./verify to verify yourself.\n:flag_fr: Une nouvelle vérification de votre part est requise, veuillez suivre le lien d'autorisation et utilisez ./verify pour vous vérifier.")

@bot.command(pass_context=True)
@has_permissions(administrator=True)
async def recheck_all(ctx):
    print("[INFO] Everyone has been asked for a new verification.")
    await ctx.send("@everyone\n[Pokémon GO Marseille]\n:flag_us: Everyone must be verified again, please follow the autorisation link and use ./verify to verify yourself.\n:flag_fr: Tout le monde doit être vérifié une nouvelle fois, veuillez suivre le lien d'autorisation et utilisez ./verify pour vous vérifier.")
    for member in ctx.message.guild.members:
        userid = member.id
        flag = False
        role = get(ctx.guild.roles, name="Admin")
        if role in member.roles:
            flag = True
        if userid == bot.user.id:
            flag=True
        if flag != True:
            role = get(ctx.guild.roles, name="Verified")
            if role in member.roles:
                await member.remove_roles(role)
            role = get(ctx.guild.roles, name="instinct")
            if role in member.roles:
                await member.remove_roles(role)
            role = get(ctx.guild.roles, name="valor")
            if role in member.roles:
                await member.remove_roles(role)
            role = get(ctx.guild.roles, name="mystic")
            if role in member.roles:
                await member.remove_roles(role)
            if os.path.isfile("servers_lists\\" + str(userid) + "_servers_list.txt") == True:
                os.remove("servers_lists\\" + str(userid) + "_servers_list.txt")

bot.run(arg)
