import discord
import random
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.utils import get
import asyncio, json, requests
import os, time, re, subprocess
from discord.utils import get


TOKEN = 'NDE1MjU1NjY4NTUxODQzODUw.XKjcIg.1AkGEUkI6x2FVtfi63SIUllovlo'

client = commands.Bot(command_prefix = "`")
client.remove_command('help')

client.counter = 0
players = {}
queues = {}

def check_queue(id):
    if queues[id] != []:
        player = queues[id].pop(0)
        players[id] = player
        player.start()


"""
***********************************************************************************************************************

Events

***********************************************************************************************************************
"""

#Event to print ready when bot starts
#Event to change game status
    #type 2 = listening
    #type 1 = playing
@client.event
async def on_ready():
    print('Ready')
    await client.change_presence(game=discord.Game(name='You', type=3))

#Event to print all messages in the server
@client.event
async def on_message(message):
    author = message.author
    content = message.content
    print('{}: {}'.format(author,content))

    """
    ***********************************************************************************************************************

                                               Simple Russian Roulette

    ***********************************************************************************************************************
    """
#if message author is client
    if message.author == client.user:
        return
#if message == 'join
    if message.content == '`enter':
        client.counter += 1
        await client.send_message(message.channel,'Player ' + str(client.counter) + ': ' + str(message.author) + ' Entered')
#if mesage == `end
    if message.content == '`end':
#chooses random number from 1 to # of players that join
        random1 = random.randint(1, (client.counter))
#Sends message with random number chosen
        await client.send_message(message.channel, 'Player ' + str(random1) + ' died a horrible death')
#resets counter back to 0
        client.counter = 0
#command so that all other commands work
    await client.process_commands(message)

@client.command(pass_context=True)
async def russian(ctx):
    await client.say('Please type `enter to enter')



"""
***********************************************************************************************************************

                                        Commands

***********************************************************************************************************************
"""

#Command to get bot to say pong
@client.command()
async def ping():
    await client.say('pong')

#Command to repeat text
@client.command()
async def echo(*args):
    output = ''
    for word in args:
        output += word
        output += ' '
    await client.say(output)

"""
***********************************************************************************************************************

                                        Simple Clear

***********************************************************************************************************************
"""

#Command to clear messages
@client.command(pass_context=True)
@has_permissions(ban_members=True)
async def clear(ctx, amount):
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amount)+1):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say(str(amount) + ' Messages Deleted')

"""
***********************************************************************************************************************

                                        Simple Embed test

***********************************************************************************************************************
"""

#Command to send an embed text
@client.command()
async def display():

    embed = discord.Embed(
        title = 'Title',
        description = 'This is the description',
        colour = discord.Colour.red()
    )

    embed.set_image(url='https://im5.ezgif.com/tmp/ezgif-5-5653b371f6e0.png')
    embed.set_author(name='Butter')
    embed.add_field(name='Field Name', value='Field Value', inline=True)
    embed.set_footer(text='This is the footer')

    await client.say(embed=embed)

"""
***********************************************************************************************************************

                                        Simple Spam

***********************************************************************************************************************
"""

#command to spam arg
@client.command(pass_context=True)
async def spam(ctx, *arg):
    await client.delete_message(ctx.message)
    for i in range(5):
        await client.say(('{}'.format(' '.join(arg))+ ' ')*5)

"""
***********************************************************************************************************************

                                        Simple Slap

***********************************************************************************************************************
"""


#command to slap mention user
@client.command(pass_context=True)
async def slap(ctx, arg):
    author = ctx.message.author.mention
    list = ['a rock', 'a pan', 'a chair', 'a fish', 'a pineapple', 'their majestic 🍆 ', 'a door', 'their hand']
    randomchoice = random.choice(list)
    await client.say(str(author) + ' has slapped ' + arg + ' with ' + randomchoice)

"""
***********************************************************************************************************************

                                        Simple Help

***********************************************************************************************************************
"""

#Command to send User a help list of all commands
@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(
        colour = discord.Colour.orange()
    )
    embed.set_author(name='Help')
    embed.add_field(name='`ping', value='Returns pong', inline=False)
    embed.add_field(name='`echo', value='Returns Entered text', inline=False)
    embed.add_field(name='`display', value='Returns embed example', inline=False)
    embed.add_field(name='`emote', value='Returns an emote ', inline=False)
    embed.add_field(name='`join/`leave ', value='Bot joins/leaves the server ', inline=False)
    embed.add_field(name='`ugg ', value='searches aram build on ugg ', inline=False)
    embed.add_field(name='`opgg ', value='searchs opgg for user ', inline=False)
    embed.add_field(name='`rps {choice} {user}', value='plays rock, paper, scissors with mentioned user ', inline=False)
    embed.add_field(name='`bj (user)', value='plays simple blackjack with mentioned user ', inline=False)
    embed.add_field(name='`roll ', value='rolls a number from 1 to 6 ', inline=False)
    embed.add_field(name='`slap ', value='slaps mentioned user ', inline=False)
    embed.add_field(name='`spam ', value='spams user input 5x5 ', inline=False)
    await client.send_message(ctx.message.channel, embed=embed)
    #send_message = sends to user DM
    #say = send in channel

"""
***********************************************************************************************************************

                                        Simple Music Player

***********************************************************************************************************************
"""




#Command to get bot to leave server
@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()

#Commands to get bot to join server
@client.command(pass_context=True)
async def play(ctx, url):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
    players[server.id] = player
    player.start()


@client.command(pass_context=True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()

@client.command(pass_context=True)
async def stop(ctx):
    id = ctx.message.server.id
    players[id].stop()

@client.command(pass_context=True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()

@client.command(pass_context=True)
async def queue(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))

    if server.id in queues:
        queues[seerver.id].append(player)
    else:
        queues[server.id] = [player]
    await client.say('Video Queued')


"""
***********************************************************************************************************************

                                        Simple Rock, Paper, Scissors 

***********************************************************************************************************************
"""

#command to play rock,paper,scissors vs the bot
@client.command(pass_context=True)
async def rps(ctx, arg1, arg2):
    list = ['rock', 'paper', 'scissors']
    randomrps = random.choice(list)
    author = ctx.message.author.mention
    await client.say(author + ' picked ' + arg1)

    #if user enters something besides rock,paper,scissors
    if (arg1 != 'rock' and arg1 != 'paper' and arg1 != 'scissors'):
        await client.say('Please enter a proper choice')

    #if user enters correct term, then lets player2 choose
    elif (arg1 == 'rock' or  arg1 =='paper' or arg1 == 'scissors'):
        await client.say(arg2 + ' picked ' + randomrps)

    #if user loses against player2, prints player2 + ' Wins'
    if(arg1 == 'rock' and randomrps == 'paper' or
            arg1 == 'scissors' and randomrps == 'rock' or
                arg1 == 'paper' and randomrps == 'scissors'):
        await client.say(arg2 + ' Wins')

    #If user wins against player2, prints 'You Win'
    if(arg1 == 'paper' and randomrps == 'rock' or
            arg1 == 'rock' and randomrps == 'scissors' or
            arg1 == 'scissors' and randomrps == 'paper'):
        await client.say(author + ' Wins')

    #If User ties with player2, prints 'You Tied'
    if(arg1 == randomrps):
        await client.say(author + ' and ' + arg2 + ' Tied')


"""
***********************************************************************************************************************

                                        Simple Blackjack

***********************************************************************************************************************
"""

#command to play simpleblackjack
@client.command(pass_context=True)
async def bj(ctx, message):
    author = ctx.message.author.mention
    #Can't use string of numbers since can't strings as int
    list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    #4 different cards 2 for each player
    randomcard1 = random.choice(list)
    randomcard2 = random.choice(list)
    randomcard3 = random.choice(list)
    randomcard4 = random.choice(list)
    #Adds the two card each player has
    sum = int(randomcard1 + randomcard2)
    sum2 = int(randomcard3 + randomcard4)
    await client.say(str(randomcard1) + ' ' + str(randomcard2) + ' = ' + str(sum))
    await client.say(str(randomcard3) + ' ' + str(randomcard4) + ' = ' + str(sum2))
    #win conditions of simpleblackjack
    if(randomcard1 + randomcard2 > randomcard3 + randomcard4):
        await client.say(author + ' Wins')
    if(randomcard1 + randomcard2 < randomcard3 + randomcard4):
        await client.say(message + ' Wins')
    if(randomcard1 + randomcard2 == randomcard3 + randomcard4):
        await client.say(author + ' and ' + member + ' Tied')


"""
***********************************************************************************************************************

                                        Simple Roll
                                        
***********************************************************************************************************************
"""


@client.command()
async def roll():
    #list of numbers 1 to 6 with their IDs
    list = ['<:one:563957318354468872>', '<:two:563957403289255936>', '<:three:563957448591802398>', '<:four:563957455885828107>', '<:five:563957461514452992>', '<:six:563957468217081874>']
    #picks a random choice out of the list
    randomnum = random.choice(list)
    #prints random number into discord channel
    await client.say(randomnum)
"""
***********************************************************************************************************************

                                        Simple Search Functions

***********************************************************************************************************************
"""
@client.command()
async def urban(*arg):
    #'{}' is the input by the users
    #'+' is what is added after each input
    #.join is what is use to join each input
    await client.say('https://www.urbandictionary.com/define.php?term=' +'{}'.format(('+'.join(arg))))

@client.command()
async def ugg(*, arg):
    await client.say('https://u.gg/lol/champions/' + arg + '/build/?queueType=normal_aram')


@client.command()
async def opgg(*arg):
    await client.say('https://na.op.gg/summoner/userName=' + '{}'.format(('+'.join(arg))))

@client.command()
async def youtube(*arg):
    await client.say('https://www.youtube.com/results?search_query=' + '{}'.format(('+'.join(arg))))

@client.command()
async def rabbit():
    await client.say('https://www.rabb.it/s/mypisc')



"""
***********************************************************************************************************************

                                        Spotify Upgrade Bot

***********************************************************************************************************************
"""


#Get account from files
def grab_accounts(US, GB):
    f = open('AccountsUS.txt', 'r')
    for line in f:
        clean = line.split('\n')
        US.append(clean[0])

    f.close()
    f = open('AccountsGB.txt', 'r')
    for line in f:
        clean = line.split('\n')
        GB.append(clean[0])

    f.close()

#Get keys from file
def keyGrab(key):
    f = open('keys.txt', 'r')
    for line in f:
        clean = line.split('\n')
        key.append(clean[0])

    f.close()

#Delete keys from file
def keyRemove(key):
    os.remove('keys.txt')
    f = open('keys.txt', 'a')
    for ELEM in key:
        f.write(ELEM + '\n')

    f.close()

#Redeem upgrades = (prefix) (country) (email) (key)
@client.command(pass_context=True)
async def redeem(ctx, arg1, arg2, arg3):
    allowed_countries = [
     'US', 'GB']
    accounts = []
    keys = []
    country = arg1.upper()
    keyGrab(keys)
    if country in allowed_countries:
        f = open('Accounts' + str(country) + '.txt', 'r')
        for line in f:
            clean = line.split('\n')
            accounts.append(clean[0])

        f.close()
    if country not in allowed_countries:
        return await (client.say('Sorry But the Country you Specified is Not Currently Offered'))
    if arg3 not in keys:
        return await (client.say('Sorry but you entered an invalid product key.'))
    if arg3 in keys:
        await client.say('Redeeming...')
        keys.remove(arg3)
        check = re.compile('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$)')
        mat = check.match(str(arg2))
        if mat:
            result = None
            while result != ',"success":true}':
                if len(accounts) == 0:
                    await client.say('Sorry We Are Out of Stock on That Country')
                    os.remove('Accounts' + str(country) + '.txt')
                    f = open('Accounts' + str(country) + '.txt', 'a')
                    for ELEM in accounts:
                        f.write(ELEM + '\n')

                    f.close()
                    break
                account = accounts.pop()
                combo = account.split(':')
                USER = combo[0]
                PASS = combo[1]
                try:
                    with requests.Session() as (c):
                        url = 'https://accounts.spotify.com/en/login?continue=https:%2F%2Fwww.spotify.com%2Fint%2Faccount%2Foverview%2F'
                        headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
                        page = c.get(url, headers=headers)
                        CSRF = page.cookies['csrf_token']
                        headers = {'Accept':'*/*',  'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1',  'Referer':'https://accounts.spotify.com/en/login/?continue=https:%2F%2Fwww.spotify.com%2Fus%2Fgooglehome%2Fregister%2F&_locale=en-US'}
                        url = 'https://accounts.spotify.com/api/login'
                        login_data = {'remember':'true',  'username':USER,  'password':PASS,  'csrf_token':CSRF}
                        cookies = dict(__bon='MHwwfC0xNDAxNTMwNDkzfC01ODg2NDI4MDcwNnwxfDF8MXwx')
                        login = c.post(url, headers=headers, data=login_data, cookies=cookies)
                        if '{"displayName":"' in login.text:
                            url = 'https://www.spotify.com/us/account/overview/'
                            capture = c.get(url, headers=headers)
                            csr = capture.headers['X-Csrf-Token']
                            url = 'https://www.spotify.com/us/family/api/master-invite-by-email/'
                            headers = {'Accept':'*/*',  'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1',  'x-csrf-token':csr}
                            login_data = {'firstName':'thomas',  'lastName':'Payne',  'email':arg2}
                            invite = c.post(url, headers=headers, json=login_data)
                            print(invite.text)
                            if '"success":true}' in invite.text:
                                await client.say(arg2 + ' has been successfully invited to a ' + country + ' Family Plan')
                                accounts.append(combo[0] + ':' + combo[1])
                                print(combo[0] + ':' + combo[1])
                                keyRemove(keys)
                                result = ',"success":true}'
                                channel = discord.utils.get(ctx.message.server.channels, name='logs')
                                await client.send_message(channel, arg2 + ' has been invited to a ' + country + ' Plan | using the key: ' + arg3 + ' | invited by the account: ' + combo[0] + ':' + combo[1] + ' | USER Who Redeemed Key: ' + str(ctx.message.author))
                                os.remove('Accounts' + str(country) + '.txt')
                                f = open('Accounts' + str(country) + '.txt', 'a')
                                for ELEM in accounts:
                                    f.write(ELEM + '\n')
                                f.close()
                                break
                            if 'message":"Invite limit reached' in invite.text:
                                result = None
                                print(combo[0] + ':' + combo[1])
                            if 'message":"No family plan found for user' in invite.text:
                                result = None
                                print(combo[0] + ':' + combo[1])
                        if '{"error":"errorInvalidCredentials"}' in login.text:
                            result = None
                            print(combo[0] + ':' + combo[1])
                except:
                    pass

                if not mat:
                    return await (client.say('Sorry But an Invalid Email Was Given'))

#Get stock of accoounts in files
@client.command()
async def stock():
    US_stock = []
    GB_stock = []
    key = []
    grab_accounts(US_stock, GB_stock)
    embed = discord.Embed(title='Stock',
      colour=discord.Colour.blue())
    embed.set_author(name='Inviter Bot', icon_url='https://cdn.discordapp.com/avatars/513839414322135062/b759fed29c2186046bfd6b7eff0bba5f.webp?size=128')
    embed.add_field(name='US', value=len(US_stock), inline=True)

    await client.say(embed=embed)

client.run(TOKEN)