import asyncio
import messages
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import find

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = commands.Bot(command_prefix=".", intents=intents, case_insensitive=True, )


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
                                      f'source, especially the people that make open source so special.\n\nMicrosoft Learn Student '
                                      f'Chapter, the organizer of this webinar. MLSC is one of the elite technical clubs at Thapar '
                                      f'Institute. It is an open-source community dedicated to elevating the coding culture at Thapar '
                                      f'and all over the nation. We at MLSC believe that if the youth is encompassed with appropriate '
                                      f'technology and skills, it holds the potential to revolutionize the world we perceive today. We '
                                      f'at MLSC aim to be a part of this revolution. We conduct various community workshops, tech events '
                                      f'and collaborate with other communities and companies on our path to elevate the coding culture '
                                      f'at Thapar Institute.',
                          colour=discord.Colour.blue())
    embed.set_image(
        url='https://ci6.googleusercontent.com/proxy/C8UxgGwLaoucxBN9rJCYvVOYnYFMjgd6Zy_xbQpuAE9dXa71YudYOwJN7MYZ4azkNQNc49u1d84eyt7Gdw2KQ8MgJJ9PJbHdbW9STiFzoNP-URezcXBKMfn0vd-1g7W5blB0WGFURZAmVbtJynA5sMV1xGcVA70=s0-d-e1-ft#https://res.cloudinary.com/dhoayd4fv/image/upload/v1664731326/MLSC/HacktoberFest_Header_3_xvtpyn.png')

    await ctx.send(embed=embed)

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            print(f"Loading {filename[:-3]}")
            await client.load_extension(f'cogs.{filename[:-3]}')


async def main():
    await load()
    await client.start(os.getenv('DISCORD_TOKEN'))


asyncio.run(main())
