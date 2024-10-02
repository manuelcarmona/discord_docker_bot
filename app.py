import os
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

# Evento de activación del bot
@bot.event
async def on_ready():
    print(f'Bot {bot.user} is connected and ready!')
    try:
        synced = await bot.tree.sync()  # Sincronizar slash commands con Discord
        print(f"Slash commands sincronizados: {len(synced)} comandos")
    except Exception as e:
        print(f"Error al sincronizar slash commands: {e}")

# Comando para gestionar contenedores de Docker (start, stop, restart)
@bot.tree.command(name="docker", description="Management docker containers")
@app_commands.describe(container_name="Container name", action="Action (start, stop, restart, logs)")
async def docker_command(interaction: discord.Interaction, container_name: str, action: str):
    await interaction.response.defer()
    try:
        container = client.containers.get(container_name)
        if action == 'start':
            container.start()
            await interaction.response.send_message(f'Container {container_name} started.')
        elif action == 'stop':
            container.stop(timeout=10)
            await interaction.followup.send(f'Container {container_name} stopped.')
        elif action == 'restart':
            container.restart()
            await interaction.response.send_message(f'Container {container_name} restarted.')
        @app_commands.describe(container_name="Container name")
async def container_logs(interaction: discord.Interaction, container_name: str):
    try:
        container = client.containers.get(container_name)
        
        await interaction.response.send_message(f"Logs of container {container_name}:\n```{logs}```")
    except docker.errors.NotFound:
        await interaction.response.send_message(f'Container not found: {container_name}')
    except Exception as e:
        await interaction.response.send_message(f'Error to get the logs: {str(e)}')
        else:
            await interaction.response.send_message(f'Invalid action: {action}. Use `start`, `stop`, or `restart`.')
    except docker.errors.APIError as e:
        if action == 'stop':
            # Attempt to force stop the container if regular stop fails
            container.kill()
            await interaction.response.send_message(f'Container {container_name} forcefully stopped.')
        else:
            await interaction.response.send_message(f'Error: {str(e)}')
    except docker.errors.NotFound:
        await interaction.response.send_message(f'Container not found: {container_name}')

# Comando para listar contenedores en estado running
@bot.tree.command(name="list_containers", description="List of containers in 'running' state")
async def list_containers(interaction: discord.Interaction):
    running_containers = client.containers.list(filters={"status": "running"})
    if running_containers:
        container_list = "\n".join([container.name for container in running_containers])
        await interaction.response.send_message(f"Running containers:\n{container_list}")
    else:
        await interaction.response.send_message("There are not containers in running state.")

# Obtiene el token desde las variables de entorno
token = os.getenv('DISCORD_TOKEN')

# Ejecutar el bot con el token
if token:
    bot.run(token)
else:
    print("Error: El token de Discord no está definido en las variables de entorno.")
