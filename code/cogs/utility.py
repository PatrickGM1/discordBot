import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Utility commands loaded.")

    @cog_ext.cog_slash(name="serverinfo", description="Displays server information.")
    async def _serverinfo(self, ctx: SlashContext):
        guild = ctx.guild
        embed = discord.Embed(title=f"Server Info: {guild.name}", color=0x00ff00)
        embed.add_field(name="Owner", value=guild.owner, inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Roles", value=len(guild.roles), inline=True)
        embed.set_thumbnail(url=guild.icon_url)
        await ctx.send(embed=embed)


    @cog_ext.cog_slash(name="userinfo", description="Displays user information.", options=[
        create_option(name="user", description="The user to get information on", option_type=6, required=False)
    ])
    async def _userinfo(self, ctx: SlashContext, user: discord.Member = None):
        user = user or ctx.author
        embed = discord.Embed(title=f"User Info: {user.name}", color=0x00ff00)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Status", value=user.status, inline=True)
        embed.add_field(name="Joined", value=user.joined_at.strftime("%d/%m/%Y, %H:%M:%S"), inline=True)
        embed.add_field(name="Created", value=user.created_at.strftime("%d/%m/%Y, %H:%M:%S"), inline=True)
        roles = [role for role in user.roles]
        roles.pop(0)
        roles.reverse()
        roles = " ".join([role.mention for role in roles])
        embed.add_field(name="Roles", value=roles, inline=False)
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Utility(bot))
