import discord
import sqlite3
import random
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
from other.colors import ECONOMY_COLOR



class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect("dataBase/economy.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                balance INTEGER DEFAULT 1000
            )
        """)
        self.conn.commit()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Economy commands loaded.")

    def get_balance(self, user_id: int) -> int:
        """Fetch user balance from database."""
        self.cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            self.cursor.execute("INSERT INTO users (user_id, balance) VALUES (?, ?)", (user_id, 1000))
            self.conn.commit()
            return 1000  # Default starting balance

    def update_balance(self, user_id: int, amount: int):
        """Update user's balance in database."""
        self.get_balance(user_id)  # Ensures user exists in DB
        self.cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
        self.conn.commit()

    @cog_ext.cog_slash(name="balance", description="Check your balance.")
    async def _balance(self, ctx: SlashContext):
        balance = self.get_balance(ctx.author.id)
        embed = discord.Embed(title="💰 Balance", description=f"{ctx.author.mention}, your balance is **${balance}**",
                              color=ECONOMY_COLOR)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="work", description="Work and earn some money!")
    async def _work(self, ctx: SlashContext):
        earnings = random.randint(100, 500)
        self.update_balance(ctx.author.id, earnings)
        embed = discord.Embed(title="🛠 Work",
                              description=f"{ctx.author.mention}, you worked and earned **${earnings}**!",
                              color=ECONOMY_COLOR)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="daily", description="Claim your daily reward.")
    async def _daily(self, ctx: SlashContext):
        reward = 100
        self.update_balance(ctx.author.id, reward)
        embed = discord.Embed(title="🎁 Daily Reward",
                              description=f"{ctx.author.mention}, you claimed your daily reward of **${reward}**!",
                              color=ECONOMY_COLOR)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="transfer", description="Transfer money to another user.", options=[
        create_option(name="user", description="The user to send money to", option_type=6, required=True),
        create_option(name="amount", description="The amount to transfer", option_type=4, required=True)
    ])
    async def _transfer(self, ctx: SlashContext, user: discord.Member, amount: int):
        if amount <= 0:
            await ctx.send("❌ You cannot transfer a negative or zero amount.")
            return

        sender_balance = self.get_balance(ctx.author.id)
        if sender_balance < amount:
            await ctx.send("❌ You do not have enough funds for this transaction.")
            return

        self.update_balance(ctx.author.id, -amount)
        self.update_balance(user.id, amount)

        embed = discord.Embed(title="💸 Transfer",
                              description=f"{ctx.author.mention} transferred **${amount}** to {user.mention}.",
                              color=ECONOMY_COLOR)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Economy(bot))
