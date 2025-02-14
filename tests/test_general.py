import pytest
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from code.cogs.general import General

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    slash = SlashCommand(bot, sync_commands=True)
    bot.add_cog(General(bot))
    return bot

@pytest.mark.asyncio
async def test_hi(bot):
    ctx = SlashContext(bot=bot, command=None, data=None)
    general_cog = bot.get_cog("General")
    await general_cog._hi(ctx)
    assert ctx.sent_messages[0].embed.title == "Hello!"

@pytest.mark.asyncio
async def test_help(bot):
    ctx = SlashContext(bot=bot, command=None, data=None)
    general_cog = bot.get_cog("General")
    await general_cog._help(ctx)
    assert ctx.sent_messages[0].embed.title == "Help"