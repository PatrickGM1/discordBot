import discord
import random
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
from colors import FUN_COLOR, MODERATION_COLOR, UTILITY_COLOR, GENERAL_COLOR

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Fun commands loaded.")

    @cog_ext.cog_slash(name="coinflip", description="Flips a coin.")
    async def _coinflip(self, ctx: SlashContext):
        result = random.choice(["Heads", "Tails"])
        embed = discord.Embed(title="Coin Flip", description=f"The coin landed on: **{result}**", color=FUN_COLOR)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="guess", description="Guess a number!", options=[
        create_option(name="number", description="Enter a number", option_type=4, required=True)
    ])
    async def _guess(self, ctx: SlashContext, number: int):
        final_number = number + random.randint(0, 5)
        result = "You guessed correctly!" if final_number % 2 == 0 else "Better luck next time!"
        embed = discord.Embed(title="Guess a Number", description=f"The chosen number is **{final_number}**. {result}", color=FUN_COLOR)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="milmoi", description="Milmoi")
    async def _milmoi(self, ctx: SlashContext):
        embed = discord.Embed(title="Milmoi", description="Milmoi", color=FUN_COLOR)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="rps", description="Play rock, paper, scissors!", options=[
        create_option(name="choice", description="Choose rock, paper, or scissors", option_type=3, required=True, choices=[
            {"name": "Rock", "value": "rock"},
            {"name": "Paper", "value": "paper"},
            {"name": "Scissors", "value": "scissors"}
        ])
    ])
    async def _rps(self, ctx: SlashContext, choice: str):
        choices = ["rock", "paper", "scissors"]
        bot_choice = random.choice(choices)
        if choice == bot_choice:
            result = "It's a tie!"
        elif choice == "rock" and bot_choice == "scissors":
            result = "You win! Rock beats scissors."
        elif choice == "paper" and bot_choice == "rock":
            result = "You win! Paper beats rock."
        elif choice == "scissors" and bot_choice == "paper":
            result = "You win! Scissors beats paper."
        else:
            result = "You lose! Try again."
        embed = discord.Embed(title="Rock, Paper, Scissors", description=result, color=FUN_COLOR)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Fun(bot))