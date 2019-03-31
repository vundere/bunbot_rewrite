import logging
import discord
import os

from Assistants.Jason import Jason
from random import randint, choice, random
from discord.ext.commands import Bot
from utils.tools import find_word

bun_bot = Bot(command_prefix='!bb.')

# region settings
startup_modules = [

]
startup_modules = ['modules/{}'.format(module) for module in startup_modules]  # not very elegant, but user-friendly

Jason = Jason()
important_files = []  # placeholder, maybe store these externally?
for f in important_files:
    name = f.split('/')[-1].split('.')[0]  # maybe there's a better way of extracting the filename from a path?
    Jason.assign(name, f)

# maybe these should be moved out of this file to reduce clutter
cat_words = [
    'cat',
    'cats',
    'kitty',
    'kitties',
    'kitten',
    'kittens',
    'cato',
    'cattos'
]
cat_reacts = [
    'nyaaa~',
    ":3",
    "(ↀДↀ)",
    "(๑ↀᆺↀ๑)✧",
    "ლ(=ↀωↀ=)ლ",
    "～((Φ◇Φ)‡",
    "(=^-ω-^=)",
    "(^･ω･^=)~"
]
dog_words = [
    'dog',
    'dogs',
    'puppy',
    'puppies',
    'doggo',
    'doggos',
    'pupper',
    'puppers'
]
dog_reacts = [
    'woof',
    '(❍ᴥ❍ʋ)',
    '੯ੁૂ‧̀͡u',
    'ฅ^•ﻌ•^ฅ',
    '₍ᐢ•ﻌ•ᐢ₎*･ﾟ｡',
    '(υ◉ω◉υ)',
    '໒( ◉ ᴥ ◉ )७',
    '▐ ☯ ᴥ ☯ ▐'
]
# endregion


# region functions
def setup_logging():
    discord_logger = logging.getLogger('discord')
    discord_logger.setLevel(logging.CRITICAL)

    intlg = logging.getLogger('bun_bot')
    intlg.setLevel(logging.INFO)
    handler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='a')
    fmt = logging.Formatter('[%(asctime)s] :%(levelname)s: %(message)s', datefmt='%H:%M:%S')
    handler.setFormatter(fmt)
    intlg.addHandler(handler)
    return intlg


def end_logging(intlg):
    handlers = intlg.handlers[:]
    for hdlr in handlers:
        hdlr.close()
        intlg.removeHandler(hdlr)


def init_vars():
    #  TODO load vars(tokens, folder paths etc.)
    pass


async def react(ctx):
    message = ctx.message
    has_cat_word = find_word(message.content, cat_words)
    has_dog_word = find_word(message.content, dog_words)
    if has_cat_word and randint(0, 10) < 2 and not message.author == bun_bot.user:
        log.info('Cat react triggered in #{0.channel.name} ({0.server.name})'.format(message))
        await ctx.send(message.channel, choice(cat_reacts))
    if has_dog_word and randint(0, 10) < 2 and not message.author == bun_bot.user:
        log.info('Dog react triggered in #{0.channel.name} ({0.server.name})'.format(message))
        await ctx.send(message.channel, choice(dog_reacts))
# endregion


# region botevents
@bun_bot.event
async def on_ready():
    await bun_bot.change_presence(game=discord.Game(name='commands: !bb.help'))
    print('Logged in as')
    print(bun_bot.user.name)
    print(bun_bot.user.id)
    print('------')
# endregion


# region botcommands
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format.
    Shamelessly stolen from the discord.py example bot,
    both as a reference and replacement for the old roll command
    """
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:  # TODO figure out which exception this throws and narrow the clause?
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for _ in range(rolls))
    await ctx.send(result)
# endregion

if __name__ == '__main__':
    log = setup_logging()
    try:
        for ext in startup_modules:
            try:
                bun_bot.load_extension(ext)
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(ext, exc))

        with open('bunbot.pid', 'w') as f:
            f.write(str(os.getpid()))
        log.info('PID file written.')

        bun_bot.run(bun_bot.token)

        log.info('Bot stopping.')
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        log.info('Bot crashed with exception: \n{}'.format(exc))
    finally:
        log.info('Removing PID file.')
        os.remove('bunbot.pid')
        end_logging(log)
