import asyncio

import discord
from discord.ext import commands
import requests
import json
import random
import requests
from datetime import datetime


def get_zodiac(date, month):
    if month == 12:
        astro_sign = 'sagittarius' if (date < 22) else 'capricorn'
    elif month == 1:
        astro_sign = 'capricorn' if (date < 20) else 'aquarius'
    elif month == 2:
        astro_sign = 'aquarius' if (date < 19) else 'pisces'
    elif month == 3:
        astro_sign = 'pisces' if (date < 21) else 'aries'
    elif month == 4:
        astro_sign = 'aries' if (date < 20) else 'taurus'
    elif month == 5:
        astro_sign = 'taurus' if (date < 21) else 'gemini'
    elif month == 6:
        astro_sign = 'gemini' if (date < 21) else 'cancer'
    elif month == 7:
        astro_sign = 'cancer' if (date < 23) else 'leo'
    elif month == 8:
        astro_sign = 'leo' if (date < 23) else 'virgo'
    elif month == 9:
        astro_sign = 'virgo' if (date < 23) else 'libra'
    elif month == 10:
        astro_sign = 'libra' if (date < 23) else 'scorpio'
    elif month == 11:
        astro_sign = 'scorpio' if (date < 22) else 'sagittarius'
    return astro_sign

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help='Use the magic 8 ball to get a random answer', name='8ball')
    async def _8ball(self, ctx, *, question):
        responses = [
            'It is certain.',
            'It is decidedly so.',
            'Without a doubt.',
            'Yes - definitely.',
            'You may rely on it.',
            'As I see it, yes.',
            'Most likely.',
            'Outlook good.',
            'Yes.',
            'Signs point to yes.',
            'Reply hazy, try again.',
            'Ask again later.',
            'Better not tell you now.',
            'Cannot predict now.',
            'Concentrate and ask again.',
            'Don\'t count on it.',
            'My reply is no.',
            'My sources say no.',
            'Outlook not so good.',
            'Very doubtful.'
        ]
        await ctx.send(embed=discord.Embed(title="Magic 8 Ball",
                                           description=f'Question: {question}\nAnswer: {random.choice(responses)}',
                                           colour=discord.Colour.blurple()))

    @commands.command(help='Roll a `n` sided die')
    async def roll(self, ctx, sides: int = 6):
        message = await ctx.send(
            embed=discord.Embed(title="Rolling...", description="Rolling a die...", colour=discord.Colour.blurple()))
        await asyncio.sleep(1)
        await message.edit(
            embed=discord.Embed(title="Rolling...", description=f"You rolled a {random.randint(1, sides)}",
                                colour=discord.Colour.blurple()))

    @commands.command(name='horoscope', help='Get your horoscope for today based on your *discord birthday*')
    async def horoscope(self, ctx):
        dob = ctx.message.author.created_at
        date = dob.day
        month = dob.month
        zodiac = get_zodiac(date, month)
        params = (
            ('sign', zodiac),
            ('day', 'today'),
        )

        content = requests.post('https://aztro.sameerkumar.website/', params=params)
        content = content.json()

        embed = discord.Embed(title=f"Horoscope: {zodiac.capitalize()}", description=f"{content['description']}", color=discord.Colour.blurple())
        embed.add_field(name="Compatibility", value=f"{content['compatibility']}", inline=True)
        embed.add_field(name="Mood", value=f"{content['mood']}", inline=True)
        embed.add_field(name="Color", value=f"{content['color']}", inline=False)
        embed.add_field(name="Lucky Number", value=f"{content['lucky_number']}", inline=True)
        embed.add_field(name="Lucky Time", value=f"{content['lucky_time']}", inline=True)

        embed.set_footer(text=f"Requested by {ctx.message.author.display_name}")
        embed.timestamp = datetime.utcnow()

        await ctx.send(embed=embed)

    @commands.command(help='Emoji-fy your text')
    async def emoji(self, ctx, *, text):
        await ctx.send(embed=discord.Embed(title="Emoji-fied Text",
                                           description=f"{' '.join([f':regional_indicator_{char.lower()}:' for char in text if char.isalpha()])}",
                                           colour=discord.Colour.blurple()))


    @commands.command(help='Get information about a random Github Repository')
    async def github(self, ctx):
        response = requests.get("https://api.github.com/repositories?since=" + str(int(random.random() * 500)))
        if(response.status_code == 200):
            json_data = json.loads(response.text)
            repo_info = json_data[random.randint(0, len(json_data))]
            embed=discord.Embed(title=f"Github Repository: {repo_info['full_name']}",
                                               description=f"Description: {repo_info['description']} \n",
                                               url=repo_info['html_url'],
                                               colour=discord.Colour.blurple())
            await ctx.send(embed=embed)
        else:
            raise AttributeError("Github API returned a non-200 status code (returned " + str(response.status_code) + ")")

    @commands.command(help='Send an adorable dog image, optionally with a specified breed')
    async def dog(self, ctx, *, breed = None):
        if breed:
            req = requests.get(f'https://dog.ceo/api/breed/{breed}/images/random')
            if req.status_code == 404:
                await ctx.send(embed=discord.Embed(
                    title='Something went wrong',
                    description="Are you sure that's the correct breed name?\nMaybe try https://dog.ceo/dog-api/breeds-list",
                    colour=discord.Colour.red()))
            else:
                await ctx.send(embed=discord.Embed(
                title="Doggo!",
                colour=discord.Colour.blurple()).set_image(url=req.json()['message']))
        else:
            req = requests.get('https://dog.ceo/api/breeds/image/random')
            await ctx.send(embed=discord.Embed(
            title="Doggo!",
            colour=discord.Colour.blurple()).set_image(url=req.json()['message']))

    @commands.command(help='Send a cute cat image, optionally with some text!')
    async def cat(self, ctx, *, text=None):
        if text:
            await ctx.send(embed=discord.Embed(
            title="Catto!",
            colour=discord.Colour.blurple()).set_image(url=f'https://cataas.com/cat/says/{text}'))
        else:
            await ctx.send(embed=discord.Embed(
            title="Catto!",
            colour=discord.Colour.blurple()).set_image(url='https://cataas.com/cat'))

    @commands.command(help='Send a random duck image!')
    async def duck(self, ctx, *, void=None):
        req = requests.get('https://random-d.uk/api/quack')
        await ctx.send(embed=discord.Embed(
            title="Ducky!!",
            colour=discord.Colour.blurple()).set_image(url=req.json()['url']))
           
async def setup(client):
    await client.add_cog(Fun(client))
