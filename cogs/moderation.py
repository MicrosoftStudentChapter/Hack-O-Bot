import discord
import datetime
import re
from discord.ext import commands

import messages

TIME_REGEX = re.compile(r"(?:(\d{1,5})([hsmdw]))+?")
TIME_DICT = {"h": 3600, "s": 1, "m": 60, "d": 86400, "w": 604800}


def convert(argument):
    args = argument.lower()
    matches = re.findall(TIME_REGEX, args)
    time = 0
    for key, value in matches:
        try:
            time += TIME_DICT[value] * float(key)
        except KeyError:
            raise commands.BadArgument(
                f"{value} is an invalid time key! h|m|s|d|w are valid arguments"
            )
        except ValueError:
            raise commands.BadArgument(f"{key} is not a number!")
    return round(time)


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['b'], help="Bans a User from the server")
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason="Violation of Rules"):
        await member.ban(reason=reason)
        await ctx.send(embed=discord.Embed(title="Member Banned",
                                           description=f'{member.name} has been banned from the server',
                                           colour=discord.Colour.blurple()))

    @commands.command(aliases=['k'], help="Kicks a User from the server")
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Reason not provided"):
        await member.kick(reason=reason)
        await ctx.send(embed=discord.Embed(title="Member Kicked",
                                           description=f'{member.name} has been kicked from the server',
                                           colour=discord.Colour.blurple()))

    @commands.command(help="Unban a member")
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, member: discord.User):
        await ctx.guild.unban(member)
        success_message = await ctx.send(embed=messages.success())
        await success_message.add_reaction('✔')

    @commands.command(aliases=['t'], help="Restricts a User from sending messages for some time")
    @commands.has_permissions(administrator=True)
    async def timeout(self, ctx, member: discord.Member, time: str = '10m', *, reason: str = "Violation of rules"):

        await member.timeout(datetime.timedelta(seconds=convert(time)), reason=reason)
        await ctx.send(embed=discord.Embed(title="Member Timed Out",
                                           description=f'{member.mention} has been timed out for **{time}**',
                                           colour=discord.Colour.blurple()))

    @commands.command(aliases=['roleadd'], help="Gives specified roles to the provided members.")
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx: commands.Context, role: discord.Role, *members: discord.Member) -> None:
        if members == tuple():
            raise commands.MissingRequiredArgument(
                self.addrole.params["members"])

        if not ctx.guild.me.guild_permissions.manage_roles:
            await ctx.send(embed=discord.Embed(
                           description=f"Bot doesn\'t have the permission to give roles.",
                           colour=discord.Colour.blurple()))
            return

        success = 0
        for member in members:
            await member.add_roles(role)
            success += 1
        await ctx.send(embed=discord.Embed(title="Member Roles",
                                           description=f'Successfully added the role {role.mention} to {success} members.',
                                           colour=discord.Colour.blurple()))
    
    @commands.command(aliases=['si'], help="Basics server information about the server")
    async def server_info(self, ctx):
        embed = discord.Embed(title="Sever Information",
                            colour=discord.Colour.blurple())
        
        fields = [("Server Name", ctx.message.guild.name, False),
                    ("Created at", ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), False),
                    ("Members", len(ctx.guild.members), False),
                    ("Roles", len(ctx.guild.roles), False),
                    ("Text Channels", len(ctx.guild.text_channels), False),
                    ("Voice channels", len(ctx.guild.voice_channels), False)]

        for name, value, inline fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)    


async def setup(client):
    await client.add_cog(Moderation(client))
