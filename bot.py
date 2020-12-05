"""
Alpha Discord Bot

This bot helps manage all necessary administration and
automation for the Salty Bacon Gamers Discord server.

Author(s):
Pyro      - https://github.com/Pyroseza
"""


from aiohttp import ClientSession
from discord.ext import commands
from pathlib import Path
from utils.config import Config
from utils.context import AlphaCtx
import json
import logging
import logging.config
import os

class AlphaBot(commands.Bot):
    """
    The main bot class where are the magic happens
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = Config()

        self.log = kwargs.get("log")


    async def on_ready(self):
        self.log.info(f"{self.user} is in!")


    async def get_context(self, message, *, cls=AlphaCtx):
        return await super().get_context(message, cls=cls)

    def user_is_admin(self, user):
        user_roles = [role.id for role in user.roles]
        if any(role in self.config.get('admin_roles') for role in user_roles):
            return True
        return False

    def user_is_ignored(self, user):
        user_roles = [role.id for role in user.roles]
        if self.config.get('ignore_role') in user_roles:
            return True
        return False


    @property
    def module_list(self):
        m = list(Path("cogs").glob("*.py"))
        all_cogs = [f"cogs.{i.name}"[:-3] for i in m]
        return all_cogs


    async def load_modules(self):
        _output = []
        for cog in self.module_list:
            try:
                self.load_extension(cog)
                _output.append(f"[{cog}] loaded")
            except commands.ExtensionAlreadyLoaded:
                _output.append(f"[{cog}] already loaded")
            except commands.ExtensionNotLoaded:
                _output.append(f"[{cog}] not loaded")
                self.log.exception(f"Failed to load {cog}")
        return "\n".join(_output)


    async def start(self, *args, **kwargs):
        self.session = ClientSession()
        load_modules = await self.load_modules()
        self.log.info(f"Load modules result: \n{load_modules}")
        token = self.config.get("token")
        if not token:
            raise KeyError("Token not found in config!")
        # await super().start(*args, **kwargs)
        await super().start(token, *args, **kwargs)


    async def close(self):
        await self.session.close()
        await super().close()


def setup_logging(filename='logging.json', env_key='LOG_CFG'):
    """
    Setup logging configuration
    source: https://docs.python.org/3/library/logging.html
    """
    # path = default_path
    path = os.path.join(os.path.dirname(__file__), filename)
    # path = filename
    value = os.getenv(env_key, None)
    if value:
        path = value
    try:
        if os.path.exists(path):
            with open(path, 'rt') as f:
                config = json.load(f)
                logging.config.dictConfig(config)
        else:
            raise FileNotFoundError
    except Exception as e:
        print(str(e))
        print("Unable to load logging config, default to console only")
        logging.basicConfig(level=logging.INFO)


def main():
    setup_logging()
    log = logging.getLogger(__name__)
    # create the alphabot instance
    bot_prefix = Config().get("prefix", "alpha")+" "
    bot_Prefix = bot_prefix.capitalize()
    bot = AlphaBot(
        command_prefix=commands.when_mentioned_or(bot_prefix, bot_Prefix),
        case_insensitive=True,
        log=log
    )

    @bot.event
    async def on_ready():
        main_id = bot.config.get('main_guild')
        bot.main_guild = bot.get_guild(main_id) or bot.guilds[0]
        log.info('-'*30)
        log.info('Active in these guilds/servers:')
        for g in bot.guilds:
            log.info(g.name)
        log.info('-'*30)
        log.info(f'Main guild: {bot.main_guild.name}')
        log.info('-'*30)
        log.info('Alphabot started successfully')
        return True


    log.info('Alphabot ready')
    bot.run()
    log.info('Alphabot has terminated')

if __name__=="__main__":
    main()

