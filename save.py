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
				embed = discord.Embed(title="**INSUFFICIENT FUNDS**", description = f"You don't have enough money to do this! :no_entry_sign: :dollar:", color = 0xAA28FF)
				await ctx.reply(embed=embed)
			elif player_cash>=0:
				db[f'@{ctx.author.id}_money'] = player_cash
				stock_list[arg1.upper()] = stock_price
				current_owned_stocks = db[f'{arg1}_{ctx.author.id}'] 
				current_owned_stocks+=shares_count
				db[f'{arg1}_{ctx.author.id}'] = current_owned_stocks
				embed = discord.Embed(title="**STOCKS PURCHASED!**", description= f"The stocks you requested were successfully purchased.", color=0xAA28FF)
				await ctx.reply(embed=embed)