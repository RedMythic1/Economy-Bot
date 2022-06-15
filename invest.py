import discord
from discord.ext import commands
import os
import asyncio
from replit import db
import yfinance as yf
import tracemalloc

tracemalloc.start()

TOKEN = os.environ['DISCORD_TOKEN']
keys = db.keys()

bot = commands.Bot(command_prefix='.')

@bot.command()
async def invest(ctx):
		aapl = yf.Ticker("AAPL")
		msft = yf.Ticker("MSFT")
		nvda = yf.Ticker("NVDA")
		intl = yf.Ticker("INTL")
		tsla = yf.Ticker("TSLA")
		embed = discord.Embed(
        title="**INVESTMENT LIST**",
        description=
        f"Here is the list of all possible investments.\n **AAPL (Apple) - {aapl.info['regularMarketPrice']} USD**\n **MSFT(Microsoft) - {msft.info['regularMarketPrice']} USD**\n **NVDA(Nvidia Corporation)-{nvda.info['regularMarketPrice']} USD**\n **INTL(Intel corporation) - {intl.info['regularMarketPrice']}**\n **TSLA(Tesla motors) - {tsla.info['regularMarketPrice']}**\n",
        color=0xAA28FF)
		await ctx.send(embed=embed)
bot.run(TOKEN)