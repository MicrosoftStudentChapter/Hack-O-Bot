import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

from help import CustomHelpCommand

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = commands.Bot(command_prefix=".", intents=intents, case_insensitive=True, )

client.help_command = CustomHelpCommand()

@client.event
async def on_ready():
    print("Hack-O-Bot is ready to roll!")


@client.command(help='Invite the bot to your server!')
async def invite(ctx):
    await ctx.reply(f"Only the First 100 can invite to their Personal "
                    f"Server\n\nhttps://discord.com/api/oauth2/authorize?client_id=1028024794081394688&permissions"
                    f"=172942961728&scope=bot")

@client.command(help='Ping the bot \n And get the latency')
async def ping(ctx):
	await ctx.channel.send(embed=discord.Embed(title="Pong!", description=f"Latency: {round(client.latency * 1000)}ms", color=discord.Color.blue()))

client.run(str(os.getenv('DISCORD_TOKEN')))
