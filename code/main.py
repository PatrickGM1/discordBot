import os
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path='.variables')

# Bot Configuration
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)  # Slash commands don't need a prefix
slash = SlashCommand(bot, sync_commands=True)


# List of cogs
COGS = ["cogs.general", "cogs.moderation", "cogs.utility", "cogs.fun", "cogs.economy"]

@bot.event
async def on_ready():
    print(f"{bot.user.name} is online!")
    await bot.change_presence(activity=discord.Game(name="/help for commands"))

# Load cogs
for cog in COGS:
    bot.load_extension(cog)

# Run the bot
bot.run(os.getenv('DISCORD_BOT_TOKEN'))
