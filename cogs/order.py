import os, discord, time, async_cse, random
from discord.ext import commands
from difflib import SequenceMatcher
from discord.ext.commands.cooldowns import BucketType

from aiogifs.tenor import TenorClient, ContentFilter
from aiogifs.giphy import GiphyClient

class Order(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    bot.loop.create_task(self.__ainit__())
  
  async def __ainit__(self):
    await self.bot.wait_until_ready()
    tenor_key = os.environ["tenor_key"]
    giphy_key = os.environ["giphy_token"] 

    image_api_key = os.environ["image_api_key"]  
    image_engine_key = os.environ["google_image_key"] 

    #self.tenor_client = TenorClient (api_key=tenor_key, session = self.bot.session)
    #self.giphy_client = GiphyClient(api_key=giphy_key, session = self.bot.session)

    self.image_client=async_cse.Search(image_api_key,engine_id=image_engine_key, session = self.bot.session)

  @commands.cooldown(1,30,BucketType.user)
  @commands.group(name="order",invoke_without_command=True)
  async def order(self, ctx, *, args = None):
    if args is None:
      await ctx.send("You can't order nothing.")

    if args:
      time_before=time.perf_counter()  
      
      try:
        results = await self.image_client.search(args, safesearch=True, image_search=True)
        emoji_image = sorted(results, key=lambda x: SequenceMatcher(None, x.image_url,args).ratio())[-1]
      except async_cse.search.NoResults:
        return await ctx.send("No results found :(")

      time_after=time.perf_counter() 
      try:
        await ctx.message.delete()
      except discord.errors.Forbidden:
        pass
    
      embed = discord.Embed(title=f"Item: {args}", description=f"{ctx.author} ordered a {args}",color=random.randint(0, 16777215),timestamp=ctx.message.created_at)
      embed.set_author(name=f"order for {ctx.author}:",icon_url=(ctx.author.avatar_url))
      embed.add_field(name="Time Spent:",value=f"{int((time_after - time_before)*1000)}MS")
      embed.add_field(name="Powered by:",value="Google Images Api")
      embed.set_image(url=emoji_image.image_url)
      embed.set_footer(text = f"{ctx.author.id} \nCopyright: I don't know the copyright.")
      await ctx.send(content="Order has been logged for safety purposes(we want to make sure no unsafe search is sent)",embed=embed)
      await self.bot.get_channel(738912143679946783).send(embed=embed)

  @commands.cooldown(1,30,BucketType.user)
  @order.command(brief="a command to shuffle images from google images")
  async def shuffle(self,ctx,*,args=None):
    if args is None:
        await self.order(ctx,args="shuffle")
    if args:
      time_before=time.perf_counter()
      try:
        results = await self.image_client.search(args, safesearch=True, image_search=True)
      except async_cse.search.NoResults:
        return await ctx.send("No results found :(")


      emoji_image = random.choice(results)
      time_after=time.perf_counter() 
      try:
        await ctx.message.delete()
      except discord.errors.Forbidden:
        pass

      embed = discord.Embed(title=f"Item: {args}", description=f"{ctx.author} ordered a {args}",color=random.randint(0, 16777215),timestamp=ctx.message.created_at)
      embed.set_author(name=f"order for {ctx.author}:",icon_url=(ctx.author.avatar_url))
      embed.add_field(name="Time Spent:",value=f"{int((time_after - time_before)*1000)}MS")
      embed.add_field(name="Powered by:",value="Google Images Api")
      embed.set_image(url=emoji_image.image_url)
      embed.set_footer(text = f"{ctx.author.id} \nCopyright: I don't know the copyright.")
      await ctx.send(content="Order has been logged for safety purposes(we want to make sure no unsafe search is sent)",embed=embed)
      await self.bot.get_channel(738912143679946783).send(embed=embed)

  @commands.cooldown(1,30,BucketType.user)
  @commands.command(brief="a command to shuffle images from google images",aliases=["order-shuffle"])
  async def order_shuffle(self,ctx,*,args=None):
    if args is None:
      await ctx.send("You can't order nothing")
    if args:
      time_before=time.perf_counter()  
      try:
        results = await self.image_client.search(args, safesearch=True, image_search=True)
      except async_cse.search.NoResults:
        return await ctx.send("No results found :(")

      emoji_image = random.choice(results)

      time_after=time.perf_counter() 
      try:
        await ctx.message.delete()
      except discord.errors.Forbidden:
        pass

      embed = discord.Embed(title=f"Item: {args}", description=f"{ctx.author} ordered a {args}",color=random.randint(0, 16777215),timestamp=ctx.message.created_at)
      embed.set_author(name=f"order for {ctx.author}:",icon_url=(ctx.author.avatar_url))
      embed.add_field(name="Time Spent:",value=f"{int((time_after - time_before)*1000)}MS")
      embed.add_field(name="Powered by:",value="Google Images Api")
      embed.set_image(url=emoji_image.image_url)
      embed.set_footer(text = f"{ctx.author.id} \nCopyright: I don't know the copyright.")
      await ctx.send(content="Order has been logged for safety purposes(we want to make sure no unsafe search is sent)",embed=embed)
      await self.bot.get_channel(738912143679946783).send(embed=embed)

  @commands.cooldown(1,30,BucketType.user)
  @commands.group(name="tenor",invoke_without_command=True)
  async def tenor(self, ctx, *, args = None):
    if args:

      safesearch_type = ContentFilter.high()
      #results = await self.tenor_client.search(args, content_filter = safesearch_type, limit = 10)

      #print(results)

    if args is None:
      await ctx.send("You can't search for nothing")

  @tenor.command(help="work in progress",name="shuffle")
  async def tenor_random(self,ctx,*,args=None):
    if args:
      await ctx.send("WIP")
    if args is None:
      await ctx.send("That doesn't have any value.")
      await ctx.send("tenor shuffle")

  @commands.command(help="work in progress",aliases=["tenor-shuffle"])
  async def tenor_shuffle(self,ctx,*,args):
    if args:
      await ctx.send("WIP")
    if args is None:
      await ctx.send("That doesn't have any value.")
      await ctx.send("tenor shuffle")
  
  @commands.group(name="giphy",invoke_without_command=True)
  async def giphy(self,ctx,*,args=None):
    if args:
      await ctx.send("WIP")
    if args is None:
      await ctx.send("That doesn't have any value.")
      await ctx.send("tenor")

  @giphy.command(help="work in progress",name="shuffle")
  async def giphy_random(self,ctx,*,args=None):
    if args:
      await ctx.send("WIP")
    if args is None:
      await ctx.send("That doesn't have any value.")
      await ctx.send("giphy shuffle")
  
  @commands.command(help="work in progress",aliases=["giphy-shuffle"])
  async def giphy_shuffle(self,ctx,*,args):
    if args:
      await ctx.send("WIP")
    if args is None:
        await ctx.send("That doesn't have any value.")
        await ctx.send("giphy shuffle")

  async def cog_command_error(self,ctx,error):
    if ctx.command and ctx.command.has_error_handler():
      pass
    else:
      await ctx.send(error)

def setup(bot):
  bot.add_cog(Order(bot))