# MemoryClaw Mentor – Your Personal Binance Trading Twin

MemoryClaw Mentor is an AI-powered trading companion built for the OpenClaw ecosystem. It remembers your trading history, analyzes your patterns, and helps you execute safe trades on Binance with a focus on risk management.

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   cd memoryclaw-mentor
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   - Rename `.env.example` to `.env`.
   - Add your [Binance API Key & Secret](https://www.binance.com/en/my/settings/api-management).
   - Set `TESTNET=true` for safe testing.

3. **Install as OpenClaw Skill**:
   ```bash
   openclaw skill install memoryclaw-mentor
   openclaw restart
   ```

## 🧠 Core Features

- **Trading Twin Report**: Analyzes your wins and losses to show you where your edge is (and where your bad habits are).
- **Binance Skills Integration**: Automatically pulls signals from `trading-signal`, `crypto-market-rank`, and `meme-rush`.
- **Smart Audit**: Every token is audited via `query-token-audit` before execution.
- **Trade Journal**: Every trade is logged with the reasoning behind it.
- **Binance Square**: Share your trading journey with the community.

## 🛠️ File Structure

- `SKILL.md`: The manifest that tells OpenClaw how to use this tool.
- `mentor.py`: Python logic for performance analysis and pattern recognition.
- `memory.json`: Local storage for your trading persona and habits.
- `trade_journal.json`: Your detailed trading diary.

## 🧪 Testing the Logic

You can run the built-in test to see the "Trading Twin" reporting in action:
```bash
python memoryclaw-mentor/mentor_test.py
```

---
Built for #AIBinance
