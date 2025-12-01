# PredictIt Arbitrage Engine

## Summary
Automates the "Buy All NO" arbitrage strategy for PredictIt. Targets mutually exclusive markets (e.g., elections) where buying "NO" on all candidates guarantees profit if the total cost is low enough. Uses Linear Programming to optimize trade quantities, accounting for the 10% profit fee and $850 limits.

## Setup & Run
1. **Install**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Run Demo** (Live Data):
   ```bash
   python run_demo.py
   ```
   ```
   *Note: If no arbitrage is found, the script lists "near miss" markets.*

3. **Reproduce Run** (Sample Data):
   ```bash
   python reproduce_run.py
   ```

## Strategy
- **Concept**: In a winner-take-all market with N candidates, exactly one wins.
- **Action**: Buy "NO" on ALL candidates.
- **Outcome**: You lose on the winner (pays $0) but win on N-1 losers (pay $1).
- **Math**: Profit = (Revenue from N-1 winners) - (Total Investment).
- **Optimization**: We solve for quantities $q_i$ to maximize min-profit across all outcomes.

## Limitations
- **Fees**: 10% profit fee significantly reduces margins.
- **Execution**: Manual execution required (TOS compliance). Prices may slip.
- **Capital**: Requires buying multiple contracts simultaneously.

## Files
- `arbitrage_engine.py`: Core LP optimization logic.
- `fetch_data.py`: PredictIt API handler.
- `run_demo.py`: Main execution script.
