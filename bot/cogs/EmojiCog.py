import os
import nextcord
from nextcord.ext import commands
import aiohttp
from PIL import Image
from io import BytesIO

class EmojiCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.domains = ('7tv', 'betterttv', 'frankerfacez')

  @commands.command()
  async def addEmoji(self, ctx: commands.Context):
    filePath = './emote.png'
    message = ctx.message.content[len(self.bot.command_prefix) + len(ctx.command.name):].lstrip().split(' ')
    name = message[0]
    url = message[1]

    if any(domain in url for domain in self.domains):
      for domain in self.domains:
        if domain in url:
          await self.add(ctx=ctx, domain=domain, url=url, name=name)
    else:
      await ctx.send('Domain not found!')

    if os.path.exists(filePath):
      os.remove(filePath)

  async def add(self, ctx: commands.Context, domain, url, name):
    match domain:
      case '7tv':
        url = url.replace('7tv', 'cdn.7tv')
        url = url.replace('emotes', 'emote')
        url = url + '/4x.png'
        await self.emote(ctx, url, name)

      case 'betterttv':
        url = url.replace('www', 'cdn')
        url = url.replace('com', 'net')
        url = url.replace('emotes', 'emote')
        url = url + '/3x.png'
        await self.emote(ctx, url, name)
      
      case 'frankerfacez':
        url = url.replace('www', 'cdn')
        index = url.find('-')
        url = url[:index] + '/4'

        await self.emote(ctx, url, name)


  async def emote(self, ctx: commands.Context, url, name):
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(url) as response:
          if response.status == 200:
            filePath = './emote.png'
            image_data = await response.read()
            image_bytes = bytes(image_data)
            image = Image.open(BytesIO(image_bytes)).convert('RGB')
            image = image.resize((128, 128))
            image.save(filePath, 'PNG')
            with open(filePath, 'rb') as emojiFile:
                emoji = await ctx.guild.create_custom_emoji(image=emojiFile.read(), name=name)

            await ctx.send(f'Added {emoji}!')
          else:
            print(url)
            print(f'Admin log: adding emote: response status {response.status}')
            await ctx.send("Problem with retrieving URL content")


def setup(bot: commands.Bot):
    bot.add_cog(EmojiCog(bot))
