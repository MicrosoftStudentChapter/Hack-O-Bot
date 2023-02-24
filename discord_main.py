import asyncio
import messages
import discord
import requests
import os
from os import environ
from datetime import datetime
import re
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import find

from help import CustomHelpCommand

load_dotenv('.env')

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
                                               color=discord.Color.blurple()))


@client.event
async def on_ready():
    print("Hack-O-Bot is ready to roll!")

@client.event
async def on_message(ctx):
    if ctx.author.bot:
        return

    mentionPattern = r"^<@[0-9]*>$"
    if re.search(mentionPattern, ctx.content) is not None:
        await ctx.reply(
            embed=discord.Embed(
                title="Hi there! Use .help for a full list of commands.",
                color=discord.Color.blurple(),
            )
        )

    await client.process_commands(ctx)

@client.command(help='Invite the bot to your server!')
async def invite(ctx):
    await ctx.reply(f"Only the First 100 can invite to their Personal "
                    f"Server\n\nhttps://discord.com/api/oauth2/authorize?client_id=1028024794081394688&permissions"
                    f"=172942961728&scope=bot")


@client.command(help='Get the bot\'s latency')
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


@client.command(help='Get the info about Hacktoberfest and MLSC\'s contribution to it', alias=['hacktoberfest', 'info'])
async def about(ctx):
    embed = discord.Embed(title='HacktoberFest x MLSC',
                          description='Hacktoberfest is DigitalOcean’s annual event that encourages people to contribute to open source '
                                      f'throughout October. Much of modern tech infrastructure—including some of DigitalOcean’s own '
                                      f'products—relies on open-source projects built and maintained by passionate people who often '
                                      f'don’t have the staff or budgets to do much more than keep the project alive. Hacktoberfest is '
                                      f'all about giving back to those projects, sharpening skills, and celebrating all things open '
                                      f'source, especially the people that make open source so special.\n\n'
                                      f'Microsoft Learn Student Chapter is one of the elite technical clubs at Thapar Institute of Engineering and Technology '
                                      f'Institute. It is an open-source community dedicated to elevating the coding culture at Thapar '
                                      f'and all over the nation. We at MLSC believe that if the youth is encompassed with appropriate '
                                      f'technology and skills, it holds the potential to revolutionize the world we perceive today. We '
                                      f'at MLSC aim to be a part of this revolution. We conduct various community workshops, tech events '
                                      f'and collaborate with other communities and companies on our path to elevate the coding culture '
                                      f'at Thapar Institute.',
                          colour=discord.Colour.blue())
    embed.set_image(
        url='https://ci6.googleusercontent.com/proxy/C8UxgGwLaoucxBN9rJCYvVOYnYFMjgd6Zy_xbQpuAE9dXa71YudYOwJN7MYZ4azk'
            'NQNc49u1d84eyt7Gdw2KQ8MgJJ9PJbHdbW9STiFzoNP-URezcXBKMfn0vd-1g7W5blB0WGFURZAmVbtJynA5sMV1xGcVA70=s0-d-e1-f'
            't#https://res.cloudinary.com/dhoayd4fv/image/upload/v1664731326/MLSC/HacktoberFest_Header_3_xvtpyn.png')

    await ctx.send(embed=embed)

CACHE = {}
@client.command(help='Get the info about the contributors', alias=['contributors-info'])
async def contributors(ctx):
    URL = "https://api.github.com/repos/MicrosoftStudentChapter/Hack-O-Bot/contributors"

    create_time = ctx.message.created_at.replace(tzinfo=None)
    cache_time = CACHE.get("time", datetime(
        create_time.year-1, 12, 31, 0, 0, 0, 0))
    if (create_time - cache_time).seconds <= 70 and CACHE.get("content", False):
        result = CACHE["content"]
    else:
        response = requests.get(URL)
        result = response.json()
        CACHE["content"] = result
        CACHE["time"] = create_time
        if not response.ok:
            embed = discord.Embed(title='Contributors',
                                  colour=discord.Colour.red())
            embed.description = f"Error {response.status_code}: {result['message']}"
            await ctx.send(embed=embed)
            return

    embed = discord.Embed(title='Contributors', colour=discord.Colour.blue())
    embed.description = ", ".join(
        [f"[{contributor['login']}]({contributor['html_url']})" for contributor in result])
    embed.set_thumbnail(
        url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
    await ctx.send(embed=embed)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        if len("|".join(ctx.command.aliases)) > 0:
            base = f'.[{ctx.command.name}|{"|".join(ctx.command.aliases)}]'
        else:
            base = f'.[{ctx.command.name}]'
        error = f'{str(error)}\nCorrect syntax: ```{base} {ctx.command.signature}```'
    else:
        if str(error).startswith("Command"):
            error = str(error)[29:]
        else:
            error = str(error)
    embed = discord.Embed(
        title="This isn't a 404 but...",
        description=error,
        colour=discord.Colour(0xE93316)
    )
    embed.set_footer(text=f'For more information try running .help')

    await ctx.message.channel.send(embed=embed)


async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            print(f"Loading {filename[:-3]}")
            await client.load_extension(f'cogs.{filename[:-3]}')


async def main():
    await load()
    await client.start(os.getenv('DISCORD_TOKEN'))


asyncio.run(main())
