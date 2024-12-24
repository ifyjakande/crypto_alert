# Crypto Analytics Bot 🤖

A real-time cryptocurrency analytics bot that sends automated alerts and market insights to Slack. The bot monitors cryptocurrency markets and provides detailed analysis including volatility alerts, relative strength indicators, volume analysis, and momentum signals.

## Features 🌟

- **Real-time Market Overview**: 
  - Total market capitalization
  - Average 24-hour market movement
  - Top cryptocurrencies by market cap

- **Volatility Alerts** 🚨
  - Identifies significant price movements
  - Tracks both short-term (1h) and medium-term (24h) volatility
  - Highlights potential reversal signals

- **Relative Strength Analysis** 💪
  - Compares individual cryptocurrency performance against market average
  - Identifies outperforming and underperforming assets
  - Tracks divergence from market trends

- **Volume Analysis** 📊
  - Monitors unusual trading volumes
  - Calculates volume multiples compared to market average
  - Identifies volume/price divergences
  - Volume to market cap ratio analysis
  - Highlights extremely high volume events

- **Momentum Tracking** 🔄
  - Multi-timeframe momentum analysis
  - Weighted scoring system across different periods
  - Identification of strong trending movements

## Setup Instructions 🛠️

### Prerequisites

- Python 3.11 or higher
- CoinMarketCap API key
- Slack workspace with bot integration

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/crypto_alert.git
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

## Usage 📱

The bot runs automatically every 30 minutes via GitHub Actions. Each alert message includes:

- Timestamp (West Africa Time)
- Market overview
- Volatility alerts
- Relative strength analysis
- Volume analysis
- Momentum signals

### Manual Trigger

You can manually trigger the alerts:
1. Go to the "Actions" tab in your repository
2. Select the "Crypto Alerts" workflow
3. Click "Run workflow"

## Alert Thresholds ⚙️

- **Volatility**: 
  - Short-term: 3% change in 1 hour
  - Medium-term: 9% change in 24 hours

- **Volume**: 
  - 2x Volume/Market Cap ratio
  - 3x above market average volume
  - 5x for extremely high volume alert

- **Momentum**: 
  - Score calculation: `(1h_Change * 0.3) + (24h_Change * 0.4) + (7d_Change * 0.3)`
  - Significant momentum threshold: ±10

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

---
*Note: This bot is for informational purposes only and should not be considered as financial advice.*
