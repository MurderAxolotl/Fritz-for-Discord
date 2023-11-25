import scripts.api.gpt as gpt
import g4f, nest_asyncio

async def onHeyFritz(ctx):
	textPrompt = str(ctx.content).split(",")[1]

	allowed_models = ['code-davinci-002', 'text-ada-001', 'text-babbage-001', 'text-curie-001', 'text-davinci-002', 'text-davinci-003', 'palm', 'gpt-4-0613']

	workMsg = await ctx.channel.send("I'm thinking, please wait...")

	# response = g4f.Completion.create(model  = 'text-davinci-003', prompt = textPrompt)
	response = g4f.ChatCompletion.create(model=g4f.models.gpt_4,messages=[{"role": "user", "content": textPrompt}], )

	if len(str(response)) > 0: await workMsg.edit(response)
	else: await workMsg.edit("Language backend is not responding")