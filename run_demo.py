from arbitrage_engine import run_arbitrage_engine, fetch_predictit_data, markets_to_dataframe
import json

def main():
    print("===================================================")
    print("   PredictIt 'Buy All NO' Arbitrage Engine Demo    ")
    print("===================================================")
    
    try:
        opps = run_arbitrage_engine()
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    print(f"\nFound {len(opps)} arbitrage opportunities.")
    
    if not opps:
        print("No arbitrage opportunities found in the current live market.")
        print("This is expected in efficient markets (fees usually eat the small raw margins).")
        print("\n--- Top 5 'Near Miss' Markets (Closest to Profitability) ---")
        
        data = fetch_predictit_data()
        df = markets_to_dataframe(data)
        df = df[df['market_status'] == 'Open']
        markets = df.groupby('market_id')
        
        near_misses = []
        for market_id, group in markets:
            valid_contracts = group.dropna(subset=['best_buy_no'])
            if len(valid_contracts) < 2: continue
            
            prices = valid_contracts['best_buy_no'].tolist()
            gap = (len(prices) - 1) - sum(prices)
            near_misses.append({
                "market": group.iloc[0]['market_name'],
                "gap": gap,
                "sum_prices": sum(prices),
                "n": len(prices)
            })
            
        near_misses.sort(key=lambda x: x['gap'], reverse=True)
        
        for nm in near_misses[:5]:
            print(f"Market: {nm['market']}")
            print(f"  Raw Margin (before fees): ${nm['gap']:.3f} (Sum NO: ${nm['sum_prices']:.2f}, N: {nm['n']})")
            
    for i, op in enumerate(opps[:5]):
        print(f"\nOpportunity #{i+1}")
        print(f"Market: {op['market_name']}")
        print(f"Total Investment: ${op['investment']}")
        print(f"Guaranteed Profit: ${op['guaranteed_profit']}")
        print(f"ROI: {op['roi_percent']}%")
        print("Buy Orders:")
        for c in op['contracts']:
            print(f"  - Buy {c['quantity']} NO contracts on '{c['name']}' @ ${c['price']} (Cost: ${c['cost']:.2f})")
        print("-" * 40)

    with open('demo_output.json', 'w') as f:
        json.dump(opps, f, indent=2)
    print("\nFull results saved to demo_output.json")

if __name__ == "__main__":
    main()
