import discord
from discord.utils import get
from discord.ext import commands
import requests
import json
from discord.ext import tasks

foundids = []
foundbans = []
userpass = {"username": "POLARIS", "password": "sl3uCMjIO1qvq0rKu2DfKm0CGKhY7g2B0IoDUREz"}
servers = {'773971022268727296': 'Olympus', '806987487174983702': 'Polaris'}
baseurl = "http://194.163.159.235:40001/"
getallid = ['508463722000416768', '193811513012649984', '218469149331030017']
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=">>", intents=intents)
guild = discord.Guild
authorizedRoles = ['Manager', 'Not Special', 'Staff', 'Ranked Mod']

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# Player Specific Commands.
@client.command()
async def getall(ctx):
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
        embed = discord.Embed(title="All Players In Database", url="https://www.edeashop.xyz",
                              description="Look at all these shitters! Haha, they got banned from all 3 servers, KEK.",
                              color=0xFF5733)
        embed.set_author(name="Soul's Automator",
                         icon_url="https://cdn.discordapp.com/avatars/709863869920837652/f25e9a614be70e82b5b9b6085244c50d.png?size=256")
        embed.set_thumbnail(
            url="https://static.wikia.nocookie.net/pixel-gun-3d/images/9/9b/Banhammerbig.png/revision/latest?cb=20200728091619")
        embed.add_field(name="Player Name", value='\n'.join(playername), inline=True)
        embed.add_field(name="Ban Type", value='\n'.join(bantype), inline=True)
        embed.set_footer(text="Information requested by: {}".format(ctx.author.display_name))
        await ctx.send(embed=embed)
    else:
        ctx.send('You are not authorized to use that command.')

@client.command()
async def getplayer(ctx, *, userID):
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
            embed.set_author(name="Soul's Automator",
                             icon_url="https://cdn.discordapp.com/avatars/709863869920837652/f25e9a614be70e82b5b9b6085244c50d.png?size=256")
            embed.set_thumbnail(
                url="https://static.wikia.nocookie.net/pixel-gun-3d/images/9/9b/Banhammerbig.png/revision/latest?cb=20200728091619")
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
async def setplayer(ctx, userID, type, *, reason):
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
async def racism(ctx, userID, *, reason):
    authorize = rolecheck(ctx)
    if authorize:
        url = baseurl + "set_player"
        player_id = str(userID)
        server_id = str(ctx.guild.id)
        assigner_id = str(ctx.author.id)
        reason = reason
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
async def software(ctx, userID, *, reason):
    authorize = rolecheck(ctx)
    if authorize:
        url = baseurl + "set_player"
        player_id = str(userID)
        server_id = str(ctx.guild.id)
        assigner_id = str(ctx.author.id)
        reason = reason
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
async def toxicity(ctx, userID, *, reason):
    authorize = rolecheck(ctx)
    if authorize:
        url = baseurl + "set_player"
        player_id = str(userID)
        server_id = str(ctx.guild.id)
        assigner_id = str(ctx.author.id)
        reason = reason
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
async def rulebreak(ctx, userID, *, reason):
    authorize = rolecheck(ctx)
    if authorize:
        url = baseurl + "set_player"
        player_id = str(userID)
        server_id = str(ctx.guild.id)
        assigner_id = str(ctx.author.id)
        reason = reason
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
async def deleteplayer(ctx, *, userID):
    authorize = rolecheck(ctx)
    if authorize:
        response = requests.delete(url=baseurl + "delete_player", headers=userpass, data=json.dumps({
            "player_id": userID
        }))
        await ctx.send(response.text)
    else:
        await ctx.send("You are not authorized to use this bot.")

@client.command()
async def deleteplayers(ctx, *, userIDs):
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
        role = get(ctx.guild.roles, id=806987487254937660)
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
        if len(responsedict) == 0:
            await ctx.send("No Players Found! Is comp clean????")
            return responsedict
        else:
            for x in range(len(responsedict)): # Makes an embed with the information
                temp = responsedict[x]
                playerid = temp["player_id"]
                bantype = temp["type"]
                foundids.append(playerid)
                foundbans.append(bantype)
                foundnames.append("<@" + playerid + ">")
            embed = discord.Embed(title="**Matches Found!**",
                                  description="** **",
                                  color=0xFF5733)
            embed.set_author(name="Soul's Automator",
                             icon_url="https://cdn.discordapp.com/avatars/709863869920837652/f25e9a614be70e82b5b9b6085244c50d.png?size=256")
            embed.set_thumbnail(
                url="https://static.wikia.nocookie.net/pixel-gun-3d/images/9/9b/Banhammerbig.png/revision/latest?cb=20200728091619")
            embed.add_field(name="Player ID", value='\n'.join(foundids), inline=True)
            embed.add_field(name="Player ID", value='\n'.join(foundnames), inline=True)
            embed.add_field(name="Ban Type", value='\n'.join(foundbans), inline=True)
            embed.set_footer(text="Information requested by: {}".format(ctx.author.display_name))
            await ctx.send(embed=embed)
            #Banning section of the code. It takes all matches from the database, checks for ranked suspended players, and adds unsuspended players to byebye?????????
            byebye = []
            susrole = get(ctx.guild.roles, id=806987487254937669)
            for idx in range(len(foundids)):
                susmember = ctx.guild.get_member(int(foundids[idx]))
                if susrole not in susmember.roles:
                    byebye.append([foundids[idx], foundbans[idx]])
            for x in range(len(byebye)): # THE FUN STUFF
                tribunal = ctx.guild.get_member(int(byebye[x][0]))
                if byebye[x][1] == 'racism' or byebye[x][1] == 'software':
                    deathsentence = await tribunal.create_dm()
                    if byebye[x][1] == 'software':
                        await deathsentence.send("You have been banned from Polaris+ for using external software on other ranked servers.\nTHIS IS AN AUTOMATED BAN BY THE AU CIA, DM xSoul#1962 IF YOU BELIEVE THIS TO BE FALSE.\nTHIS DOES NOT MEAN A SECOND CHANCE, YOUR BAN WAS NOT ACCIDENTAL IF YOU HAVE BEEN BANNED FOR EXTERNAL SOFTWARE BEFORE.")
                    else:
                        await deathsentence.send("You have been banned from Polaris+ for racism on other ranked servers.\nTHIS IS AN AUTOMATED BAN BY THE AU CIA, DM xSoul#1962 IF YOU BELIEVE THIS TO BE FALSE.\nTHIS DOES NOT MEAN A SECOND CHANCE, YOUR BAN WAS NOT ACCIDENTAL IF YOU HAVE BEEN BANNED FOR RACISM BEFORE.")
                    await tribunal.ban()
                else:
                    deathsentence = await tribunal.create_dm()
                    if byebye[x][1] == 'rulebreak':
                        await deathsentence.send(
                            "You have been banned from Polaris+ for severe rulebreaks on other ranked servers.\nTHIS IS AN AUTOMATED BAN BY THE AU CIA, DM xSoul#1962 IF YOU BELIEVE THIS TO BE FALSE.\nTHIS DOES NOT MEAN A SECOND CHANCE, YOUR BAN WAS NOT ACCIDENTAL IF YOU HAVE BEEN SUSPENDED FOR REFUSING SS OR BREAKING MULTIPLE RULES.")
                    else:
                        await deathsentence.send(
                            "You have been suspended from Polaris+ ranked play for severe toxicity on other ranked servers.\nTHIS IS AN AUTOMATED BAN BY THE AU CIA, DM xSoul#1962 IF YOU BELIEVE THIS TO BE FALSE.\nTHIS DOES NOT MEAN A SECOND CHANCE, YOUR BAN WAS NOT ACCIDENTAL IF YOU HAVE BEEN SUSPENDED FOR SEVERE TOXICITY.")
                    await tribunal.add_roles(susrole)

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


def rolecheck(ctx):
    member = ctx.author
    authorize = False
    for i in range(len(authorizedRoles)):
        role = discord.utils.get(ctx.guild.roles, name=authorizedRoles[i])
        if role in member.roles:
            authorize = True
            break
    return authorize


@tasks.loop(seconds=120)
async def autobanning():
    guild = client.get_guild(806987487174983702)
    channel = client.get_channel(878040462194253824)
    idchecklist = []
    fullplayerlist = []
    foundids = []
    foundbans = []
    foundnames = []
    members = guild.members
    role = get(guild.roles, id=806987487254937660)
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
    if len(responsedict) == 0:
        await channel.send("No Players Found! Is comp clean????")
        return responsedict
    else:
        for x in range(len(responsedict)):  # Makes an embed with the information
            temp = responsedict[x]
            playerid = temp["player_id"]
            bantype = temp["type"]
            foundids.append(playerid)
            foundbans.append(bantype)
            foundnames.append("<@" + playerid + ">")
        embed = discord.Embed(title="**Matches Found!**",
                              description="** **",
                              color=0xFF5733)
        embed.set_author(name="Soul's Automator",
                         icon_url="https://cdn.discordapp.com/avatars/709863869920837652/f25e9a614be70e82b5b9b6085244c50d.png?size=256")
        embed.set_thumbnail(
            url="https://static.wikia.nocookie.net/pixel-gun-3d/images/9/9b/Banhammerbig.png/revision/latest?cb=20200728091619")
        embed.add_field(name="Player ID", value='\n'.join(foundids), inline=True)
        embed.add_field(name="Player ID", value='\n'.join(foundnames), inline=True)
        embed.add_field(name="Ban Type", value='\n'.join(foundbans), inline=True)
        embed.set_footer(text="Automated Ban Check.")
        await channel.send(embed=embed)
        # Banning section of the code. It takes all matches from the database, checks for ranked suspended players, and adds unsuspended players to byebye?????????
        byebye = []
        susrole = get(guild.roles, id=806987487254937669)
        for idx in range(len(foundids)):
            susmember = guild.get_member(int(foundids[idx]))
            if susrole not in susmember.roles:
                byebye.append([foundids[idx], foundbans[idx]])
        for x in range(len(byebye)):  # THE FUN STUFF
            tribunal = guild.get_member(int(byebye[x][0]))
            if byebye[x][1] == 'racism' or byebye[x][1] == 'software':
                deathsentence = await tribunal.create_dm()
                if byebye[x][1] == 'software':
                    reason = "software | AUCIA"
                    await deathsentence.send(
                        "You have been banned from Polaris+ for using external software on other ranked servers.\nTHIS IS AN AUTOMATED BAN BY THE AU CIA, DM xSoul#1962 IF YOU BELIEVE THIS TO BE FALSE.\nTHIS DOES NOT MEAN A SECOND CHANCE, YOUR BAN WAS NOT ACCIDENTAL IF YOU HAVE BEEN BANNED FOR EXTERNAL SOFTWARE BEFORE.")
                else:
                    reason = "racism | AUCIA"
                    await deathsentence.send(
                        "You have been banned from Polaris+ for racism on other ranked servers.\nTHIS IS AN AUTOMATED BAN BY THE AU CIA, DM xSoul#1962 IF YOU BELIEVE THIS TO BE FALSE.\nTHIS DOES NOT MEAN A SECOND CHANCE, YOUR BAN WAS NOT ACCIDENTAL IF YOU HAVE BEEN BANNED FOR RACISM BEFORE.")
                await tribunal.ban(reason=reason)
            else:
                deathsentence = await tribunal.create_dm()
                if byebye[x][1] == 'rulebreak':
                    await deathsentence.send(
                        "You have been suspended from Polaris+ for severe rulebreaks on other ranked servers.\nTHIS IS AN AUTOMATED BAN BY THE AU CIA, DM xSoul#1962 IF YOU BELIEVE THIS TO BE FALSE.\nTHIS DOES NOT MEAN A SECOND CHANCE, YOUR BAN WAS NOT ACCIDENTAL IF YOU HAVE BEEN SUSPENDED FOR REFUSING SS OR BREAKING MULTIPLE RULES.")
                else:
                    await deathsentence.send(
                        "You have been suspended from Polaris+ ranked play for severe toxicity on other ranked servers.\nTHIS IS AN AUTOMATED BAN BY THE AU CIA, DM xSoul#1962 IF YOU BELIEVE THIS TO BE FALSE.\nTHIS DOES NOT MEAN A SECOND CHANCE, YOUR BAN WAS NOT ACCIDENTAL IF YOU HAVE BEEN SUSPENDED FOR SEVERE TOXICITY.")
                await tribunal.add_roles(susrole)

@autobanning.before_loop
async def before():
    await client.wait_until_ready()

# Token.
#autobanning.start()
client.run('NzA5ODYzODY5OTIwODM3NjUy.XrsGPw.kLO9btLFkvjmP_F7FSfzLdfLMeg')
