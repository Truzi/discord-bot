import nextcord
import os
import sqlite3
from dotenv import load_dotenv
from nextcord.ext import commands


# open connection to db & create cursor
connection = sqlite3.connect('../db.sqlite3')
cursor = connection.cursor()

# loading env variables
load_dotenv()
token = os.getenv("DISCORD_TOKEN")
prefix = os.getenv("PREFIX")

# creating necessary tables
cursor.execute('''CREATE TABLE IF NOT EXISTS USERS(
  UserID INTEGER PRIMARY KEY AUTOINCREMENT,
  Username TEXT NOT NULL
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS QUOTES(
  QuoteID INTEGER PRIMARY KEY AUTOINCREMENT,
  UserID INTEGER, 
  Quote TEXT,
  FOREIGN KEY(UserID) REFERENCES Users(UserID)
)''')

# declaring intents
intents = nextcord.Intents.default()
intents.message_content = True
intents.emojis = True

# creating bot instance
bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.event
async def on_ready(bot=bot):
  print(f'Logged as {bot.user}')


# loading cogs
bot.load_extension('cogs.EmojiCog')
bot.load_extension('cogs.QuotesCog')

# starting bot
bot.run(token=token)