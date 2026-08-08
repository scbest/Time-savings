"""
FIFO tax lot tracker for SOL trades.

Each buy creates a lot. Each sell consumes lots in FIFO order and calculates
short-term (<1 year) vs long-term (>=1 year) capital gain/loss.
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

TAX_LOTS_PATH = Path(__file__).parent.parent / "sol_tax_lots.json"
HOLDING_PERIOD_DAYS = 365


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _parse_dt(iso_str):
    dt = datetime.fromisoformat(iso_str)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def load_data():
    if TAX_LOTS_PATH.exists():
        with open(TAX_LOTS_PATH) as f:
            return json.load(f)
    return {"lots": [], "sells": []}


def save_data(data):
    with open(TAX_LOTS_PATH, "w") as f:
        json.dump(data, f, indent=2)


def _classify(buy_date_str, sell_dt=None):
    """Return ('short_term'|'long_term', held_days)."""
    buy_dt = _parse_dt(buy_date_str)
    sell_dt = sell_dt or datetime.now(timezone.utc)
    if sell_dt.tzinfo is None:
        sell_dt = sell_dt.replace(tzinfo=timezone.utc)
    held = (sell_dt - buy_dt).days
    return ("long_term" if held >= HOLDING_PERIOD_DAYS else "short_term"), held


def record_buy(qty_sol, price_per_sol, dollar_amount, date=None):
    """Add a new lot. Call this after a buy is confirmed."""
    data = load_data()
    lot = {
        "id": str(uuid.uuid4())[:8],
        "date": (date or _now_iso()),
        "qty_sol": qty_sol,
        "cost_per_sol": price_per_sol,
        "total_cost": dollar_amount,
        "remaining_qty": qty_sol,
    }
    data["lots"].append(lot)
    save_data(data)
    return lot


def estimate_sell_impact(qty_sol, current_price, short_term_rate=0.32, long_term_rate=0.15):
    """
    Estimate tax impact of selling qty_sol at current_price using FIFO.
    Does NOT modify the lot data — call record_sell() after confirming the trade.
    """
    data = load_data()
    open_lots = [l for l in data["lots"] if l["remaining_qty"] > 0]

    total_holdings = sum(l["remaining_qty"] for l in open_lots)
    if total_holdings == 0:
        return {"error": "No open lots to sell", "total_holdings_sol": 0}

    qty_to_sell = min(qty_sol, total_holdings)
    proceeds = qty_to_sell * current_price
    remaining = qty_to_sell
    total_basis = 0.0
    short_gain = 0.0
    long_gain = 0.0
    lots_consumed = []

    for lot in sorted(open_lots, key=lambda l: l["date"]):  # FIFO
        if remaining <= 0:
            break
        consume = min(remaining, lot["remaining_qty"])
        basis = consume * lot["cost_per_sol"]
        gain = consume * current_price - basis
        term, held_days = _classify(lot["date"])

        lots_consumed.append({
            "lot_id": lot["id"],
            "bought": lot["date"][:10],
            "held_days": held_days,
            "term": term,
            "qty": round(consume, 6),
            "cost_basis": round(basis, 2),
            "proceeds": round(consume * current_price, 2),
            "gain_loss": round(gain, 2),
        })
        total_basis += basis
        if term == "short_term":
            short_gain += gain
        else:
            long_gain += gain
        remaining -= consume

    total_gain = short_gain + long_gain
    est_tax = max(short_gain * short_term_rate, 0) + max(long_gain * long_term_rate, 0)
    net = proceeds - est_tax

    return {
        "qty_sol": round(qty_to_sell, 6),
        "current_price": current_price,
        "proceeds": round(proceeds, 2),
        "total_cost_basis": round(total_basis, 2),
        "total_gain_loss": round(total_gain, 2),
        "short_term_gain": round(short_gain, 2),
        "long_term_gain": round(long_gain, 2),
        "estimated_tax": round(est_tax, 2),
        "net_after_tax": round(net, 2),
        "effective_rate": round(est_tax / proceeds * 100, 1) if proceeds > 0 else 0,
        "total_holdings_sol": round(total_holdings, 6),
        "lots_consumed": lots_consumed,
    }


def record_sell(qty_sol, price_per_sol, date=None):
    """Consume lots FIFO and persist the sell record. Call after a trade is confirmed."""
    data = load_data()
    sell_dt = _parse_dt(date) if date else datetime.now(timezone.utc)
    open_lots = [l for l in data["lots"] if l["remaining_qty"] > 0]

    remaining = qty_sol
    consumed = []
    for lot in sorted(open_lots, key=lambda l: l["date"]):
        if remaining <= 0:
            break
        consume = min(remaining, lot["remaining_qty"])
        lot["remaining_qty"] = round(lot["remaining_qty"] - consume, 8)
        term, held_days = _classify(lot["date"], sell_dt)
        consumed.append({
            "lot_id": lot["id"],
            "qty": round(consume, 6),
            "cost_basis": round(consume * lot["cost_per_sol"], 2),
            "term": term,
            "held_days": held_days,
        })
        remaining -= consume

    sell_record = {
        "date": sell_dt.isoformat(),
        "qty_sol": qty_sol,
        "price_per_sol": price_per_sol,
        "proceeds": round(qty_sol * price_per_sol, 2),
        "lots_consumed": consumed,
    }
    data["sells"].append(sell_record)
    save_data(data)
    return sell_record


def get_holdings_summary():
    data = load_data()
    open_lots = [l for l in data["lots"] if l["remaining_qty"] > 0]
    total_sol = sum(l["remaining_qty"] for l in open_lots)
    total_basis = sum(l["remaining_qty"] * l["cost_per_sol"] for l in open_lots)
    return {
        "total_sol": round(total_sol, 6),
        "total_cost_basis": round(total_basis, 2),
        "avg_cost_per_sol": round(total_basis / total_sol, 2) if total_sol > 0 else 0.0,
        "open_lots": len(open_lots),
    }
