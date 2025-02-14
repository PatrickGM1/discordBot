import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from other.colors import GENERAL_COLOR

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("General commands loaded.")

    @cog_ext.cog_slash(name="hi", description="Greets the user.")
    async def _hi(self, ctx: SlashContext):
        embed = discord.Embed(title="Hello!", description="How can I assist you today?", color=GENERAL_COLOR)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="help", description="Displays available commands.")
    async def _help(self, ctx: SlashContext):
        embed = discord.Embed(title="Help", description="Here are the available commands:", color=GENERAL_COLOR)
        embed.add_field(name="/hi", value="Greets the user.", inline=False)
        embed.add_field(name="/guess", value="Play a guessing game.", inline=False)
        embed.add_field(name="/coinflip", value="Flip a coin.", inline=False)
        embed.add_field(name="/rps", value="Play rock, paper, scissors.", inline=False)
        embed.add_field(name="/milmoi", value="Milmoi.", inline=False)
        embed.add_field(name="/serverinfo", value="Get server details.", inline=False)
        embed.add_field(name="/userinfo", value="Get user details.", inline=False)
        embed.add_field(name="/kick", value="Kick a user.", inline=False)
        embed.add_field(name="/ban", value="Ban a user.", inline=False)
        embed.add_field(name="/mute", value="Mute a user.", inline=False)
        embed.add_field(name="/unmute", value="Unmute a user.", inline=False)
        embed.add_field(name="/warn", value="Warn a user.", inline=False)
        embed.add_field(name="/balance", value="Check your balance.", inline=False)
        embed.add_field(name="/work", value="Work and earn money.", inline=False)
        embed.add_field(name="/daily", value="Claim your daily reward.", inline=False)
        embed.add_field(name="/pay", value="Pay another user. Usage: /pay @user [amount]", inline=False)
        embed.add_field(name="/gamble", value="Gamble your money. Usage: /gamble [amount]", inline=False)
        embed.add_field(name="/slots", value="Play the slots game.", inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(General(bot))