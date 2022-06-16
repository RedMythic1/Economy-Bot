import discord
from discord.ext import commands
import os
from replit import db
import finnhub
import time
import requests
from ratelimit import limits, RateLimitException
from backoff import on_exception, expo

TEN = 600

@on_exception(expo, RateLimitException, max_tries=8)
@limits(calls=10000, period=TEN)
def call_api(url):
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception('API response: {}'.format(response.status_code))
    return response

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
        'Welcome to Stonkbroker, the Discord game bot based off of the real life **stock market**. Experience ups :chart_with_upwards_trend:, downs :chart_with_downwards_trend:, financial issues :sob:, and economic success :money_mouth: :moneybag:!',
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
		keys = db.keys()
		if f'{ctx.author.id}_daily_cooldown' not in keys:
					db[f'{ctx.author.id}_daily_cooldown'] = 0
		player_time_daily = db[f'{ctx.author.id}_daily_cooldown']
		if time.time() - player_time_daily > 86400:
			money = db[f'@{ctx.author.id}_money']
			money += 100
			db[f'@{ctx.author.id}_money'] = money
			db[f'@{ctx.author.id}_daily'] = 'claimed'
			db[f'{ctx.author.id}_daily_cooldown'] = time.time()
			embed = discord.Embed(title="**DAILY CLAIMED**", description = "You have successfully claimed today's daily. :city_sunset:", color =0xAA28FF)
			await ctx.reply(embed=embed)
		else:
			embed = discord.Embed(title="**DAILY ALREADY CLAIMED**", description = "You have already claimed today's daily, come back tomorrow for your daily :city_sunset:", color =0xAA28FF)
			await ctx.reply(embed=embed)
#allows the user to send another user a certain amount of cash.
@bot.command()
async def pay(ctx, member: discord.Member, arg2):
			cash_to_send = int(arg2)
			if cash_to_send>0:
				cash_reciever_current_cash = db[f'@{member.id}_money']
				print(member.id)
				new_cash = cash_reciever_current_cash + cash_to_send
				print(cash_reciever_current_cash)
				print(cash_to_send)
				db[f'{member.id}_money'] = new_cash
				money_deductable = db[f'@{ctx.author.id}_money']
				new_money = money_deductable - cash_to_send
				db[f'@{member.id}_money'] = new_cash
			if new_money < 0:
					cash_reciever_current_cash -= cash_to_send
					db[f'@{member.id}_money'] = cash_reciever_current_cash
					db[f'@{ctx.author.id}_money'] = (money_deductable + cash_to_send)
					embed = discord.Embed(title="**INSUFFICIENT FUNDS**", description = "You don't have enough money to do this! :no_entry_sign: :dollar:", color=0xAA28FF)
					await ctx.reply(embed=embed)
			elif new_money >= 0:
				db[f'@{ctx.author.id}_money'] = new_money
				embed = discord.Embed(
					title="***MONEY SENT***",
					description=f'**You, {ctx.author}, sent {cash_to_send} USD to {member.mention}!**',
					color=0xAA28FF)
				await ctx.reply(embed=embed)
			if cash_to_send<=0:
				embed = discord.Embed(title="**INSUFFICIENT FUNDS**", description="You cannot give negative money or 0 money! :no_entry_sign: :dollar:", color=0xAA28FF)
				await ctx.reply(embed=embed)




#display's the user's balance.
@bot.command()
async def wallet(ctx):
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
				payxyz = intarg2 / shooplen
				paydue = int(payxyz)
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
		keys = db.keys()
		if f'{ctx.author.id}_stock_price' not in keys:
			db[f'{ctx.author.id}_stock_price'] = {}
		if f'{ctx.author.id}_stock_shares' not in keys:
			db[f'{ctx.author.id}_stock_shares'] = {}
		player_cash = db[f'@{ctx.author.id}_money']
		shares = int(arg2)
		stock_trans = finnhub_client.quote(f'{arg1.upper()}')
		stock_price = stock_trans['o']
		price_to_pay = shares * stock_price
		player_cash -= price_to_pay
		if player_cash < 0:
			embed = discord.Embed(
			title='**INSUFFICIENT FUNDS**',
			description=f"You don't have enough money to do that!",
			color=0xAA28FF
		)
			await ctx.reply(embed = embed)
		if player_cash >= 0:
			db[f'@{ctx.author.id}_money'] = player_cash
			stock_price_dict = db[f'{ctx.author.id}_stock_price']
			stock_shares_dict = db[f'{ctx.author.id}_stock_shares']
			stock_price_dict[f'{arg1}'] = stock_price
			if f'{arg1}_shares' not in stock_shares_dict.keys():
				stock_shares_dict[f'{arg1}_shares'] = shares
			elif f'{arg1}_shares' in stock_shares_dict.keys():
				current_shares = stock_shares_dict[f'{arg1}_shares']
				new_shares = current_shares + shares
				stock_shares_dict[f'{arg1}_shares'] = new_shares
			embed = discord.Embed(
				title='**STOCKS PURCHASED**',
				description=f'You purchased {arg2} share(s) of {arg1.upper()} stock at a rate of {stock_price} per share!',
				color=0xAA28FF
			)
			await ctx.reply(embed = embed)

@bot.command()
async def investments(ctx, arg1):
	stock_shares_dict = db[f'{ctx.author.id}_stock_shares']
	if arg1 in stock_shares_dict.keys():
		stock_shares_dict = db[f'{ctx.author.id}_stock_shares']
		stock_price_dict = db[f'{ctx.author.id}_stock_price']
		stock_shares = stock_shares_dict[f'{arg1}']
		stock_price = stock_price_dict[f'{arg1}']
		embed = discord.Embed(
			title="INVESTMENTS",
			description=f"You own {stock_shares} of {arg1.upper()}, which you bought at {stock_price}!",
			color=0xAA28FF
		)
		await ctx.reply(embed = embed)
	else:
		embed = discord.Embed(
			title="ERROR",
			description=f"You don't own that stock!",
			color=0xAA28FF
		)
		await ctx.reply(embed = embed)
		



@bot.command()
async def deposit(ctx, arg1):
	bank = db[f'@{ctx.author.id}_bank']
	intarg1 = int(arg1)
	if intarg1>-1:
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
		
	elif intarg1<=0:
			embed = discord.Embed(
				title="**INSUFFICIENT FUNDS**",
				description=f"You cannot withdraw negative funds! :no_entry_sign: :dollar:",
				color=0xAA28FF
			)
			await ctx.reply(embed = embed)
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
	global dudescash
	bank = db[f'@{ctx.author.id}_bank']
	intarg1 = int(arg1)
	if intarg1>=0:
		bank-=intarg1
		db[f'@{ctx.author.id}_bank'] = bank
		dudescash = db[f'@{ctx.author.id}_money']
		if bank<0:
			bank = db[f'@{ctx.author.id}_bank']
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
	else:
		embed = discord.Embed(
				title="**INSUFFICIENT FUNDS**",
				description=f"You cannot withdraw negative funds! :no_entry_sign: :dollar:",
				color=0xAA28FF
			)
		await ctx.reply(embed=embed)
@bot.command()
async def interviewas(ctx, arg1):
	keys = db.keys()
	if arg1 == 'artist':
		if f'@{ctx.author.id}_job' not in keys:
			db[f'@{ctx.author.id}_job'] = 'None'
		db[f'@{ctx.author.id}_job'] = 'Artist'
		embed = discord.Embed(
        title='**ARTIST JOB ACQUIRED**',
        description=
        'Congratulations, your have got the job, "The Artist". Run the .paint command every hour, and if the people like you painting, you will earn 850 USD!',
				color=0xAA28FF
)
		await ctx.reply(embed=embed)
@bot.command()
async def paint(ctx):
			keys = db.keys()
			if f'{ctx.author.id}_jobs_cooldown' not in keys:
						db[f'{ctx.author.id}_jobs_cooldown'] = 0
			player_time_daily = db[f'{ctx.author.id}_jobs_cooldown']
			if time.time() - player_time_daily > 84600:
				money = db[f'@{ctx.author.id}_money']
				db[f'@{ctx.author.id}_paint'] = 'claimed'
				db[f'{ctx.author.id}_jobs_cooldown'] = time.time()
				embed = discord.Embed(title="**PAINTING COMPLETE**", description = "You have appeased the audience! :city_sunset:", color =0xAA28FF)
				await ctx.reply(embed=embed)
				if db[f'@{ctx.author.id}_job'] == 'Artist':
					money+=100
				if db[f'@{ctx.author.id}_job'] == 'Baker':
					money+=150
				if db[f'@{ctx.author.id}_job'] == 'Banker':
					money+=300
				if db[f'@{ctx.author.id}_job'] == 'Boba':
					money+=50
				if db[f'@{ctx.author.id}_job'] == 'Book':
					money+=60
				if db[f'@{ctx.author.id}_job'] == 'Gamer':
					money+=500
				if db[f'@{ctx.author.id}_job'] == 'Math':
					money+=400
				if db[f'@{ctx.author.id}_job'] == 'None':
					embed = discord.Embed(title="**WRONG JOB**", description = "You must be an artist to do this. Please run .interviewas artist to get this job.", color =0xAA28FF)
					await ctx.reply(embed=embed)
				db[f'@{ctx.author.id}_money'] = money
			else:
				embed = discord.Embed(title="**JOB ALREADY DONE**", description = "You have already done your job, come back in a day to work more! :city_sunset:", color =0xAA28FF)
				await ctx.reply(embed=embed)
bot.run(TOKEN)