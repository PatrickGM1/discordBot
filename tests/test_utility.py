import pytest
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from code.cogs.utility import Utility

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    slash = SlashCommand(bot, sync_commands=True)
    bot.add_cog(Utility(bot))
    return bot

@pytest.mark.asyncio
async def test_serverinfo(bot):
    ctx = SlashContext(bot=bot, command=None, data=None)
    utility_cog = bot.get_cog("Utility")
    await utility_cog._serverinfo(ctx)
    assert ctx.sent_messages[0].embed.title == f"Server Info: {ctx.guild.name}"

@pytest.mark.asyncio
async def test_userinfo(bot):
    ctx = SlashContext(bot=bot, command=None, data=None)
    utility_cog = bot.get_cog("Utility")
    user = ctx.guild.get_member(123456789)  # Replace with a valid user ID
    await utility_cog._userinfo(ctx, user)
    assert ctx.sent_messages[0].embed.title == f"User Info: {user.name}"