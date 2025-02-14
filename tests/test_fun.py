import pytest
import random
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from code.cogs.fun import Fun

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    slash = SlashCommand(bot, sync_commands=True)
    bot.add_cog(Fun(bot))
    return bot

@pytest.mark.asyncio
async def test_coinflip(bot):
    ctx = SlashContext(bot=bot, command=None, data=None)
    fun_cog = bot.get_cog("Fun")
    await fun_cog._coinflip(ctx)
    assert ctx.sent_messages[0].embed.title == "Coin Flip"

@pytest.mark.asyncio
async def test_guess(bot):
    ctx = SlashContext(bot=bot, command=None, data=None)
    fun_cog = bot.get_cog("Fun")
    await fun_cog._guess(ctx, 3)
    assert ctx.sent_messages[0].embed.title == "Guess a Number"

@pytest.mark.asyncio
async def test_rps(bot):
    ctx = SlashContext(bot=bot, command=None, data=None)
    fun_cog = bot.get_cog("Fun")
    await fun_cog._rps(ctx, "rock")
    assert ctx.sent_messages[0].embed.title == "Rock, Paper, Scissors"