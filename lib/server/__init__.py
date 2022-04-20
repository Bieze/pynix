from nextcord.ext.commands import Bot as BotBase
from datetime import datetime
import nextcord
import asyncpg
import toml
import time
import os


class Bot(BotBase):
    def __init__(self):
        self.ConfigFile = toml.load('config.toml')
        super().__init__(command_prefix="?", intents=nextcord.Intents.all())

    def loadExt(self):
        for cog in os.listdir('lib/extensions'):
            if cog is None:
                print(f"[{time.ctime()}] No extensions to load")
            elif cog.endswith('.py'):
                self.load_extension(f'lib.extensions.{cog[:-3]}')
                print(f"[{time.ctime()}] Loaded extension: {cog[:-3]}.py")

    def run(self, version):
        self.VERSION = version
        TOKEN = self.ConfigFile['bot']['token']
        super().run(TOKEN, reconnect=True)

    async def on_connect(self):
        print(f"[{time.ctime()}] Connected to Discord")

    async def on_ready(self):
        try:
            self.pool = await asyncpg.create_pool(self.ConfigFile['database']['dsn'])
            print(f"[{time.ctime()}] Created database pool")
            self.cur = await self.pool.acquire()
            print(f"[{time.ctime()}] Acquired cursor")
            await self.cur.execute("""
            CREATE TABLE IF NOT EXISTS prod.users
            (
                name text NOT NULL,
                id bigint NOT NULL,
                afk text NOT NULL
            );
            """)
            await self.cur.execute("""
            CREATE TABLE IF NOT EXISTS prod.servers
            (
                id bigint NOT NULL,
                welcome text,
                goodbye text,
                logger bigint
            );
            """)
        except Exception as e:
            print(f"[{time.ctime()}] {e}")
        except KeyboardInterrupt:
            await self.pool.release(self.cur)
            await self.pool.close()
            print(f"[{time.ctime()}] Released cursor and closed pool")
        self.loadExt()
        print(f"[{time.ctime()}] Bot ready")


bot = Bot()
