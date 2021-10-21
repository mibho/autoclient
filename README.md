# autoclient
WIP 1st push

NOTE: code structure/design for autoDB, BotFunctionTools, and BotFunctions are absolute garbage, as they were (still are) WIP. The logic of this entire bot has
been overhauled several times and maintained solely by me. I refined the core logic so many times, it's almost at an acceptable state (after cleaning ofc). I was 
keeping a log of updates every now and then on a discord server I made to keep track of this project. In hindsight, I should've just done everything on github <_>
Discord logs will be included to provide insight on how I was approaching design/implementation problems.

Brief details regarding each .py file:

dumpsysparse - automatically scan for proper input device required for ADB commands in Nox.

processTools - use win32 API to detect running instances of Nox client

NoxClientHandler - handles initializing ADB and manages state of client (ie, is client id_x running? if not, open it for them)
  [ideal end goal of this project is to just "set it and forget it". if nox client freezes/crashes, Auto will restart it and handle it]
 
NoxClientManager - auto-detect every running instance of Nox and correctly match each client w/ their respective port IDs (required for ADB). Supports multi-client.

autoDB - use sqlite3 to store/retrieve data regarding each client (in-game account stats, 

BotData - currently accessing data by having the pngs locally in same directory. Once all the img templates are collected, they will be converted into base64 strings.
          (ie, it'll be a standalone .exe thatll run w/o needing extra files on a system [via py2exe])

BotTools - img processing + comparisons and implementations of certain ADB commands to be used by the bot.

BotFunctionTools - consists of functions pertaining to the game and those are put together in BotFunctions and make up a bot feature.

BotFunctions - functions that each represent a feature of the bot: (eg: autofame, autoquest, autocompletemissions, etc)

------------
constants
gamestatus
coords
ROIcoords
------------
the above files are related to game data used in BotFunctionTools. 
