import discord
from discord.ext import commands


TOKEN = ''

client = commands.Bot(command_prefix = "`")

@client.event
async def on_ready():
    print('Ready')


@client.event
async def on_message(message):
    author = message.author
    content = message.content
    print('{}: {}'.format(author,content))
    await client.process_commands(message)

""""@client.event
async def on_message_delete(message):
    author = message.author
    content = message.content
    channel = message.channel
    await client.send_message(channel, '{}: {}'.format(author,content))
    """


@client.command()
async def ping():
    await client.say('pong')

@client.command()
async def echo(*args):
    output = ''
    for word in args:
        output += word
        output += ' '
    await client.say(output)

@client.command(pass_context=True)
async def clear(ctx, amount):
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amount)+1):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say(str(amount) + ' Messages Deleted')

client.run(TOKEN)