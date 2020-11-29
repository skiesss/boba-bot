import os
import random

import json

import discord
from dotenv import load_dotenv
from discord.ext import commands
from tabulate import tabulate

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='b!')

boba_drinks = {
    'classic': [
        'LONGAN JUJUBE TEA',
        'BLACK/GREEN/OOLONG TEA',
        'HONEY TEA',
        'WINTER MELON TEA'
    ],
    'milktea': [
        'BLACK MILK TEA',
        'MILK GREEN TEA',
        'ROSEHIP MILK TEA',
        'COFFEE MILK TEA',
        'TARO MILK TEA',
        'HONEY MILK TEA',
        'THAI MILK TEA',
        'WINTER MELON MILK GREEN TEA',
        'OOLONG MILK TEA',
        'COCONUT MILK TEA',
        'ALMOND MILK TEA'
    ]
}

def read_file():
    with open('all_boba_drinks.json', 'r') as f:
        return json.load(f)

def write_file(all_boba_drinks):
    json_object = json.dumps(all_boba_drinks, indent = 4) 
    with open('all_boba_drinks.json', 'w') as outfile:
        outfile.write(json_object)

def reset_data():
    all_boba_drinks = {}

    for category in boba_drinks:
        for name in boba_drinks[category]:
            all_boba_drinks[name] = {
                'name': name,
                'category': category,
                'user_likes': []
            }
    
    write_file(all_boba_drinks)

def capitalize_first_letter(s):
    l = s.split(' ')
    return (' ').join([w.capitalize() for w in l])

@bot.command(name='all', help='Get all boba drinks')
async def boba(ctx):
    data = []

    all_boba_drinks = read_file()

    for name in all_boba_drinks:
        boba = all_boba_drinks[name]
        data.append([capitalize_first_letter(name), len(boba['user_likes'])])

    res = tabulate(data, headers=['Boba', 'Likes'])
    print(res)
    await ctx.send(res)

@bot.command(name='random', help='Get a random boba drink')
async def boba(ctx):
    all_boba_drinks = read_file()
    boba = random.choice(all_boba_drinks.keys())
    await ctx.send(boba['name'])

def toggle_like(name, id):
    all_boba_drinks = read_file()

    res = 'No such boba exists'
    
    if name in all_boba_drinks:
        boba = all_boba_drinks[name]

        if boba['name'] in boba['user_likes']:
            boba['user_likes'].remove(id)
        else:
            boba['user_likes'].append(id)

        name = capitalize_first_letter(boba['name'])
        likes = len(boba['user_likes'])

        res = f'{name}: 1 like'

        if likes != 1:
            res = f'{name}: {likes} likes'

    write_file(all_boba_drinks)

    return res

@bot.command(name='like', help='Like a boba drink')
async def boba(ctx):
    prefix = 'b!like'
    arg = ctx.message.content[len(prefix):].strip().upper()

    res = toggle_like(arg, ctx.message.author.id)

    await ctx.send(res)

@bot.command(name='unlike', help='Unlike a boba drink')
async def boba(ctx):
    prefix = 'b!unlike'
    arg = ctx.message.content[len(prefix):].strip().upper()

    res = toggle_like(arg, ctx.message.author.id)
    
    await ctx.send(res)

@bot.command(name='likes', help='See likes for a boba drink')
async def boba(ctx):
    all_boba_drinks = read_file()

    prefix = 'b!likes'
    arg = ctx.message.content[len(prefix):].strip().upper()

    name = capitalize_first_letter(arg)

    res = f'No likes for {arg}.'
    
    if arg in all_boba_drinks:
        boba = all_boba_drinks[arg]

        ids = boba['user_likes']
        users = []
        for id in ids:
            user = await bot.fetch_user(id)
            users.append(user.name)
            res = f'{name} ' + '{' + f'{len(users)}' + '}: ' + (', ').join(users)

    await ctx.send(res)

bot.run(TOKEN)