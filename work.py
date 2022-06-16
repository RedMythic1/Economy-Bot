async def work(ctx, arg1):
	keys = db.keys()
	if arg1 == artist:
		if f'@{ctx.author.id}_job' not in keys:
			db[f'@{ctx.author.id}_job'] = 'None'
		db[f'@{ctx.author.id}_job'] = 'Artist'
		embed = discord.Embed(
        title='**ARTIST JOB ACQUIRED**',
        description=
        'Congratulations, you have got the job, "The Artist". Run the .paint command every hour, and if the people like you painting, you will earn 850 USD!',
				color=0xAA28FF
)
		await ctx.reply(embed=embed)