import discord
from discord.ext import commands
import json
import requests
import os
import random

client = commands.Bot(command_prefix="e!")


@client.event
async def on_ready():
    print("Bot is ready")

@client.command()
@commands.has_role('storageHandler')
async def create(ctx):
    # we create json data if its not created
    url = 'https://api.jsonbin.io/b'
    headers = {
        'Content-Type': 'application/json',
        'secret-key': '$2b$10$c89s/iiSGakICOZ4K4Nl8uSNCpziZ9OutIp3VnCzaPZhHaFbocOs.'
    }
    users = await get_users_data()
    req = requests.post(url, json=users, headers=headers)
    print(req.text)

@client.command()
@commands.has_role('storageHandler')
async def update(ctx):
    url = 'https://api.jsonbin.io/b/5fc6a83c9abe4f6e7cae4181'
    headers = {'secret-key': '$2b$10$c89s/iiSGakICOZ4K4Nl8uSNCpziZ9OutIp3VnCzaPZhHaFbocOs.'}
    users = await load_users()
    await set_users_data(users)
    req = requests.put(url, json=users, headers=headers)

@client.command()
async def show(ctx, member: discord.Member):
    await open_account(member)

    user = member
    users = await load_users()

    em = discord.Embed(title=f"{member.name}'s troops formation info", color=discord.Color.red())

    for troopIndex in range(0, 6):
        em.add_field(name=users[str(user.id)]["Formation"]["names"][troopIndex],
                     value="Lvl " + str(users[str(user.id)]["Formation"]["lvls"][troopIndex]))

    await ctx.send(embed=em)


@client.command()
async def info(ctx):
    await ctx.send("1-Set troop command: e!set index(1-6) troopName troopLvl(1-80)")
    await ctx.send("Example: e!set 1 Bulma 75")
    await ctx.send("2-Show Troops command: e!show @AnyPlayerName")
    await ctx.send("Example: e!show @shaun")

@client.command()
async def set(ctx, index=None, name=None, lvl=None):

    await open_account(ctx.author)
    try:
        index = int(index)
        lvl = int(lvl)
    except:
        await ctx.send("index or lvl wrongly typed or missing")
        return

    index = index - 1

    if (index is None) or (name is None) or (lvl is None):
        await ctx.send("Check your index, name or lvl something is missing")
        return
    elif (index < 0) or (index > 5):
        await ctx.send("Index needs to be between 1 and 6")
        return

    if lvl < 1 or lvl > 80:
        await ctx.send("Level needs to be between 1 and 80")
        return

    if len(name) > 15:
        await ctx.send("Name too long 15 letters MAX")
        return

    data = [index, name, lvl]
    await update_data(ctx.author, data)

    await ctx.send(f"Added.")


async def open_account(user):
    users = await load_users()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        current_user = users[str(user.id)]
        current_user["PlayerLVL"] = 1
        current_user["Formation"] = {}
        current_user["Formation"]["names"] = ["empty1", "empty2", "empty3", "empty4", "empty5", "empty6"]
        current_user["Formation"]["lvls"] = [1, 2, 3, 4, 5, 6]

    with open("data.json", "w") as f:
        json.dump(users, f)
    return True


async def get_users_data():
    with open("data.json", "r") as f:
        users = json.load(f)
    return users


async def set_users_data(users):
    # store changes
    with open("data.json", "w") as f:
        json.dump(users, f)

async def load_users():
    url = 'https://api.jsonbin.io/b/5fc6a83c9abe4f6e7cae4181'
    headers = {'secret-key': '$2b$10$c89s/iiSGakICOZ4K4Nl8uSNCpziZ9OutIp3VnCzaPZhHaFbocOs.'}
    users = await get_users_data()
    # if information is missing we load from jsonbin and update it
    if users == {}:
        url = 'https://api.jsonbin.io/v3/b/5fc6a83c9abe4f6e7cae4181/latest'
        headers = {
            'X-Master-Key': '$2b$10$c89s/iiSGakICOZ4K4Nl8uSNCpziZ9OutIp3VnCzaPZhHaFbocOs.'
        }
        req = requests.get(url, json=None, headers=headers)
        conv = json.loads(req.text)
        await set_users_data(conv['record'])
        users = await get_users_data()

    return users


async def update_data(user, data):
    users = await get_users_data()
    # index,name,lvl

    users[str(user.id)]["Formation"]["names"][data[0]] = data[1]
    users[str(user.id)]["Formation"]["lvls"][data[0]] = data[2]

    # store changes
    with open("data.json", "w") as f:
        json.dump(users, f)


client.run("NzgyNDQ2OTQwMzQwMDkyOTQ4.X8MUfw.hweyRBSL0a8xzMwxmqCqjqdhq48")