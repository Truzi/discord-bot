import nextcord
import os
import sqlite3
from dotenv import load_dotenv
from nextcord.ext import commands
from cogs.EmojiCog import EmojiCog

# open connection to db & create cursor
connection = sqlite3.connect('db.sqlite3')
cursor = connection.cursor()

# loading env variables
load_dotenv()
token = os.getenv("DISCORD_TOKEN")
prefix = os.getenv("PREFIX")

# declaring intents
intents = nextcord.Intents.default()
intents.message_content = True
intents.emojis = True

# creating bot instance
bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.event
async def on_ready(bot=bot):
  print(f'Logged as {bot.user}')

bot.load_extension('cogs.EmojiCog')

# starting bot
bot.run(token=token)