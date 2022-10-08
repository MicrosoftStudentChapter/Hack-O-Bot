from discord.ext import commands
import discord

class CustomHelpCommand(commands.HelpCommand):

    async def send_bot_help(self, mapping):
        """
        This is triggered when .help is invoked.
        """
        filtered = await self.filter_commands(self.context.bot.commands, sort=True)

        embed  = discord.Embed(title="Help Command", description="", color=discord.Color.blue())
        embed.add_field(name="Available Commands", value="`" + "`, `".join([command.name for command in filtered]) + "`", inline=False)
        embed.set_footer(text=f"Type '.help <CommandName>' for details on a command")
        await self.context.send(embed=embed)

    async def send_command_help(self, command):
        """This is triggered when .help <command> is invoked."""
        embed = discord.Embed(title=f"Help Command: {command.name}", description="", color=discord.Color.blue())
        embed.add_field(name=f".{command.name}", value=command.help, inline=False)
        await self.context.send(embed=embed)


    async def send_cog_help(self, cog):
        """This is triggered when .help <cog> is invoked."""
        embed = discord.Embed(title=f"Help Command: {cog.qualified_name}", description="", color=discord.Color.blue())
        for command in cog.get_commands():
            embed.add_field(name=f".{command.name}", value=command.help, inline=False)
        await self.context.send(embed=embed)
