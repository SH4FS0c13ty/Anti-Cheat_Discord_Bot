# Anti-Cheat Discord Bot
A bot that kicks cheaters based on their server list.
<br />
<br />

## Requirements

 - Windows or Linux (recents versions that supports Python 3.7.4)
 - [Python 3.7.4](https://www.python.org/downloads/release/python-374/)

## Installation

Install Python 3.7.4 wherever you want but do NOT forget to add it to the PATH if you're on Windows. <br />
Install the requirements using `pip install -r requirements.txt` or `python -m pip install -r requirements.txt`.
<br /> <br />

## Usage

Example: `python main.py <OAUTH2_CLIENT_ID> <OAUTH2_CLIENT_SECRET> <CLIENT_ID>` <br />
You can also use the "Anti-Cheat.bat" or "Anti-Cheat.sh" files to run the Bot without arguments.<br />
Don't forget to modify the files above with your real IDs to make the bot work.<br />
Don't forget to modify the "oauth.py" file according to your server to make it work.<br />
<br />
WARNING: When editing the blacklist, please add a blank line at the end of the file.<br />
The bot verify the whole line with the \[CR\]\[LF\] invisible characters at the end of the line.<br />
To see the characters, you can use Notepad++ > View > Show Symbol > Show End of Line.<br />
<br />
 
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
SH4FS0c13ty (Twitter: @SH4FS0c13ty, Discord: Le Panda Roux#1562, Github: https://github.com/SH4FS0c13ty)<br />
123321mario ((http://123321mario.tk/ , Twitter: @123321mario, Discord: 123321mario#1337, GitHub: https://github.com/123321mario)<br />
<br />
Thanks to Stanislav Vishnevskiy for his Discord OAuth2 module (https://github.com/discordapp/discord-oauth2-example)
