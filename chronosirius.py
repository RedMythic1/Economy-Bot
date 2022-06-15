bot = commands.Bot(...)
finc = finnhub.Client(...)

@bot.command()
def start(ctx):
	if ctx.author.id not in db.keys():
		db[ctx.author.id] = {
			'wallet': 0,
			'bank': 0,
			'stocks': {
				'aapl': 0,
				...
			},
			#other account setup goes here in the dict
		}
		await ctx.send('your message here', embed=Embed('title', 'body')) #or however it is im writing realy fast
	else:
		await ctx.send('acc alr exists message')

