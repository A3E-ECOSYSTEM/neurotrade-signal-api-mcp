#!/usr/bin/env python3
"""
NeuroTrade Signal API — MCP Server
Exposes NeuroTrade trading signals as native tools for AI coding assistants.

Setup:
  1. Get a free API key: https://rapidapi.com/cooa3e/api/neurotrade-signal
  2. Set NEUROTRADE_API_KEY=nt_xxx in your environment
  3. Add to your MCP client config (see .mcp.json at repo root)

Run directly:
  python -m mcp_server.neurotrade_mcp
"""
import os
import httpx
from mcp.server.fastmcp import FastMCP

BASE_URL = os.getenv("NEUROTRADE_BASE_URL", "http://127.0.0.1:9000")
API_KEY = os.getenv("NEUROTRADE_API_KEY", "")

SUPPORTED_SYMBOLS = [
    # Tier 1 — Majors (highest volume, tightest spreads)
    "BTC/USDT", "ETH/USDT", "SOL/USDT", "XRP/USDT", "DOGE/USDT", "BNB/USDT",
    # Tier 2 — High-cap (real movement, real volume)
    "TAO/USDT", "TRX/USDT", "WLD/USDT", "FET/USDT", "SUI/USDT", "PEPE/USDT",
    "ADA/USDT", "LTC/USDT", "LINK/USDT", "BCH/USDT", "ENA/USDT",
    # Tier 3 — Volatile movers (higher swing potential)
    "AVAX/USDT", "DOT/USDT", "AAVE/USDT", "NEAR/USDT", "TON/USDT",
    "UNI/USDT", "APT/USDT", "ARB/USDT",
]

SUPPORTED_TIMEFRAMES = ["1m", "5m", "15m", "30m", "1h", "4h", "1d"]

mcp = FastMCP(
    "neurotrade-signal-api",
    instructions=(
        "NeuroTrade Signal API gives you AI-powered crypto trading signals. "
        "Call generate_signal(symbol, timeframe) to get a directional signal with "
        "confidence, entry, TP, and SL. Use get_quota() to check your remaining calls. "
        "Freemium plan: 10 calls/month free. Upgrade at https://rapidapi.com/cooa3e/api/neurotrade-signal"
    ),
)


def _headers() -> dict:
    if not API_KEY:
        raise ValueError(
            "NEUROTRADE_API_KEY environment variable is not set. "
            "Get a free key at https://rapidapi.com/cooa3e/api/neurotrade-signal"
        )
    return {"Authorization": f"Bearer {API_KEY}"}


@mcp.tool()
async def generate_signal(symbol: str, timeframe: str = "1h") -> dict:
    """
    Generate an AI trading signal for a crypto pair.

    Args:
        symbol: Trading pair in 'BASE/QUOTE' format (e.g. 'BTC/USDT', 'ETH/USDT').
                Call list_symbols() for the full list of 25 supported pairs.
        timeframe: Candle timeframe — '1m', '5m', '15m', '30m', '1h', '4h', '1d'.
                   Default: '1h'.

    Returns a dict with:
        signal      — OPEN_LONG | OPEN_SHORT | NO_SIGNAL
        confidence  — float 0.0–1.0 (higher = stronger conviction)
        entry_price — suggested entry (may be null if market-order)
        tp          — take-profit price
        sl          — stop-loss price
        thesis      — one-sentence rationale
        reasoning   — full multi-factor breakdown
        risk_flags  — list of active risk warnings
        _quota      — remaining API calls this period
    """
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{BASE_URL}/api/v1/signals/generate",
            headers=_headers(),
            json={"symbol": symbol, "timeframe": timeframe},
        )
    if resp.status_code == 402:
        return {
            "error": "quota_exceeded",
            "message": (
                "Monthly quota reached. "
                "Upgrade at https://rapidapi.com/cooa3e/api/neurotrade-signal"
            ),
        }
    if resp.status_code == 422:
        detail = resp.json().get("detail", {})
        if isinstance(detail, dict) and detail.get("error") == "no_signal":
            return {
                "signal": "NO_SIGNAL",
                "symbol": symbol,
                "timeframe": timeframe,
                "message": detail.get("message", "No signal available yet — engine is ticking, try again shortly."),
            }
    resp.raise_for_status()
    return resp.json()


@mcp.tool()
async def get_quota() -> dict:
    """
    Check remaining API calls for the current billing period.

    Returns a dict with:
        plan            — current plan name (e.g. 'freemium', 'developer', 'pro')
        calls_used      — calls consumed this period
        calls_remaining — calls left before quota reset
        calls_limit     — total calls allowed per period
        reset_at        — ISO 8601 timestamp when quota resets
        is_active       — whether the API key is active
    """
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(
            f"{BASE_URL}/api/v1/account",
            headers=_headers(),
        )
    resp.raise_for_status()
    return resp.json()


@mcp.tool()
async def list_symbols() -> list:
    """
    List supported trading symbols.

    Returns a list of symbol strings in 'BASE/QUOTE' format.
    Use these exact strings as the 'symbol' argument to generate_signal().
    """
    return SUPPORTED_SYMBOLS


if __name__ == "__main__":
    mcp.run()
