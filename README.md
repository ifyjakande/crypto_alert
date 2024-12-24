# Crypto Analytics Bot 🤖

A real-time cryptocurrency analytics bot that sends automated alerts and market insights to Slack. The bot monitors the top 100 cryptocurrencies by market cap and provides detailed analysis including market overview, volatility alerts, relative strength indicators, volume analysis, and momentum signals.

## Features 🌟

> **Note:** All analyses and alerts are based on the top 100 cryptocurrencies by market capitalization.

### Market Overview 📊
- Total market capitalization in billions USD
- Average 24-hour market movement percentage
- Top 3 cryptocurrencies by market cap with:
  - Current prices
  - 24-hour price changes

### Volatility Alerts 🚨
- Identifies significant price movements
- Monitors both short-term (1h) and medium-term (24h) volatility
- Alert categories:
  - Strong upward momentum
  - Price stabilization after surge
  - Strong downward momentum
  - Potential reversal signals

### Relative Strength Analysis 💪
- Compares individual cryptocurrency performance against market average
- Reports top 3 outperforming cryptocurrencies
- Reports bottom 3 underperforming cryptocurrencies
- Includes percentage difference from market average
- Shows actual 24h price changes

### Volume Analysis 📊
- Market average 24h volume baseline
- Three volume alert levels:
  - 🔥 Extremely High Volume (>5x average)
  - ⚡ Very High Volume (3-5x average)
  - 📈 High Volume (>2x average)
- Volume metrics per coin:
  - Volume in USD millions
  - Multiple vs market average
  - Volume/Market Cap ratio
- Top 3 volume gainers compared to market average

### Momentum Tracking 🔄
- Multi-timeframe momentum analysis (1h, 24h, 7d)
- Weighted scoring system
- Separate tracking for positive and negative momentum
- Detailed breakdown of changes across all timeframes

## Setup Instructions 🛠️

### Prerequisites

- Python 3.11 or higher
- CoinMarketCap API key
- Slack workspace with bot integration

### Installation

1. Clone the repository:
```bash
git clone https://github.com/ifyjakande/crypto_alert.git
cd crypto_alert
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

### Configuration

1. Set up your Slack bot:
   - Create a new Slack App at [api.slack.com/apps](https://api.slack.com/apps)
   - Add Bot Token Scopes: `chat:write`, `channels:read`
   - Install the app to your workspace
   - Invite the bot to your desired channel using `/invite @YourBotName`

2. Get your CoinMarketCap API key:
   - Sign up at [pro.coinmarketcap.com](https://pro.coinmarketcap.com)
   - Get your API key from the dashboard

3. Configure GitHub Secrets:
   - Go to your repository's Settings > Secrets and variables > Actions
   - Add the following secrets:
     - `SLACK_TOKEN`: Your Slack Bot User OAuth Token
     - `CMC_API_KEY`: Your CoinMarketCap API key

## Alert Thresholds ⚙️

### Volatility
- Short-term: 3% change in 1 hour
- Medium-term: 9% change in 24 hours (3x the short-term threshold)
- Triggers different alert types based on combination of 1h and 24h changes

### Volume
- Primary triggers:
  - Volume/Market Cap ratio > 2.0
  - Volume > 3x market average
- Volume strength categories:
  - Extremely High: >5x market average
  - Very High: 3-5x market average
  - High: >2x market average

### Relative Strength
- Compares individual 24h change against market average
- Reports top 3 outperforming and bottom 3 underperforming coins
- Calculates exact deviation from market average

### Momentum
- Weighted score calculation: 
  - 30% weight: 1-hour change
  - 40% weight: 24-hour change
  - 30% weight: 7-day change
- Significant momentum threshold: ±10
- Reports both positive and negative momentum patterns

## Automation ⚡

The bot runs automatically via GitHub Actions:
- Scheduled every 30 minutes
- Each report includes:
  - Timestamp in West Africa Time (WAT)
  - Complete market overview
  - All active alerts
  - Volume analysis
  - Momentum signals

### Manual Trigger

You can manually trigger the alerts:
1. Go to the "Actions" tab in your repository
2. Select the "Crypto Alerts" workflow
3. Click "Run workflow"

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request. Areas for potential enhancement:
- Additional technical indicators
- Custom alert thresholds
- More timeframe analyses
- Enhanced volume metrics

## Disclaimer ⚠️

This bot is for informational purposes only. The alerts and analyses provided should not be considered as financial advice. Always do your own research and consider consulting with a financial advisor before making investment decisions.

---
*Built with Python 3.11, using CoinMarketCap API for data and Slack SDK for notifications.*
