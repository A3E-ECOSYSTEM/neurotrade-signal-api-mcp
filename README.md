# NeuroTrade Signal API: MCP Server

An MCP (Model Context Protocol) server exposing [NeuroTrade Signal API](https://neurotrade.a3eecosystem.com) as native tools for AI coding assistants. Drop it into Claude Code, Cursor, Zed, Continue, or any MCP-compatible client and your agent can generate AI-reasoned crypto trading signals inline.

## What you get

- **Directional call** per signal: `OPEN_LONG` / `OPEN_SHORT` / `CLOSE`
- **Confidence score** (0.0 to 1.0) with calibrated uncertainty
- **Entry / Take-Profit / Stop-Loss** prices with computed R:R ratio
- **Natural-language thesis** explaining the setup in plain English
- **Technical breakdown**: RSI, MACD, EMA-9/21, ATR, regime tag
- **Risk flags**: news spike aftermath, RSI extremes, low liquidity, etc.
- **Quota visibility** via `get_quota` tool

## Supported markets

25 pairs across three tiers (majors, high-cap, volatile movers): BTC, ETH, SOL, XRP, DOGE, BNB, TAO, TRX, WLD, FET, SUI, PEPE, ADA, LTC, LINK, BCH, ENA, AVAX, DOT, AAVE, NEAR, TON, UNI, APT, ARB.

Timeframes: `1m`, `5m`, `15m`, `30m`, `1h`, `4h`, `1d`.

## Install

### 1. Get an API key

Pick a plan on one of the marketplaces:

- **Zyla**: https://zylalabs.com/api-marketplace/other/neurotrade+signal+api/12432
- **RapidAPI** (legacy, still active): https://rapidapi.com/cooa3e/api/neurotrade-signal

Free tier: 10 calls/month. Paid plans from $24.99/mo.

### 2. Set the environment variable

```bash
export NEUROTRADE_API_KEY=nt_your_key_here
```

### 3. Install the package

```bash
pip install git+https://github.com/A3E-ECOSYSTEM/neurotrade-signal-api-mcp.git
```

Or clone + install for local dev:

```bash
git clone https://github.com/A3E-ECOSYSTEM/neurotrade-signal-api-mcp.git
cd neurotrade-signal-api-mcp
pip install -e .
```

### 4. Wire into your MCP client

**Claude Code** (`~/.claude/mcp.json` or project `.mcp.json`):

```json
{
  "mcpServers": {
    "neurotrade-signal": {
      "command": "python",
      "args": ["-m", "mcp_server.neurotrade_mcp"],
      "env": {
        "NEUROTRADE_API_KEY": "nt_your_key_here"
      }
    }
  }
}
```

**Cursor**: same JSON in your Cursor MCP config.
**Zed**: add to `~/.config/zed/settings.json` under `context_servers`.
**Continue**: add to `~/.continue/config.json` under `contextProviders`.

Restart your editor. The tools appear automatically.

## Tools exposed

### `generate_signal(symbol, timeframe, strategy, personality, include_thesis)`

Generates an AI-reasoned signal. Returns JSON with direction, confidence, entry, TP, SL, thesis, reasoning, technical breakdown, and risk flags.

Parameters:
- `symbol` (required): trading pair, e.g. `"BTC/USDT"`
- `timeframe` (required): `"1m"`, `"5m"`, `"15m"`, `"30m"`, `"1h"`, `"4h"`, `"1d"`
- `strategy` (optional): `"trend_rider"`, `"mean_reversion"`, `"breakout"`, `"momentum"`
- `personality` (optional): `"scalper"`, `"swing"`, `"position"`
- `include_thesis` (optional, default `true`): include LLM thesis + reasoning

### `get_quota()`

Returns your current plan, calls used, calls remaining, and reset timestamp. No arguments.

### `list_supported_symbols()`

Returns the 25-pair catalog grouped by tier.

### `list_supported_timeframes()`

Returns the 7 supported timeframes.

## Run standalone

```bash
NEUROTRADE_API_KEY=nt_xxx python -m mcp_server.neurotrade_mcp
```

Useful for debugging or as a long-running service.

## License

MIT. See `LICENSE`.

## Links

- NeuroTrade: https://neurotrade.a3eecosystem.com
- A3E Ecosystem Inc.: https://a3eecosystem.com
- Issues + feature requests: https://github.com/A3E-ECOSYSTEM/neurotrade-signal-api-mcp/issues
