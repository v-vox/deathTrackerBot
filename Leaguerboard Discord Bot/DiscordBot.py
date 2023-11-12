import discord
import time
import DataThings
import scraper
import asyncio

# Discord Stuff
intents = discord.Intents.default()
intents.members = True 
intents.message_content = True
client = discord.Client(command_prefix='!', intents = intents);
GENERAL_CHANNEL_ID = 1171086803562938391 
TERRARIA_CHANNEL_ID = 1158058728717819957

@client.event
async def on_ready():
    print("Bot is Logged In as {0.user}!".format(client))

    if not DataThings.doesExist('HanooStreet'):
        DataThings.newPlayer('HanooStreet')

    if not DataThings.doesExist('Willworm123'):
        DataThings.newPlayer('Willworm123')

    while True:
        temp = DataThings.checkChange("HanooStreet")
        if temp != -1: 
            print("HENRY'S DYING")
            generalChannel = client.get_channel(TERRARIA_CHANNEL_ID)
            await generalChannel.send("aint no way " + "<@" + str(439520735585763328) + ">" + " died " + str(temp) + " times last game")
        await asyncio.sleep(240)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.upper() == "HELLO":
        await message.channel.send(f"Hello {message.author.mention}")
    if message.content.upper() == "PING ME":
        await message.channel.send("<@" + str(711634956916359209) + ">")

async def printmsg():
    print("HENRY'S DYING")
    generalChannel = client.get_channel(GENERAL_CHANNEL_ID)
    await generalChannel.send("aint no way" + "<@" + str(711634956916359209) + ">" + "is dying to noobs")


# if (checkChange): 
#     print("HENRY'S DYING")
#     generalChannel = client.get_channel(GENERAL_CHANNEL_ID)
#     await generalChannel.send("aint no way" + "<@" + str(711634956916359209) + ">" + "is dying to noobs")



# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
    

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#     if message.content.startswith("!addPlayer")


BOT_TOKEN = "MTE3MTA4NTIxOTk0ODkyMDg4Mg.G8gQCA.MAhlmZ7ZpXzwWgs9z3l5a-ySQXojVt4C_1aDvE"
client.run(BOT_TOKEN)


