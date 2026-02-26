# Binance Futures Testnet Bot

A lightweight, robust, and modular Python automation bot for executing trades on the Binance Futures Testnet (USDT-M).

## Features
* **Order Types**: Market, Limit, and OCO (Take Profit/Stop Loss) support.
* **Security**: API credentials are kept separate via `.env` files.
* **Logging**: Comprehensive log tracking for all API interactions.
* **Clean UI**: Professional table output using `rich`.
* **Mobile Ready**: Optimized for Termux (Android/iOS).

## Setup Instructions

### 1. Prerequisites
Ensure you have Python 3 installed. If using Termux:
```bash
pkg update && pkg upgrade -y
pkg install python rust binutils -y

## Setup & Quick Start

### 1. Installation
Clone the repository and install the required dependencies:

```bash
# Clone the repository
git clone https://github.com/DataZahard/binance-trader-bot.git
cd binance-trader-bot

# Setup virtual environment and requirements
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

### Configuration & Permissions

# Edit your API keys
nano .env 

# Grant execution permissions
chmod +x cli.py

## Usage Examples

# Market Order
python cli.py --symbol BTCUSDT --side BUY --type MARKET --qty 0.001

# Limit Order
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --qty 0.001 --price 65000

# OCO (Take Profit & Stop Loss)
python cli.py --symbol BTCUSDT --side BUY --qty 0.001 --oco --price 70000 --stop_price 55000

## Logging
The bot records all API interactions in real-time. 
You can monitor the activity log located in the logs/ directory:

tail -f logs/trading.log
```

# Note:

The bot is currently configured with placeholder keys. To run the bot, please update the .env file with your valid Binance Futures Testnet API credentials.

# Developed by-datazahard
