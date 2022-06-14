import discord
import threading
from discord.ext import commands
import os
from replit import db
import yfinance as yf

keys = db.keys()

TOKEN = os.environ['DISCORD_TOKEN']

bot=commands.Bot(command_prefix='.')

@bot.command()
async def start(ctx):
	embed = discord.Embed(title='**WELCOME**', description='Welcome to Stonkbroker, the Discord game bot based off of the real life *stock market*. Experience ups :chart_with_upwards_trend:, downs :chart_with_downwards_trend:, and everything in between.', color=0xAA28FF)
	if ctx.author not in keys:
		db[ctx.author] = 'active'
		db[f'{ctx.author}_money'] = 0
	else:
		print("hi")
	await ctx.send(embed=embed)

@bot.command()
async def commands(ctx):
	embed = discord.Embed(title = '**COMMANDS LIST**', description= "Here is the complete list of Stonkbroker's current commands.\n**.start**\n```bash\nStarts a new profile in Stonkbroker.```\n **.commands**\n ```bash\n Opens up a list of all the commands in the game bot.```\n **.invest**\n```bash\nShows the list of possible investments to invest in.```", color=0xAA28FF)
	await ctx.send(embed = embed)
@bot.command() 
async def invest(ctx):
	aapl = yf.Ticker("AAPL")
	msft = yf.Ticker("MSFT")
	nvda = yf.Ticker("NVDA")
	embed = discord.Embed(title="**INVESTMENT LIST**", description=f"Here is the list of all possible investments.\n **AAPL (Apple) - {aapl.info['regularMarketPrice']} USD**\n **MSFT(Microsoft) - {msft.info['regularMarketPrice']} USD**\n **NVDA(Nvidia Corporation)-{nvda.info['regularMarketPrice']} USD**", color=0xAA28FF)
	await ctx.send(embed = embed)											 
bot.run(TOKEN)
