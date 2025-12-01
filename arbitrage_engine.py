import pulp
from fetch_data import fetch_predictit_data, markets_to_dataframe

def find_no_arbitrage(prices, fee=0.10, max_budget=850.0, max_scale=850):
    n = len(prices)
    if n < 2: 
        return None
    
    net_revenue = [1.0 - fee * (1.0 - p) for p in prices]
    
    prob = pulp.LpProblem("Arb", pulp.LpMaximize)
    q = [pulp.LpVariable(f"q{i}", lowBound=0) for i in range(n)]
    pi = pulp.LpVariable("pi")
    
    investment = pulp.lpSum(q[i] * prices[i] for i in range(n))
    
    prob += pi
    
    for j in range(n):
        revenue_j = pulp.lpSum(q[i] * net_revenue[i] for i in range(n) if i != j)
        profit_j = revenue_j - investment
        prob += profit_j >= pi
        
    prob += investment == 100.0
    
    status = prob.solve(pulp.PULP_CBC_CMD(msg=False))
    
    if status != 1 or pulp.value(pi) <= 0:
        return None
        
    frac = [pulp.value(var) for var in q]
    best_solution = None
    
    for scale in range(1, max_scale + 1):
        for rounding in ["round", "up", "down"]:
            if rounding == "round":
                q_int = [int(round(x * scale)) for x in frac]
            elif rounding == "up":
                q_int = [int(x * scale + 0.999) for x in frac]
            else:
                q_int = [int(x * scale) for x in frac]

            if min(q_int) <= 0:
                continue

            curr_investment = sum(q_int[i] * prices[i] for i in range(n))
            if curr_investment > max_budget or curr_investment <= 0:
                continue

            profits = []
            for j in range(n):
                revenue = sum(
                    q_int[i] * (1.0 - fee * (1.0 - prices[i]))
                    for i in range(n) if i != j
                )
                profit = revenue - curr_investment
                profits.append(profit)
            
            min_profit = min(profits)
            
            if min_profit > 0.01:
                roi = min_profit / curr_investment
                if best_solution is None or roi > best_solution['roi_percent']/100.0:
                     best_solution = {
                        "quantities": q_int,
                        "investment": round(curr_investment, 2),
                        "guaranteed_profit": round(min_profit, 2),
                        "roi_percent": round(roi * 100, 2),
                        "scale": scale,
                        "rounding": rounding
                    }
    
    return best_solution

def run_arbitrage_engine():
    data = fetch_predictit_data()
    df = markets_to_dataframe(data)
    df = df[df['market_status'] == 'Open']
    markets = df.groupby('market_id')
    
    opportunities = []
    
    for market_id, group in markets:
        valid_contracts = group.dropna(subset=['best_buy_no'])
        if len(valid_contracts) < 2:
            continue
            
        prices = valid_contracts['best_buy_no'].tolist()
        contract_ids = valid_contracts['contract_id'].tolist()
        contract_names = valid_contracts['contract_name'].tolist()
        
        result = find_no_arbitrage(prices)
        
        if result:
            result['market_name'] = group.iloc[0]['market_name']
            result['market_id'] = market_id
            result['contracts'] = []
            for k, qty in enumerate(result['quantities']):
                if qty > 0:
                    result['contracts'].append({
                        'name': contract_names[k],
                        'price': prices[k],
                        'quantity': qty,
                        'cost': prices[k] * qty
                    })
            opportunities.append(result)
            
    opportunities.sort(key=lambda x: x['roi_percent'], reverse=True)
    
    return opportunities
