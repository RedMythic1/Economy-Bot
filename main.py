import discord
from discord.ext import commands
import os
from replit import db
import finnhub
import asyncio
APIKEY = os.environ['API_KEY']
finnhub_client = finnhub.Client(api_key=APIKEY)

TOKEN = os.environ['DISCORD_TOKEN']
keys = db.keys()

bot = commands.Bot(command_prefix='.', activity=discord.Activity(type=discord.ActivityType.watching, name='.start'))

@bot.event
async def on_ready():
	print('logged in')


#starts a user's profile and/or restarts a user's profile-$0 USD.
@bot.command()
async def start(ctx):
		embed = discord.Embed(
        title='**WELCOME**',
        description=
        'Welcome to Stonkbroker, the Discord game bot based off of the real life **stock market**. Experience ups :chart_with_upwards_trend:, downs :chart_with_downwards_trend:, and everything in between.',
				color=0xAA28FF)
		if f'{ctx.author}_money' not in keys:
				db[f'{ctx.author}_money'] = 0
				db[f'{ctx.author}_bank'] = 0
		print("hi")
		await ctx.reply(embed=embed)




#shows the user a list of commands
@bot.command()
async def commands(ctx):
    embed = discord.Embed(
        title='**COMMANDS LIST**',
        description=
        "Here is the complete list of Stonkbroker's current commands.\n **.start** - Starts a new profile in Stonkbroker.\n **.commands** - Opens up a list of all the commands in the game bot.\n **.invest**(***TAKES A MINUTE***) - Shows the list of possible investments to invest in.",
        color=0xAA28FF)
    await ctx.reply(embed=embed)




#allows the user to claim their daily cash amount
@bot.command()
async def daily(ctx):
		money = db[f'{ctx.author.id}_money']
		money += 100
		db[f'{ctx.author}_money'] = money
		db[f'{ctx.author}_daily'] = 'claimed'
		await ctx.reply("Daily for today has been claimed")
#allows the user to send another user a certain amount of cash.
@bot.command()
async def pay(ctx, member: discord.Member, arg2):
		cash_app = int(arg2)
		if cash_app>0:
			cash_sent = db[f'{member.id}_money']
			new_cash = cash_sent + cash_app
			print(cash_sent)
			print(cash_app)
			db[f'{member.id}_money'] = new_cash
			money_deductable = db[f'{ctx.author}_money']
			new_money = money_deductable - cash_app
			if money_deductable < 0:
					cash_sent -= cash_app
					db[f'{member.id}_money'] = cash_sent
					await ctx.reply('Insufficeint Funds**!!!**')
					db[f'{ctx.author}_money'] = (money_deductable + cash_app)
			db[f'{ctx.author.id}_money'] = new_money
			embed = discord.Embed(
					title="***MONEY SENT***",
					description=f"**You, {ctx.author}, sent {cash_app} USD to {member.mention}!**",
					color=0xAA28FF)
			await ctx.reply(embed=embed)
		if cash_app<=0:
			await ctx.reply("Insufficient Funds!!!!")




#display's the user's balance.
@bot.command()
async def wallet(ctx):
    global contents
    big_boi_cash = db[f'{ctx.author}_money']
    embed = discord.Embed(title="**WALLET**",
                          description=f'You have **${big_boi_cash} USD**',
                          color=0xAA28FF)
    await ctx.reply(embed=embed)




#allows the user to pay someone else's shop.
@bot.command()
async def payshop(ctx, arg1, arg2):
			keys = db.keys()
			if arg1 not in keys:
				embed = discord.Embed(
					title='**OOPSIES**',
          description='That shop does not exist',
        	color=0xAA28FF
				)
			if arg1 in keys:
				shoop = db[f'{arg1}']
				shooplen = len(shoop)
				intarg2 = int(arg2)
				paydue = intarg2 / shooplen
				print(paydue)
				print(intarg2)
				print(shooplen)
				print(shoop)
				while shooplen >= 0:
						shooplen -= 1
						payto = shoop[shooplen]
						cashmoney = db[f'{payto}_money']
						cashmoney += paydue
						print(cashmoney)
						db[f'{payto}_money'] = cashmoney
				if shooplen < 1:
						cashboi = db[f'{ctx.author}_money']
						cashboi -= intarg2
						print(cashboi)
						print(intarg2)
						if cashboi<0:
							cashboi+= intarg2
							db[f'{ctx.author}_money'] = cashboi
							embed = discord.Embed(
                title='**INSUFFIECENT**',
                description=f"You don't have enough money to do that!",
                color=0xAA28FF
							)
							await ctx.reply(embed=embed)
						if cashboi>=0:
							db[f'{ctx.author}_money'] = cashboi
								
							embed = discord.Embed(
	                title='**PAID**',
	                description=
	                f'You paid the owners of {arg1} {arg2} USD for their services!',
	                color=0xAA28FF)
							await ctx.reply(embed=embed)




#allows the user to add a shop.
@bot.command()
async def addshop(ctx, arg1, arg2):
		keys = db.keys()
		if arg1 not in keys:
			db[f'{arg1}'] = []
		shoppe = db[f'{arg1}']
		shoppe.append(f'{arg2}')
		if 'shop' not in keys:
			db['shop'] = []
		sop = db[f'shop']
		print(sop)
		print(shoppe)
		if arg1 not in sop:
			sop.append(f'{arg1}')
		embed = discord.Embed(title='**SHOP CREATED**',
                          description=f'You are the *owner* of **{arg1}**!',
                          color=0xAA28FF)
		await ctx.reply(embed=embed)

#allows the user to give another user some items.
@bot.command()
async def give(ctx, arg1, arg2):
	db[f'{arg1}_items'] = []
	items = db[f'{arg1}_items']
	items.append(f'{arg2}')
	embed = discord.Embed(
		title=f'**GAVE ITEMS TO {arg1}**',
		description=f'You gave {arg1} {arg2}!',
		color=0xAA28FF
	)
	await ctx.reply(embed = embed)

#shows the user's items.
@bot.command()
async def items(ctx):
	list = db[f'{ctx.author}_items']
	listlen = len(list)
	embed = discord.Embed(
		title='ITEMS THAT YOU OWN',
		description=db[f'{ctx.author}_items'],
		color=0xAA28FF
	)
	await ctx.reply(embed = embed)

#gives the user a list of jobs they can hold.
@bot.command()
async def jobs(ctx):
    embed=discord.Embed(
			title="**JOBS**",
			description= "Below is the list of jobs that you can apply for.\n" "**Mathematician**-Solve math problems to earn $1,000 USD a day.(.work math)\n" "**Hitman**-Kill people and risk a moderately high chance of being caught, but for 2,000 dollars a kill. (.work hitman)\n **Baker**-Bake breads and other yummy goods to earn a 850 dollars a day.(.work baker) \n **Police**-Work for the government catching domestic criminals and slamming them in jail for 1,500 dollars a day (.work police). \n **Politician**-Compete against other politicians to gain control of the government.(.work politician) \n **President**-Lead the country and earn a whopping 5,000 a day. (.work president)", 
			color=0xAA28FF
		)
    await ctx.reply(embed = embed)
@bot.command()
async def invest(ctx):
		aapl = finnhub_client.quote('AAPL')
		msft = finnhub_client.quote('MSFT')
		nvda = finnhub_client.quote('NVDA')
		intc = finnhub_client.quote("INTC")
		tsla = finnhub_client.quote("TSLA")
		embed = discord.Embed(
        title="**INVESTMENT LIST**",
        description=
        f"Here is the list of all possible investments.\n **AAPL (Apple) - {aapl['o']} USD (.investin aapl)**\n **MSFT(Microsoft) - {msft['o']} USD (.investin msft)**\n **NVDA(Nvidia Corporation)-{nvda['o']} USD (.investin nvda)**\n **INTC(Intel corporation) - {intc['o']} USD (.investin intc)**\n **TSLA(Tesla motors) - {tsla['o']} USD  (.investin tsla)**\n",
        color=0xAA28FF)
		await ctx.reply(embed=embed)

@bot.command()
async def investin(ctx, arg1, arg2):
		if f'{ctx.author}_stonks' not in keys:
			db[f'{ctx.author}_stonks'] = {}
		player_cash = db[f'{ctx.author}_money']
		stock_list = db[f'{ctx.author}_stonks']
		stock = finnhub_client.quote(f'{arg1.upper()}')
		stock_price = int(stock['o'])
		shares_count = int(arg2)
		price = shares_count*stock_price
		player_cash -= price
		if player_cash<0:
			player_cash+=price
			db[f'{ctx.author}_money'] = player_cash
			await ctx.send("You don't have enough money!")
		if player_cash>=0:
			db[f'{ctx.author}_money'] = player_cash
			while shares_count>0:
				stock_list[f'{arg1.upper()}'] = stock_price
				shares_count -= 1
			print(stock)
			print(stock_price)
			print(stock_list)
			print(player_cash)
			print(shares_count)
			print(price)
			await ctx.send("Stocks purchased!")


@bot.command()
async def investments(ctx):
	stock_list = db[f'{ctx.author}_stonks']
	await ctx.send(f'You currently own {stock_list}.')




@bot.command()
async def deposit(ctx, arg1):
	bank = db[f'{ctx.author}_bank']
	intarg1 = int(arg1)
	bank+=intarg1
	db[f'{ctx.author}_bank'] = bank
	dudescash = db[f'{ctx.author}_money']
	dudescash -= intarg1
	if dudescash<0:
		bank = db[f'{ctx.author}_bank']
		bank -= intarg1
		db[f'{ctx.author}_bank'] = bank
		embed = discord.Embed(
			title="**INSUFFICIENT FUNDS**",
			description="You don't have enough to do that.",
			color=0xAA28FF
		)
		await ctx.reply(embed = embed)
	else:
		db[f'{ctx.author}_money'] = dudescash
		embed = discord.Embed(
			title="**MONEY IN BANK**",
			description=f"You deposited {arg1} USD.",
			color=0xAA28FF
		)
		await ctx.reply(embed=embed)

#allows the user to 
@bot.command()
async def bank(ctx):
	cashmoney  = str(db[f'{ctx.author}_bank'])
	embed = discord.Embed(
		title="**BANK**",
		description=f'You have ' + cashmoney + ' USD in the bank!',
		color=0xAA28FF
	)
	await ctx.reply(embed=embed)

#allows user to withdraw money from above bank
@bot.command()
async def withdraw(ctx, arg1):
	bank = db[f'{ctx.author}_bank']
	intarg1 = int(arg1)
	bank-=intarg1
	db[f'{ctx.author}_bank'] = bank
	dudescash = db[f'{ctx.author}_money']
	if bank<0:
		bank = db[f'{ctx.author}_bank']
		bank += intarg1
		db[f'{ctx.author}_bank'] = bank
		embed = discord.Embed(
			title="**INSUFFICIENT FUNDS**",
			description="You don't have enough to do that.",
			color=0xAA28FF
		)
		await ctx.reply(embed = embed)
	else:
		dudescash += intarg1
		db[f'{ctx.author}_money'] = dudescash
		embed = discord.Embed(
			title="**MONEY IN WALLET**",
			description=f"You withdrew {arg1} USD.",
			color=0xAA28FF
		)
		await ctx.reply(embed=embed) 
bot.run(TOKEN)