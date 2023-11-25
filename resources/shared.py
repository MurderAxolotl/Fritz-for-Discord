import discord, dotenv, os

dotenv.load_dotenv(".env")

INVITE_URL = "https://discord.com/oauth2/authorize?client_id=1070042394009014303&permissions=535260691552&scope=bot"

TOKEN = os.getenv("discordToken")
CHATGPT_TOKEN = os.getenv("chatgptToken")
CAI_TOKEN = os.getenv("charAIToken")

intents = discord.Intents(messages=True, message_content=True, voice_states=True)

banned_from_nsfw = ["1170869996856016956", "1169039508193427646", "1064071365449228338", "292134570940301312"]

registeredDevelopersU = ["murderaxo#0", "awshitherewego#0"]
registeredDevelopers = ["1063584978081951814", "1067843602480377907"]

version = "1.11"