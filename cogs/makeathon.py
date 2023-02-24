import re
import datetime
from dateutil import tz
import discord
from discord.ext import commands
import pandas as pd


class Makeathon(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.df = pd.read_csv("assets/data.csv")
        self.email = self.df["Email"]
        self.team_name = self.df["Team Name"]
        self.timezone = tz.gettz('Asia/Kolkata')
        self.timeline = {
            (datetime.datetime(2023, 2, 25, 10, 30,00,00, tzinfo=self.timezone), datetime.datetime(2023,2,25,12,00,00,00,self.timezone)): 'Opening Ceremony by Dr. Prashant Singh Rana and Hackathon Expert',
            (datetime.datetime(2023, 2, 25, 14, 00,00,00, tzinfo=self.timezone)): 'Hack Begins',
            (datetime.datetime(2023, 2, 25, 19, 00,00,00, tzinfo=self.timezone), datetime.datetime(2023, 2, 25, 22, 00,00,00, tzinfo=self.timezone)): 'Checkpoint 1',
            (datetime.datetime(2023, 2, 25, 22, 30,00,00, tzinfo=self.timezone)): 'CodeChef MiniGame 1',
            (datetime.datetime(2023, 2, 26, 2, 00,00,00, tzinfo=self.timezone), datetime.datetime(2023, 2, 26, 5, 00,00,00, tzinfo=self.timezone)): 'Checkpoint 2',
            (datetime.datetime(2023, 2, 26, 5, 00,00,00, tzinfo=self.timezone)): 'CodeChef MiniGame 2',
            (datetime.datetime(2023, 2, 26, 11, 00,00,00, tzinfo=self.timezone), datetime.datetime(2023, 2, 26, 13, 00,00,00, tzinfo=self.timezone)): 'Checkpoint 3',
        (datetime.datetime(2023, 2, 26, 13, 00,00,00, tzinfo=self.timezone)): 'Soft Deadline for Submission',
        (datetime.datetime(2023, 2, 26, 14, 00,00,00, tzinfo=self.timezone)): "Submission Ends",
        (datetime.datetime(2023, 2, 26, 16, 00,00,00, tzinfo=self.timezone)): 'Pitching Round',
        (datetime.datetime(2023, 2, 26, 19, 00,00,00, tzinfo=self.timezone)): 'Prize Distribution'
        }


    @commands.command(help="Register yourself for MAKEATHON 5 (Online Only)")
    async def register(self, ctx, email: str, team_name: str):
        #check email ID regex
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise commands.CommandError("Please enter a valid email ID")
        # check if author has "Makeathon 5 Registered ✅" Role
        role = discord.utils.get(ctx.guild.roles, name="Makeathon 5 Registered ✅")
        if role in ctx.author.roles:
            raise commands.CommandError("You are already registered for Makeathon 5, Please Contact an admin if you think this is a mistake")
        if team_name in list(self.team_name) and email.lower() in list(self.email):
            #sluggify team name
            team_slug = team_name.replace(" ", "-")
            # add role, if role doesnt exist, create it
            team_role = discord.utils.get(ctx.guild.roles, name=team_slug)
            if team_role is None:
                team_role = await ctx.guild.create_role(name=team_slug)
            await ctx.author.add_roles(team_role)
            # add user to channel with team name, if channel doesnt exist, create it
            team_channel = discord.utils.get(ctx.guild.channels, name=team_slug)
            list_of_categories = ["teams-1", "teams-2", 'teams-3', 'teams-4']
            #create categories if they dont exist
            for category in list_of_categories:
                if discord.utils.get(ctx.guild.categories, name=category) is None:
                    await ctx.guild.create_category(category)
            if team_channel is None:
                #create voice channel with team name, only users with team role can see it
                #add channel to category which isnt full
                for category in list_of_categories:
                    category = discord.utils.get(ctx.guild.categories, name=category)
                    if len(category.channels) < 50:
                        team_channel = await ctx.guild.create_voice_channel(team_slug, overwrites={
                            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                            team_role: discord.PermissionOverwrite(read_messages=True)}, category=category)
                        break

            #create a discord embed with the text "User has registered for {team_name} with email {email}"
            embed = discord.Embed(title="New User Added to Team", description=f"{ctx.author.name} has registered for {team_name} with email {email}", color=0x00ff00)
            #send embed to channel with team name
            await team_channel.send(embed=embed)
            # DM user with "You have successfully registered for {team_name} with email {email}"
            await ctx.author.send(f"You have successfully registered for {team_name} with email {email}")
            #send message to logs channel with "User has registered for {team_name} with email {email}"
            await self.client.get_channel(904798217965826078).send(embed=embed)
            await ctx.author.add_roles(role)
        else:
            raise commands.CommandError("Please enter a valid email ID and/or Team Name")

    @commands.command(help="Displays next event in the Timeline for the hackathon")
    async def timeline(self, ctx):
        india_time = datetime.datetime.now(self.timezone)
        for time in self.timeline:
            if type(time) == tuple:
                    #create an embed to send to the user
                    if time[0] < india_time < time[1]:
                        embed = discord.Embed(title=f"Next Event ({time[0].strftime('%I:%M %p')} - {time[1].strftime('%I:%M %p')})", description=self.timeline[time], color=0x00ff00)
                        await ctx.send(embed=embed)
                        return
            else:
                if time > india_time:
                    embed = discord.Embed(title=f"Next Event ({time.strftime('%I:%M %p')})", description=self.timeline[time], color=0x00ff00)
                    await ctx.send(embed=embed)
                    return

async def setup(client):
    await client.add_cog(Makeathon(client))