# Anti-Cheat Discord Bot
Anti-Cheat v1.3 (The Masterkiller) by SH4FS0c13ty<br />
A Discord bot that kicks cheaters based on their server list and their Pokémon GO ID.<br />
<br />
Version française : https://github.com/SH4FS0c13ty/Anti-Cheat_Discord_Bot_FR
<br />

## Requirements

The requirements below can be installed when executing "Anti-Cheat Requirements Installer.bat".<br />
See the Installation section to know more.<br />
 - Windows 10
 - [Python 3.7.4](https://www.python.org/downloads/release/python-374/)
 - [Tesseract OCR](https://opensource.google.com/projects/tesseract)

## Installation

Run "Anti-Cheat Requirements Installer.bat" and select the installation that suits your system.
<br />
The installation will begin and no further action is needed.
<br />

## Usage

Run "Anti-Cheat.bat" and enter the command you want to use.<br />

### Command set<br />
Anti-Cheat process:<br />
`start|stop|restart`<br />
Anti-Cheat show lists and configuration:<br />
`show config|blacklist|cheaters_lists`<br />
Anti-Cheat reset lists and configuration:<br />
`reset config|cheaters_lists|servers_lists`<br />
Anti-Cheat set configuration:<br />
`set CLIENT_ID|CLIENT_SECRET|TOKEN|HOST|PORT`<br />
<br />
### Files used<br />
Configuration file:<br />
`scripts/config.json`<br />
Servers blacklist:<br />
`lists/blacklist.txt`<br />
Cheaters Pokémon GO IDs list (see the template included):<br />
`lists/cheaters.xlsx`<br />
Cheaters Discord IDs list:<br />
`lists/cheaters_id.txt`<br />
Cheaters associated IDs (<POKEMON_GO_ID>:<DISCORD_ID>):<br />
`lists/Associated_IDs.txt`<br />
Servers lists of users:<br />
`server_lists/<DISCORD_ID>.txt`<br />
<br />
Don't forget to configure Anti-Cheat before using it!<br />
To configure it, either modify the "config.json" file or use `set <PARAM>` commands.<br />
You should also modify "blacklist.txt" and "cheaters.xlsx" files to make it works properly.<br />
<br />
### Bot commands
 - ./verify <IMG_URL_OR_EMBEDDED_IMAGE>
 - ./kick <USER_NAME>
 - ./recheck <USER_NAME>
 
## License

MIT License (https://opensource.org/licenses/mit-license.php)<br />

Copyright (c) 2019 SH4FS0c13ty & 123321mario<br />

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and<br />
associated documentation files (the "Software"), to deal in the Software without restriction,<br />
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,<br />
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,<br />
subject to the following conditions:<br />

The above copyright notice and this permission notice shall be included in all copies or substantial<br />
portions of the Software.<br />

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT<br />
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.<br />
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,<br />
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE<br />
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.<br />
<br />

## Credits

Authors:
<br />
SH4FS0c13ty (Website: https://sh4fs0c13ty.tk/ , Twitter: @SH4FS0c13ty, Discord: SH4FS0c13ty#1562, Github: https://github.com/SH4FS0c13ty)<br />
123321mario (Website: http://123321mario.tk/ , Twitter: @123321mario, Discord: 123321mario#1337, Github: https://github.com/123321mario)<br />
<br />
Thanks to Stanislav Vishnevskiy for his Discord OAuth2 module (https://github.com/discordapp/discord-oauth2-example)