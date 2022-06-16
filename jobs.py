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
	        'Congratulations, your have got the job, "The Artist". Run the .work command every day, and if the people like your work, you will earn 100 USD!',
					color=0xAA28FF
	)
			await ctx.reply(embed=embed)
	@bot.command()
	async def work(ctx):
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