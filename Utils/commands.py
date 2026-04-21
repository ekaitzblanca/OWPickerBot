import random
from typing import Mapping

import discord
from discord import app_commands


def build_utils_group() -> app_commands.Group:
    group = app_commands.Group(name="utils", description="Comandos útiles para el bot")

    @group.command(name="speak", description="El bot habla")
    async def ow_speak(interaction: discord.Interaction):
        await interaction.response.send_message("¡Hola, mundo!")

    return group