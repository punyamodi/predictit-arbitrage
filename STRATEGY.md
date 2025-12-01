# Strategy: Buy All NO

## The Math
In a mutually exclusive market with $N$ candidates, exactly one wins.
We buy "No" shares on **every** candidate.

### Variables
- $q_i$: Quantity of "No" shares for candidate $i$
- $p_i$: Price of "No" for candidate $i$
- $f$: Fee rate (0.10)

### Payout Scenario (Candidate $j$ wins)
- **Loss**: Contract $j$ pays \$0.
- **Win**: All other contracts $i \neq j$ pay \$1.
- **Net Payout**: For each winner $i$, we get $1 - f(1 - p_i)$.

### Optimization
Maximize $\pi$ (minimum profit) subject to:
1. $\text{Profit}_j \ge \pi$ for all scenarios $j=1..N$
2. $\text{Investment} \le 850$
3. $q_i \ge 0$ (Integer)

We use Linear Programming to solve this, ensuring a risk-free profit regardless of the election outcome.
