@echo off
title Anti-Cheat Discord Bot by SH4FS0c13ty
chcp 65001
cls
echo.
echo  █████╗ ███╗   ██╗████████╗██╗       ██████╗██╗  ██╗███████╗ █████╗ ████████╗
echo ██╔══██╗████╗  ██║╚══██╔══╝██║      ██╔════╝██║  ██║██╔════╝██╔══██╗╚══██╔══╝
echo ███████║██╔██╗ ██║   ██║   ██║█████╗██║     ███████║█████╗  ███████║   ██║   
echo ██╔══██║██║╚██╗██║   ██║   ██║╚════╝██║     ██╔══██║██╔══╝  ██╔══██║   ██║   
echo ██║  ██║██║ ╚████║   ██║   ██║      ╚██████╗██║  ██║███████╗██║  ██║   ██║   
echo ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝       ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   
echo.
echo Anti-Cheat v1.3 (The Masterkiller) by SH4FS0c13ty
echo A Discord bot that kicks cheaters based on their server list and their Pokémon GO ID.
echo.
echo Type "help" to show the help menu.

:prompt
echo.
set /p start=Anti-Cheat:~$ 
echo.
if /i "%start%" EQU "exit" exit
if /i "%start%" EQU "help" goto help
if /i "%start%" EQU "about" goto about
if /i "%start%" EQU "license" goto license

if /i "%start%" EQU "start" goto start
if /i "%start%" EQU "stop" goto stop
if /i "%start%" EQU "restart" goto restart

if /i "%start%" EQU "show config" goto show_conf
if /i "%start%" EQU "show blacklist" goto show_bl
if /i "%start%" EQU "show cheaters_lists" goto show_cheaters

if /i "%start%" EQU "reset cheaters_lists" goto reset_cheaters
if /i "%start%" EQU "reset servers_lists" goto reset_servers
if /i "%start%" EQU "reset config" goto reset_conf

if /i "%start%" EQU "set CLIENT_ID" goto set_client_id
if /i "%start%" EQU "set CLIENT_SECRET" goto set_client_secret
if /i "%start%" EQU "set TOKEN" goto set_token
if /i "%start%" EQU "set HOST" goto set_host
if /i "%start%" EQU "set PORT" goto set_port
if /i "%start%" EQU "set REDIRECT_URL" goto set_redirect_url

echo Unknown command.

goto prompt

:help
echo Help - Command set
echo.
echo exit                              Exit the Anti-Cheat command prompt
echo help                              Show this menu
echo about                             Show the about section
echo license                           Show the license
echo.
echo start                             Start Anti-Cheat (Bot and webserver)
echo stop                              Stop Anti-Cheat (Bot and webserver)
echo restart                           Restart Anti-Cheat (Bot and webserver)
echo.
echo show config                       Show the configuration
echo show blacklist                    Show the current blacklist
echo show cheaters_lists               Show the cheaters lists [MENU]
echo.
echo reset cheaters_lists              Reset the cheaters lists [MENU]
echo reset servers_lists               Reset the servers lists
echo reset config                      Reset the configuration file
echo.
echo set CLIENT_ID                     Set the OAUTH2_CLIENT_ID value in configuration file
echo set CLIENT_SECRET                 Set the OAUTH2_CLIENT_SECRET value in configuration file
echo set TOKEN                         Set the BOT_TOKEN value in configuration file
echo set HOST                          Set the IP address of the webserver host
echo set PORT                          Set the port number in configuration file
echo set REDIRECT_URL                  Set the URL for redirection in configuration file
goto prompt

:about
cls
echo.
echo  █████╗ ███╗   ██╗████████╗██╗       ██████╗██╗  ██╗███████╗ █████╗ ████████╗
echo ██╔══██╗████╗  ██║╚══██╔══╝██║      ██╔════╝██║  ██║██╔════╝██╔══██╗╚══██╔══╝
echo ███████║██╔██╗ ██║   ██║   ██║█████╗██║     ███████║█████╗  ███████║   ██║   
echo ██╔══██║██║╚██╗██║   ██║   ██║╚════╝██║     ██╔══██║██╔══╝  ██╔══██║   ██║   
echo ██║  ██║██║ ╚████║   ██║   ██║      ╚██████╗██║  ██║███████╗██║  ██║   ██║   
echo ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝       ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   
echo.
echo Anti-Cheat v1.3 (The Masterkiller) by SH4FS0c13ty
echo A Discord bot that kicks cheaters based on their server list and their Pokémon GO ID.
echo.
echo This project was born on a demand of 123321mario (http://123321mario.tk/) who
echo wanted to prevent cheaters from entering legit Pokémon GO servers.
echo As I like to get my hands dirty, I started this project, improved it until the
echo last build which is at https://github.com/SH4FS0c13ty/Anti-Cheat_Discord_Bot
echo.
scripts\tools.py contact
goto prompt

:license
type LICENSE
goto prompt

:start
python scripts\\main.py scripts\\config.json
goto prompt

:stop
for /F %%q in (scripts\\oauth_pid.txt) do (
	echo Killing Anti-Cheat OAuth2 module with PID %%q ...
	taskkill /F /PID:%%q
)
for /F %%p in (scripts\\check_pid.txt) do (
	echo Killing Anti-Cheat Checker module with PID %%p ...
	taskkill /F /PID:%%p
)
goto prompt

:restart
echo Restarting Anti-Cheat ...
for /F %%q in (scripts\\oauth_pid.txt) do (
	echo Killing Anti-Cheat OAuth2 module with PID %%q ...
	taskkill /F /PID:%%q
)
for /F %%p in (scripts\\check_pid.txt) do (
	echo Killing Anti-Cheat Checker module with PID %%p ...
	taskkill /F /PID:%%p
)
echo.
python scripts\\main.py scripts\\config.json
goto prompt

:show_conf
python scripts\\tools.py show_config
goto prompt

:show_bl
type lists\\blacklist.txt
goto prompt

:show_cheaters
cls
echo.
echo Cheaters lists menu
echo ===================
echo.
echo 1 - Show cheaters Discord IDs
echo 2 - Show cheaters Pokémon Go IDs
echo 3 - Show cheaters associated IDs
echo.
echo 0 - Exit this menu
echo.
set /p menu1=Enter a number [0~3]:~$ 
echo.
if /i "%menu1%" EQU "0" cls && goto prompt
if /i "%menu1%" EQU "1" goto show_cheaters_did
if /i "%menu1%" EQU "2" goto show_cheaters_pid
if /i "%menu1%" EQU "3" goto show_cheaters_aid

echo Unknown number.

goto show_cheaters

:show_cheaters_did
echo Cheaters Discord IDs
echo ====================
echo.
type lists\\cheaters_ids
echo.
pause
goto show_cheaters

:show_cheaters_pid
echo Cheaters Pokémon GO IDs
echo =======================
echo.
python scripts\\tools.py show_cheaters_pid
pause
goto show_cheaters

:show_cheaters_aid
echo Cheaters associated IDs
echo =======================
echo.
type lists\\Associated_IDs.txt
echo.
pause
goto show_cheaters

:reset_cheaters
cls
echo.
echo Cheaters lists menu
echo ===================
echo.
echo 1 - Resest cheaters Discord IDs
echo 2 - Reset cheaters Pokémon Go IDs
echo 3 - Reset cheaters associated IDs
echo.
echo 0 - Exit this menu
echo.
set /p menu2=Enter a number [0~3]:~$ 
echo.
if /i "%menu2%" EQU "0" cls && goto prompt
if /i "%menu2%" EQU "1" goto reset_cheaters_did
if /i "%menu2%" EQU "2" goto reset_cheaters_pid
if /i "%menu2%" EQU "3" goto reset_cheaters_aid

echo Unknown number.

goto reset_cheaters

:reset_cheaters_did
del /Q lists\\cheaters_ids
echo.
echo Cheaters Discord IDs list deleted.
echo.
pause
goto reset_cheaters

:reset_cheaters_pid
del /Q lists\\cheaters.json
echo.
echo Cheaters Pokémon GO IDs list deleted.
echo.
pause
goto reset_cheaters

:reset_cheaters_aid
del /Q lists\\Associated_IDs.txt
echo.
echo Cheaters associated IDs list deleted.
echo.
pause
goto reset_cheaters

:reset_servers
del /Q servers_lists\\*
echo Server lists have been deleted.
goto prompt

:reset_conf
echo Resetting configuration file ...
scripts\\tools.py reset_json
goto prompt

:set_client_id
echo CLIENT_ID value must be only a number.
echo.
scripts\\tools.py set CLIENT_ID
goto prompt

:set_client_secret
scripts\\tools.py set CLIENT_SECRET
goto prompt

:set_token
scripts\\tools.py set TOKEN
goto prompt

:set_host
echo HOST value must be somthing like XXX.XXX.XXX.XXX (the number of Xs doesn't matter).
echo.
scripts\\tools.py set HOST
goto prompt

:set_port
echo PORT value must be only a number.
echo.
scripts\\tools.py set PORT
goto prompt

:set_redirect_url
scripts\\tools.py set REDIRECT_URL
goto prompt