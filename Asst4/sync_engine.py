import time
import requests
import json
import os
from datetime import datetime, timezone
from __init__ import app, db
from models import Crypto, PortfolioItem

ALERTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'alerts.json')

def log_alert(user_id, message):
    """Writes an alert to the JSON log file."""
    alerts = []
    if os.path.exists(ALERTS_FILE):
        with open(ALERTS_FILE, 'r') as f:
            try:
                alerts = json.load(f)
            except json.JSONDecodeError:
                pass
    
    alerts.insert(0, {
        "timestamp": datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC'),
        "user_id": user_id,
        "message": message
    })
    
    alerts = alerts[:100]  # Keep only the latest 100 alerts globally
    
    with open(ALERTS_FILE, 'w') as f:
        json.dump(alerts, f, indent=4)

# THE BACKGROUND WORKER
def sync_crypto_prices():
    """
    Fetches the latest prices for tracked cryptocurrencies from the CoinGecko API
    and updates the database.
    """
    print("Starting background sync worker...")
    
    # Provide the application context since we are interacting with the database outside of a web request
    with app.app_context():
        while True:
            try:
                # Get all cryptocurrencies currently in our database
                cryptos = Crypto.query.all()
                
                if cryptos:
                    # Create a mapping from lowercase name to our Crypto objects
                    # Note: CoinGecko API expects lowercase names (e.g., 'bitcoin', 'ethereum')
                    crypto_map = {c.name.lower(): c for c in cryptos}
                    crypto_ids = ",".join(crypto_map.keys())
                    
                    # Fetch live prices from CoinGecko
                    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_ids}&vs_currencies=usd&include_market_cap=true&include_24hr_change=true"
                    response = requests.get(url, timeout=10)
                    data = response.json()
                    
                    # Update prices in the database
                    for coin_id, price_info in data.items():
                        if coin_id in crypto_map and 'usd' in price_info:
                            crypto_map[coin_id].price = price_info['usd']
                            crypto_map[coin_id].market_cap = price_info.get('usd_market_cap')
                            crypto_map[coin_id].change_24h = price_info.get('usd_24h_change')
                            crypto_map[coin_id].last_updated = datetime.now(timezone.utc)
                    
                    db.session.commit()
                
                # Check for smart alerts
                items = PortfolioItem.query.all()
                alerts_triggered = False
                for item in items:
                    if item.target_price and item.crypto.price:
                        if item.crypto.price >= item.target_price:
                            log_alert(item.user_id, f"🎯 TARGET HIT: {item.crypto.name} reached your target of ${item.target_price}! Current price: ${item.crypto.price}")
                            item.target_price = None  # Clear the target so it doesn't spam
                            alerts_triggered = True
                
                if alerts_triggered:
                    db.session.commit()

                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Successfully synced {len(data)} cryptocurrency prices.")
                
            except Exception as e:
                print(f"Error occurred during sync: {e}")
            
            time.sleep(30)  # Wait for 30 seconds before syncing again

if __name__ == '__main__':
    sync_crypto_prices()