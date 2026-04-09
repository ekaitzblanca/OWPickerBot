# OWPickerBot

Bot de Discord para elegir heroes aleatorios de Overwatch usando slash commands.

## Caracteristicas

- Comandos slash agrupados en `/ow`
- Seleccion aleatoria por rol: `tank`, `damage`, `support`
- Modo reto diario
- Modo mirror para 2 jugadores
- Lista de heroes configurable en `heroes.json`

## Requisitos

- Python 3.10+
- Un bot creado en Discord Developer Portal
- Token del bot

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

```bash
python bot.py
```

Si todo va bien deberias ver en consola:

- `Conectado como ...`
- `Comandos sincronizados: ...`

## Comandos disponibles

Comandos slash bajo `/ow`:

- `/ow random`: heroe aleatorio de cualquier rol
- `/ow tank`: heroe aleatorio de tanque
- `/ow damage`: heroe aleatorio de dano
- `/ow support`: heroe aleatorio de soporte
- `/ow reto`: reto del dia con heroe random
- `/ow mirror usuario:@alguien`: asigna heroe aleatorio a dos jugadores

## Configuracion en Discord Portal

Para evitar advertencias o comportamientos incompletos:

1. Ve a tu aplicacion en Discord Developer Portal.
2. En `Bot`, verifica intents segun lo que uses.
3. Invita el bot al servidor con scope `bot` y `applications.commands`.

## Estructura del proyecto

- `bot.py`: logica del bot y comandos
- `heroes.json`: pool de heroes por rol
- `.env.example`: plantilla de variables de entorno
- `requirements.txt`: dependencias de Python

## Seguridad

- No subas tu `.env` a GitHub.
- Tu `.gitignore` ya excluye `.env` y `.venv/`.

## Licencia

Uso personal/educativo. Puedes adaptar este proyecto a tus necesidades.
