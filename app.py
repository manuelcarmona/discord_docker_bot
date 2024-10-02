import os
import json
import discord
import docker
from discord.ext import commands
from discord import app_commands

# Define los intents
intents = discord.Intents.default()
intents.message_content = True

# Inicializar cliente de Docker y bot de Discord
client = docker.from_env()
bot = commands.Bot(command_prefix='', intents=intents)  # Dejar command_prefix vacío para usar solo slash commands

# Cargar el archivo de idioma basado en la variable de entorno
language = os.getenv('LANGUAGE', 'en')  # Valor predeterminado: inglés
try:
    with open(f'messages_{language}.json', 'r') as f:
        messages = json.load(f)
except FileNotFoundError:
    print(f"Archivo de idioma no encontrado: messages_{language}.json. Usando inglés por defecto.")
    with open('messages_en.json', 'r') as f:
        messages = json.load(f)

# Evento de activación del bot
@bot.event
async def on_ready():
    print(f'Bot {bot.user} is connected and ready!')
    try:
        synced = await bot.tree.sync()  # Sincronizar slash commands con Discord
        print(f"Slash commands synchronized: {len(synced)} commands")
    except Exception as e:
        print(f"Error to synchronize slash commands: {e}")

# Comandos de Docker (start, stop, restart) en un solo comando /docker
@bot.tree.command(name="docker", description="Management a docker container")
@app_commands.describe(container_name="Container's name", action="Action to do (start, stop, restart, logs)")
async def docker_command(interaction: discord.Interaction, container_name: str, action: str):
    try:
        container = client.containers.get(container_name)
        logs = container.logs(tail=50).decode('utf-8')
        if action == 'start':
            container.start()
            await interaction.response.send_message(messages['container_started'].format(name=container_name))
        elif action == 'stop':
            container.stop()
            await interaction.response.send_message(messages['container_stopped'].format(name=container_name))
        elif action == 'restart':
            container.restart()
            await interaction.response.send_message(messages['container_restarted'].format(name=container_name))
        elif action == 'logs':
            container.logs()
            await interaction.response.send_message(messages['logs_header'].format(name=container_name))
        else:
            await interaction.response.send_message(f'Invalid action: {action}. Use `start`, `stop`, `restart` or `logs`.')
    except docker.errors.NotFound:
        await interaction.response.send_message(messages['container_not_found'].format(name=container_name))

# Comando para listar contenedores en estado running
@bot.tree.command(name="list", description="List of containers in 'running' state")
async def list_containers(interaction: discord.Interaction):
    running_containers = client.containers.list(filters={"status": "running"})
    if running_containers:
        container_list = "\n".join([container.name for container in running_containers])
        await interaction.response.send_message(f"Containers running:\n{container_list}")
    else:
        await interaction.response.send_message("No containers running")

# Obtiene el token desde las variables de entorno
token = os.getenv('DISCORD_TOKEN')

# Ejecutar el bot con el token
if token:
    bot.run(token)
else:
    print("Error: Discord token is undefined in environment vars.")
