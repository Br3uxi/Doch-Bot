import discord
import asyncio
import json
import re
import configparser
import os

client = discord.Client()

json_file = ''
blacklist = ''
token = ''

# regexp = re.compile(r'(\bn+?[a, e, o]+?i+?(([n,]+?)|e+?n+?)\b)|(\bn+?[o, u]+?p+?e+?\b)|(n(ö+|ö+?h+?ö+?))|ne+',
# re.IGNORECASE)
regexp = re.compile(r'(\bn+?[a, e, o]+?i+?(([n,]+?)|e+?n+?)\b)|(\bn+?[o, u]+?p+?e+?\b)|(n(ö+|ö+?h+?ö+?))|ne+',
                    re.IGNORECASE)

if os.path.exists('config.ini'):
    config = configparser.ConfigParser()
    config.read("config.ini")
    token = config.get('Doch-Bot', 'token')


def load_config():
    global json_file
    global blacklist
    json_file = open("blacklist.json").read()
    blacklist = json.loads(json_file)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    for server in client.servers:
        print('- Name: {} | Id: {}'.format(server.name, server.id))
    print('------')
    load_config()
    await client.change_presence(game=discord.Game(name="!help"))


@client.event
async def on_message(message):
    # if re.match(r'(\bn[a, e, o]+?i+?[e,]n+\b)|\bn+?o+?p+?e+?\b|nö+?|ne+?', str(message.content).lower(), re.IGNORECASE):
    if regexp.search(str(message.content).lower()):
        for i in range(0, len(blacklist)):
            if str(message.author.name).lower() in blacklist[i]:
                return

        await client.send_message(message.channel, 'Dooooooooch!')
    elif re.match(r'g+?a+?r+? n+?i+?c+?h+?t+?', str(message.content).lower()):
        if str(message.author.name).lower() not in blacklist:
            await client.send_message(message.channel, 'Wohl!')
    elif message.content.startswith("!blacklist"):
        if 'show' in str(message.content).lower():
            msg = await client.send_message(message.channel,
                                            'In der Blacklist sind aktuell {}'.format(str.join(", ", blacklist)))
            await asyncio.sleep(5)
            try:
                await client.delete_message(message)
            except discord.Forbidden:
                pass
            await client.delete_message(msg)
        elif 'add' in str(message.content).lower():
            args = message.content.split()
            user = args[2]
            blacklist.append(user)
            with open('blacklist.json', 'w') as f:
                f.write(json.dumps(blacklist))
            load_config()
            msg = await client.send_message(message.channel, "{} wurde zur Blacklist hinzugefügt!".format(user))
            await asyncio.sleep(5)
            try:
                await client.delete_message(message)
            except discord.Forbidden:
                pass
            await client.delete_message(msg)
        elif 'remove' in str(message.content).lower():
            args = message.content.split()
            user = args[2]
            blacklist.remove(args[2])
            with open('blacklist.json', 'w') as f:
                f.write(json.dumps(blacklist))
            load_config()
            msg = await client.send_message(message.channel, "{} wurde aus der Blacklist endfernt!".format(user))
            await asyncio.sleep(5)
            try:
                await client.delete_message(message)
            except discord.Forbidden:
                pass
            await client.delete_message(msg)
    elif message.content.startswith('!help'):
        msg = await client.send_message(message.channel,
                                        'Toller Bot von Breuxi! Gern geschehen Dizzli :D\n'
                                        '\n'
                                        '**Commands:**\n'
                                        '    !blacklist - User in der Blacklist werden ignoriert\n'
                                        '        **Parameter:**\n'
                                        '            * add <user> - Fügt einen User zur Blacklist hinzu\n'
                                        '            * remove <user> - Entfernt einen User aus der Blacklist\n'
                                        '            * show - Zeigt alle User in der Blacklist an\n'
                                        '\n'
                                        '!help - Diese Seite\n'
                                        'Invite Link: https://discordapp.com/api/oauth2/authorize?client_id=' + client.user.id + '&scope=bot&permissions=1')
        await asyncio.sleep(20)
        try:
            await client.delete_message(message)
        except discord.Forbidden:
            pass
        await client.delete_message(msg)


# setup()
client.run(token)
