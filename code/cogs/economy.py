import discord
import sqlite3
import random
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
from other.colors import ECONOMY_COLOR
from discord.ext.commands import has_permissions

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_db_connection(self, guild):
        server_name = guild.name.replace(" ", "_")
        conn = sqlite3.connect(f"dataBase/economy_{server_name}.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                balance INTEGER DEFAULT 1000
            )
        """)
        conn.commit()
        return conn, cursor

    @commands.Cog.listener()
    async def on_ready(self):
        print("Economy commands loaded.")

    def get_balance(self, guild, user_id: int) -> int:
        conn, cursor = self.get_db_connection(guild)
        cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            cursor.execute("INSERT INTO users (user_id, balance) VALUES (?, ?)", (user_id, 1000))
            conn.commit()
            return 1000

    def update_balance(self, guild, user_id: int, amount: int):
        conn, cursor = self.get_db_connection(guild)
        self.get_balance(guild, user_id)
        cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
        conn.commit()

    @cog_ext.cog_slash(name="balance", description="Check your balance.")
    async def _balance(self, ctx: SlashContext):
        balance = self.get_balance(ctx.guild, ctx.author.id)
        embed = discord.Embed(title="💰 Balance", description=f"{ctx.author.mention}, your balance is **${balance}**",
                              color=ECONOMY_COLOR)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="work", description="Work and earn some money!")
    async def _work(self, ctx: SlashContext):
        earnings = random.randint(100, 500)
        self.update_balance(ctx.guild, ctx.author.id, earnings)
        embed = discord.Embed(title="🛠 Work",
                              description=f"{ctx.author.mention}, you worked and earned **${earnings}**!",
                              color=ECONOMY_COLOR)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="daily", description="Claim your daily reward.")
    async def _daily(self, ctx: SlashContext):
        reward = 100
        self.update_balance(ctx.guild, ctx.author.id, reward)
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

        sender_balance = self.get_balance(ctx.guild, ctx.author.id)
        if sender_balance < amount:
            await ctx.send("❌ You do not have enough funds for this transaction.")
            return

        self.update_balance(ctx.guild, ctx.author.id, -amount)
        self.update_balance(ctx.guild, user.id, amount)

        embed = discord.Embed(title="💸 Transfer",
                              description=f"{ctx.author.mention} transferred **${amount}** to {user.mention}.",
                              color=ECONOMY_COLOR)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="gamble", description="Bet an amount and see if you win!", options=[
        create_option(name="amount", description="The amount to gamble", option_type=4, required=True)
    ])
    async def _gamble(self, ctx: SlashContext, amount: int):
        user_balance = self.get_balance(ctx.guild, ctx.author.id)

        if amount <= 0:
            await ctx.send("❌ You must gamble a positive amount!")
            return

        if user_balance < amount:
            await ctx.send("❌ You do not have enough money to gamble that amount!")
            return

        if random.random() < 0.5:
            self.update_balance(ctx.guild, ctx.author.id, amount)
            embed = discord.Embed(title="🎲 Gamble",
                                  description=f"{ctx.author.mention}, you won **${amount}**!",
                                  color=ECONOMY_COLOR)
        else:
            self.update_balance(ctx.guild, ctx.author.id, -amount)
            embed = discord.Embed(title="🎲 Gamble",
                                  description=f"{ctx.author.mention}, you lost **${amount}**. Better luck next time!",
                                  color=discord.Color.red())

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="slots", description="Spin the slot machine!", options=[
        create_option(name="bet", description="The amount to bet", option_type=4, required=True)
    ])
    async def _slots(self, ctx: SlashContext, bet: int):
        user_balance = self.get_balance(ctx.guild, ctx.author.id)

        if bet <= 0:
            await ctx.send("❌ Your bet must be a positive number!")
            return

        if user_balance < bet:
            await ctx.send("❌ You do not have enough money to place this bet!")
            return

        symbols = ["🍒", "🍋", "🍉", "⭐", "💎"]
        slot_result = [random.choice(symbols) for _ in range(3)]

        payout_multiplier = 0
        if slot_result[0] == slot_result[1] == slot_result[2]:
            payout_multiplier = 5
        elif slot_result[0] == slot_result[1] or slot_result[1] == slot_result[2] or slot_result[0] == slot_result[2]:
            payout_multiplier = 2
        else:
            payout_multiplier = 0

        winnings = bet * payout_multiplier
        self.update_balance(ctx.guild, ctx.author.id, winnings - bet)

        embed = discord.Embed(title="🎰 Slots", description=f"{ctx.author.mention} spun: {' | '.join(slot_result)}\n\n",
                              color=ECONOMY_COLOR)

        if payout_multiplier == 5:
            embed.description += f"🎉 **JACKPOT!** You won **${winnings}**!"
        elif payout_multiplier == 2:
            embed.description += f"✨ You won **${winnings}**!"
        else:
            embed.description += "💀 You lost your bet!"

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="setFunds", description="Set a user's balance (Admin only).", options=[
        create_option(name="user", description="The user to set the balance for", option_type=6, required=True),
        create_option(name="amount", description="The amount to set", option_type=4, required=True)
    ])
    @has_permissions(administrator=True)
    async def _set_funds(self, ctx: SlashContext, user: discord.Member, amount: int):
        if amount < 0:
            await ctx.send("❌ The amount cannot be negative.")
            return

        conn, cursor = self.get_db_connection(ctx.guild)
        cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (amount, user.id))
        conn.commit()

        embed = discord.Embed(title="💰 Set Funds",
                              description=f"{ctx.author.mention} set {user.mention}'s balance to **${amount}**.",
                              color=ECONOMY_COLOR)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Economy(bot))