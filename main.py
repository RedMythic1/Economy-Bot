import discord
from discord.ext import commands
import os
from replit import db
import tracemalloc
import yfinance as yf
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
        color=0xAA28FF
		)
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
        color=0xAA28FF
		)
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
    db[f'{arg1}_money'] = new_cash
    money_deductable = db[f'{ctx.author}_money']
    new_money = money_deductable - cash_app
    if money_deductable < 0:
        cash_sent -= cash_app
        db[f'{arg1}_money'] = cash_sent
        await ctx.send('Insufficeint Funds**!!!**')
        db[f'{ctx.author}_money'] = (money_deductable + cash_app)
    db[f'{ctx.author}_money'] = new_money
    embed = discord.Embed(
        title="***MONEY SENT***",
        description=f"**You, {ctx.author}, sent {cash_app} USD to {arg1}!**",
        color=0xAA28FF)
    await ctx.send(embed=embed)


@bot.command()
async def balance(ctx):
		global contents
		big_boi_cash = db[f'{ctx.author}_money']
		embed = discord.Embed(
			title="**BALANCE**",
      description=f'You have **${big_boi_cash} USD**',
      color=0xAA28FF
		)
		await ctx.send(embed=embed)

@bot.command()
async def payshop(ctx, arg1, arg2):
	f=open("shop.txt","r+")
	contents = f.read()
	if arg1 not in contents:
		embed = discord.Embed(
			title='**OOPSIES**',
			description='That shop does not exist',
			color=0xAA28FF
		)
	if arg1 in contents:
		shoop=db[f'{arg1}']
		shooplen = len(shoop)
		intarg2 = int(arg2)
		paydue = intarg2/shooplen
		while shooplen>=0:
			shooplen-=1
			payto = shoop[shooplen]
			cashmoney = db[f'{payto}_money']
			cashmoney+=paydue
			print(cashmoney)
			db[f'{payto}_money'] = cashmoney
		if shooplen<1:
				cashboi = db[f'{ctx.author}_money']
				cashboi -= intarg2
				print(cashboi)
				print(intarg2)
				db[f'{ctx.author}_money'] = cashboi
				embed = discord.Embed(
					title='**PAID**',
					description=f'You paid the owners of {arg1} {arg2} USD for their services!',
					color=0xAA28FF
				)
				await ctx.send(embed = embed)
				
@bot.command()
async def addshop(ctx, arg1, arg2):
	db[f'{arg1}'] = []
	shoppe = db[f'{arg1}']
	shoppe.append(f'{arg2}')
	f1=open("shop.txt","w")
	f1.write(f"{arg1}")
	embed = discord.Embed(
		title='**SHOP CREATED**',
		description=f'You are the *owner* of **{arg1}**!',
		color=0xAA28FF
	)
	await ctx.send(embed = embed)
@bot.command()
async def invest(ctx):
		aapl = yf.Ticker("AAPL")
		msft = yf.Ticker("MSFT")
		nvda = yf.Ticker("NVDA")
		intc = yf.Ticker("INTC")
		tsla = yf.Ticker("TSLA")
		rivn = yf.Ticker("RIVN")
		embed = discord.Embed(
        title="**INVESTMENT LIST**",
        description=
        f"Here is the list of all possible investments.\n **AAPL (Apple) - {aapl.info['regularMarketPrice']} USD**\n **MSFT(Microsoft) - {msft.info['regularMarketPrice']} USD**\n **NVDA(Nvidia Corporation)-{nvda.info['regularMarketPrice']} USD**\n **INTL(Intel corporation) - {intc.info['regularMarketPrice']}**\n **TSLA(Tesla motors) - {tsla.info['regularMarketPrice']}**\n",
        color=0xAA28FF)
		await ctx.send(embed=embed)
bot.run(TOKEN)
	
bot.run(TOKEN)
