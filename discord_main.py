import asyncio
import messages
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import find

from help import CustomHelpCommand

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = commands.Bot(command_prefix=".", intents=intents, case_insensitive=True, )

client.help_command = CustomHelpCommand()

@client.event
async def on_guild_join(guild):
    general = find(lambda x: ('general' in x.name.lower()), guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send(embed=discord.Embed(title=f"Hello {guild.name}!",
                                               description="I am a bot that can help you to run fun commands. Type '.help' to get started",
                                               color=discord.Color.blue()))


@client.event
async def on_ready():
    print("Hack-O-Bot is ready to roll!")


@client.command(help='Invite the bot to your server!')
async def invite(ctx):
    await ctx.reply(f"Only the First 100 can invite to their Personal "
                    f"Server\n\nhttps://discord.com/api/oauth2/authorize?client_id=1028024794081394688&permissions"
                    f"=172942961728&scope=bot")

@client.command()
async def ping(ctx):
    await ctx.channel.send(embed=discord.Embed(title="Pong!", description=f"Latency: {round(client.latency * 1000)}ms",
                                               color=discord.Color.blue()))


@client.command(help='Enables Different Categories\nAccess: Administrator')
@commands.check_any(commands.is_owner())
async def enable(ctx, extension: str):
    await client.load_extension(f'cogs.{extension.lower()}')
    success_message = await ctx.send(embed=messages.success())
    await success_message.add_reaction('✔')


@client.command(help='Disables Different Categories\nAccess: Administrator')
@commands.check_any(commands.is_owner())
async def disable(ctx, extension: str):
    await client.unload_extension(f'cogs.{extension.lower()}')
    success_message = await ctx.send(embed=messages.success())
    await success_message.add_reaction('✔')

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            print(f"Loading {filename[:-3]}")
            await client.load_extension(f'cogs.{filename[:-3]}')

async def main():
    await load()
    await client.start(os.getenv('DISCORD_TOKEN'))

asyncio.run(main())