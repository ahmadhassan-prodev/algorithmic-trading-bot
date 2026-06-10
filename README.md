# Algorithmic Trading Bot

**A Python-based algorithmic trading system for Binance (SOLUSDT) using technical analysis indicators and multi-timeframe strategies.**

This repository implements an automated trading bot that monitors market conditions, identifies trading signals based on candlestick patterns, EMAs, RSI, volume, and trend analysis, and executes trades on the Binance exchange (with support for testnet).

---

## Overview

This project is a **full algorithmic trading bot** focused on SOL/USDT perpetual or spot trading. It combines multiple technical indicators and custom logic to detect high-probability setups in uptrend and downtrend scenarios. The bot runs in a continuous loop, checking 15min, 30min, and 1h timeframes, managing orders, stop-losses, and profit targets.

It serves as both a functional trading tool and an educational example of building a complete trading system with real exchange integration.

## Repository Purpose

- Implement automated trading strategies using technical analysis
- Demonstrate integration with the Binance API for data fetching and order execution
- Provide a modular structure for indicators, order management, and trade execution
- Serve as a practical learning resource for algorithmic trading concepts

## Key Features

- **Multi-timeframe Analysis**: 15min, 30min, and 1h candles
- **Technical Indicators**:
  - Candlestick pattern recognition (Doji, Hammer, Spinning Top, etc.)
  - EMA (Exponential Moving Average)
  - RSI (Relative Strength Index)
  - Trend detection
  - Volume analysis
- **Trading Logic**:
  - Uptrend and Downtrend modes
  - Dynamic stop-loss and take-profit management
  - OCO (One-Cancels-the-Other) order support
  - Order status monitoring and adjustment
- **Risk Management**: Stop-loss handling, position sizing checks
- **Live & Testnet Support**

## Technologies Used

- **Python 3**
- **Binance Python API** (`binance` library)
- **Pandas** (for candle data processing)
- **Datetime & Time** modules for scheduling
- Modular architecture with separate packages for data, indicators, orders, strategies, etc.

## Project Structure

```bash
Algorithmic-Trading-Bot/
├── main.py                     # Main trading loop and orchestration
├── api/
│   └── exchange_client.py      # Binance client configuration (live/testnet)
├── assets/
│   └── exchange_assets.py      # Balance checks and asset utilities
├── data/
│   └── data_fetcher.py         # Fetches OHLCV data for multiple intervals
├── indicators/
│   ├── candlestick_details.py  # Candlestick pattern detection
│   ├── ema.py                  # EMA calculations
│   ├── rsi.py                  # RSI indicator
│   ├── trend.py                # Trend analysis
│   └── volume.py               # Volume-based signals
├── orders/
│   └── exchange_orders.py      # Order placement, cancellation, status
├── strategies/
│   └── profit_strategies.py    # Profit target and strategy logic
├── trading/
│   └── trade_execution_helper.py # Trade execution and management
├── utils/
│   ├── exchange_helpers.py     # General exchange utilities
│   └── wait_time.py            # Timing and scheduling helpers
├── test/                       # Test scripts for components
└── README.md
```

**How the Code Works**

- **Initialization**: User selects trend direction (Uptrend/Downtrend) and provides key price levels.
- **Data Fetching**: Continuously retrieves latest candle data from Binance for multiple timeframes.
- **Signal Generation**: Analyzes candles using indicators to identify entry opportunities.
- **Order Execution**: Places market/limit orders, sets stop-loss and take-profit levels.
- **Monitoring**: Runs in an infinite loop, checking order status, adjusting positions, and managing risk.
- **Timing**: Uses precise sleep functions aligned with candle close times.

The core logic resides in main.py, which coordinates all modules.

**Installation**

- Clone the repository:

Bash

git clone &lt;repository-url&gt;

cd Algorithmic-Trading-Bot

- Install dependencies:

Bash

pip install python-binance pandas

- Update API credentials in api/exchange_client.py:
  - Replace placeholder keys with your Binance API keys.
  - Toggle LIVE_MODE for testnet or live trading.

**⚠️ Warning**: Trading involves financial risk. Use testnet first and never risk more than you can afford to lose.

**Usage**

Bash

python main.py

- Follow the console prompts for trend selection and price levels.
- The bot will begin monitoring and executing trades according to the defined logic.
- Monitor the terminal for real-time logs and status updates.

**Learning Outcomes**

By studying this codebase, you can learn:

- Integration with cryptocurrency exchange APIs
- Technical analysis indicator implementation
- Multi-timeframe trading strategies
- Order management and risk control in live environments
- Modular Python project structure for complex applications
- Handling real-time data and timing in trading bots

**Future Improvements**

- Add backtesting capabilities
- Implement configuration via .env or YAML files
- Add more sophisticated strategies and machine learning models
- Web dashboard for monitoring
- Logging and performance analytics
- Support for additional trading pairs

**Notes**

- The bot is currently optimized for **SOLUSDT**.
- Always test thoroughly on testnet before using real funds.
- API rate limits and exchange fees should be considered in production.
- This is for educational and experimental purposes.
