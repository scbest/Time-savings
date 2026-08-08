"""
SOL trading signal engine.
Combines technical indicators (RSI, EMA crossover, MACD) with sentiment (Fear & Greed).
"""

import json
import urllib.request

COINGECKO_OHLC_URL = (
    "https://api.coingecko.com/api/v3/coins/solana/ohlc?vs_currency=usd&days=30"
)
FEAR_GREED_URL = "https://api.alternative.me/fng/?limit=1"


def _fetch_json(url, timeout=15):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "SOL-Trader/1.0", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def fetch_ohlcv():
    """Return list of [timestamp_ms, open, high, low, close] for SOL/USD 4h candles."""
    return _fetch_json(COINGECKO_OHLC_URL)


def fetch_fear_greed():
    """Return Fear & Greed index value (0=extreme fear, 100=extreme greed)."""
    data = _fetch_json(FEAR_GREED_URL)
    return int(data["data"][0]["value"])


# --- Technical indicators ---

def compute_rsi(closes, period=14):
    if len(closes) < period + 1:
        return None
    gains, losses = [], []
    for i in range(1, len(closes)):
        delta = closes[i] - closes[i - 1]
        gains.append(max(delta, 0.0))
        losses.append(max(-delta, 0.0))

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period

    if avg_loss == 0:
        return 100.0
    return 100 - (100 / (1 + avg_gain / avg_loss))


def compute_ema(values, period):
    """Return EMA list; length = len(values) - period + 1."""
    if len(values) < period:
        return []
    k = 2 / (period + 1)
    ema = [sum(values[:period]) / period]
    for v in values[period:]:
        ema.append(v * k + ema[-1] * (1 - k))
    return ema


def compute_macd(closes, fast=12, slow=26, signal_period=9):
    """Return (macd_value, signal_value) for the most recent candle, or (None, None)."""
    if len(closes) < slow + signal_period:
        return None, None
    ema_fast = compute_ema(closes, fast)
    ema_slow = compute_ema(closes, slow)

    # ema_fast is longer; align by offset
    offset = slow - fast
    macd_line = [ema_fast[i + offset] - ema_slow[i] for i in range(len(ema_slow))]
    if len(macd_line) < signal_period:
        return None, None

    signal_line = compute_ema(macd_line, signal_period)
    return macd_line[-1], signal_line[-1] if signal_line else None


# --- Scoring functions (each returns a value in [-1.0, 1.0]) ---

def _score_rsi(rsi):
    if rsi is None:
        return 0.0
    if rsi < 30:
        return 0.8
    if rsi < 45:
        return 0.4
    if rsi < 55:
        return 0.0
    if rsi < 70:
        return -0.4
    return -0.8


def _score_ema_crossover(closes):
    ema20 = compute_ema(closes, 20)
    ema50 = compute_ema(closes, 50)
    if len(ema20) < 2 or len(ema50) < 2:
        return 0.0

    # Align both to the same (shorter) time window
    min_len = min(len(ema20), len(ema50))
    e20 = ema20[-min_len:]
    e50 = ema50[-min_len:]

    prev_diff = e20[-2] - e50[-2]
    curr_diff = e20[-1] - e50[-1]

    if prev_diff < 0 and curr_diff >= 0:
        return 0.6   # Bullish crossover
    if prev_diff >= 0 and curr_diff < 0:
        return -0.6  # Bearish crossover
    return 0.2 if curr_diff > 0 else -0.2  # Sustained trend


def _score_macd(closes):
    macd, signal = compute_macd(closes)
    if macd is None or signal is None:
        return 0.0

    prev_macd, prev_signal = compute_macd(closes[:-1])
    if prev_macd is None or prev_signal is None:
        return 0.2 if (macd - signal) > 0 else -0.2

    prev_diff = prev_macd - prev_signal
    curr_diff = macd - signal

    if prev_diff < 0 and curr_diff >= 0:
        return 0.5   # Bullish crossover
    if prev_diff >= 0 and curr_diff < 0:
        return -0.5  # Bearish crossover
    return 0.2 if curr_diff > 0 else -0.2


def _score_fear_greed(value):
    # Contrarian: extreme readings are buy/sell signals
    if value <= 25:
        return 0.4
    if value <= 45:
        return 0.2
    if value <= 55:
        return 0.0
    if value <= 75:
        return -0.2
    return -0.4


# --- Composite signal ---

def compute_signal(ohlcv, fear_greed_value, buy_threshold=0.45, sell_threshold=-0.45):
    """
    Compute a composite buy/sell/hold signal.

    Weights: RSI 35%, EMA crossover 20%, MACD 15%, Fear & Greed 30%.
    Returns a dict with action, composite_score, current_price, and breakdown.
    """
    closes = [candle[4] for candle in ohlcv]
    current_price = closes[-1]

    rsi = compute_rsi(closes)
    rsi_score = _score_rsi(rsi)
    ema_score = _score_ema_crossover(closes)
    macd_score = _score_macd(closes)
    fg_score = _score_fear_greed(fear_greed_value)

    tech_weighted = rsi_score * 0.35 + ema_score * 0.20 + macd_score * 0.15
    sentiment_weighted = fg_score * 0.30
    composite = tech_weighted + sentiment_weighted

    if composite >= buy_threshold:
        action = "BUY"
    elif composite <= sell_threshold:
        action = "SELL"
    else:
        action = "HOLD"

    return {
        "action": action,
        "composite_score": round(composite, 4),
        "current_price": current_price,
        "breakdown": {
            "rsi": round(rsi, 2) if rsi is not None else None,
            "rsi_score": rsi_score,
            "ema_score": ema_score,
            "macd_score": macd_score,
            "fear_greed_index": fear_greed_value,
            "fear_greed_score": fg_score,
            "tech_weighted": round(tech_weighted, 4),
            "sentiment_weighted": round(sentiment_weighted, 4),
        },
    }
