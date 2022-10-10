from discord.ext import commands
import discord
from datetime import datetime

class CustomHelpCommand(commands.HelpCommand):

    async def send_bot_help(self, mapping):

        """This is triggered when .help is invoked."""
        filtered = await self.filter_commands(self.context.bot.commands, sort=True)

        cogs = self.context.bot.cogs.values()

        embed = discord.Embed(title="Help", description="", color=discord.Color.blue())
        embed.add_field(name="Available Commands \u200b", value="\n".join(["**Category: " + cog.qualified_name + "** \n```diff\n " + "``````diff\n ".join([command.name for command in cog.get_commands()]) + "```" for cog in cogs]), inline=False)

        embed.add_field(name="Other Commands", value="```diff\n " + "``````diff\n ".join([command.name for command in filtered if command.cog_name is None]) + "```", inline=False)

        embed.set_footer(text=f"Type '.help <Command/Category>' for more information | [Optional arg], <Required arg>")
        embed.timestamp = datetime.now()

        await self.context.send(embed=embed)

    async def send_command_help(self, command):

        """This is triggered when .help <command> is invoked."""
        alaises = command.aliases
        if alaises:
            call = self.context.bot.command_prefix + command.name + " | " + "| ".join([self.context.bot.command_prefix + alias for alias in alaises])
        else:
            call = self.context.bot.command_prefix + command.name

        embed = discord.Embed(title=f"Command: {command.name.capitalize()}", description=command.help + f"```diff\n {call} {command.signature}```", color=discord.Color.blue())

        embed.set_footer(text=f"Type '.help <Command/Category>' for more information | [Optional arg], <Required arg>")
        embed.timestamp = datetime.now()

        await self.context.send(embed=embed)


    async def send_cog_help(self, cog):
        """This is triggered when .help <cog> is invoked."""
        filtered = await self.filter_commands(cog.get_commands(), sort=True)

        embed = discord.Embed(title=f"Category: {cog.qualified_name.capitalize()}", description="", color=discord.Color.blue())
        embed.add_field(name="Available Commands", value="```diff\n " + " ``````diff\n ".join([command.name for command in filtered]) + " ```", inline=False)
        
        embed.set_footer(text=f"Type '.help <Command/Category>' for more information | [Optional arg], <Required arg>")
        embed.timestamp = datetime.now()

        await self.context.send(embed=embed)
