# ArkBot - Discord Stock Analysis Bot

ArkBot is an intelligent Discord bot that helps users analyze stocks using Large Language Models (LLM). It integrates with Fugle's trading platform and provides various commands for stock analysis and portfolio management.

https://github.com/user-attachments/assets/544e730c-b4af-405b-b0dc-dbafb161c112

## Features

- Stock inventory checking
- LLM-powered stock analysis
- Integration with Fugle trading platform
- Customizable commands
- Web scraping capabilities
- Yahoo Finance integration

## Prerequisites

- Python 3.8+
- Discord Bot Token
- Fugle API credentials
- Tavily API key (for search functionality)
- OpenAI API key (optional, for GPT-4 integration)

## Installation

1. Clone the repository:
```
git clone https://github.com/acelan/ArkBot.git
cd ArkBot
```

2. Create and activate a virtual environment:
```
python3 -m ArkBot .venv
source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
```

3. Install the required packages:
```
pip install -r requirements.txt
```

4. Set up your environment variables:
Create a `.env` file in the project root and add the following:
```
DISCORD_TOKEN=your_discord_token
ACTIVE_CHANNELS=channel_id1,channel_id2
FUGLE_CONFIG_INI=path/to/fugle_config.ini
TAVILY_SEARCH_API=your_tavily_api_key
OPENAI_API_KEY=your_openai_api_key  # Optional
OLLAMA_ADDR=http://localhost:11434  # If using Ollama
OLLAMA_MODEL=your_ollama_model
SYSTEM_PROMPT=your_system_prompt
LOG_LEVEL=INFO  # or DEBUG for more verbose logging
```

## Usage

To start the bot, run:
```
python main.py
```

### Available Commands

- `!help`: Display available commands
- `!inventory [stock_id]`: Check your stock inventory
- `!inv [stock_id]`: Shorthand for inventory command

To interact with the bot's AI capabilities, mention the bot and ask your question.

## Running with Supervisord

To ensure that ArkBot runs continuously and restarts automatically if it crashes, we use Supervisord.

### Installing Supervisord

On Ubuntu or Debian-based systems:
```
sudo apt-get update
sudo apt-get install supervisor
```
On CentOS or RHEL-based systems:
```
sudo yum install supervisor
```
### Configuring Supervisord for ArkBot

1. Copy the provided `arkbot.conf` file to the Supervisord configuration directory:
(Remember to change the path and [USERNAME] to suit your environment)
```
sudo cp arkbot.conf /etc/supervisor/conf.d/
```
2. Update the paths in `arkbot.conf` if your installation directory is different.

3. Reload the Supervisord configuration:
```
sudo supervisorctl reread
sudo supervisorctl update
```
### Managing ArkBot with Supervisord

- To start ArkBot:
```
sudo supervisorctl start arkbot
```
- To stop ArkBot:
```
sudo supervisorctl stop arkbot
```
- To restart ArkBot:
```
sudo supervisorctl restart arkbot
```
- To check the status of ArkBot:
```
sudo supervisorctl status arkbot
```
- To view the log output:
```
sudo tail -f /home/[USERNAME]/discord_bot/ArkBot/arkbot.log
```
With this setup, ArkBot will start automatically when your system boots and will be automatically restarted if it crashes.


## Project Structure

- `main.py`: Entry point of the application
- `arkbot.py`: Main bot logic and message handling
- `arkbrain.py`: LLM integration and AI processing
- `bot_commands.py`: Command definitions and handlers
- `fugle_integration.py`: Integration with Fugle trading platform

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Discord.py](https://discordpy.readthedocs.io/)
- [LlamaIndex](https://www.llamaindex.ai/)
- [Fugle Trade SDK](https://github.com/fugle-dev/fugle-trade-python)
