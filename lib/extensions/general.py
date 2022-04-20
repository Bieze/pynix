from nextcord.ext.commands import Cog, command, Context
from ..server import bot as BotCon
from nextcord import Embed
import requests


class General(Cog):
    def __init__(self, bot):
        self.bot = BotCon

    @command(name="mcserver")
    async def FetchServerStatus(self, ctx : Context):
        status = requests.get('https://api.horus64.org/server')

        em = Embed(
            colour=0xF8BD96,
        )

        em.set_author(
            name="Status of the Server64 Minecraft server",
            icon_url="https://horus64.org/server64.png")
        if status.json()['Status'] == "up":
            mcstatus = "Up"
        else:
            mcstatus = "Down"
        em.add_field(name="Server status", value=mcstatus)
        em.add_field(name="Players online", value=f"{status.json()['NumberPlayersOnline']}/100")
        em.add_field(name="Server software", value=status.json()['Version'])
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(General(bot))
