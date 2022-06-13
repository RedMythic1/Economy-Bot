import discord
from discord.ext import commands
import os
from replit import db
import yfinance as yf

keys = db.keys()

TOKEN = os.environ['DISCORD_TOKEN']

bot=commands.Bot(command_prefix='.')

@bot.command()
async def invest(ctx):
	aapl = yf.Ticker("AAPL")
	msft = yf.Ticker("MSFT")
	nvda = yf.Ticker("NVDA")
	embed = discord.Embed(title="**INVESTMENT LIST**", description=f"Here is the list of all possible investments.\n **AAPL (Apple) - {aapl.info['regularMarketPrice']} USD**\n **MSFT(Microsoft) - {msft.info['regularMarketPrice']} USD**\n **NVDA(Nvidia Corporation)-{nvda.info['regularMarketPrice']} USD**", color=0xAA28FF)
	await ctx.send(embed = embed)
bot.run(TOKEN)