from nextcord.ext import commands
import sqlite3

connection = sqlite3.connect('../db.sqlite3')
cursor = connection.cursor()

class QuotesCog(commands.Cog):
  def __init__(self, bot):
      self.bot = bot

  @commands.command()
  async def addQuote(self, ctx: commands.Context, username, *, quote):
    if not ctx.author.guild_permissions.manage_guild:
      return await ctx.send("You don't have sufficient permissions!")
    
    else:
      sql = "SELECT * FROM USERS WHERE USERS.Username=?"
      params = (username,)
      users = cursor.execute(sql, params).fetchall()

      for user in users:
        UserID = user[0]

        sql = "INSERT INTO QUOTES (UserID, Quote) VALUES(?, ?)"
        params = (UserID, quote,)
        cursor.execute(sql, params)
        connection.commit()

        await ctx.send("Quote added!")


def setup(bot: commands.Bot):
  bot.add_cog(QuotesCog(bot))