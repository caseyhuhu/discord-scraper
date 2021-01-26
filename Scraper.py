import discord
import pandas as pd
import asyncio

TOKEN = None # token goes here
class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        elif message.content.startswith('$bot'):
            for guild in self.guilds:
                for chan in guild.channels:
                    if str(chan.type) == 'text':
                        print(chan.name)

        elif message.content.startswith('!run'):
            print('Received command')
            await message.add_reaction('😊')
            print("Guild: " + message.guild.name)
            for chan in message.guild.channels:
                if str(chan.type) == 'text':
                    print(' - Channel: ' + chan.name)
                    try:
                        data = pd.DataFrame(columns=['content', 'attachment','time', 'author'])
                        num = 0
                        async for msg in chan.history(limit=100000):
                            if msg.author != client.user:
                                if len(msg.attachments) > 0:
                                    data = data.append({'content': msg.content,
                                                'attachment': msg.attachments[0].url,
                                                'time': msg.created_at,
                                                'author': msg.author.name}, ignore_index=True)
                                else:
                                    data = data.append({'content': msg.content,
                                        'time': msg.created_at,
                                        'author': msg.author.name}, ignore_index=True)
                                if num % 500 == 0:
                                    print(msg.author.name + ": " + msg.content)
                                num += 1
                        data.to_csv('My Documents/Python/' + chan.name + '.csv')
                    except discord.Forbidden:
                        print('No permissions')

                print('Finished: ' + chan.name)

client = MyClient()
client.run(TOKEN)
