import pytest
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from code.cogs.moderation import Moderation

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    slash = SlashCommand(bot, sync_commands=True)
    bot.add_cog(Moderation(bot))
    return bot

@pytest.mark.asyncio
async def test_kick(bot):
    ctx = SlashContext(bot=bot, command=None, data=None)
    moderation_cog = bot.get_cog("Moderation")
    user = ctx.guild.get_member(123456789)  # Replace with a valid user ID
    await moderation_cog._kick(ctx, user)
    assert ctx.sent_messages[0].embed.title == "User Kicked"

@pytest.mark.asyncio
async def test_ban(bot):
    ctx = SlashContext(bot=bot, command=None, data=None)
    moderation_cog = bot.get_cog("Moderation")
    user = ctx.guild.get_member(123456789)  # Replace with a valid user ID
    await moderation_cog._ban(ctx, user)
    assert ctx.sent_messages[0].embed.title == "User Banned"

@pytest.mark.asyncio
async def test_mute(bot):
    ctx = SlashContext(bot=bot, command=None, data=None)
    moderation_cog = bot.get_cog("Moderation")
    user = ctx.guild.get_member(123456789)  # Replace with a valid user ID
    await moderation_cog._mute(ctx, user)
    assert ctx.sent_messages[0].embed.title == "User Muted"

@pytest.mark.asyncio
async def test_unmute(bot):
    ctx = SlashContext(bot=bot, command=None, data=None)
    moderation_cog = bot.get_cog("Moderation")
    user = ctx.guild.get_member(123456789)  # Replace with a valid user ID
    await moderation_cog._unmute(ctx, user)
    assert ctx.sent_messages[0].embed.title == "User Unmuted"

@pytest.mark.asyncio
async def test_warn(bot):
    ctx = SlashContext(bot=bot, command=None, data=None)
    moderation_cog = bot.get_cog("Moderation")
    user = ctx.guild.get_member(123456789)  # Replace with a valid user ID
    await moderation_cog._warn(ctx, user, "Test reason")
    assert ctx.sent_messages[0].embed.title == "User Warned"