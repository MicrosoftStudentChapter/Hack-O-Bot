import discord
from discord.ext import commands
from PIL import Image
from io import BytesIO


class Photo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help="Make yourself the most wanted person in all of the wild west")
    async def wanted(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        wanted = Image.open("assets/wanted.png")
        asset = user.avatar
        data = BytesIO(await asset.read())
        pfp = Image.open(data)

        pfp = pfp.resize((571, 726))
        wanted.paste(pfp, (327, 500))

        wanted.save("assets/wantedProfile.png")

        await ctx.send(file=discord.File("assets/wantedProfile.png"))


async def setup(client):
    await client.add_cog(Photo(client))