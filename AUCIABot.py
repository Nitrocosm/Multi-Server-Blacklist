import discord
from discord.utils import get
from discord.ext import commands
import requests
import json
from discord.ext import tasks

foundids = []
foundbans = []
userpass = {"username": "user", "password": "password"} # These go in the headers of requests.
servers = {'serverID #1': 'Server Name #1', 'serverID #2': 'Server Name #2'} # A dictionary with all the servers that participate in the multi-server blacklist and their ID
baseurl = "The URL without methods attached to the URL" # The server itself, like so: "https://127.0.0.1/". Add the slash at the end.
intents = discord.Intents.default() # This allows the bot to actually use calls that require downloading a member list possible.
intents.members = True # This took me 4 hours to find out about. Remember to always enable Intents.
client = commands.Bot(command_prefix=">>", intents=intents) # I actually don't know what this does, other than make stuff work, set intents, and set the prefix.
guild = discord.Guild # This also does something, however, I have been too scared to remove it, even if it looks like it does nothing since ctx exists.
bannableOffenses = ["racism", "software"] # These are bannable offenses. They come handy in checkbans() and autobanning().
authorizedRoles = ['Manager', 'Not Special', 'Staff', 'Ranked Mod'] # These are the roles authorised to use the bot at all.

# There's still things I want to do to make this better, so I'll still be updating this as much as I can.

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# Player Specific Commands.
@client.command()
async def getall(ctx): # This gets all of the player in the database. When I have time, I'll add in pages for the embed, as there's a 2000 char limit to them.
    authorize = rolecheck(ctx)
    if authorize:
        playername = []
        bantype = []
        response = requests.get(baseurl + "get_all", headers=userpass, data="")
        players = json.loads(response.text)
        for i in range(len(players)):
            temp = players[i]
            playerid = temp["player_id"]
            banid = temp["type"]
            playername.append("<@" + playerid + ">")
            bantype.append(banid)
        embed = discord.Embed(title="All Players In Database",
                              description="Description Field for your Embed",
                              color=0xFF5733)
        embed.set_author(name="Bot Name",
                         icon_url="Bot Icon")
        embed.set_thumbnail(
            url="Picture in the top-right corner")
        embed.add_field(name="Player Name", value='\n'.join(playername), inline=True)
        embed.add_field(name="Ban Type", value='\n'.join(bantype), inline=True)
        embed.set_footer(text="Information requested by: {}".format(ctx.author.display_name))
        await ctx.send(embed=embed)
    else:
        ctx.send('You are not authorized to use that command.')

@client.command()
async def getplayer(ctx, *, userID): # This gets a specific player from the database by ID, and creates an embed with the relevant information.
    authorize = rolecheck(ctx)
    if authorize:
        response = requests.get(baseurl + "get_player", headers=userpass, data=json.dumps({
            "player_id": userID
        }))
        player = json.loads(response.text)
        if response.text != "Player not found.":
            playerID = player["player_id"]
            serverID = servers[player["server_id"]]
            issueID = player["assigner_id"]
            banID = player["type"]
            reason = player["reason"]
            embed = discord.Embed(title='Lookup for ' + playerID,
                                  description="Specific lookup of a single user.",
                                  color=0xFF5733)
            embed.set_author(name="Bot Name",
                             icon_url="Bot Icon")
            embed.set_thumbnail(
                url="Picture in the top-right corner")
            embed.add_field(name="Player Name(if any)", value="<@{}>".format(playerID), inline=True)
            embed.add_field(name="Mod Name(if any)", value="<@{}>".format(issueID), inline=True)
            embed.add_field(name="Mod ID", value=issueID, inline=True)
            embed.add_field(name="Server ID", value=serverID, inline=True)
            embed.add_field(name="Ban Type", value=banID, inline=True)
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.set_footer(text="Information requested by: {}".format(ctx.author.display_name))
            await ctx.send(embed=embed)
    else:
        await ctx.send("You are not authorized to use this bot.")

@client.command()
async def setplayer(ctx, userID, type, *, reason): # This makes a new entry in the database. There are 4 types of bans in our database, racism, software, rulebreak, and toxicity.
    authorize = rolecheck(ctx)
    if authorize:
        url = baseurl + "set_player"
        player_id = str(userID)
        server_id = str(ctx.guild.id)
        assigner_id = str(ctx.author.id)
        bantype = type
        reason = reason
        content = {
            'player_id': player_id,
            'server_id': server_id,
            'assigner_id': assigner_id,
            'type': bantype,
            'reason': reason
        }
        data = json.dumps(content)
        response = requests.post(url, headers=userpass, data=data)
        await ctx.send(response.text)
    else:
        await ctx.send("You are not authorized to use this bot.")

@client.command()
async def racism(ctx, userID, *, reason):  # This is a racism-specific command. It is just setplayer() but the bantype is just determined by the command itself.
    authorize = rolecheck(ctx)
    if authorize:
        url = baseurl + "set_player"
        player_id = str(userID)
        server_id = str(ctx.guild.id)
        assigner_id = str(ctx.author.id)
        content = {
            'player_id': player_id,
            'server_id': server_id,
            'assigner_id': assigner_id,
            'type': "racism",
            'reason': reason
        }
        data = json.dumps(content)
        response = requests.post(url, headers=userpass, data=data)
        await ctx.send(response.text)
    else:
        await ctx.send("You are not authorized to use this bot.")

@client.command()
async def software(ctx, userID, *, reason):  # This is a software-specific command. It is just setplayer() but the bantype is just determined by the command itself.
    authorize = rolecheck(ctx)
    if authorize:
        url = baseurl + "set_player"
        player_id = str(userID)
        server_id = str(ctx.guild.id)
        assigner_id = str(ctx.author.id)
        content = {
            'player_id': player_id,
            'server_id': server_id,
            'assigner_id': assigner_id,
            'type': "software",
            'reason': reason
        }
        data = json.dumps(content)
        response = requests.post(url, headers=userpass, data=data)
        await ctx.send(response.text)
    else:
        await ctx.send("You are not authorized to use this bot.")

@client.command()
async def toxicity(ctx, userID, *, reason):  # This is a toxicity-specific command. It is just setplayer() but the bantype is just determined by the command itself.
    authorize = rolecheck(ctx)
    if authorize:
        url = baseurl + "set_player"
        player_id = str(userID)
        server_id = str(ctx.guild.id)
        assigner_id = str(ctx.author.id)
        content = {
            'player_id': player_id,
            'server_id': server_id,
            'assigner_id': assigner_id,
            'type': "toxicity",
            'reason': reason
        }
        data = json.dumps(content)
        response = requests.post(url, headers=userpass, data=data)
        await ctx.send(response.text)
    else:
        await ctx.send("You are not authorized to use this bot.")

@client.command()
async def rulebreak(ctx, userID, *, reason): # This is a rulebreak-specific command. It is just setplayer() but the bantype is just determined by the command itself.
    authorize = rolecheck(ctx)
    if authorize:
        url = baseurl + "set_player"
        player_id = str(userID)
        server_id = str(ctx.guild.id)
        assigner_id = str(ctx.author.id)
        content = {
            'player_id': player_id,
            'server_id': server_id,
            'assigner_id': assigner_id,
            'type': "rulebreak",
            'reason': reason
        }
        data = json.dumps(content)
        response = requests.post(url, headers=userpass, data=data)
        await ctx.send(response.text)
    else:
        await ctx.send("You are not authorized to use this bot.")

@client.command()
async def deleteplayer(ctx, *, userID): # Self explanatory, this deletes a player from the database.
    authorize = rolecheck(ctx)
    if authorize:
        response = requests.delete(url=baseurl + "delete_player", headers=userpass, data=json.dumps({
            "player_id": userID
        }))
        await ctx.send(response.text)
    else:
        await ctx.send("You are not authorized to use this bot.")

@client.command()
async def deleteplayers(ctx, *, userIDs): # Self explanatory, this deletes multiple players delimited by a comma.
    deletion = []
    authorize = rolecheck(ctx)
    if authorize:
        deletelist = userIDs.split(",")
        print(deletelist)
        for i in range(len(deletelist)):
            content = {
                "player_id": str(deletelist[i])
            }
            deletion.append(content)
        data = json.dumps(deletion)
        response = requests.delete(url=baseurl + "delete_players", headers=userpass, data=data)
        print(response.text)
        await ctx.send(response.text)
    else:
        await ctx.send("You are not authorized to use this bot.")

@client.command()
async def checkbans(ctx):
    authorize = rolecheck(ctx)
    if authorize:
        idchecklist = []
        fullplayerlist = []
        foundids = []
        foundbans = []
        foundnames = []
        members = ctx.guild.members
        role = get(ctx.guild.roles, id=806987487254937660) # Gets Ranked Player role
        for member in members: # Gets all players with Ranked Player role.
            if role in member.roles:
                idchecklist.append(member.id)
        url = baseurl + "get_players"
        for i in range(len(idchecklist)): # Creates the data to send to API with get_players method.
            content = {
                "player_id": idchecklist[i]
            }
            fullplayerlist.append(content)
        data = json.dumps(fullplayerlist) # Turns it suitable to send to API.
        response = requests.get(url, headers=userpass, data=data) # Request for data
        responsedict = json.loads(response.text) # Turns the response into a dictionary. This contains data on any unbanned player with Ranked Player role.
        if len(responsedict) == 0: #If there are no matches, this means all players that are on the database either are banned or aren't in the server
            await ctx.send("No Players Found! Is comp clean????")
            return responsedict
        else:
            for x in range(len(responsedict)): # Appends information recieved to according lists. There's other ways of doing this, but I couldn't be asked, as it just works.
                temp = responsedict[x]
                playerid = temp["player_id"]
                bantype = temp["type"]
                foundids.append(playerid) # Will be used for banning/suspending players later
                foundbans.append(bantype) # Will be used to check whether to ban the player or suspend them. The list here corresponds with the positions in foundids.
                foundnames.append("<@" + playerid + ">")
            embed = discord.Embed(title="**Matches Found!**",
                                  description="** **",
                                  color=0xFF5733)
            embed.set_author(name="Bot Name",
                             icon_url="Bot Icon")
            embed.set_thumbnail(
                url="Picture for top-right")
            embed.add_field(name="Player ID", value='\n'.join(foundids), inline=True)
            embed.add_field(name="Player ID", value='\n'.join(foundnames), inline=True)
            embed.add_field(name="Ban Type", value='\n'.join(foundbans), inline=True)
            embed.set_footer(text="Information requested by: {}".format(ctx.author.display_name))
            await ctx.send(embed=embed)
            #Banning section of the code. It takes all matches from the database, checks for ranked suspended players, and adds unsuspended players to byebye.
            byebye = []
            susrole = get(ctx.guild.roles, id=806987487254937669) # Gets "Ranked | Suspended" role.
            for idx in range(len(foundids)):
                susmember = ctx.guild.get_member(int(foundids[idx])) # Creates Member object using ID. get_user only gets User object, which is a parent obj independent of any guild.
                if susrole not in susmember.roles:
                    byebye.append([foundids[idx], foundbans[idx]]) # Appends any unpunished player.
            for x in range(len(byebye)): # This is where members go byebye and are either suspended from ranked play or banned from the server
                tribunal = ctx.guild.get_member(int(byebye[x][0]))
                if byebye[x][1] in bannableOffenses: # This is the ban section, for bannable offenses
                    deathsentence = await tribunal.create_dm()
                    if byebye[x][1] == 'Bantype1':
                        await deathsentence.send("Banned for bantype 1")
                    else:
                        await deathsentence.send("Banned for bantype 2")
                    await tribunal.ban(reason=byebye[x][1])
                else: # This is the suspension section, for lesser but still punishable offenses
                    deathsentence = await tribunal.create_dm()
                    if byebye[x][1] == 'rulebreak':
                        await deathsentence.send(
                            "Suspended for bantype 3")
                    else:
                        await deathsentence.send(
                            "Suspended for bantype 4")
                    await tribunal.add_roles(susrole)
    else:
        await ctx.send("You are not authorized to use this bot.")

# This was a testing command for rolecheck(). I keep it here in case I want to modify rolecheck() and want to try something new.
@client.command()
async def seerolecheck(ctx):
    member = ctx.author
    authorized = False
    for i in range(len(authorizedRoles)):
        role = discord.utils.get(ctx.guild.roles, name=authorizedRoles[i])
        if role in member.roles:
            authorized = True
            break
    if authorized:
        await ctx.send(f"You're good to go {member.mention}, you have the {role} role.")
    else:
        await ctx.send("HA, fucking non, you don't have roles, kek.")

# This regular function is the authorization function. This checks whether you have any role from the list of roles in authorized roles and will return true if you do.
def rolecheck(ctx):
    member = ctx.author # This creates a Member obj
    authorize = False 
    for i in range(len(authorizedRoles)): # This iterates through all the roles in authorizedRoles. There's more efficient ways of doing it, but when I found out 
        role = discord.utils.get(ctx.guild.roles, name=authorizedRoles[i]) # this was already a core function, and I'm too scared to fuck with it right now.
        if role in member.roles:
            authorize = True
            break
    return authorize

# This is an automated version of checkbans(), and is here because I'm forgetful and can't remember to do one thing every 8 hours.
# What's special is that you have to pass context yourself, as tasks.loop can't pass context.
# Why is guild set to one ID? I've only used it for one server, so the need hasn't risen yet. However, if I make this public, this gets fixed by adding all servers the bot
# is in to a dictionary, and if it gets bigger than 10 servers, into a database.
@tasks.loop(seconds=120)
async def autobanning():
    guild = client.get_guild("GuildID")
    channel = client.get_channel("This channel is meant to log this task.")
    idchecklist = []
    fullplayerlist = []
    foundids = []
    foundbans = []
    foundnames = []
    members = guild.members
    role = get(guild.roles, id=806987487254937660) # Gets Ranked Player role
    for member in members:  # Gets all players with Ranked Player role.
        if role in member.roles:
            idchecklist.append(member.id)
    url = baseurl + "get_players"
    for i in range(len(idchecklist)):  # Creates the data to send to API with get_players method.
        content = {
            "player_id": idchecklist[i]
        }
        fullplayerlist.append(content)
    data = json.dumps(fullplayerlist)  # Turns it suitable to send to API.
    response = requests.get(url, headers=userpass, data=data)  # Request for data
    responsedict = json.loads(
        response.text)  # Turns the response into a dictionary. This contains data on any unbanned player with Ranked Player role.
    if len(responsedict) == 0: # If there are no matches, this means all players that are on the database either are banned or aren't in the server.
        await channel.send("No Players Found! Is comp clean????")
        return responsedict
    else:
        for x in range(len(responsedict)):  # Appends information recieved to according lists. There's other ways of doing this, but I couldn't be asked, as it just works.
            temp = responsedict[x]
            playerid = temp["player_id"]
            bantype = temp["type"]
            foundids.append(playerid) # Will be used for banning/suspending players later
            foundbans.append(bantype) # Will be used to check whether to ban the player or suspend them. The list here corresponds with the positions in foundids.
            foundnames.append("<@" + playerid + ">")
        embed = discord.Embed(title="**Matches Found!**",
                              description="** **",
                              color=0xFF5733)
        embed.set_author(name="Bot Name",
                         icon_url="Bot Icon")
        embed.set_thumbnail(
            url="Picture for top-right")
        embed.add_field(name="Player ID", value='\n'.join(foundids), inline=True)
        embed.add_field(name="Player ID", value='\n'.join(foundnames), inline=True)
        embed.add_field(name="Ban Type", value='\n'.join(foundbans), inline=True)
        embed.set_footer(text="Automated Ban Check.")
        await channel.send(embed=embed)
        # Banning section of the code. It takes all matches from the database, checks for ranked suspended players, and adds unsuspended players to byebye.
        byebye = []
        susrole = get(guild.roles, id=806987487254937669)  # Gets "Ranked | Suspended" role
        for idx in range(len(foundids)):
            susmember = guild.get_member(int(foundids[idx])) # Creates Member object using ID. get_user only gets User object, which is a parent obj independent of any guild.
            if susrole not in susmember.roles:
                byebye.append([foundids[idx], foundbans[idx]]) # Appends any unpunished player.
        for x in range(len(byebye)):  # This is where members go byebye and are either suspended from ranked play or banned from the server.
            tribunal = guild.get_member(int(byebye[x][0]))
            if byebye[x][1] in bannableOffenses: # This is the ban section, for bannable offenses
                deathsentence = await tribunal.create_dm()
                if byebye[x][1] == 'Punishment Type #1':
                    reason = "Punishment Type #1"
                    await deathsentence.send(
                        "DM Message based on the punishment")
                else:
                    reason = "Punishment Type #2"
                    await deathsentence.send(
                        "DM Message based on the punishment")
                await tribunal.ban(reason=reason)
            else: # This is the suspension section, for lesser but still punishable offenses
                deathsentence = await tribunal.create_dm()
                if byebye[x][1] == 'Punishment Type #3':
                    await deathsentence.send(
                        "DM Message based on the punishment")
                else:
                    await deathsentence.send(
                        "DM Message based on the punishment")
                await tribunal.add_roles(susrole)

# This stops the bot from running autobanning() until the bot is ready, and therefore stops it from shitting itself
@autobanning.before_loop
async def before():
    await client.wait_until_ready()


autobanning.start()
# Your token can be found in your Developer Dashboard.
client.run('token')
