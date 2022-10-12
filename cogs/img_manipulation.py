from http import client
import discord
from discord.ext import commands
import datetime
import asyncio
import random

from PIL import Image
from io import BytesIO

client = commands.Bot(command_prefix=".")

@client.command()
async def wanted(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author

    wanted = Image.open("assets/wanted.png")
    asset = user.avatar_url_as(size = 128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((571,726))
    wanted.paste(pfp, (327,500))

    wanted.save("wantedProfile.jpg")
    
    await ctx.send(file = discord.File("wantedProfile.jpg"))