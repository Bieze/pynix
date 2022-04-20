from nextcord.ext.commands import (
    Cog, command, Context, has_permissions)
from nextcord import (
    Embed, Member, utils, Permissions,
    TextChannel)
from ..server import bot as BotCon
import time


class Moderators(Cog):
    def __init__(self, bot):
        self.bot = BotCon

    @command(name="ban")
    @has_permissions(ban_members=True)
    async def BanUser(self, ctx : Context, member : Member = None, *, reason="No reason specified"):
        if Member is None:
            await ctx.send(":x: You didn't specify a member")
        else:
            try:
                em = Embed(colour=0xF8BD96)
                em.title = f"Banned from {ctx.guild.name}"
                em.add_field(name="Reason", value=reason)
                await member.send(embed=em)
                await member.ban(reason=reason)
                time.sleep(1)
                em = Embed(colour=0xF8BD96)
                em.title = f"Banned {member.name} from {ctx.guild.name}"
                em.add_field(name="Reason", value=reason)
                await ctx.send(embed=em)
            except Exception as e:
                await ctx.send(f":x: Could not ban user: {e}")
                print(f"[{time.ctime()}] {e}")

    @command(name="unban")
    @has_permissions(ban_members=True)
    async def UnbanUser(self, ctx : Context, id=None):
        if id is None:
            await ctx.send(":x: You didn't specify a user")
        else:
            try:
                user = await self.bot.fetch_user(id)
                await ctx.guild.unban(user)
                em = Embed(colour=0xF8BD96)
                em.title = f"Unbanned {user.name}"
                await ctx.send(embed=em)
            except Exception as e:
                await ctx.send(f":x: Could not unban user: {e}")

    @command(name="kick")
    @has_permissions(kick_members=True)
    async def KickUser(self, ctx : Context, member : Member = None, *, reason="No reason specified"):
        if Member is None:
            await ctx.send(":x: You didn't specify a member")
        else:
            try:
                em = Embed(colour=0xF8BD96)
                em.title = f"Kicked from {ctx.guild.name}"
                em.add_field(name="Reason", value=reason)
                await member.send(embed=em)
                await member.kick(reason=reason)
                time.sleep(1)
                em = Embed(colour=0xF8BD96)
                em.title = f"Kicked {member.name} from {ctx.guild.name}"
                em.add_field(name="Reason", value=reason)
                await ctx.send(embed=em)
            except Exception as e:
                await ctx.send(f":x: Could not kick user: {e}")
                print(f"[{time.ctime()}] {e}")

    @command(name="mute")
    @has_permissions(manage_messages=True)
    async def MuteUser(self, ctx : Context, member : Member = None, *, reason="No reason specified"):
        if member is None:
            await ctx.send(":x: You didn't specify a member")
        else:
            try:
                if utils.get(ctx.guild.roles, name="muted"):
                    mutedRole = utils.get(ctx.guild.roles, name="muted")
                    await member.add_roles(mutedRole)
                else:
                    perms = Permissions(send_messages=False, read_messages=True)
                    await ctx.guild.create_role(name="muted", permissions=perms)
                    mutedRole = utils.get(ctx.guild.roles, name="muted")
                    await member.add_roles(mutedRole)
                em = Embed(colour=0xF8BD96)
                em.title = f"Muted in {ctx.guild.name}"
                em.add_field(name="Reason", value=reason)
                await member.send(embed=em)
                em = Embed(colour=0xF8BD96)
                em.title = f"Muted {ctx.guild.name}"
                em.add_field(name="Reason", value=reason)
                await ctx.send(embed=em)
            except Exception as e:
                await ctx.send(f":x: Could not mute user: {e}")

    @command(name="unmute")
    @has_permissions(manage_messages=True)
    async def UnmuteUser(self, ctx : Context, member : Member = None):
        if member is None:
            await ctx.send(":x: You haven't specified a user")
        else:
            try:
                if utils.get(ctx.guild.roles, name="muted"):
                    mutedRole = utils.get(ctx.guild.roles, name="muted")
                    if mutedRole in member.roles:
                        await member.remove_roles(mutedRole)
                        em = Embed(colour=0xF8BD96)
                        em.title = f"Unmuted in {ctx.guild.name}"
                        await member.send(embed=em)
                        em = Embed(colour=0xF8BD96)
                        em.title = f"Unmuted in {member.name}"
                        await ctx.send(embed=em)
                    else:
                        await ctx.send(":x: That user is not muted")
                else:
                    perms = Permissions(send_messages=False, read_messages=True)
                    await ctx.guild.create_role(name="muted", permissions=perms)
                    await ctx.send(":x: That user is not muted")
            except Exception as e:
                await ctx.send(f":x: Could not unmute user: {e}")

    @command(name="setLogChan")
    @has_permissions(manage_permissions=True)
    async def SetLogChannel(self, ctx : Context, channel : TextChannel = None):
        if channel is None:
            await ctx.send(":x: No channel specified")
        else:
            try:
                log = await self.bot.pool.fetch("SELECT logger FROM prod.servers WHERE id = $1", ctx.guild.id)
                if log is None:
                    await self.bot.pool.execute("""
                    INSERT INTO prod.servers(id, logger) VALUES($1, $2)""", ctx.guild.id, channel.id)
                    em = Embed(colour=0xF8BD96)
                    em.description = f"Set log channel to <#{channel.id}>"
                    await ctx.send(embed=em)
                else:
                    await self.bot.pool.execute("UPDATE prod.servers SET logger = $1", channel.id)
                    em = Embed(colour=0xF8BD96)
                    em.description = f"Set log channel to <#{channel.id}>"
                    await ctx.send(embed=em)
            except Exception as e:
                await ctx.send(f":x: Could not set the log channel: {e}")


def setup(bot):
    bot.add_cog(Moderators(bot))
