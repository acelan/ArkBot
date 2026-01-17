# ArkBot - Discord Stock Analysis Bot

ArkBot is an intelligent Discord bot that helps users analyze stocks using Large Language Models (LLM). It integrates with E.SUN Trade SDK and provides various commands for stock analysis and portfolio management.

https://github.com/user-attachments/assets/544e730c-b4af-405b-b0dc-dbafb161c112

## Features

- Stock inventory checking
- LLM-powered stock analysis (Google Gemini)
- Integration with E.SUN Trade SDK
- Quick stock info commands
- Customizable commands
- Yahoo Finance integration

## Prerequisites

- Python 3.8+
- Discord Bot Token
- E.SUN Trade SDK credentials
- Google Gemini API key

## Installation

1. Clone the repository:
```
git clone https://github.com/acelan/ArkBot.git
cd ArkBot
```

2. Create and activate a virtual environment:
```
python3 -m venv --prompt "ArkBot" .venv
source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
```

3. Install the required packages:
```
pip install -r requirements.txt
```

4. Install E.SUN Trade SDK manually:
```bash
# Download the wheel file from E.SUN Securities:
# https://www.esunsec.com.tw/trading-platforms/api-trading/docs/download/download-sdk/
# Choose the appropriate file for your platform:
# - Linux x86_64: esun_trade-2.2.0-cp37-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
# - Windows: esun_trade-2.2.0-cp37-abi3-win_amd64.whl
# - macOS ARM64: esun_trade-2.2.0-cp37-abi3-macosx_11_0_arm64.whl

# Save to wheels/ directory and install:
pip install wheels/esun_trade-2.2.0-*.whl
```

5. Set up your environment variables:
Create a `.env` file in the project root and add the following:
```
DISCORD_TOKEN=your_discord_token
ACTIVE_CHANNELS=channel_id1,channel_id2
ESUN_CONFIG_INI=path/to/esun_config/config.ini
GOOGLE_GENAI_API_KEY=your_gemini_api_key
SYSTEM_PROMPT=your_system_prompt
LOG_LEVEL=INFO  # or DEBUG for more verbose logging
```

6. Configure E.SUN Trade SDK:
Create `esun_config/config.ini`:
```ini
[Core]
Entry = https://esuntradingapi.esunsec.com.tw/api/v1

[Cert]
Path = esun_config/YOUR_CERTIFICATE.p12

[Api]
Key = YOUR_API_KEY
Secret = YOUR_API_SECRET

[User]
Account = YOUR_ACCOUNT_NUMBER
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
- `!stock [symbol]`: Get quick stock information (e.g., `!stock AAPL` or `!stock 2330.TW`)
- `!price [symbol] [period]`: Get price history (e.g., `!price AAPL 1mo`)

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
- `arkbrain.py`: LLM integration and AI processing (Google Gemini)
- `bot_commands.py`: Command definitions and handlers
- `esun_integration.py`: Integration with E.SUN Trade SDK
- `stock_tools.py`: Stock analysis tools using yfinance
- `stock_cache.py`: Caching layer for stock data
- `gemini_tools.py`: Gemini function declarations

## Migration Notes

### Phase 1: LLM Migration (Completed)
- Migrated from LlamaIndex + OpenAI to Google Gemini
- Removed ~15 llama-index packages
- Added native yfinance integration with 15 stock analysis functions
- Added TTL-based caching for API optimization

### Phase 2: Trading SDK Migration (Completed)
- Migrated from Fugle Trade SDK to E.SUN Trade SDK
- API compatibility: ~95% identical
- **Important**: Fugle Trade SDK < 2.2.0 deprecated as of 2026-01-01
- E.SUN Trade SDK must be manually installed (not on PyPI)

See `docs/plans/` for detailed migration documentation.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Discord.py](https://discordpy.readthedocs.io/)
- [Google Gemini AI](https://ai.google.dev/)
- [E.SUN Trade SDK](https://www.esunsec.com.tw/trading-platforms/api-trading/)
- [yfinance](https://github.com/ranaroussi/yfinance)
