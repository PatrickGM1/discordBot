import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
import json
import os

CONFIG_FILE = "dataBase/welcome_config.json"


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.load_config()

    def load_config(self):
        """Loads the welcome configuration from a JSON file."""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                self.config = json.load(f)
        else:
            self.config = {}

    def save_config(self):
        """Saves the welcome configuration to a JSON file."""
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.config, f, indent=4)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Welcome commands loaded.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_id = str(member.guild.id)

        if guild_id in self.config and self.config[guild_id].get("enabled", True):
            data = self.config[guild_id]

            # Send Welcome Message
            if data.get("welcome_message") and data.get("welcome_channel"):
                channel = self.bot.get_channel(data["welcome_channel"])
                if channel:
                    embed = discord.Embed(
                        description=f"{member.mention} {data['welcome_message'].replace('{user}', member.mention)}",
                        color=discord.Color.green())
                    await channel.send(embed=embed)

            # Assign Welcome Role
            if data.get("welcome_role"):
                role = discord.utils.get(member.guild.roles, id=data["welcome_role"])
                if role:
                    await member.add_roles(role)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild_id = str(member.guild.id)

        if guild_id in self.config and self.config[guild_id].get("leave_enabled", False):
            data = self.config[guild_id]

            # Send Leave Message
            if data.get("leave_message") and data.get("leave_channel"):
                channel = self.bot.get_channel(data["leave_channel"])
                if channel:
                    embed = discord.Embed(
                        description=f"{member.mention} {data['leave_message'].replace('{user}', member.mention)}",
                        color=discord.Color.red())
                    await channel.send(embed=embed)

    # ─────────────── Welcome System Commands (Admin-Only) ─────────────── #

    @cog_ext.cog_slash(name="setWelcomeMessage", description="Set a custom welcome message.",
                       options=[create_option(name="message", description="Use {user} to mention the new member.",
                                              option_type=3, required=True)])
    @has_permissions(administrator=True)
    async def _set_welcome_message(self, ctx: SlashContext, message: str):
        guild_id = str(ctx.guild.id)
        self.config.setdefault(guild_id, {})["welcome_message"] = message
        self.save_config()
        await ctx.send("✅ Welcome message updated!")

    @cog_ext.cog_slash(name="setWelcomeRole", description="Set a role to assign to new members.",
                       options=[create_option(name="role", description="Select a role.",
                                              option_type=8, required=True)])
    @has_permissions(administrator=True)
    async def _set_welcome_role(self, ctx: SlashContext, role: discord.Role):
        guild_id = str(ctx.guild.id)
        self.config.setdefault(guild_id, {})["welcome_role"] = role.id
        self.save_config()
        await ctx.send(f"✅ New members will now be assigned the {role.mention} role!")

    @cog_ext.cog_slash(name="setWelcomeChannel", description="Set the channel for welcome messages.",
                       options=[create_option(name="channel", description="Select a channel.",
                                              option_type=7, required=True)])
    @has_permissions(administrator=True)
    async def _set_welcome_channel(self, ctx: SlashContext, channel: discord.TextChannel):
        guild_id = str(ctx.guild.id)
        self.config.setdefault(guild_id, {})["welcome_channel"] = channel.id
        self.save_config()
        await ctx.send(f"✅ Welcome messages will be sent in {channel.mention}.")

    @cog_ext.cog_slash(name="removeWelcomeRole", description="Remove the assigned welcome role.")
    @has_permissions(administrator=True)
    async def _remove_welcome_role(self, ctx: SlashContext):
        guild_id = str(ctx.guild.id)
        if "welcome_role" in self.config.get(guild_id, {}):
            del self.config[guild_id]["welcome_role"]
            self.save_config()
            await ctx.send("✅ Welcome role removed!")
        else:
            await ctx.send("⚠ No welcome role is currently set.")

    @cog_ext.cog_slash(name="toggleWelcome", description="Enable or disable welcome messages.",
                       options=[create_option(name="state", description="Enable or disable.",
                                              option_type=3, required=True, choices=[
                               {"name": "Enable", "value": "enable"},
                               {"name": "Disable", "value": "disable"}
                           ])])
    @has_permissions(administrator=True)
    async def _toggle_welcome(self, ctx: SlashContext, state: str):
        guild_id = str(ctx.guild.id)
        self.config.setdefault(guild_id, {})["enabled"] = state == "enable"
        self.save_config()
        await ctx.send(f"✅ Welcome messages {'enabled' if state == 'enable' else 'disabled'}.")

    @cog_ext.cog_slash(name="resetWelcomeSettings", description="Reset all welcome settings for this server.")
    @has_permissions(administrator=True)
    async def _reset_welcome_settings(self, ctx: SlashContext):
        guild_id = str(ctx.guild.id)
        if guild_id in self.config:
            del self.config[guild_id]
            self.save_config()
            await ctx.send("✅ Welcome settings reset!")
        else:
            await ctx.send("⚠ No welcome settings found.")

    # ─────────────── Leave System Commands (Admin-Only) ─────────────── #

    @cog_ext.cog_slash(name="setLeaveMessage", description="Set a custom leave message.",
                       options=[create_option(name="message", description="Use {user} to mention the member.",
                                              option_type=3, required=True)])
    @has_permissions(administrator=True)
    async def _set_leave_message(self, ctx: SlashContext, message: str):
        guild_id = str(ctx.guild.id)
        self.config.setdefault(guild_id, {})["leave_message"] = message
        self.save_config()
        await ctx.send("✅ Leave message updated!")

    @cog_ext.cog_slash(name="setLeaveChannel", description="Set the channel for leave messages.",
                       options=[create_option(name="channel", description="Select a channel.",
                                              option_type=7, required=True)])
    @has_permissions(administrator=True)
    async def _set_leave_channel(self, ctx: SlashContext, channel: discord.TextChannel):
        guild_id = str(ctx.guild.id)
        self.config.setdefault(guild_id, {})["leave_channel"] = channel.id
        self.save_config()
        await ctx.send(f"✅ Leave messages will be sent in {channel.mention}.")

    @cog_ext.cog_slash(name="toggleLeaveMessage", description="Enable or disable leave messages.",
                       options=[create_option(name="state", description="Enable or disable.",
                                              option_type=3, required=True, choices=[
                               {"name": "Enable", "value": "enable"},
                               {"name": "Disable", "value": "disable"}
                           ])])
    @has_permissions(administrator=True)
    async def _toggle_leave_message(self, ctx: SlashContext, state: str):
        guild_id = str(ctx.guild.id)
        self.config.setdefault(guild_id, {})["leave_enabled"] = state == "enable"
        self.save_config()
        await ctx.send(f"✅ Leave messages {'enabled' if state == 'enable' else 'disabled'}.")


# ───────────────────────────────────────── #

def setup(bot):
    bot.add_cog(Welcome(bot))
