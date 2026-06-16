"""
Trade execution layer. Currently alert-only.

To add live trading, subclass TradeExecutor and swap it in sol_trader/main.py:
    from sol_trader.executor import CoinbaseExecutor  # (future)
    executor = CoinbaseExecutor(api_key=..., api_secret=...)
"""


class TradeExecutor:
    def execute_buy(self, amount_usd: float, price: float) -> dict:
        raise NotImplementedError

    def execute_sell(self, qty_sol: float, price: float) -> dict:
        raise NotImplementedError


class AlertOnlyExecutor(TradeExecutor):
    """No-op executor: logs intent but takes no action. Safe default."""

    def execute_buy(self, amount_usd: float, price: float) -> dict:
        qty = amount_usd / price
        print(f"  [ALERT ONLY] Would buy {qty:.4f} SOL at ${price:,.2f} (${amount_usd:.2f})")
        return {"status": "alert_only", "qty_sol": qty, "price": price, "amount_usd": amount_usd}

    def execute_sell(self, qty_sol: float, price: float) -> dict:
        proceeds = qty_sol * price
        print(f"  [ALERT ONLY] Would sell {qty_sol:.4f} SOL at ${price:,.2f} (${proceeds:.2f})")
        return {"status": "alert_only", "qty_sol": qty_sol, "price": price, "proceeds": proceeds}


# --- Future exchange executors ---
# class CoinbaseExecutor(TradeExecutor): ...
# class KrakenExecutor(TradeExecutor): ...
# class BinanceExecutor(TradeExecutor): ...
