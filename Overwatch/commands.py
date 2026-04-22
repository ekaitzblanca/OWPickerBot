import random
import json
from pathlib import Path
from typing import Mapping

import discord
from discord import app_commands


HEROES_PATH = Path(__file__).resolve().parent / "heroes.json"


def load_heroes(path: Path = HEROES_PATH) -> dict[str, list[str]]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_overwatch_group(heroes: Mapping[str, list[str]] | None = None) -> app_commands.Group:
    if heroes is None:
        heroes = load_heroes()

    group = app_commands.Group(name="ow", description="Comandos de Overwatch")

    def pick_random_hero(role: str | None = None) -> tuple[str, str]:
        """
        Devuelve (rol, héroe).
        Si role es None, elige un rol aleatorio y luego un héroe.
        """
        if role is None:
            role = random.choice(list(heroes.keys()))

        hero = random.choice(heroes[role])
        return role, hero

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

    return group
