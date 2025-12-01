from arbitrage_engine import find_no_arbitrage

def reproduce_single_run():
    print("--- Reproducing Single Arbitrage Inference Run ---")
    
    # Sample Data: A hypothetical market with 3 candidates.
    # "Best Buy No" prices are set to $0.60 for all three.
    # This is a clear arbitrage opportunity:
    # Cost to buy 1 NO for each = $1.80.
    # Payout (1 winner, 2 losers) = $2.00.
    # Raw Profit = $0.20.
    # Net Profit (after 10% fee on $0.40 profit per winning share) will be positive.
    
    sample_prices = [0.60, 0.60, 0.60]
    contract_names = ["Candidate A", "Candidate B", "Candidate C"]
    
    print(f"\nInput Prices (Buy NO): {sample_prices}")
    
    # Run the optimization engine
    result = find_no_arbitrage(sample_prices)
    
    if result:
        print("\n✅ Arbitrage Opportunity Found!")
        print(f"Total Investment: ${result['investment']}")
        print(f"Guaranteed Profit: ${result['guaranteed_profit']}")
        print(f"ROI: {result['roi_percent']}%")
        print("\nOptimal Buy Orders:")
        for i, qty in enumerate(result['quantities']):
            print(f"  - Buy {qty} NO contracts on '{contract_names[i]}' @ ${sample_prices[i]}")
    else:
        print("\n❌ No opportunity found (Unexpected for this sample).")

if __name__ == "__main__":
    reproduce_single_run()
