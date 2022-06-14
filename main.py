import discord
from discord.ext import commands
import os
from replit import db
import yfinance as yf
import tracemalloc

tracemalloc.start()

TOKEN = os.environ['DISCORD_TOKEN']
keys = db.keys()

bot = commands.Bot(command_prefix='.')


@bot.command()
async def start(ctx):
    embed = discord.Embed(
        title='**WELCOME**',
        description=
        'Welcome to Stonkbroker, the Discord game bot based off of the real life **stock market**. Experience ups :chart_with_upwards_trend:, downs :chart_with_downwards_trend:, and everything in between.',
        color=0xAA28FF)
    if ctx.author not in keys:
        db[f'{ctx.author}_money'] = 0
    else:
        print("hi")
    await ctx.send(embed=embed)


@bot.command()
async def commands(ctx):
    embed = discord.Embed(
        title='**COMMANDS LIST**',
        description=
        "Here is the complete list of Stonkbroker's current commands.\n**.start**\n```bash\nStarts a new profile in Stonkbroker.```\n **.commands**\n ```bash\n Opens up a list of all the commands in the game bot.```\n **.invest(***DOESN'T WORK***)**\n```bash\nShows the list of possible investments to invest in.```",
        color=0xAA28FF)
    await ctx.send(embed=embed)

@bot.command()
async def daily(ctx):	
		money = db[f'{ctx.author}_money']
		money += 500
		db[f'{ctx.author}_money'] = money
		db[f'{ctx.author}_daily'] = 'claimed'
		await ctx.send("Daily for today has been claimed")

@bot.command()
async def send(ctx, arg1, arg2):
		cash_app = int(arg2)
		cash_sent = db[f'{arg1}_money']
		new_cash = cash_sent + cash_app
		print(cash_sent)
		print(cash_app)
		db[f'{arg1}'] = new_cash
		money_deductable = db[f'{ctx.author}_money']
		new_money = money_deductable - cash_app
		if money_deductable < 0:
			cash_sent -= cash_app
			db[f'{arg1}_money'] = cash_sent
			await ctx.send('Insufficeint Funds**!!!**')
			db[f'{ctx.author}_money'] = (money_deductable + cash_app)
		db[f'{ctx.author}_money'] = new_money
		await ctx.send("Money transferred.")

@bot.command()
async def balance(ctx):
	big_boi_cash = db[f'{ctx.author}_money']
	embed = discord.Embed(
		title="**BALANCE**"
		description=f'You have **{big_boi_cash} USD**',
		color=0xAA28FF
	)
	await ctx.send(embed = embed)

bot.run(TOKEN)
