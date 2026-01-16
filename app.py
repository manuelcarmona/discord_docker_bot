import os
import re
import discord
import docker
from discord.ext import commands
from discord import app_commands
import logging

# Define los intents
intents = discord.Intents.default()
intents.message_content = True

# Inicializar cliente de Docker y bot de Discord
client = docker.from_env()
bot = commands.Bot(command_prefix='', intents=intents)  # Dejar command_prefix vacío para usar solo slash commands

# fix logging and format correctly
log_level = logging.INFO
match os.getenv('LOG_LEVEL').upper():
    case 'DEBUG':
        log_level = logging.DEBUG
    case 'INFO':
        log_level = logging.INFO
    case 'WARNING':
        log_level = logging.WARNING
    case 'ERROR':
        log_level = logging.ERROR
    case 'CRITICAL':
        log_level = logging.CRITICAL
    case _:
        log_level = logging.INFO

discord.utils.setup_logging(level=log_level, root=True)
logger = logging.getLogger('discord-docker-bot')

# Función para eliminar códigos ANSI de una cadena
def remove_ansi_codes(logs: str) -> str:
    ansi_escape = re.compile(r'(?:\x1B[@-_][0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', logs)

# Evento de activación del bot
@bot.event
async def on_ready():
    logger.info(f'Bot {bot.user} is connected and ready!')
    try:
        synced = await bot.tree.sync()  # Sincronizar slash commands con Discord
        logger.debug(f"Synchronized slash commands: {len(synced)} commands")
    except Exception as e:
        logger.error(f"Error when synchronizing slash commands: {e}")


# Comando para gestionar contenedores de Docker (start, stop, restart)
@bot.tree.command(name="docker", description="Manage docker containers")
@app_commands.describe(container_name="Container name", action="Action (start, stop, restart, logs)")
async def docker_command(interaction: discord.Interaction, container_name: str, action: str):

    try:
        container = client.containers.get(container_name)
        if action == 'start':
            await interaction.response.defer(thinking=True)
            container.start()
            await interaction.followup.send(f'> Container {container_name} started.')
        elif action == 'stop':
            await interaction.response.defer(thinking=True)
            container.stop(timeout=10)
            await interaction.followup.send(f'> Container {container_name} stopped.')
        elif action == 'restart':
            await interaction.response.defer(thinking=True)
            container.restart()
            await interaction.followup.send(f'> Container {container_name} restarted.')
        elif action == 'logs':
            await interaction.response.defer(thinking=True)
            logs = container.logs(tail=50).decode('utf-8')  # Obtener las últimas 50 líneas de los logs
            clean_logs = remove_ansi_codes(logs)  # Eliminar códigos ANSI
            if clean_logs:
                await interaction.followup.send(f'> Logs from {container_name} (last 50 lines):\n```{clean_logs}```')
            else:
                await interaction.followup.send(f'> No logs available for {container_name}.')
        else:
            await interaction.response.send_message(f'> Invalid action: {action}. Use `start`, `stop`, `restart` or `logs`.')
    except docker.errors.APIError as e:
        if action == 'stop':
            # Attempt to force stop the container if regular stop fails
            container.kill()
            await interaction.followup.send(f'> Container {container_name} forcefully stopped.')
        else:
            await interaction.followup.send(f'> Error: {str(e)}')
    except docker.errors.NotFound:
        await interaction.response.send_message(f'> Container not found: {container_name}')

# Comando para listar contenedores en estado running
@bot.tree.command(name="list_containers", description="List of containers in 'running' state")
async def list_containers(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    running_containers = client.containers.list(filters={"status": "running"})
    if running_containers:
        container_list = "\n".join([container.name for container in running_containers])
        await interaction.followup.send(f"> Running containers:\n {container_list}")
    else:
        await interaction.followup.send("There are not containers in running state.")

# Obtiene el token desde las variables de entorno
token = os.getenv('DISCORD_TOKEN')

# Ejecutar el bot con el token
if token:
    bot.run(token)
else:
    logger.error("Discord token is undefined at environment vars.")
