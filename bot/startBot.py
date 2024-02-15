import discord
from discord import Intents, Embed, Member
from time import sleep
from discord.ext.commands import Bot, has_permissions, MissingPermissions
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
from discord import File
import random
# Create a bot instance with specific intents
intents = Intents.default()
intents.members = True  # Enable member intents
bot = Bot(command_prefix="!", intents=intents)
slash = SlashCommand(bot, sync_commands=True)  # Enable slash commands


@bot.event  # Event listener for when the bot is ready
async def on_ready():
    print(f"{bot.user.name} is up and running!")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="☭USSR Anthem☭"))


@bot.event  # Error handling for missing permissions for text-based commands
async def on_command_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have permission to do that!")


@bot.event  # Error handling for slash commands, including missing permissions
async def on_slash_command_error(ctx: SlashContext, error):
    # Check if the error is due to missing permissions
    if "missing_permissions" in str(error).lower():
        await ctx.send(content="You do not have permission to use this command!", hidden=True)
    else:
        # Handle other errors here
        pass


@bot.event  # Event listener for new member join
async def on_member_join(member):
    welcome_channel = bot.get_channel(1196434128812384308)  # Replace with your channel ID
    autorole_name = 'Member'  # Replace with your role name
    role = discord.utils.get(member.guild.roles, name=autorole_name)
    await member.add_roles(role)

    if welcome_channel:
        await welcome_channel.send(f"Hello {member.mention}, welcome to the server!")


@slash.slash(name="hi", description="Says hi!")  # Slash command for /hi
async def _hi(ctx: SlashContext):
    await ctx.send(content="Hello comrade")


@slash.slash(name="drake", description="Sends a photo of drake")
async def _drake(ctx: SlashContext):
    file_path = 'drake.gif'  # Make sure this path is correct
    spoiler_file_path = f"SPOILER_{file_path}"  # Prefix the filename with 'SPOILER_'
    file = File(fp=file_path, filename=spoiler_file_path)  # Set the filename parameter to the spoiler version
    await ctx.send(file=file)


@slash.slash(name="milmoi", description="Says milmoi!")  # Slash command for /milmoi
async def _milmoi(ctx: SlashContext):
    await ctx.send(content="Milmoi!")


@slash.slash(name="tabinet", description="Let's play a game, choose a number", options=[  # Slash command for /tabinet
    create_option(name="numar", description="insert a number", option_type=3, required=True)
])
async def _tabinet(ctx: SlashContext, numar: str = ""):
    numar = int(numar)
    await ctx.send(content="The government is choosing...")
    sleep(0.5)
    numar = int(numar) + 1
    numar = str(numar)
    gen = random.randint(0,1)
    if gen == 1:
        await ctx.send(content=numar + ", you won a trip to gulag")
    else:
        await ctx.send(content=numar + ", you lost blyat")

@slash.slash(name="help", description="Shows this message")  # Slash command for /help
async def _help(ctx: SlashContext):
    embed = Embed(title="Help", description="List of available commands:", color=0x00ff00)
    embed.add_field(name="/hi", value="Says hi!", inline=False)
    embed.add_field(name="/kick", value="Kicks a user from the server. Usage: /kick @user [reason]", inline=False)
    embed.add_field(name="/warn", value="Warns a user. Usage: /warn @user [reason]", inline=False)
    embed.add_field(name="/ban", value="Bans a user from the server. Usage: /ban @user [reason]", inline=False)
    embed.add_field(name="/mute", value="Mutes a user. Usage: /mute @user", inline=False)
    await ctx.send(embed=embed)


@slash.slash(name="kick", description="Kick a user from the server", options=[  # Slash command for /kick

    create_option(name="user", description="The user to kick", option_type=6, required=True),
    create_option(name="reason", description="The reason for kicking", option_type=3, required=False)
])
@has_permissions(kick_members=True)
async def _kick(ctx: SlashContext, user: Member, reason: str = "deserting"):
    await user.kick(reason=reason)
    await ctx.send(f"{user.name} has been deported from our server for: {reason}")


@slash.slash(name="warn", description="Warn a user", options=[  # Slash command for /warn

    create_option(name="user", description="The user to warn", option_type=6, required=True),
    create_option(name="reason", description="The reason for the warning", option_type=3, required=False)
])
@has_permissions(manage_messages=True)
async def _warn(ctx: SlashContext, user: Member, reason: str = "being naughty"):
    await ctx.send(f"Be careful {user.mention} comrade, you have been warned for: {reason}")


@slash.slash(name="ban", description="Ban a user from the server", options=[  # Slash command for /ban
    create_option(name="user", description="The user to ban", option_type=6, required=True),
    create_option(name="reason", description="The reason for banning", option_type=3, required=False)
])
@has_permissions(ban_members=True)
async def _ban(ctx: SlashContext, user: Member, reason: str = "deserting"):
    await user.ban(reason=reason)
    await ctx.send(f"User {user.name} has been exiled from our server for:: {reason}")


@slash.slash(name="mute", description="Mute a user in the server", options=[  # Slash command for /mute
    create_option(name="user", description="The user to mute", option_type=6, required=True)
])
@has_permissions(manage_roles=True)
async def _mute(ctx: SlashContext, user: Member):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    member_role = discord.utils.get(ctx.guild.roles, name="Member")
    if muted_role:
        await user.add_roles(muted_role)
        await user.remove_roles(member_role)
        await ctx.send(f"{user.mention} has been silenced by the government.")
    else:
        await ctx.send("No 'Muted' role found. Please create a 'Muted' role with appropriate permissions.")


@slash.slash(name="unmute", description="Unmute a user in the server", options=[  # Slash command for /unmute
    create_option(name="user", description="The user to unmute", option_type=6, required=True)
])
@has_permissions(manage_roles=True)
async def _unmute(ctx: SlashContext, user: Member):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    member_role = discord.utils.get(ctx.guild.roles, name="Member")

    if muted_role in user.roles:  # Check if the user has the "Muted" role
        await user.remove_roles(muted_role)
        if member_role:  # Ensure the "Member" role exists before adding it back
            await user.add_roles(member_role)
        await ctx.send(f"{user.mention}'s right to speak was retrieved.")
    else:
        await ctx.send(f"{user.mention} is not muted.")  # Inform that the user is not muted


@bot.event  # Error handling for missing permissions
async def on_command_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have permission to do that!")


# Run the bot

bot.run('ODE4MDg0Njg5MTA5NDUwNzgy.GO3XIq.XuAgxpoLyZt8ZjgazydExFmgvPvqJhRK_TFWg4')
