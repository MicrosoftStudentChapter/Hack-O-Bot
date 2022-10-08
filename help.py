from discord.ext import commands
import discord
from datetime import date

class CustomHelpCommand(commands.HelpCommand):

    async def send_bot_help(self, mapping):

        """This is triggered when .help is invoked."""
        filtered = await self.filter_commands(self.context.bot.commands, sort=True)
        cogs = [cog for cog in self.context.bot.cogs.values()]

        embed  = discord.Embed(title="Help", description="", color=discord.Color.blue())
        embed.add_field(name="Available Commands", value="``` " + " `````` ".join([command.name for command in filtered]) + " ```", inline=False)

        if cogs:
            embed.add_field(name="Available Categories", value="` " + " `, ` ".join([cog.qualified_name for cog in cogs]) + " `", inline=False)

        embed.set_footer(text=f"Type '.help <Command/Category>' for more information | [Optional arg], <Required arg> • {date.today().strftime('%d/%m/%Y')}")
        await self.context.send(embed=embed)

    async def send_command_help(self, command):

        """This is triggered when .help <command> is invoked."""
        embed = discord.Embed(title=f"Command: {command.name.capitalize()}", description=command.help + f"```.{command.name}```", color=discord.Color.blue())

        embed.set_footer(text=f"Type '.help <Command/Category>' for more information | [Optional arg], <Required arg> • {date.today().strftime('%d/%m/%Y')}")

        await self.context.send(embed=embed)


    async def send_cog_help(self, cog):
        """This is triggered when .help <cog> is invoked."""
        filtered = await self.filter_commands(cog.get_commands(), sort=True)

        embed = discord.Embed(title=f"Category: {cog.qualified_name.capitalize()}", description="", color=discord.Color.blue())
        embed.add_field(name="Available Commands", value="``` " + " `````` ".join([command.name for command in filtered]) + " ```", inline=False)
        
        embed.set_footer(text=f"Type '.help <Command/Category>' for more information | [Optional arg], <Required arg> • {date.today().strftime('%d/%m/%Y')}")

        await self.context.send(embed=embed)
