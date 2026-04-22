import asyncio
import os
import shutil
import tempfile
from urllib.parse import urlencode
from urllib.request import urlretrieve

import discord
import json
import random
from pathlib import Path
from discord import app_commands


def build_utils_group() -> app_commands.Group:
    group = app_commands.Group(name="utils", description="Comandos útiles para el bot")

    advice_file = Path(__file__).resolve().parent / "advice.json"
    insults_file = Path(__file__).resolve().parent / "insults.json"
    alba_file = Path(__file__).resolve().parent / "frasesalba.json"
    audio_file = Path(__file__).resolve().parent / "retinohipotalamico.mp3"

    async def load_random_phrase(
        interaction: discord.Interaction,
        file_path: Path,
        file_label: str,
    ) -> str | None:
        try:
            with file_path.open("r", encoding="utf-8") as f:
                phrases = json.load(f)
        except Exception as exc:
            await interaction.response.send_message(
                f"No pude leer {file_label}: {type(exc).__name__}: {exc}",
                ephemeral=True,
            )
            return None

        if not isinstance(phrases, list) or not phrases:
            await interaction.response.send_message(
                f"El archivo {file_label} no tiene una lista valida.",
                ephemeral=True,
            )
            return None

        selected_phrase = random.choice(phrases)
        if not isinstance(selected_phrase, str) or not selected_phrase.strip():
            await interaction.response.send_message(
                f"La frase elegida en {file_label} no es valida.",
                ephemeral=True,
            )
            return None

        return selected_phrase.strip()

    async def speak_phrase(interaction: discord.Interaction, phrase: str) -> None:
        if not discord.voice_client.has_nacl:
            await interaction.response.send_message(
                "No puedo usar voz porque falta PyNaCl.\n"
                "Instala con: `python -m pip install -U \"discord.py[voice]\"`",
                ephemeral=True,
            )
            return

        # Verifica ffmpeg
        if shutil.which("ffmpeg") is None:
            await interaction.response.send_message(
                "No encuentro `ffmpeg` en el sistema.\n"
                "Instálalo y asegúrate de que esté en el PATH.",
                ephemeral=True,
            )
            return

        # Verifica que sea dentro de un servidor
        if not interaction.guild or not isinstance(interaction.user, discord.Member):
            await interaction.response.send_message(
                "Este comando solo funciona dentro de un servidor.",
                ephemeral=True,
            )
            return

        # Verifica que el usuario esté en voz
        voice_state = interaction.user.voice
        if not voice_state or not voice_state.channel:
            await interaction.response.send_message(
                "Debes estar en un canal de voz para usar este comando.",
                ephemeral=True,
            )
            return

        await interaction.response.defer(ephemeral=True)

        temp_file = None
        voice_client: discord.VoiceClient | None = interaction.guild.voice_client

        try:
            # Conectar o mover el bot al canal de voz del usuario
            if voice_client and voice_client.channel != voice_state.channel:
                await voice_client.move_to(voice_state.channel)
            elif not voice_client:
                voice_client = await voice_state.channel.connect()

            # Crear archivo temporal mp3
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp:
                temp_file = temp.name

            # Descargar TTS de Google Translate
            params = urlencode(
                {
                    "ie": "UTF-8",
                    "tl": "es",
                    "client": "tw-ob",
                    "q": phrase,
                }
            )
            tts_url = f"https://translate.google.com/translate_tts?{params}"

            await asyncio.to_thread(urlretrieve, tts_url, temp_file)

            # Crear audio con ffmpeg
            audio = discord.FFmpegPCMAudio(
                executable="ffmpeg",
                source=temp_file,
            )

            # Reproducir audio
            voice_client.play(audio)

            while voice_client.is_playing():
                await asyncio.sleep(0.25)

            await interaction.followup.send(
                "Listo, ya hablé en el canal de voz.",
                ephemeral=True,
            )

        except Exception as exc:
            await interaction.followup.send(
                f"No pude hablar en voz: {type(exc).__name__}: {exc}",
                ephemeral=True,
            )

        finally:
            try:
                if voice_client and voice_client.is_connected():
                    await voice_client.disconnect()
            except Exception:
                pass

            if temp_file and os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except Exception:
                    pass

    async def play_audio_file(interaction: discord.Interaction, source_file: Path) -> None:
        if not discord.voice_client.has_nacl:
            await interaction.response.send_message(
                "No puedo usar voz porque falta PyNaCl.\n"
                "Instala con: `python -m pip install -U \"discord.py[voice]\"`",
                ephemeral=True,
            )
            return

        if shutil.which("ffmpeg") is None:
            await interaction.response.send_message(
                "No encuentro `ffmpeg` en el sistema.\n"
                "Instálalo y asegúrate de que esté en el PATH.",
                ephemeral=True,
            )
            return

        if not source_file.exists():
            await interaction.response.send_message(
                f"No encontré el archivo de audio: {source_file.name}",
                ephemeral=True,
            )
            return

        if not interaction.guild or not isinstance(interaction.user, discord.Member):
            await interaction.response.send_message(
                "Este comando solo funciona dentro de un servidor.",
                ephemeral=True,
            )
            return

        voice_state = interaction.user.voice
        if not voice_state or not voice_state.channel:
            await interaction.response.send_message(
                "Debes estar en un canal de voz para usar este comando.",
                ephemeral=True,
            )
            return

        await interaction.response.defer(ephemeral=True)

        voice_client: discord.VoiceClient | None = interaction.guild.voice_client

        try:
            if voice_client and voice_client.channel != voice_state.channel:
                await voice_client.move_to(voice_state.channel)
            elif not voice_client:
                voice_client = await voice_state.channel.connect()

            audio = discord.FFmpegPCMAudio(
                executable="ffmpeg",
                source=str(source_file),
                options="-filter:a volume=0.2",
            )

            voice_client.play(audio)

            while voice_client.is_playing():
                await asyncio.sleep(0.25)

            await interaction.followup.send(
                "Listo, ya reproduje el audio en el canal de voz.",
                ephemeral=True,
            )

        except Exception as exc:
            await interaction.followup.send(
                f"No pude reproducir el audio: {type(exc).__name__}: {exc}",
                ephemeral=True,
            )

        finally:
            try:
                if voice_client and voice_client.is_connected():
                    await voice_client.disconnect()
            except Exception:
                pass

    @group.command(name="advice", description="El bot entra a voz y dice un consejo random")
    async def utils_advice(interaction: discord.Interaction):
        phrase = await load_random_phrase(interaction, advice_file, "advice.json")
        if not phrase:
            return

        await speak_phrase(interaction, phrase)

    @group.command(name="insult", description="El bot entra a voz y dice un insulto random")
    async def utils_insult(interaction: discord.Interaction):
        phrase = await load_random_phrase(interaction, insults_file, "insults.json")
        if not phrase:
            return

        await speak_phrase(interaction, phrase)

    @group.command(name="alba", description="El bot entra a voz y dice una frase random de Alba")
    async def utils_alba(interaction: discord.Interaction):
        phrase = await load_random_phrase(interaction, alba_file, "frasesalba.json")
        if not phrase:
            return

        await speak_phrase(interaction, phrase)

    @group.command(name="audio", description="El bot entra a voz y reproduce el MP3 de utils")
    async def utils_audio(interaction: discord.Interaction):
        await play_audio_file(interaction, audio_file)

    return group