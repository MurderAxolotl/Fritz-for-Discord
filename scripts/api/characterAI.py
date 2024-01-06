from characterai import PyAsyncCAI

from resources.shared import CAI_TOKEN, AI_BLACKLIST, NoneType

CHARACTERS = {
	"bryce the bear":"GXGDvaTDHSF77mgVh2e8HOz4b_LC76bp9qYAePOLquo",
	"caine": "99iPJ7tzD_HoaJyNi3lRDq3diOJZ7EI90vtUu-XkjW4",
	"childe":"qUyZhAJhbQ9UQWLv-zwrUibvhAT3uV6iJPWRPmPao-Y",
	"connor": "32s_oiKKRLR2D-7a4otjvRa0UEpIFUUVtIVssD2ez64",
	"cyno":"DCKUsZ-oNCKOe2nUcDIpk3hBcCNjhR1UsnoIHF-G4Nk",
	"daddy": "75TOU_oL1QLib1XP8MpdGHRiu78DmjpBCHDcGRW0KIg",
	"goose":"Nvt8JStFgrJJ0ssEhk2bato1tjiTm8MFw0z5SNjhPIU",
	"ii dottore":"qUyZhAJhbQ9UQWLv-zwrUibvhAT3uV6iJPWRPmPao-Y", 
	"kaeya":"1-hkfvky9mPLhz2SN5rReTe3VJOblHId2Wfw8UgjfH8",
	"lyney":"_52oONdEiPJyVxNRBoTTrAVL3mlaXTZhsPNBQiQdot0",
	"markiplier":"4CvFRPck3FDXNv2Aa23gJ17BHMmiRCQugbR_gI5AyRk",
	"neuvillette":"WhXlEtl2VOaT5wRyqEdtkXGXit42moQIy6KuR-KM-hA",
	"neuvillette_punisher":"g7STZs-qe82O665S7FpZzBZ_q_j2vvw4FcWFXebMKhY",
	"proto": "Vohv3F4oEjVKaDmD5quQYYQtcST0VqKGIfXAcewuZ-o",
	"ralsei": "YLualttErjbl_BgjnlG1gntDXTJWY-EFtkuOJGEnG5s",
	"scaramouche":"ZciLSmnkMriz3RtRcvKgafqiWqRlgRULdwzykCyH_pM",
	"scaramouche_dommy":"NaG9__a7jQ89cgJcgH2ueTyaBlskQ_zgbQRwAZui-4w",
	"taylor": "faymYHmsei0EsPH0cDlhrnMXg2cQz8pqLC83eQSvtzo",
	"tighnari":"29YAp_A1WIskNgycOorSd6erabVcUnGqsX23Rxr-E1I",
	"vsauce/michael":"nCFbTLQNVZssDULCaIyYG85kPDtERk7ke17zap6KABo",
	"wanderer":"qUyZhAJhbQ9UQWLv-zwrUibvhAT3uV6iJPWRPmPao-Y",
	"xiao":"PsEGZOFC_kWx8rOqayWx1xWBI7RfRYJ3rqZKlk2NHJk",
	"zhongli":"yXx1xCuVxFPb8zLdTGRQmwL4zezxgGILs2yfu8YN5sQ",
}

async def doTheThing(ctx, prompt, character, reset):

	match not isinstance(ctx.guild, NoneType):
		case True:
			match ctx.guild.id in AI_BLACKLIST:
				case True: await ctx.respond("That command is disabled on this server"); return -1

	await ctx.defer()
	opts = CHARACTERS

	try:
		client = PyAsyncCAI(CAI_TOKEN)

		if character in str(opts.keys()): char = opts[character]
		else: char = opts["scaramouche"]

		if reset: await client.chat.new_chat(char)

		chat = await client.chat.get_chat(char)
		participants = chat['participants']

		if not participants[0]['is_human']:
			tgt = participants[0]['user']['username']
		else:
			tgt = participants[1]['user']['username']

		message = prompt

		data = await client.chat.send_message(chat['external_id'], tgt, message)
		name = data['src_char']['participant']['name']	
		text = data['replies'][0]['text']
		
		await ctx.respond(f"""{str(ctx.author)}: {prompt}
{name}: {text}""")
		
	except:
		client = PyAsyncCAI(CAI_TOKEN)
		if character in str(opts.keys()): char = opts[character]
		else: char = opts["scaramouche"]

		if reset: await client.chat2.new_chat(char)

		chat = await client.chat2.get_chat(char)
		author = {'author_id': chat['chats'][0]['creator_id']}

		msg1 = prompt

		async with client.connect() as chat2:
				data = await chat2.send_message(
						char, chat['chats'][0]['chat_id'], 
						msg1, author
				)
		text = data['turn']['candidates'][0]['raw_content']

		await ctx.respond(f"""{str(ctx.author)}: {prompt}
{character}: {text}""")