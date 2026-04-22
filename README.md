# OWPickerBot

Bot de Discord para Overwatch con slash commands para picks aleatorios y utilidades.

## Caracteristicas

- Comandos slash agrupados en `/ow` para seleccion de heroes.
- Seleccion aleatoria por rol: `tank`, `damage`, `support`.
- Modo reto diario.
- Modo mirror para 2 jugadores.
- Grupo `/utils` con comandos de voz `/utils advice`, `/utils insult`, `/utils alba` y `/utils audio`.
- Reproduccion de audio local MP3 con volumen reducido al 20% en `/utils audio`.
- Verificaciones de dependencias de voz (PyNaCl y ffmpeg) antes de reproducir audio.

## Requisitos

- Python 3.10+
- Bot creado en Discord Developer Portal
- Token del bot
- ffmpeg instalado y en `PATH` (para voz)

## Instalacion

1. Clona el repositorio.
2. Crea y activa un entorno virtual.
3. Instala dependencias:

```bash
pip install -r requirements.txt
```

4. Crea tu archivo de entorno a partir del ejemplo:

```bash
copy .env.example .env
```

5. Edita `.env` y coloca tu token real:

```env
DISCORD_TOKEN=TU_TOKEN_REAL
```

## Ejecucion

Forma general:

```bash
python bot.py
```

En Windows, para asegurar el entorno correcto del proyecto:

```bash
c:/Users/Ekapro/Desktop/Desarrollos/OWPickerBot/.venv/Scripts/python.exe bot.py
```

Si todo va bien deberias ver en consola:

- `Conectado como ...`
- `Comandos sincronizados: ...`

## Comandos disponibles

### Overwatch (`/ow`)

- `/ow random`: heroe aleatorio de cualquier rol.
- `/ow tank`: heroe aleatorio de tanque.
- `/ow damage`: heroe aleatorio de dano.
- `/ow support`: heroe aleatorio de soporte.
- `/ow reto`: reto del dia con heroe random.
- `/ow mirror usuario:@alguien`: asigna heroe aleatorio a dos jugadores.

### Utilidades (`/utils`)

- `/utils advice`: el bot entra al canal de voz del usuario, toma un consejo random desde `Utils/advice.json`, lo reproduce en TTS y se desconecta.
- `/utils insult`: el bot entra al canal de voz del usuario, toma un insulto random desde `Utils/insults.json`, lo reproduce en TTS y se desconecta.
- `/utils alba`: el bot entra al canal de voz del usuario, toma una frase random desde `Utils/frasesalba.json`, lo reproduce en TTS y se desconecta.
- `/utils audio`: el bot entra al canal de voz del usuario, reproduce `Utils/retinohipotalamico.mp3` y se desconecta.
- En `/utils audio`, el volumen se reproduce al 20% (`volume=0.2`) para que suene mas bajo.
- El comando valida:
	- PyNaCl instalado para soporte de voz en `discord.py`.
	- ffmpeg disponible en `PATH`.
	- ejecucion dentro de servidor.
	- usuario conectado a canal de voz.

## Solucion de problemas de voz

Si aparece `RuntimeError: PyNaCl library needed in order to use voice`:

1. Asegurate de ejecutar el bot con el Python del entorno virtual correcto.
2. Reinstala soporte de voz en ese mismo entorno:

```bash
python -m pip install -U "discord.py[voice]"
```

3. Verifica ffmpeg:

```bash
ffmpeg -version
```

4. Verifica desde Python que PyNaCl este disponible:

```bash
python -c "import nacl; print(nacl.__version__)"
```

## Cambios realizados en esta iteracion

- Se agrego y dejo operativo el comando de voz `/utils advice`.
- Se agrego y dejo operativo el comando de voz `/utils insult`.
- Se agrego y dejo operativo el comando de voz `/utils alba`.
- Se agrego y dejo operativo el comando de voz `/utils audio` para reproducir MP3 local.
- Se ajusto el volumen de `/utils audio` al 20% (`volume=0.2`).
- Se incorporaron validaciones previas para PyNaCl, ffmpeg, contexto de servidor y estado de voz del usuario.
- Se mejoro el manejo de errores mostrando `tipo + mensaje` al fallar voz.
- Se valido en entorno local:
	- `ffmpeg -version` responde correctamente.
	- PyNaCl carga correctamente en la venv.
	- `discord.py` detecta soporte de voz activo.
- Se documentaron pasos para evitar el uso de un interprete Python incorrecto.

## Configuracion en Discord Portal

Para evitar advertencias o comportamientos incompletos:

1. Ve a tu aplicacion en Discord Developer Portal.
2. En `Bot`, verifica intents segun lo que uses.
3. Invita el bot al servidor con scope `bot` y `applications.commands`.

## Estructura del proyecto

- `bot.py`: inicio del bot, carga de `.env`, sync de comandos.
- `Overwatch/commands.py`: comandos del grupo `/ow`.
- `Overwatch/heroes.json`: pool de heroes por rol.
- `Utils/commands.py`: comandos del grupo `/utils`, incluidos advice, insult, alba y audio.
- `Utils/advice.json`: banco de 100 consejos para el comando de voz.
- `Utils/insults.json`: banco de insultos para el comando de voz.
- `Utils/frasesalba.json`: frases para el comando de voz `/utils alba`.
- `Utils/retinohipotalamico.mp3`: audio local reproducido por `/utils audio`.
- `requirements.txt`: dependencias del proyecto.

## Seguridad

- No subas tu `.env` a GitHub.
- Mantener `.venv/` fuera de control de versiones.

## Licencia

Uso personal/educativo. Puedes adaptar este proyecto a tus necesidades.
