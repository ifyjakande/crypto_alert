from requests import Session
import json
import pandas as pd
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import time
from datetime import datetime
import os
import pytz

# Configuration
SLACK_TOKEN = os.getenv('SLACK_TOKEN')
CMC_API_KEY = os.getenv('CMC_API_KEY')

class CryptoDataExtractor:
    def __init__(self, api_key):
        self.api_key = api_key
        
    def fetch_data(self, limit=100):
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {
            'start': '1',
            'limit': str(limit),
            'convert': 'USD'
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.api_key,
        }

        session = Session()
        session.headers.update(headers)
        
        try:
            response = session.get(url, params=parameters)
            response.raise_for_status()
            data = json.loads(response.text)
            return self._process_raw_data(data)
        except Exception as e:
            print(f'Error fetching data: {e}')
            return None
        finally:
            session.close()
            
    def _process_raw_data(self, data):
        crypto_data = []
        for crypto in data['data']:
            crypto_dict = {
                'Name': crypto['name'],
                'Symbol': crypto['symbol'],
                'Price': crypto['quote']['USD']['price'],
                '1h_Change': crypto['quote']['USD']['percent_change_1h'],
                '24h_Change': crypto['quote']['USD']['percent_change_24h'],
                '7d_Change': crypto['quote']['USD']['percent_change_7d'],
                'Market_Cap': crypto['quote']['USD']['market_cap'],
                'Volume_24h': crypto['quote']['USD']['volume_24h'],
                'Circulating_Supply': crypto['circulating_supply']
            }
            crypto_data.append(crypto_dict)
        return pd.DataFrame(crypto_data)

class CryptoAlertSystem:
    def __init__(self, df, slack_token):
        self.df = df
        self.slack_client = WebClient(token=slack_token)
        self.channel = "#real-time-crypto-analytics"
        self.timestamp = datetime.now(pytz.timezone('Africa/Lagos')).strftime("%Y-%m-%d %H:%M WAT")

    def send_slack_message(self, message):
        """Sends formatted message to Slack"""
        try:
            response = self.slack_client.chat_postMessage(
                channel=self.channel,
                text=message,
                mrkdwn=True
            )
            return response
        except SlackApiError as e:
            print(f"Error sending message: {e.response['error']}")

    def generate_and_send_alerts(self):
        """Generates and sends all alerts to Slack with timestamp"""
        header = f"🕒 *Crypto Analysis Report* - {self.timestamp}\n\n"
        
        # Initialize full report
        full_report = header
        
        # Append each section
        full_report += self._generate_market_overview() + "\n\n"
        full_report += self._generate_volatility_alerts() + "\n\n"
        full_report += self._generate_relative_strength_alerts() + "\n\n"
        full_report += self._generate_volume_alerts() + "\n\n"
        full_report += self._generate_momentum_alerts()
        
        # Send complete report
        self.send_slack_message(full_report)

    def _generate_market_overview(self):
        """Generates market overview section"""
        total_market_cap = self.df['Market_Cap'].sum()
        avg_24h_change = self.df['24h_Change'].mean()
        
        message = "📊 *MARKET OVERVIEW*\n"
        message += f"Total Market Cap: ${total_market_cap/1e9:.2f}B\n"
        message += f"Average 24h Change: {avg_24h_change:.2f}%\n"
        
        # Top 3 by market cap
        top_3 = self.df.nlargest(3, 'Market_Cap')
        message += "\nTop 3 by Market Cap:\n"
        for _, coin in top_3.iterrows():
            message += f"• {coin['Symbol']}: ${coin['Price']:.2f} ({coin['24h_Change']:.2f}%)\n"
            
        return message

    def _generate_volatility_alerts(self, threshold=3.0):
        """Generates volatility alerts message"""
        volatility_alerts = self.df[
            (abs(self.df['1h_Change']) > threshold) |
            (abs(self.df['24h_Change']) > threshold * 3)
        ]
        
        message = "🚨 *VOLATILITY ALERTS*\n"
        if len(volatility_alerts) > 0:
            for _, row in volatility_alerts.iterrows():
                if row['24h_Change'] > threshold * 3:
                    if row['1h_Change'] > 0:
                        message += f"⚠️ *{row['Symbol']}*: Strong upward momentum (24h: {row['24h_Change']:.2f}%, 1h: {row['1h_Change']:.2f}%)\n"
                    else:
                        message += f"👀 *{row['Symbol']}*: Price stabilizing after surge (24h: {row['24h_Change']:.2f}%)\n"
                elif row['24h_Change'] < -threshold * 3:
                    if row['1h_Change'] < 0:
                        message += f"📉 *{row['Symbol']}*: Strong downward momentum (24h: {row['24h_Change']:.2f}%)\n"
                    else:
                        message += f"💡 *{row['Symbol']}*: Potential reversal signal (24h: {row['24h_Change']:.2f}%)\n"
        else:
            message += "No significant volatility detected\n"
        
        return message

    def _generate_relative_strength_alerts(self):
        """Generates relative strength alerts message"""
        market_avg_24h = self.df['24h_Change'].mean()
        relative_strength = self.df.copy()
        relative_strength['RS_Score'] = relative_strength['24h_Change'] - market_avg_24h
        sorted_rs = relative_strength.sort_values('RS_Score', ascending=False)
        
        message = "💪 *RELATIVE STRENGTH ALERTS*\n"
        
        for _, row in sorted_rs.head(3).iterrows():
            message += f"📈 *{row['Symbol']}*: Outperforming market by {row['RS_Score']:.2f}% (24h change: {row['24h_Change']:.2f}%)\n"
        for _, row in sorted_rs.tail(3).iterrows():
            message += f"📉 *{row['Symbol']}*: Underperforming market by {abs(row['RS_Score']):.2f}% (24h change: {row['24h_Change']:.2f}%)\n"
        
        return message

    def _generate_volume_alerts(self, volume_threshold=2.0):
        """Generates volume analysis alerts message"""
        self.df['Volume_to_Market_Cap'] = self.df['Volume_24h'] / self.df['Market_Cap']
        
        # Calculate average 24h volume
        avg_volume = self.df['Volume_24h'].mean()
        self.df['Volume_vs_Avg'] = self.df['Volume_24h'] / avg_volume
        
        # Find coins with unusual volume
        unusual_volume = self.df[
            (self.df['Volume_to_Market_Cap'] > volume_threshold) |
            (self.df['Volume_vs_Avg'] > 3.0)  # Volume 3x above average
        ]
        
        message = "📊 *VOLUME ALERTS*\n"
        message += f"Market Average 24h Volume: ${avg_volume/1e6:.2f}M\n\n"
        
        if len(unusual_volume) > 0:
            # Sort by volume
            unusual_volume = unusual_volume.sort_values('Volume_24h', ascending=False)
            
            for _, row in unusual_volume.iterrows():
                volume_multiple = row['Volume_vs_Avg']
                price_change = row['24h_Change']
                volume_usd = row['Volume_24h']
                
                # Determine volume strength indicators
                if volume_multiple > 5:
                    volume_indicator = "🔥 *Extremely High Volume*"
                elif volume_multiple > 3:
                    volume_indicator = "⚡ *Very High Volume*"
                else:
                    volume_indicator = "📈 *High Volume*"
                
                message += f"{volume_indicator} {row['Symbol']}:\n"
                message += f"• Volume: ${volume_usd/1e6:.2f}M ({volume_multiple:.1f}x market average)\n"
                
                if price_change > 0:
                    message += f"• Price: ${row['Price']:.2f} (+{price_change:.2f}%)\n"
                else:
                    message += f"• Price: ${row['Price']:.2f} ({price_change:.2f}%)\n"
                
                message += f"• Volume/Market Cap Ratio: {row['Volume_to_Market_Cap']:.3f}\n\n"
        else:
            message += "No unusual volume patterns detected\n"
        
        # Add top volume gainers and losers
        message += "\n*24h Volume Changes*:\n"
        top_gainers = self.df.nlargest(3, 'Volume_vs_Avg')
        for _, row in top_gainers.iterrows():
            message += f"📈 *{row['Symbol']}* volume {row['Volume_vs_Avg']:.1f}x above average\n"
        
        return message

    def _generate_momentum_alerts(self):
        """Generates price momentum alerts message"""
        momentum = self.df.copy()
        momentum['Momentum_Score'] = (
            momentum['1h_Change'] * 0.3 + 
            momentum['24h_Change'] * 0.4 + 
            momentum['7d_Change'] * 0.3
        )
        sorted_momentum = momentum.sort_values('Momentum_Score', ascending=False)
        
        message = "🔄 *MOMENTUM ALERTS*\n"
        momentum_found = False
        
        for _, row in sorted_momentum.head(3).iterrows():
            if row['Momentum_Score'] > 10:
                momentum_found = True
                message += f"🚀 *{row['Symbol']}*: Strong positive momentum (Score: {row['Momentum_Score']:.2f})\n"
                message += f"  1h: {row['1h_Change']:.2f}% | 24h: {row['24h_Change']:.2f}% | 7d: {row['7d_Change']:.2f}%\n"
        for _, row in sorted_momentum.tail(3).iterrows():
            if row['Momentum_Score'] < -10:
                momentum_found = True
                message += f"🔻 *{row['Symbol']}*: Strong negative momentum (Score: {row['Momentum_Score']:.2f})\n"
                message += f"  1h: {row['1h_Change']:.2f}% | 24h: {row['24h_Change']:.2f}% | 7d: {row['7d_Change']:.2f}%\n"
        
        if not momentum_found:
            message += "No significant momentum patterns detected\n"
        
        return message

def main():
    try:
        # Initialize data extraction
        extractor = CryptoDataExtractor(CMC_API_KEY)
        df = extractor.fetch_data()
        
        if df is not None and not df.empty:
            # Initialize and run alert system
            alert_system = CryptoAlertSystem(df, SLACK_TOKEN)
            alert_system.generate_and_send_alerts()
            return True
            
    except Exception as e:
        print(f"Error during execution: {str(e)}")
        return False

if __name__ == "__main__":
    main()
