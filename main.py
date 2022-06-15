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

bot = commands.Bot(command_prefix='.', activity=discord.Activity(type=discord.ActivityType.watching, name='for .commands', help_command=False))

@bot.event
async def on_ready():
	print('Successfully logged into Discord.')


#starts a user's profile and/or restarts a user's profile-$0 USD.
@bot.command()
async def start(ctx):
		db[f'@{ctx.author.id}_money'] = 0
		db[f'@{ctx.author.id}_bank'] = 0
		embed = discord.Embed(
        title='**WELCOME**',
        description=
        'Welcome to Stonkbroker, the Discord game bot based off of the real life **stock market**. Experience ups :chart_with_upwards_trend:, downs :chart_with_downwards_trend:, financial problems :sob:, and economic success :money_mouth: :moneybag:!',
				color=0xAA28FF
)
		await ctx.reply(embed=embed)




#shows the user a list of commands
@bot.command()
async def commands(ctx):
    embed = discord.Embed(
        title='**COMMANDS LIST**',
        description=
        "Here is the complete list of Stonkbroker's current commands (in alphabetical order).\n **.addshop <shop name> ** - With the required arguments, this command allows you to open up your shop.\n **.bank** - This command allows you to see how much money you have deposited in your own personal bank!\n **.commands** - Opens up a list of all the commands in the game bot.\n **.daily** - This command allows you to claim your daily cash amount that gets directly placed in your own personal wallet!\n **.deposit <cash amount>** - Deposits the money from your wallet into your safe bank!\n **.give <user#tag> <item>** - Allows you to give another user an item!\n  **.invest** - Shows the list of possible investments to invest in.\n **.investin <company(via .invest)> <number of shares>** - This allows you to buy shares and own a part of the company!\n **.investments** - Shows you the shares you own in all available company stock. \n **.items** - Displays the items you have that were given to you by another user.\n **.jobs** - Shows the list of available jobs.\n **.pay <@mention user> <amount>** - Allows you to pay another user. \n **.payshop <shop name> <amount>** -  Allows you to pay a shop's owners a certain amount. This amount is then divided among the number of owners.\n **.start** - Starts a new profile in Stonkbroker.\n **.wallet** - Displays the amount of cash in your wallet.\n **.withdraw** - Allows you to withdraw money from your bank and into your wallet to spend or pay.",
        color=0xAA28FF)
    await ctx.reply(embed=embed)




#allows the user to claim their daily cash amount
@bot.command()
async def daily(ctx):
		money = db[f'@{ctx.author.id}_money']
		money += 100
		db[f'@{ctx.author.id}_money'] = money
		db[f'@{ctx.author.id}_daily'] = 'claimed'
		embed = discord.Embed(title="**DAILY CLAIMED**", description = "You have successfully claimed today's daily. :city_sunset:", color =0xAA28FF)
		await ctx.reply(embed=embed)
#allows the user to send another user a certain amount of cash.
@bot.command()
async def pay(ctx, member: discord.Member, arg2):
		cash_app = int(arg2)
		if cash_app>0:
			cash_sent = db[f'@{member.id}_money']
			print(member.id)
			new_cash = cash_sent + cash_app
			print(cash_sent)
			print(cash_app)
			db[f'{member.id}_money'] = new_cash
			money_deductable = db[f'@{ctx.author.id}_money']
			new_money = money_deductable - cash_app
			if money_deductable < 0:
					cash_sent -= cash_app
					db[f'@{member.id}_money'] = cash_sent
					db[f'@{ctx.author.id}_money'] = (money_deductable + cash_app)
					embed = discord.Embed(title="**INSUFFICIENT FUNDS**", description = "You don't have enough money to do this! :no_entry_sign: :dollar:", color=0xAA28FF)
					await ctx.reply(embed=embed)
			elif money_deductable >= 0:
				db[f'@{ctx.author.id}_money'] = new_money
				embed = discord.Embed(
					title="***MONEY SENT***",
					description=f"**You, {ctx.author}, sent {cash_app} USD to {member.mention}!**",
					color=0xAA28FF)
				await ctx.reply(embed=embed)
		if cash_app<=0:
			embed = discord.Embed(title="**INSUFFICIENT FUNDS**", description="You cannot give negative money or 0 money! :no_entry_sign: :dollar:", color=0xAA28FF)
			await ctx.reply(embed=embed)




#display's the user's balance.
@bot.command()
async def wallet(ctx):
    global contents
    big_boi_cash = db[f'@{ctx.author.id}_money']
    embed = discord.Embed(title="**WALLET**",
                          description=f'You have **${big_boi_cash} USD** :dollar: in your wallet!',
                          color=0xAA28FF)
    await ctx.reply(embed=embed)




#allows the user to pay someone else's shop.
@bot.command()
async def payshop(ctx, arg1, arg2):
			keys = db.keys()
			if arg1 not in keys:
				embed = discord.Embed(
					title='**OOPSIES**',
          description='That shop does not exist :no_entry_sign:',
        	color=0xAA28FF
				)
				await ctx.reply(embed=embed)
			if arg1 in keys:
				shoop = db[f'{arg1}']
				shooplen = len(shoop)
				intarg2 = int(arg2)
				paydue = intarg2 / shooplen
				print(paydue)
				print(intarg2)
				print(shooplen)
				print(shoop)
				while shooplen > 0:
						payto = shoop[shooplen-1]
						cashmoney = db[f'{payto}_money']
						cashmoney += paydue
						print(cashmoney)
						db[f'{payto}_money'] = cashmoney
						shooplen -= 1
				if shooplen < 1:
						cashboi = db[f'@{ctx.author.id}_money']
						cashboi -= intarg2
						print(cashboi)
						print(intarg2)
						if cashboi<0:
							cashboi+= intarg2
							db[f'@{ctx.author.id}_money'] = cashboi
							embed = discord.Embed(
                title='**INSUFFIECENT**',
                description=f"You don't have enough money to do that!",
                color=0xAA28FF
							)
							await ctx.reply(embed=embed)
						if cashboi>=0:
							db[f'@{ctx.author.id}_money'] = cashboi
								
							embed = discord.Embed(
	                title='**PAID**',
	                description=
	                f'You paid the owners of {arg1} **${arg2} USD** for their services!',
	                color=0xAA28FF)
							await ctx.reply(embed=embed)




#allows the user to add a shop.
@bot.command()
async def addshop(ctx, arg1):
		keys = db.keys()
		if arg1 not in keys:
			db[f'{arg1}'] = []
		shoppe = db[f'{arg1}']
		shoppe.append(f'@{ctx.author.id}')
		if 'shop' not in keys:
			db['shop'] = []
		sop = db[f'shop']
		print(sop)
		print(shoppe)
		if arg1 not in sop:
			sop.append(f'{arg1}')
		embed = discord.Embed(title='**SHOP CREATED**',
                          description=f'You are the *owner* of **{arg1}** :shopping_cart:!',
                          color=0xAA28FF)
		await ctx.reply(embed=embed)

#allows the user to give another user some items.
@bot.command()
async def give(ctx, member: discord.Member, arg2):
	keys = db.keys()
	if 	f'@{member.id}_items' not in keys:
			db[f'@{member.id}_items'] = []
	items = db[f'@{member.id}_items']
	items.append(f'{arg2}')
	embed = discord.Embed(
		title=f'**GAVE ITEMS TO {member}**',
		description=f'You gave {member} {arg2} !',
		color=0xAA28FF
	)
	await ctx.reply(embed = embed)

#shows the user's items.
@bot.command()
async def items(ctx):
	embed = discord.Embed(
		title='ITEMS THAT YOU OWN',
		description=db[f'@{ctx.author.id}_items'],
		color=0xAA28FF
	)
	await ctx.reply(embed = embed)

#gives the user a list of jobs they can hold.
@bot.command()
async def jobs(ctx):
    embed=discord.Embed(
			title="**JOBS**",
			description= "Below is the list of jobs that you can try to apply for. \n **Artist** - Create works of art to earn **$100 USD a day.**\n **Baker** - Create yummy pastries and breads to earn up to **$150 USD a day.**\n **Banker** - Keep a list of people's transactions to earn a whopping **$300 USD a day.**\n **Boba Seller** - Sell boba to earn **$50 USD a day.**\n **Book seller** - Sell books to earn **$60 USD a day.**\n **CIA Operative** - Work for the government abroad to catch international criminals to earn **$1,000 USD a day.**\n **Defense Minister** - Work for the government defending your country to earn **$1,000 USD a day.**\n **Gamer** - Be a professional gamer and play video games to earn **$500 USD a day.**\n **Governor** - Work for your local state and govern your states people to earn **$850 USD a day.**\n **Math Tutor** - Teach people math to earn **$400 USD a day.**\n **President** - The highest possible job, lead your country and earn **$3,000 USD a day.**\n **Steak Seller** - Sell steak at your steak restaurant to earn", 
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
		if f'@{ctx.author.id}_stonks' not in keys:
			db[f'@{ctx.author.id}_stonks'] = {}
		if f'{arg1}_{ctx.author.id}' not in keys:
			db[f'{arg1}_{ctx.author.id}'] = 0
		player_cash = db[f'@{ctx.author.id}_money']
		stock_list = db[f'@{ctx.author.id}_stonks']
		stock = finnhub_client.quote(f'{arg1.upper()}')
		stock_price = int(stock['o'])
		shares_count = int(arg2)
		price = shares_count*stock_price
		player_cash -= price
		if player_cash<0 or player_cash<stock_price:
			player_cash+=price
			db[f'@{ctx.author.id}_money'] = player_cash
			embed = discord.Embed(title="**INSUFFICIENT FUNDS**", description = f"You don't have enough money to do this!", color = 0xAA28FF)
			await ctx.reply(embed=embed)
		elif player_cash>=0:
			db[f'@{ctx.author.id}_money'] = player_cash
			stock_list[arg1.upper()] = stock_price
			current_owned_stocks = db[f'{arg1}_{ctx.author.id}'] 
			current_owned_stocks+=shares_count
			db[f'{arg1}_{ctx.author.id}'] = current_owned_stocks
			embed = discord.Embed(title="**STOCKS PURCHASED!**", description= f"The stocks you requested were successfully purchased.", color=0xAA28FF)
			await ctx.reply(embed=embed)


@bot.command()
async def investments(ctx):
	stock_list = db[f'@{ctx.author.id}_stonks']
	dict_len = len(stock_list.keys())
	while dict_len>0:
		current_stock = stock_list[dict_len-1]
		current_stock_shares = db[f'{current_stock}_{ctx.author.id}']
		await ctx.reply(f'You currently own {current_stock_shares} shares of {current_stock}.')
		dict_len-=1




@bot.command()
async def deposit(ctx, arg1):
	bank = db[f'@{ctx.author.id}_bank']
	intarg1 = int(arg1)
	bank+=intarg1
	db[f'@{ctx.author.id}_bank'] = bank
	dudescash = db[f'@{ctx.author.id}_money']
	dudescash -= intarg1
	if dudescash<0:
		bank = db[f'@{ctx.author.id}_bank']
		bank -= intarg1
		db[f'@{ctx.author.id}_bank'] = bank
		embed = discord.Embed(
			title="**INSUFFICIENT FUNDS**",
			description="You don't have enough to do that. :no_entry_sign: :dollar:",
			color=0xAA28FF
		)
		await ctx.reply(embed = embed)
	else:
		db[f'@{ctx.author.id}_money'] = dudescash
		embed = discord.Embed(
			title="**MONEY IN BANK**",
			description=f"You deposited **${arg1} USD.** :dollar:",
			color=0xAA28FF
		)
		await ctx.reply(embed=embed)

#allows the user to 
@bot.command()
async def bank(ctx):
	cashmoney  = str(db[f'@{ctx.author.id}_bank'])
	embed = discord.Embed(
		title="**BANK**",
		description=f'You have **$' + cashmoney + ' USD** :dollar: in the bank :bank:!',
		color=0xAA28FF
	)
	await ctx.reply(embed=embed)

#allows user to withdraw money from above bank
@bot.command()
async def withdraw(ctx, arg1):
	bank = db[f'@{ctx.author.id}_bank']
	intarg1 = int(arg1)
	bank-=intarg1
	db[f'@{ctx.author.id}_bank'] = bank
	dudescash = db[f'@{ctx.author.id}_money']
	if bank<0:
		bank = db[f'{ctx.author.id}_bank']
		bank += intarg1
		db[f'@{ctx.author.id}_bank'] = bank
		embed = discord.Embed(
			title="**INSUFFICIENT FUNDS**",
			description="You don't have enough to do that. :no_entry_sign: :dollar:",
			color=0xAA28FF
		)
		await ctx.reply(embed = embed)
	else:
		dudescash += intarg1
		db[f'@{ctx.author.id}_money'] = dudescash
		embed = discord.Embed(
			title="**MONEY IN WALLET**",
			description=f"You withdrew **${arg1} USD.** :dollar:",
			color=0xAA28FF
		)
		await ctx.reply(embed=embed) 
bot.run(TOKEN)