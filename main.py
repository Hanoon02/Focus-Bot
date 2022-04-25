# bot.py
import os
from types import NoneType
import requests, json
import discord
import datetime
from dotenv import load_dotenv
import backend

users = []

def input_date(date):
    d, m, y = date.split('/', 3)
    try:
        datetime.datetime(int(y), int(m), int(d))
        return d + '/' + m
    except:
        return False

def get_events(date):
    tasks = user.getTask(date)
    print(tasks)
    if (tasks is NoneType) or (len(tasks) == 0):
        return ['There are no tasks on the given day']
    return tasks

def get_quote():
    resp = requests.get('https://zenquotes.io/api/random')
    data = json.loads(resp.text)
    quote = data[0]['q'] + " -" + data[0]['a']
    return quote

def sign_up():
    if user.signUp() is False:
        return 'Authentication unsuccessful'
    return 'Signup successful'
    return 'You do not need to sign-up again'

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('GUILD')

intents = discord.Intents.default()
intents.members = True
bot = discord.Client(intents = intents)

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
    global user
    user = backend.User()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == 'bad bot':
        await message.author.send('Hey hey, if u don\'t like me, leave the server.')
    elif message.content == 'good bot':
        await message.add_reaction('\N{THUMBS UP SIGN}')
    elif message.content == '--help':
        await message.channel.send('enter the command --sign_up to connect your account. Then enter --D followed by date in DD/MM/YYYY format to see your schedule.')
    elif message.content == '--hello':
        await message.channel.send("hey")
    elif message.content == '--quote':
        await message.channel.send(get_quote())
    # elif message.content == '--test_image':
    #     await message.channel.send(file = discord.File(r'C:\Users\dell\AppData\Local\Programs\Python\Python310\Discord Reminder bot\cat.jpg'), content = 'Image')
    elif message.content == '--sign_up':
        msg = sign_up()
        await message.channel.send(msg)
    elif message.content.startswith('--D'):
        date = input_date(message.content[3::])
        if date is False:
            await message.channel.send('Please enter the date in DD/MM/YYYY format')
            return
        for user_event in get_events(date):
            await message.channel.send(user_event)
    elif message.content.startswith('--'):
        await message.channel.send('Invalid command, please use --help to view all the commands.')
bot.run(TOKEN)