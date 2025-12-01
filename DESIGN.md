# Design Decisions

## 1. Linear Programming (PuLP)
We use LP to maximize the *minimum* profit across all possible outcomes. This guarantees the strategy is risk-free.
- **Objective**: Maximize $\pi$.
- **Constraints**: Profit in every scenario $\ge \pi$.

## 2. Integer Search
LP gives fractional results (e.g., 10.5 shares). We can't buy fractions.
- **Solution**: We scale the LP ratios and search for the best integer combination (rounding up/down/nearest) that fits the $850 budget.

## 3. Data Fetching
- **Source**: Direct PredictIt API (`https://www.predictit.org/api/marketdata/all/`).
- **Bypass**: Uses standard `User-Agent` headers to mimic a browser and avoid basic blocking.

## 4. Fee Handling
- PredictIt charges 10% on *profit*.
- We calculate net payout per share as $1 - 0.10 \times (1 - \text{price})$.
- This ensures our profit calculation is realistic.
