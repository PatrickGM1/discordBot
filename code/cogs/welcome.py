import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
import json
import os

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_config_file(self, guild):
        server_name = guild.name.replace(" ", "_")
        return f"dataBase/welcome_config_{server_name}.json"

    def load_config(self, guild):
        config_file = self.get_config_file(guild)
        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                return json.load(f)
        return {}

    def save_config(self, guild, config):
        config_file = self.get_config_file(guild)
        with open(config_file, "w") as f:
            json.dump(config, f, indent=4)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Welcome commands loaded.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        config = self.load_config(guild)

        if config.get("enabled", True):
            if config.get("welcome_message") and config.get("welcome_channel"):
                channel = self.bot.get_channel(config["welcome_channel"])
                if channel:
                    embed = discord.Embed(
                        description=f"{member.mention} {config['welcome_message'].replace('{user}', member.mention)}",
                        color=discord.Color.green())
                    await channel.send(embed=embed)

            if config.get("welcome_role"):
                role = discord.utils.get(member.guild.roles, id=config["welcome_role"])
                if role:
                    await member.add_roles(role)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        config = self.load_config(guild)

        if config.get("leave_enabled", False):
            if config.get("leave_message") and config.get("leave_channel"):
                channel = self.bot.get_channel(config["leave_channel"])
                if channel:
                    embed = discord.Embed(
                        description=f"{member.mention} {config['leave_message'].replace('{user}', member.mention)}",
                        color=discord.Color.red())
                    await channel.send(embed=embed)

    @cog_ext.cog_slash(name="setWelcomeMessage", description="Set a custom welcome message.",
                       options=[create_option(name="message", description="Use {user} to mention the new member.",
                                              option_type=3, required=True)])
    @has_permissions(administrator=True)
    async def _set_welcome_message(self, ctx: SlashContext, message: str):
        guild = ctx.guild
        config = self.load_config(guild)
        config["welcome_message"] = message
        self.save_config(guild, config)
        await ctx.send("✅ Welcome message updated!")

    @cog_ext.cog_slash(name="setWelcomeRole", description="Set a role to assign to new members.",
                       options=[create_option(name="role", description="Select a role.",
                                              option_type=8, required=True)])
    @has_permissions(administrator=True)
    async def _set_welcome_role(self, ctx: SlashContext, role: discord.Role):
        guild = ctx.guild
        config = self.load_config(guild)
        config["welcome_role"] = role.id
        self.save_config(guild, config)
        await ctx.send(f"✅ New members will now be assigned the {role.mention} role!")

    @cog_ext.cog_slash(name="setWelcomeChannel", description="Set the channel for welcome messages.",
                       options=[create_option(name="channel", description="Select a channel.",
                                              option_type=7, required=True)])
    @has_permissions(administrator=True)
    async def _set_welcome_channel(self, ctx: SlashContext, channel: discord.TextChannel):
        guild = ctx.guild
        config = self.load_config(guild)
        config["welcome_channel"] = channel.id
        self.save_config(guild, config)
        await ctx.send(f"✅ Welcome messages will be sent in {channel.mention}.")

    @cog_ext.cog_slash(name="removeWelcomeRole", description="Remove the assigned welcome role.")
    @has_permissions(administrator=True)
    async def _remove_welcome_role(self, ctx: SlashContext):
        guild = ctx.guild
        config = self.load_config(guild)
        if "welcome_role" in config:
            del config["welcome_role"]
            self.save_config(guild, config)
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
        guild = ctx.guild
        config = self.load_config(guild)
        config["enabled"] = state == "enable"
        self.save_config(guild, config)
        await ctx.send(f"✅ Welcome messages {'enabled' if state == 'enable' else 'disabled'}.")

    @cog_ext.cog_slash(name="resetWelcomeSettings", description="Reset all welcome settings for this server.")
    @has_permissions(administrator=True)
    async def _reset_welcome_settings(self, ctx: SlashContext):
        guild = ctx.guild
        config_file = self.get_config_file(guild)
        if os.path.exists(config_file):
            os.remove(config_file)
            await ctx.send("✅ Welcome settings reset!")
        else:
            await ctx.send("⚠ No welcome settings found.")

    @cog_ext.cog_slash(name="setLeaveMessage", description="Set a custom leave message.",
                       options=[create_option(name="message", description="Use {user} to mention the member.",
                                              option_type=3, required=True)])
    @has_permissions(administrator=True)
    async def _set_leave_message(self, ctx: SlashContext, message: str):
        guild = ctx.guild
        config = self.load_config(guild)
        config["leave_message"] = message
        self.save_config(guild, config)
        await ctx.send("✅ Leave message updated!")

    @cog_ext.cog_slash(name="setLeaveChannel", description="Set the channel for leave messages.",
                       options=[create_option(name="channel", description="Select a channel.",
                                              option_type=7, required=True)])
    @has_permissions(administrator=True)
    async def _set_leave_channel(self, ctx: SlashContext, channel: discord.TextChannel):
        guild = ctx.guild
        config = self.load_config(guild)
        config["leave_channel"] = channel.id
        self.save_config(guild, config)
        await ctx.send(f"✅ Leave messages will be sent in {channel.mention}.")

    @cog_ext.cog_slash(name="toggleLeaveMessage", description="Enable or disable leave messages.",
                       options=[create_option(name="state", description="Enable or disable.",
                                              option_type=3, required=True, choices=[
                               {"name": "Enable", "value": "enable"},
                               {"name": "Disable", "value": "disable"}
                           ])])
    @has_permissions(administrator=True)
    async def _toggle_leave_message(self, ctx: SlashContext, state: str):
        guild = ctx.guild
        config = self.load_config(guild)
        config["leave_enabled"] = state == "enable"
        self.save_config(guild, config)
        await ctx.send(f"✅ Leave messages {'enabled' if state == 'enable' else 'disabled'}.")

def setup(bot):
    bot.add_cog(Welcome(bot))