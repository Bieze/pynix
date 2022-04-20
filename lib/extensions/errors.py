from nextcord.ext.commands import Context
from ..server import bot as BotCon
from nextcord.ext import commands


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = BotCon

    @commands.Cog.listener()
    async def on_command_error(self, ctx : Context, error):
        if hasattr(ctx.command, 'on_error'):
            return
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return
        error = getattr(error, 'original', error)

        if isinstance(error, commands.CommandNotFound):
            await ctx.send(":x: That command does not exist")
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send(":x: This command does not work in private messages")
        elif isinstance(error, commands.PrivateMessageOnly):
            await ctx.send(":x: This command only works in private messages")
        elif isinstance(error, commands.UserInputError):
            await ctx.send(f"""
            :x: You have too many arguments in your command, these are the problems: {''.join(error.args)}""")  # noqa" E501
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"""
            :x: This command is on cooldown, please retry after {round(error.retry_after)}""")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(f":x: Member: {commands.MemberNotFound.args} not found")
        elif isinstance(error, commands.MissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_permissions]

            if len(missing) > 2:
                fmt = '{}, and {}'.format(", ".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            await ctx.send(f":x: You are missing the following permission(s): {fmt}")


def setup(bot):
    bot.add_cog(Errors(bot))
