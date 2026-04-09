import os
import json
import random
from pathlib import Path
from dotenv import load_dotenv

import discord
from discord.ext import commands
from discord import app_commands

ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN or TOKEN == "PEGA_AQUI_TU_TOKEN_DE_DISCORD":
    raise ValueError("Falta DISCORD_TOKEN en el archivo .env")

with open("heroes.json", "r", encoding="utf-8") as f:
    HEROES = json.load(f)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


def pick_random_hero(role: str | None = None) -> tuple[str, str]:
    """
    Devuelve (rol, héroe).
    Si role es None, elige un rol aleatorio y luego un héroe.
    """
    if role is None:
        role = random.choice(list(HEROES.keys()))

    hero = random.choice(HEROES[role])
    return role, hero


@bot.event
async def on_ready():
    print(f"Conectado como {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Comandos sincronizados: {len(synced)}")
    except Exception as e:
        print(f"Error sincronizando comandos: {e}")


group = app_commands.Group(name="ow", description="Comandos de Overwatch")


@group.command(name="random", description="Te da un héroe aleatorio de Overwatch")
async def ow_random(interaction: discord.Interaction):
    role, hero = pick_random_hero()

    embed = discord.Embed(
        title="Héroe aleatorio",
        description=f"Te tocó **{hero}**",
    )
    embed.add_field(name="Rol", value=role.capitalize(), inline=True)

    await interaction.response.send_message(embed=embed)


@group.command(name="tank", description="Te da un tank aleatorio")
async def ow_tank(interaction: discord.Interaction):
    _, hero = pick_random_hero("tank")
    await interaction.response.send_message(f"🛡️ Tu tank aleatorio es: **{hero}**")


@group.command(name="damage", description="Te da un damage aleatorio")
async def ow_damage(interaction: discord.Interaction):
    _, hero = pick_random_hero("damage")
    await interaction.response.send_message(f"💥 Tu damage aleatorio es: **{hero}**")


@group.command(name="support", description="Te da un support aleatorio")
async def ow_support(interaction: discord.Interaction):
    _, hero = pick_random_hero("support")
    await interaction.response.send_message(f"💚 Tu support aleatorio es: **{hero}**")


@group.command(name="reto", description="Te da un héroe random como reto")
async def ow_reto(interaction: discord.Interaction):
    role, hero = pick_random_hero()
    await interaction.response.send_message(
        f"🎯 Reto del día: juega una partida con **{hero}** ({role.capitalize()})"
    )


@group.command(name="mirror", description="Asigna héroes aleatorios a dos jugadores")
@app_commands.describe(usuario="El otro jugador")
async def ow_mirror(interaction: discord.Interaction, usuario: discord.Member):
    role1, hero1 = pick_random_hero()
    role2, hero2 = pick_random_hero()

    await interaction.response.send_message(
        f"🎮 {interaction.user.mention} jugará **{hero1}** ({role1.capitalize()})\n"
        f"🎮 {usuario.mention} jugará **{hero2}** ({role2.capitalize()})"
    )


bot.tree.add_command(group)
bot.run(TOKEN)