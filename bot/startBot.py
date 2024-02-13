import discord
from discord import Intents, Embed, Member
from time import sleep
from discord.ext.commands import Bot, has_permissions, MissingPermissions
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
from discord import File
# Create a bot instance with specific intents
intents = Intents.default()
intents.members = True  # Enable member intents
bot = Bot(command_prefix="!", intents=intents)
slash = SlashCommand(bot, sync_commands=True)  # Enable slash commands

# Event listener for when the bot is ready
@bot.event
async def on_ready():
    print(f"{bot.user.name} is up and running!")

# Error handling for missing permissions for text-based commands
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have permission to do that!")

# Error handling for slash commands, including missing permissions
@bot.event
async def on_slash_command_error(ctx: SlashContext, error):
    # Check if the error is due to missing permissions
    if "missing_permissions" in str(error).lower():
        await ctx.send(content="You do not have permission to use this command!", hidden=True)
    else:
        # Handle other errors here
        pass


# Event listener for new member join
@bot.event
@bot.event
async def on_member_join(member):
    welcome_channel = bot.get_channel(1196434128812384308)  # Replace with your channel ID
    autorole_name = 'Member'  # Replace with your role name
    role = discord.utils.get(member.guild.roles, name=autorole_name)
    await member.add_roles(role)

    if welcome_channel:
        await welcome_channel.send(f"Hello {member.mention}, welcome to the server!")

# Slash command for /hi
@slash.slash(name="hi", description="Says hi!")
async def _hi(ctx: SlashContext):
    await ctx.send(content="Hi!")


@slash.slash(name="drake", description="Sends a photo of drake")
async def _drake(ctx: SlashContext):
    file_path = 'drake.gif'  # Make sure this path is correct
    spoiler_file_path = f"SPOILER_{file_path}"  # Prefix the filename with 'SPOILER_'
    file = File(fp=file_path, filename=spoiler_file_path)  # Set the filename parameter to the spoiler version
    await ctx.send(file=file)

# Slash command for /milmoi
@slash.slash(name="milmoi", description="Says milmoi!")
async def _milmoi(ctx: SlashContext):
    await ctx.send(content="Milmoi!")

# Slash command for /tabinet
@slash.slash(name="tabinet", description="Let's play a game, choose a number", options=[
                 create_option(name="numar", description="insert a number", option_type=3, required=True)
             ])
async def _tabinet(ctx: SlashContext, numar: str =""):
    numar = int(numar)
    await ctx.send(content="I choose...")
    sleep(2)
    numar = int(numar) + 1
    numar = str(numar)
    await ctx.send(content= numar +", skill issue you lost")

# Slash command for /help
@slash.slash(name="help", description="Shows this message")
async def _help(ctx: SlashContext):
    embed = Embed(title="Help", description="List of available commands:", color=0x00ff00)
    embed.add_field(name="/hi", value="Says hi!", inline=False)
    embed.add_field(name="/kick", value="Kicks a user from the server. Usage: /kick @user [reason]", inline=False)
    embed.add_field(name="/warn", value="Warns a user. Usage: /warn @user [reason]", inline=False)
    embed.add_field(name="/ban", value="Bans a user from the server. Usage: /ban @user [reason]", inline=False)
    embed.add_field(name="/mute", value="Mutes a user. Usage: /mute @user", inline=False)
    await ctx.send(embed=embed)

# Slash command for /kick
@slash.slash(name="kick", description="Kick a user from the server", options=[
                 create_option(name="user", description="The user to kick", option_type=6, required=True),
                 create_option(name="reason", description="The reason for kicking", option_type=3, required=False)
             ])
@has_permissions(kick_members=True)
async def _kick(ctx: SlashContext, user: Member, reason: str = "No reason provided"):
    await user.kick(reason=reason)
    await ctx.send(f"User {user.name} has been kicked for: {reason}")

# Slash command for /warn
@slash.slash(name="warn", description="Warn a user", options=[
                 create_option(name="user", description="The user to warn", option_type=6, required=True),
                 create_option(name="reason", description="The reason for the warning", option_type=3, required=False)
             ])
@has_permissions(manage_messages=True)
async def _warn(ctx: SlashContext, user: Member, reason: str = "No reason provided"):
    await ctx.send(f"{user.mention}, you have been warned for: {reason}")

# Slash command for /ban
@slash.slash(name="ban", description="Ban a user from the server", options=[
                 create_option(name="user", description="The user to ban", option_type=6, required=True),
                 create_option(name="reason", description="The reason for banning", option_type=3, required=False)
             ])
@has_permissions(ban_members=True)
async def _ban(ctx: SlashContext, user: Member, reason: str = "No reason provided"):
    await user.ban(reason=reason)
    await ctx.send(f"User {user.name} has been banned for: {reason}")

# Slash command for /mute
@slash.slash(name="mute", description="Mute a user in the server", options=[
                 create_option(name="user", description="The user to mute", option_type=6, required=True)
             ])
@has_permissions(manage_roles=True)
async def _mute(ctx: SlashContext, user: Member):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    member_role = discord.utils.get(ctx.guild.roles, name= "Member")
    if muted_role:
        await user.add_roles(muted_role)
        await user.remove_roles(member_role)
        await ctx.send(f"{user.mention} has been muted.")
    else:
        await ctx.send("No 'Muted' role found. Please create a 'Muted' role with appropriate permissions.")

# Slash command for /unmute
@slash.slash(name="unmute", description="Unmute a user in the server", options=[
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
        await ctx.send(f"{user.mention} has been unmuted.")
    else:
        await ctx.send(f"{user.mention} is not muted.")  # Inform that the user is not muted


# Error handling for missing permissions
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have permission to do that!")

# Run the bot

bot.run('ODE4MDg0Njg5MTA5NDUwNzgy.GO3XIq.XuAgxpoLyZt8ZjgazydExFmgvPvqJhRK_TFWg4')