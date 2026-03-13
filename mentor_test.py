import json
import os
from mentor import MemoryClawMentor

def test_mentor():
    print("--- Starting MemoryClaw Mentor Test Mode ---")
    mentor = MemoryClawMentor()
    
    # Mock some patterns if memory is empty
    if not mentor.memory.get('patterns', {}).get('total_trades'):
        print("Initializing with mock trading data...")
        mock_patterns = {
            "total_trades": 42,
            "win_rate": 0.62,
            "favorite_tokens": ["SOL", "BTC", "PEPE"],
            "top_traded": "SOLUSDT",
            "volume_by_symbol": {"SOLUSDT": 15000, "BTCUSDT": 8000, "PEPEUSDT": 2000}
        }
        mentor.memory['patterns'].update(mock_patterns)
        mentor.save_memory()

    print("\n[1] Generating Trading Twin Report:")
    print(mentor.generate_report())

    print("\n[2] Portfolio Review (Mock/Env):")
    print(json.dumps(mentor.get_portfolio_review(), indent=2))

    print("\n[3] Logging a mock trade:")
    mock_trade = {
        "symbol": "BTCUSDT",
        "side": "BUY",
        "price": 65000,
        "amount": 0.01,
        "reason": "Strong signal from Binance Skills Hub"
    }
    print(json.dumps(mentor.log_trade(mock_trade), indent=2))

    print("\n--- Test Complete ---")

if __name__ == "__main__":
    test_mentor()
