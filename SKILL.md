---
name: memoryclaw-mentor
version: 1.0
description: Your personal on-chain AI Trading Mentor for Binance. Remembers trades, analyzes patterns, suggests strategies, and executes safe trades.
author: Built for #AIBinance
triggers: 
  - "mentor me"
  - "analyze my trades"
  - "review my portfolio"
  - "suggest strategy"
  - "execute safe trade"
  - "backtest this idea"
  - "show my trading twin"
  - "daily journal"
icon: 🧠
category: binance-trading-mentor
permissions:
  - filesystem:read
  - filesystem:write
  - network:outbound
env:
  - BINANCE_API_KEY: YOUR_BINANCE_SPOT_API_KEY_HERE
  - BINANCE_SECRET: YOUR_BINANCE_SPOT_SECRET_HERE
  - SQUARE_API_KEY: fb1330b92c6b4db9b3abe2fc5e009e1f
  - RISK_MODE: conservative          # conservative / balanced / aggressive
  - TESTNET: true                    # Set false only when ready for mainnet
---

# MemoryClaw Mentor – Your Personal Binance Trading Twin

## What it does (Full Cycle)
1. Pulls your real Binance trade history & portfolio (via spot skill)
2. Stores everything in OpenClaw long-term memory (learns YOUR style)
3. Analyzes patterns: “You over-leverage SOL during narratives – win rate drops 18%”
4. Scans live opportunities using official Binance Skills:
   - crypto-market-rank
   - meme-rush
   - trading-signal
   - query-token-audit
   - query-token-info
5. Gives clear, personalized advice + backtest
6. Executes ONLY after you say “YES” (spot skill)
7. Logs every trade in journal + (optional) auto-posts summary to Binance Square using your key

## Instructions for Agent
- **Setup**: On first run, check if `memory.json` exists. If not, greet the user and ask them to set up their `.env` with Binance keys.
- **Analysis**: When asked to "analyze trades" or "mentor me", run `python mentor.py analyze` and `python mentor.py review`. Use the output to provide personalized advice.
- **Pattern Recognition**: Use `python mentor.py report` to show the user their "Trading Twin" report, highlighting their habits.
- **Trading**: 
   - Before suggesting a trade, use Binance skills: `trading-signal` and `crypto-market-rank`.
   - Before executing, use `query-token-audit` to ensure the contract is safe.
   - **MANDATORY**: Always ask "Do you want to execute this [BUY/SELL] for [AMOUNT] [SYMBOL]?" 
   - After execution via `spot` skill, log the trade using `python mentor.py log '<trade_json>'`.
- **Journaling**: When the user asks for "daily journal", summarize the contents of `trade_journal.json`.
- **Binance Square**: After a successful winning trade or a weekly summary, offer to post a summary to Binance Square using the `SQUARE_API_KEY`.


## How to use (just chat)
- “Mentor me” → full portfolio review + suggestions
- “Analyze my last 30 trades”
- “Suggest strategy for SOL right now”
- “Execute safe 0.5% BTC buy if signal strong”
- “Show my trading twin report”

## Required Setup (Do this first)
1. Create Binance API key[](https://www.binance.com/en/my/settings/api-management)
   - Enable: “Spot & Margin Trading” + “Enable Reading”
   - Copy API Key & Secret → paste in env above
   - Start with TESTNET=true (testnet.binance.vision)
2. Your Square key is already added //added your squre api.

## Safety (Built-in Hedge-Fund Rules)
- Never executes without your “YES”
- Max 2% portfolio risk per trade
- Auto-rejects high-risk moves based on YOUR history
- Testnet mode by default
