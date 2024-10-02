
# Discord Docker Bot - Manage Docker Containers with Multilanguage Support

## Description
This Discord bot allows you to manage Docker containers directly from a Discord server using slash commands. It provides functionalities such as starting, stopping, and restarting containers, listing running containers, and showing logs of a specific container. The bot also supports multiple languages, enabling you to switch between languages for the bot's responses by using an environment variable defined in the `docker-compose.yml` file.

## Key Features
- **Container Management**: Supports starting, stopping, and restarting Docker containers via simple commands.
- **List Running Containers**: Displays a list of containers currently running.
- **View Logs**: Shows the last 50 log entries of a specified container.
- **Multilanguage Support**: The bot’s messages can be switched between different languages such as English and Spanish through the `LANGUAGE` environment variable.
- **Integration with Docker and Discord**: Utilizes the official Docker Python client (`docker-py`) and `discord.py` library for seamless interaction.

## How to Use

### 1. Available Commands:
- `/docker <container_name> <action>`: Manages containers with the actions `start`, `stop`, or `restart`. Example: `/docker my_container start`.
- `/list_containers`: Lists all containers currently in the `running` state.
- `/container_logs <container_name>`: Shows the logs for a specific container.

### 2. Environment Variables:
- `DISCORD_TOKEN`: The token for your Discord bot.
- `LANGUAGE`: Sets the language for the bot’s responses. Supported values are `en` (English) and `es` (Spanish). You can add more languages by modifying the message JSON files.

### 3. Configuration with `docker-compose`:
Here’s an example of how to configure the bot using `docker-compose`:

```yaml
version: '3'
services:
  discord-bot:
    image: <dockerhub_username>/discord-bot:v1.0
    environment:
      - DISCORD_TOKEN=your_discord_token
      - LANGUAGE=en  # Set the language here
    volumes:
      - ./messages_en.json:/app/messages_en.json
      - ./messages_es.json:/app/messages_es.json
```

## How to Set Up Your Discord Bot

### 1. Create a Discord Bot
To use this bot, you need to create a bot in the [Discord Developer Portal](https://discord.com/developers/applications):

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click on **New Application** and give it a name.
3. On the application page, go to the **Bot** section and click **Add Bot**.
4. Copy the **Token** from this page (you’ll use it in your `docker-compose.yml` under `DISCORD_TOKEN`).

### 2. Set Bot Permissions
To ensure the bot has the correct permissions:

1. In the **OAuth2** section, go to **URL Generator**.
2. Under **OAuth2 Scopes**, select `bot` and `applications.commands` (for slash commands).
3. Under **Bot Permissions**, check the necessary permissions for the bot, such as:
   - `Send Messages`
   - `Read Messages/View Channels`
   - `Manage Messages`
4. Copy the generated URL and paste it into your browser to invite the bot to your server.

### 3. Invite the Bot to Your Server
Use the URL generated in the previous step to invite the bot to your server. The bot will now be able to interact with the server where it’s invited, using the correct permissions.

## Example of Use
1. **Run the Bot**: Ensure that your `docker-compose.yml` is configured correctly with the necessary environment variables. Then, run the following command to bring up the container:

   ```bash
   docker-compose up -d
   ```

2. **Commands in Discord**: From any channel in the server where the bot is active, you can execute commands such as:
   - `/docker <container_name> start`: Start a specific container.
   - `/list_containers`: List all running containers.
   - `/container_logs <container_name>`: Show the recent logs of a container.

## Requirements
- **Docker**: The image requires Docker to manage containers on your server.
- **Discord Bot**: You need to register a Discord bot and obtain its token from the Discord Developer Portal.
- **Docker Permissions**: Ensure that the bot's container has access to Docker on the host machine where it is running.

## Customization
If you want to add more languages or customize the bot's messages, you can modify the message JSON files (`messages_en.json`, `messages_es.json`, etc.). Simply mount these files into the container and use the `LANGUAGE` environment variable to select the correct language.

## Contribution
This project is open for contributions. If you want to add new features, fix bugs, or add support for more languages, feel free to submit a pull request on the linked GitHub repository.
