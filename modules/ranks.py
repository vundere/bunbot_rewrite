from Assistants.Squirrel import Squirrel
from discord.ext import commands


def check_for_table(server):
    """
    It's not possible to have table names as a parameter, but this should be safe.
    """
    with Squirrel('database') as db:
        db.modify("CREATE TABLE IF NOT EXISTS %s "
                  "(user_id text PRIMARY KEY, " %  # TODO actually design a db structure for this
                  db.sanitise(server.id))


class Ranks:
    def __init__(self, bot):
        self.bot = bot
