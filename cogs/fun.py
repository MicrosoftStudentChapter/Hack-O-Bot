import discord
from discord.ext import commands
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


    @commands.command(name='horoscope', help='Get your horoscope for today based on your *discord birthday*')
    async def horoscope(self, ctx):
        dob = ctx.message.author.created_at
        date = dob.day
        month = dob.month
        zodiac = get_zodiac(date, month)
        # print(date, month, zodiac)
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

async def setup(client):
    await client.add_cog(Fun(client))
