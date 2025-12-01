import requests
import pandas as pd
from datetime import datetime

def fetch_predictit_data():
    """Fetch market data from PredictIt (JSON API)"""
    url = "https://www.predictit.org/api/marketdata/all/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json"
    }
    print(f"Requesting {url}...")
    r = requests.get(url, headers=headers)
    print(f"Response Status: {r.status_code}")
    r.raise_for_status()
    return r.json()

def markets_to_dataframe(data):
    """Flatten PredictIt JSON markets + contracts into a DataFrame"""
    rows = []

    if "markets" not in data:
        print("Error: 'markets' key not found in API response")
        return pd.DataFrame()

    for market in data["markets"]:
        market_id = market["id"]
        market_name = market["name"]
        market_status = market["status"]
        market_url = market.get("url", "")

        for contract in market["contracts"]:
            rows.append({
                "timestamp": datetime.utcnow().isoformat(),
                "market_id": market_id,
                "market_name": market_name,
                "market_status": market_status,
                "market_url": market_url,

                "contract_id": contract["id"],
                "contract_name": contract["name"],
                "contract_short_name": contract["shortName"],
                "contract_status": contract["status"],

                "last_trade_price": contract.get("lastTradePrice"),
                "best_buy_yes": contract.get("bestBuyYesCost"),
                "best_buy_no": contract.get("bestBuyNoCost"),
                "best_sell_yes": contract.get("bestSellYesCost"),
                "best_sell_no": contract.get("bestSellNoCost"),
                "last_close_price": contract.get("lastClosePrice"),

                "date_end": contract.get("dateEnd")
            })

    return pd.DataFrame(rows)

if __name__ == "__main__":
    print("Fetching PredictIt market data...")
    try:
        data = fetch_predictit_data()
        
        print("Converting to DataFrame...")
        df = markets_to_dataframe(data)

        print(f"Total rows: {len(df)}")
        if not df.empty:
            print(df.head())

            # Save to CSV
            output_path = "predictit_markets.csv"
            df.to_csv(output_path, index=False)
            print(f"\nSaved all markets to: {output_path}")
        else:
            print("No data found.")
            
    except Exception as e:
        print(f"Error: {e}")