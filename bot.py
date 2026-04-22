import os
from pathlib import Path
from dotenv import load_dotenv

import discord
from discord.ext import commands
from Overwatch.commands import build_overwatch_group
from Utils.commands import build_utils_group


ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN or TOKEN == "PEGA_AQUI_TU_TOKEN_DE_DISCORD":
    raise ValueError("Falta DISCORD_TOKEN en el archivo .env")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)

@bot.event
async def on_ready():
    print(f"Conectado como {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Comandos sincronizados: {len(synced)}")
    except Exception as e:
        print(f"Error sincronizando comandos: {e}")


bot.tree.add_command(build_overwatch_group())
bot.tree.add_command(build_utils_group())
bot.run(TOKEN)