import discord, sys, os, requests, json, ctypes, traceback
import ocr, tools, getcolor
from discord.ext import commands
from discord.ext.commands import has_permissions, CommandNotFound
from discord.utils import get
import colorama
from colorama import Fore, Style

colorama.init()

ctypes.windll.kernel32.SetConsoleTitleW("Anti-Cheat Checker module")

client = discord.Client()
bot = commands.Bot(command_prefix="./", description="A Discord bot that kicks cheaters based on their server list and their Pokémon GO ID.")

arg = sys.argv[1]

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        user = str(ctx.author)
        userid = str(ctx.author.id)
        print(Fore.RED + Style.BRIGHT + "[WARN] An unknown command has been submitted. Please check the Anti-Cheat.log file to know more." + Style.RESET_ALL)
        print(Fore.RED + Style.BRIGHT + "[WARN] Error triggered by " + user + " with ID " + userid + "." + Style.RESET_ALL)
        tools.log("[WARN] User " + user + " with ID " + userid + " triggered the following error:")
        tools.log("[ERRO] " + str(error))

@bot.event
async def on_member_join(member):
    try:
        global blacklisted
        blacklisted = 0
        userid = str(member.id)
        username = str(member.name)
        print("[INFO] " + username + " joined the server.")
        tools.log("[INFO] " + username + " joined the server.")
        try:
            file =  open("lists\\cheaters_ids.txt").read()
            if file.find(userid) != -1:
                print(Fore.RED + Style.BRIGHT + "[WARN] " + "User " + userid + " is in the cheaters list." + Style.RESET_ALL)
                print("[INFO] " + "Kicking " + username + ".")
                tools.log("[WARN] " + "User " + userid + " is in the cheaters list.")
                tools.log("[INFO] " + "Kicking " + username + ".")
                user = usr(userid)
                await member.guild.kick(user)
            else:
                print("[INFO] " + username + " is not in the cheaters list.")
                tools.log("[INFO] " + username + " is not in the cheaters list.")
        except:
            print(Fore.RED + Style.BRIGHT + "[WARN] Cheaters list is missing. Cannot verify " + username + "." + Style.RESET_ALL)
            tools.log("[WARN] Cheaters list is missing. Cannot verify " + username + ".")
    except KeyboardInterrupt:
        return
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + "[WARN] An unknown error occured. Please check the Anti-Cheat.log and Anti-Cheat_traceback.log files to know more." + Style.RESET_ALL)
        tools.log("[ERRO] " + str(e))
        tools.log_traceback(traceback.format_exc())
    

@bot.command(pass_context=True)
async def verify(ctx, url=None):
    try:
        global pokeid
        global blacklisted
        blacklisted = 0
        userid = str(ctx.author.id)
        username = str(ctx.author.name)
        role = get(ctx.guild.roles, name="Verified")
        if role in ctx.author.roles:
            print(Fore.RED + Style.BRIGHT + "[WARN] " + username + " tried to use ./verify but is already verified." + Style.RESET_ALL)
            tools.log("[WARN] " + username + " tried to use ./verify but is already verified.")
            await ctx.message.delete()
        else:
            if url is None:
                try:
                    url = str(ctx.message.attachments[0].url)
                except:
                    print(Fore.RED + Style.BRIGHT + "[WARN] " + username + " used ./verify without any arguments." + Style.RESET_ALL)
                    tools.log("[WARN] " + username + " used ./verify without any arguments.")
                    await ctx.channel.purge(limit=None, check=lambda msg: not msg.pinned)
                    print("[INFO] Channel cleared.")
                    tools.log("[INFO] Channel cleared.")
                    return 0
            print("[INFO] " + username + " is being verified.")
            tools.log("[INFO] " + username + " is being verified.")
            get_img(url, userid)
            if pokeid == "ERROR":
                print(Fore.RED + Style.BRIGHT + "[WARN] Wrong Pokémon GO page submitted. Cannot verify " + username + "." + Style.RESET_ALL)
                tools.log("[WARN] Wrong Pokémon GO page submitted. Cannot verify " + username + ".")
                await ctx.author.send("[Pokémon GO Marseille]\n:flag_us: The image you submitted for verification is wrong!\n:flag_fr: L'image que vous avez soumis pour la vérification est incorrecte !")
                await ctx.channel.purge(limit=None, check=lambda msg: not msg.pinned)
                return 0
            bcheck(userid)
            if blacklisted == 0:
                print("[INFO] " + "New verified user: " + username + ".")
                tools.log("[INFO] " + "New verified user: " + username + ".")
                await ctx.author.send("[Pokémon GO Marseille]\n:flag_us: Welcome to the server Pokémon GO Marseille!\n:flag_fr: Bienvenue dans le serveur Pokémon GO Marseille !")
                role = get(ctx.guild.roles, name="Verified")
                await ctx.author.add_roles(role)
                print("[INFO] " + "Verified role applied to " + username + ".")
                tools.log("[INFO] " + "Verified role applied to " + username + ".")
                global team
                teamrole = get(ctx.guild.roles, name=team)
                await ctx.author.add_roles(teamrole)
                print("[INFO] " + team + " role applied to " + username + ".")
                tools.log("[INFO] " + team + " role applied to " + username + ".")
                await ctx.author.edit(nick=pokeid)
                print("[INFO] " + username + " nickname changed to " + pokeid + ".")
                tools.log("[INFO] " + username + " nickname changed to " + pokeid + ".")
                blacklisted = 0
            if blacklisted == 1:
                print(Fore.RED + Style.BRIGHT + "[WARN] " + "Cheater detected!\n[WRAN] Kicking " + username + "." + Style.RESET_ALL)
                tools.log("[WARN] " + "Cheater detected!\n[WARN] Kicking " + username + ".")
                await ctx.author.send("[Pokémon GO Marseille]\n https://cdn.discordapp.com/attachments/451360093607297054/599226877277634561/IMG_20190511_111313.jpg \n:flag_us: You have been detected as a cheater, please contact an administrator and prove that you are not a cheater to access the server.\n:flag_fr: Vous êtes soupçonné d'être un tricheur, veuillez contacter un administrateur et lui prouver que vous n'êtes pas un tricheur afin d'accéder au serveur.")
                write_cheater_id(userid)
                user = usr(userid)
                await ctx.guild.kick(user)
                blacklisted = 0
            if blacklisted == 2:
                print(Fore.RED + Style.BRIGHT + "[WARN] " + username + " did not authorize the bot to access his informations." + Style.RESET_ALL)
                tools.log("[WARN] " + username + " did not authorize the bot to access his informations.")
                await ctx.author.send(":flag_us: You must authorize the bot to access your informations before verifying yourself!\n:flag_fr: Vous devez autoriser le bot à accéder à vos informations avant de vous vérifier !")
                blacklisted = 0
            await ctx.channel.purge(limit=None, check=lambda msg: not msg.pinned)
            print("[INFO] Channel cleared.")
            tools.log("[INFO] Channel cleared.")
    except KeyboardInterrupt:
        return
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + "[WARN] An unknown error occured. Please check the Anti-Cheat.log and Anti-Cheat_traceback.log files to know more." + Style.RESET_ALL)
        tools.log("[ERRO] " + str(e))
        tools.log_traceback(traceback.format_exc())

@verify.error
async def verify_error(ctx, error):
    user = str(ctx.author)
    userid = str(ctx.author.id)
    print(Fore.RED + Style.BRIGHT + "[WARN] An error occured while trying to use the ./verify command. Please check the Anti-Cheat.log file to know more." + Style.RESET_ALL)
    print(Fore.RED + Style.BRIGHT + "[WARN] Error triggered by " + user + " with ID " + userid + "." + Style.RESET_ALL)
    tools.log("[WARN] User " + user + " with ID " + userid + " triggered the following error while using ./verify command:")
    tools.log("[ERRO] " + str(error))

def get_img(url, userid):
    try:
        filename = url.rsplit('/', 1)[1]
        r = requests.get(url, allow_redirects=True)
        open(filename, 'wb').write(r.content)
        global team
        team = getcolor.main_color(filename)
        global pokeid
        pokeid = ocr.getid(filename, userid)
    except KeyboardInterrupt:
        return
    except IndexError as i:
        print(Fore.RED + Style.BRIGHT + "[WARN] Incorrect URL submitted. Please check the Anti-Cheat.log and Anti-Cheat_traceback.log files to know more." + Style.RESET_ALL)
        tools.log("[ERRO] " + str(i))
        tools.log_traceback(traceback.format_exc())
        pokeid = "ERROR"
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + "[WARN] An unknown error occured. Please check the Anti-Cheat.log and Anti-Cheat_traceback.log files to know more." + Style.RESET_ALL)
        tools.log("[ERRO] " + str(e))
        tools.log_traceback(traceback.format_exc())

def write_cheater_id(id):
    try:
        if os.path.isfile("lists\\cheaters_ids.txt") == True:
            file = open("lists\\cheaters_ids.txt", "r").read()
            if file.find(id) != -1:
                print("[INFO] " + "User " + id + " is already in the cheaters list.")
                tools.log("[INFO] " + "User " + id + " is already in the cheaters list.")
            else:
                f=open("lists\\cheaters_ids.txt", "a+", encoding="utf-8")
                f.write(id + "\n")
                f.close()
                print("[INFO] " + "User " + id + " has been added to the cheaters list.")
                tools.log("[INFO] " + "User " + id + " has been added to the cheaters list.")
        else:
            f=open("lists\\cheaters_ids.txt", "w+", encoding="utf-8")
            f.write(id + "\n")
            f.close()
            print("[INFO] " + "User " + id + " has been added to the cheaters list.")
            tools.log("[INFO] " + "User " + id + " has been added to the cheaters list.")
    except KeyboardInterrupt:
        return
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + "[WARN] An unknown error occured. Please check the Anti-Cheat.log and Anti-Cheat_traceback.log files to know more." + Style.RESET_ALL)
        tools.log("[ERRO] " + str(e))
        tools.log_traceback(traceback.format_exc())

@bot.event
async def on_ready():
    try:
        bot_id = str(bot.user.id)
        print("Logged in successfully.")
        print("Name: " + bot.user.name)
        print("ID: " + bot_id)
        print("========================")
        tools.log("[INFO] Logged in as " + bot.user.name + " with ID " + bot_id + ".")
    except KeyboardInterrupt:
        return
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + "[WARN] An unknown error occured. Please check the Anti-Cheat.log file to know more." + Style.RESET_ALL)
        tools.log("[ERRO] " + str(e))
        tools.log_traceback(traceback.format_exc())

@bot.command(pass_context=True)
@has_permissions(administrator=True)
async def kick(ctx, user: discord.Member):
    try:
        username = str(user.name)
        print("[INFO] " + "User kicked: " + username + ".")
        tools.log("[INFO] " + "User kicked: " + username + ".")
        await user.send(":flag_us: You have been kicked from the server. Please verify yourself again to access the server.\n:flag_fr: Vous avez été kické du serveur. Veuillez vous soumettre à une nouvelle vérification afin d'accéder au serveur.")
        await ctx.guild.kick(user)
    except KeyboardInterrupt:
        return
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + "[WARN] An unknown error occured. Please check the Anti-Cheat.log and Anti-Cheat_traceback.log files to know more." + Style.RESET_ALL)
        tools.log("[ERRO] " + str(e))
        tools.log_traceback(traceback.format_exc())

@kick.error
async def kick_error(ctx, error):
    user = str(ctx.author)
    userid = str(ctx.author.id)
    print(Fore.RED + Style.BRIGHT + "[WARN] An error occured while trying to use the ./kick command. Please check the Anti-Cheat.log file to know more." + Style.RESET_ALL)
    print(Fore.RED + Style.BRIGHT + "[WARN] Error triggered by " + user + " with ID " + userid + "." + Style.RESET_ALL)
    tools.log("[WARN] User " + user + " with ID " + userid + " triggered the following error while using ./kick command:")
    tools.log("[ERRO] " + str(error))

def bcheck(userid):
    try:
        global blacklisted
        global pokeid
        blacklisted = 0
        blacklist = open("lists\\blacklist.txt", "r")
        if os.path.isfile("servers_lists\\" + userid + "_servers_list.txt") == True:
            print("[INFO] " + "Checking for blacklisted servers ...")
            tools.log("[INFO] " + "Checking for blacklisted servers ...")
            guilds = open("servers_lists\\" + userid + "_servers_list.txt", "r")
            bline = blacklist.readlines()
            gline = guilds.readlines()
            for x in bline:
                x = x.split("\n", 1)[0]
                for y in gline:
                    y = y.split("\n", 1)[0]
                    if x == y:
                        print("[INFO] " + "Blacklisted server found!")
                        tools.log("[INFO] " + "Blacklisted server found!")
                        blacklisted = 1
            blacklist.close()
            guilds.close()
            if blacklisted != 1:
                print("[INFO] " + "No blacklisted server found.")
                tools.log("[INFO] " + "No blacklisted server found.")
            json_check(pokeid, userid)
        else:
            blacklisted = 2
    except KeyboardInterrupt:
        return
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + "[WARN] An unknown error occured. Please check the Anti-Cheat.log and Anti-Cheat_traceback.log files to know more." + Style.RESET_ALL)
        tools.log("[ERRO] " + str(e))
        tools.log_traceback(traceback.format_exc())

def json_check(pokid, usrid):
    try:
        global blacklisted
        print("[INFO] " + "Checking Pokémon GO cheaters list ...")
        tools.log("[INFO] " + "Checking Pokémon GO cheaters list ...")
        if os.path.isfile("lists\\cheaters.json") == False:
            tools.excel2json()
        with open("lists\\cheaters.json") as json_file:
            data = json.load(json_file)
            for p in data:
                if pokeid == p["Pseudo*"]:
                    print(Fore.RED + Style.BRIGHT + "[WARN] " + "Known Pokémon GO cheater detected." + Style.RESET_ALL)
                    tools.log("[WARN] " + "Known Pokémon GO cheater detected.")
                    if os.path.isfile("lists\\Associated_IDs.txt") == False:
                        f = open("lists\\Associated_IDs.txt", "w")
                        f.write("Pokémon_GO_ID:Discord_ID\n")
                        f.close()
                    associated_ids = str(pokid + ":" + usrid + "\n")
                    file = open("lists\\Associated_IDs.txt", "r").read()
                    if file.find(associated_ids) != -1:
                        print("[INFO] " + "IDs already associated: " + pokid + ":" + usrid)
                        tools.log("[INFO] " + "IDs already associated: " + pokid + ":" + usrid)
                    else:
                        f = open("lists\\Associated_IDs.txt", "a")
                        f.write(pokid + ":" + usrid + "\n")
                        f.close()
                    blacklisted = 1
        if blacklisted != 1:
            print("[INFO] " + pokeid + " is not in the cheaters list.")
            tools.log("[INFO] " + pokeid + " is not in the cheaters list.")
    except KeyboardInterrupt:
        return
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + "[WARN] An unknown error occured. Please check the Anti-Cheat.log and Anti-Cheat_traceback.log files to know more." + Style.RESET_ALL)
        tools.log("[ERRO] " + str(e))
        tools.log_traceback(traceback.format_exc())

class usr():
    def __init__(self, userid):
        self.id = userid

@bot.command(pass_context=True)
@has_permissions(administrator=True)
async def recheck(ctx, user: discord.Member):
    try:
        userid = str(user.id)
        username = str(user.name)
        print("[INFO] " + username + " has been asked for a new verification.")
        tools.log("[INFO] " + username + " has been asked for a new verification.")
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
    except KeyboardInterrupt:
        return
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + "[WARN] An unknown error occured. Please check the Anti-Cheat.log and Anti-Cheat_traceback.log files to know more." + Style.RESET_ALL)
        tools.log("[ERRO] " + str(e))
        tools.log_traceback(traceback.format_exc())

@recheck.error
async def recheck_error(ctx, error):
    user = str(ctx.author)
    userid = str(ctx.author.id)
    print(Fore.RED + Style.BRIGHT + "[WARN] An error occured while trying to use the ./recheck command. Please check the Anti-Cheat.log file to know more." + Style.RESET_ALL)
    print(Fore.RED + Style.BRIGHT + "[WARN] Error triggered by " + user + " with ID " + userid + "." + Style.RESET_ALL)
    tools.log("[WARN] User " + user + " with ID " + userid + " triggered the following error while using ./recheck command:")
    tools.log("[ERRO] " + str(error))

@bot.command(pass_context=True)
@has_permissions(administrator=True)
async def recheck_all(ctx):
    try:
        print("[INFO] Everyone has been asked for a new verification.")
        tools.log("[INFO] Everyone has been asked for a new verification.")
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
    except KeyboardInterrupt:
        return
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + "[WARN] An unknown error occured. Please check the Anti-Cheat.log and Anti-Cheat_traceback.log files to know more." + Style.RESET_ALL)
        tools.log("[ERRO] " + str(e))
        tools.log_traceback(traceback.format_exc())

@recheck_all.error
async def recheck_all_error(ctx, error):
    user = str(ctx.author)
    userid = str(ctx.author.id)
    print(Fore.RED + Style.BRIGHT + "[WARN] An error occured while trying to use the ./recheck_all command. Please check the Anti-Cheat.log file to know more." + Style.RESET_ALL)
    print(Fore.RED + Style.BRIGHT + "[WARN] Error triggered by " + user + " with ID " + userid + "." + Style.RESET_ALL)
    tools.log("[WARN] User " + user + " with ID " + userid + " triggered the following error while using ./recheck_all command:")
    tools.log("[ERRO] " + str(error))

bot.run(arg)
