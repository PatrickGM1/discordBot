import os
import discord
from discord import Intents, Embed, Member
from discord.ext.commands import Bot, has_permissions, MissingPermissions
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
import random
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv(dotenv_path='.variables')

# Bot Configuration
intents = Intents.default()
intents.members = True  # Enable member intents
bot = Bot(command_prefix="!", intents=intents)
slash = SlashCommand(bot, sync_commands=True)  # Enable slash commands


# Bot startup
@bot.event
async def on_ready():
    print(f"{bot.user.name} is online and ready!")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="User Commands"))


# Error Handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have permission to do that.")


@bot.event
async def on_slash_command_error(ctx: SlashContext, error):
    if "missing_permissions" in str(error).lower():
        await ctx.send(content="You do not have permission to use this command!", hidden=True)


# Welcome new members and assign a role
@bot.event
async def on_member_join(member):
    welcome_channel = bot.get_channel(1196434128812384308)  # Replace with your channel ID
    role_name = 'Member'  # Replace with your role name
    role = discord.utils.get(member.guild.roles, name=role_name)

    if role:
        await member.add_roles(role)

    if welcome_channel:
        await welcome_channel.send(f"Welcome {member.mention} to the server! We're happy to have you here.")


# Basic commands
@slash.slash(name="hi", description="Greets the user.")
async def _hi(ctx: SlashContext):
    await ctx.send(content="Hello! How can I assist you today?")


@slash.slash(name="milmoi", description="Sends a friendly greeting.")
async def _milmoi(ctx: SlashContext):
    await ctx.send(content="Milmoi!")


# Fun game command
@slash.slash(name="guess", description="Guess a number game!", options=[
    create_option(name="number", description="Enter a number", option_type=4, required=True)
])
async def _guess(ctx: SlashContext, number: int):
    await ctx.send(content="Thinking...")
    random_adjustment = random.randint(0, 5)
    final_number = number + random_adjustment
    result = "You guessed correctly!" if final_number % 2 == 0 else "Better luck next time!"
    await ctx.send(content=f"The chosen number is **{final_number}**. {result}")


# Help command
@slash.slash(name="help", description="Displays available commands.")
async def _help(ctx: SlashContext):
    embed = Embed(title="Help", description="Here are the available commands:", color=0x00ff00)
    embed.add_field(name="/hi", value="Greets the user.", inline=False)
    embed.add_field(name="/kick", value="Kicks a user from the server. Usage: /kick @user [reason]", inline=False)
    embed.add_field(name="/warn", value="Warns a user. Usage: /warn @user [reason]", inline=False)
    embed.add_field(name="/ban", value="Bans a user from the server. Usage: /ban @user [reason]", inline=False)
    embed.add_field(name="/mute", value="Mutes a user. Usage: /mute @user", inline=False)
    embed.add_field(name="/unmute", value="Unmutes a user. Usage: /unmute @user", inline=False)
    embed.add_field(name="/userinfo", value="Displays user information. Usage: /userinfo @user", inline=False)
    embed.add_field(name="/serverinfo", value="Displays server information.", inline=False)
    embed.add_field(name="/coinflip", value="Flips a coin.", inline=False)
    embed.add_field(name="/roll", value="Rolls a dice.", inline=False)
    embed.add_field(name="/rps", value="Play Rock Paper Scissors.", inline=False)
    await ctx.send(embed=embed)


# Moderation Commands
@slash.slash(name="kick", description="Kick a user from the server", options=[
    create_option(name="user", description="The user to kick", option_type=6, required=True),
    create_option(name="reason", description="Reason for kicking", option_type=3, required=False)
])
@has_permissions(kick_members=True)
async def _kick(ctx: SlashContext, user: Member, reason: str = "No reason provided"):
    await user.kick(reason=reason)
    await ctx.send(f"{user.name} has been removed from the server. Reason: {reason}")


@slash.slash(name="warn", description="Warn a user", options=[
    create_option(name="user", description="The user to warn", option_type=6, required=True),
    create_option(name="reason", description="Reason for warning", option_type=3, required=False)
])
@has_permissions(manage_messages=True)
async def _warn(ctx: SlashContext, user: Member, reason: str = "No reason provided"):
    await ctx.send(f"{user.mention}, you have been warned for: {reason}")


@slash.slash(name="ban", description="Ban a user from the server", options=[
    create_option(name="user", description="The user to ban", option_type=6, required=True),
    create_option(name="reason", description="Reason for banning", option_type=3, required=False)
])
@has_permissions(ban_members=True)
async def _ban(ctx: SlashContext, user: Member, reason: str = "No reason provided"):
    await user.ban(reason=reason)
    await ctx.send(f"{user.name} has been banned from the server. Reason: {reason}")


@slash.slash(name="mute", description="Mute a user", options=[
    create_option(name="user", description="The user to mute", option_type=6, required=True)
])
@has_permissions(manage_roles=True)
async def _mute(ctx: SlashContext, user: Member):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if muted_role:
        await user.add_roles(muted_role)
        await ctx.send(f"{user.mention} has been muted.")
    else:
        await ctx.send("No 'Muted' role found. Please create a 'Muted' role.")


@slash.slash(name="unmute", description="Unmute a user", options=[
    create_option(name="user", description="The user to unmute", option_type=6, required=True)
])
@has_permissions(manage_roles=True)
async def _unmute(ctx: SlashContext, user: Member):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if muted_role in user.roles:
        await user.remove_roles(muted_role)
        await ctx.send(f"{user.mention} has been unmuted.")
    else:
        await ctx.send(f"{user.mention} is not muted.")


# Utility Commands
@slash.slash(name="serverinfo", description="Displays server information.")
async def _serverinfo(ctx: SlashContext):
    guild = ctx.guild
    embed = Embed(title=f"Server Info: {guild.name}", color=0x00ff00)
    embed.add_field(name="Owner", value=guild.owner, inline=True)
    embed.add_field(name="Members", value=guild.member_count, inline=True)
    embed.add_field(name="Roles", value=len(guild.roles), inline=True)
    embed.set_thumbnail(url=guild.icon_url)
    await ctx.send(embed=embed)


@slash.slash(name="userinfo", description="Displays user information.", options=[
    create_option(name="user", description="User to view", option_type=6, required=True)
])
async def _userinfo(ctx: SlashContext, user: Member):
    embed = Embed(title=f"User Info: {user.name}", color=0x00ff00)
    embed.add_field(name="Username", value=user.name, inline=True)
    embed.add_field(name="Joined Server", value=user.joined_at.strftime("%Y-%m-%d"), inline=True)
    embed.set_thumbnail(url=user.avatar_url)
    await ctx.send(embed=embed)


@slash.slash(name="coinflip", description="Flips a coin.")
async def _coinflip(ctx: SlashContext):
    coin = random.choice(["Heads", "Tails"])
    await ctx.send(f"The coin landed on: **{coin}**")

# Run the bot
bot_token = os.getenv('DISCORD_BOT_TOKEN')
bot.run(bot_token)
