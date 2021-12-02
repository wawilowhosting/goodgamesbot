import discord


discord_token = """OTE1Njg3NjgzNzg1ODg3Nzc0.YafOnA.wfhglCXzI73gIulKNVvWgJUmPkY"""
client = discord.

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run('your token here')
