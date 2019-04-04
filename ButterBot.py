import discord
from discord.ext import commands



TOKEN = ''

client = commands.Bot(command_prefix = "`")
client.remove_command('help')



"""
***********************************************************************************************************************

Events

***********************************************************************************************************************
"""

#Event to print ready when bot starts
@client.event
async def on_ready():
    print('Ready')

#Event to print all messages in the server
@client.event
async def on_message(message):
    author = message.author
    content = message.content
    print('{}: {}'.format(author,content))
    await client.process_commands(message)

#Event to repeat back deleted message
""""@client.event
async def on_message_delete(message):
    author = message.author
    content = message.content
    channel = message.channel
    await client.send_message(channel, '{}: {}'.format(author,content))
    """

#Event to show status of bot
@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='You', type= 3))
    #type=2 Listening to
    #type=3 Watching


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

#Command to clear messages
@client.command(pass_context=True)
async def clear(ctx, amount):
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amount)+1):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say(str(amount) + ' Messages Deleted')

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

#Command to send one emote
@client.command()
async def emote():
    await client.say('<:monkaHmm:563030503523876864>')

#Command to send User a help list of all commands
@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(
        colour = discord.Colour.orange()
    )
    embed.set_author(name='Help')
    embed.add_field(name='`ping', value='Returns pong', inline=False)
    embed.add_field(name='`echo {text}', value='Returns Entered text', inline=False)
    embed.add_field(name='`display', value='Returns embed example', inline=False)
    embed.add_field(name='`emote', value='Returns an emote ', inline=False)
    embed.add_field(name='`join/`leave ', value='Bot joins/leaves the server ', inline=False)
    await client.send_message(author, embed=embed)
    #send_message = sends to user DM
    #say = send in channel

#Commands to get bot to join server
@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)

#Command to get bot to leave server
@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()

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