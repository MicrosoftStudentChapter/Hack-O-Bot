from discord.ext import commands
import discord

class CustomHelpCommand(commands.HelpCommand):

    async def send_bot_help(self, mapping):
        """
        This is triggered when .help is invoked.
        """
        filtered = await self.filter_commands(self.context.bot.commands, sort=True)
        embed  = discord.Embed(title="Help", description="Available commands : ", color=discord.Color.blue())
        for command in filtered:
            embed.add_field(name=command.name, value=command.help, inline=False)
        embed.set_footer(text=f"Requested by {self.context.author.display_name}")
        await self.context.send(embed=embed)

    async def send_command_help(self, command):
        """This is triggered when .help <command> is invoked."""
        await self.context.send(embed=discord.Embed(title=command.name, description=command.help, color=discord.Color.blue()))


    async def send_cog_help(self, cog):
        """This is triggered when .help <cog> is invoked."""
        await self.context.send(embed=discord.Embed(title=cog.qualified_name, description=cog.description, color=discord.Color.blue()))
