import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
from colors import FUN_COLOR, MODERATION_COLOR, UTILITY_COLOR, GENERAL_COLOR


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderation commands loaded.")


    @cog_ext.cog_slash(name="kick", description="Kick a user", options=[
        create_option(name="user", description="The user to kick", option_type=6, required=True)
    ])
    @has_permissions(kick_members=True)
    async def _kick(self, ctx: SlashContext, user: discord.Member):
        await user.kick(reason="Kicked by moderator.")
        embed = discord.Embed(title="User Kicked", description=f"{user.name} has been kicked.", color=MODERATION_COLOR)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="ban", description="Ban a user", options=[
        create_option(name="user", description="The user to ban", option_type=6, required=True)
    ])
    @has_permissions(ban_members=True)
    async def _ban(self, ctx: SlashContext, user: discord.Member):
        await user.ban(reason="Banned by moderator.")
        embed = discord.Embed(title="User Banned", description=f"{user.name} has been banned.", color=MODERATION_COLOR)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="mute", description="Mute a user", options=[
        create_option(name="user", description="The user to mute", option_type=6, required=True)
    ])
    @has_permissions(manage_roles=True)
    async def _mute(self, ctx: SlashContext, user: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if role:
            await user.add_roles(role)
            embed = discord.Embed(title="User Muted", description=f"{user.mention} has been muted.",
                                  color=MODERATION_COLOR)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Muted role not found.")


    @cog_ext.cog_slash(name="unmute", description="Unmute a user", options=[
    create_option(name="user", description="The user to unmute", option_type=6, required=True)
    ])
    @has_permissions(manage_roles=True)
    async def _unmute(self, ctx: SlashContext, user: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if role:
            await user.remove_roles(role)
            embed = discord.Embed(title="User Unmuted", description=f"{user.mention} has been unmuted.", color=MODERATION_COLOR)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Muted role not found.")

    @cog_ext.cog_slash(name="warn", description="Warn a user", options=[
        create_option(name="user", description="The user to warn", option_type=6, required=True),
        create_option(name="reason", description="The reason for the warning", option_type=3, required=True)
    ])
    @has_permissions(manage_roles=True)
    async def _warn(self, ctx: SlashContext, user: discord.Member, reason: str):
        embed = discord.Embed(title="User Warned", description=f"{user.mention} has been warned for {reason}.",
                              color=MODERATION_COLOR)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
