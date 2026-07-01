from binance.client import Client
import argparse
import logging

# -------------------------------
# Binance Client Setup
# -------------------------------
class BinanceClient:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret, testnet=testnet)

    def place_order(self, symbol, side, order_type, quantity, price=None):
        if order_type == "MARKET":
            return self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=order_type,
                quantity=quantity
            )
        elif order_type == "LIMIT":
            return self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=order_type,
                timeInForce="GTC",
                quantity=quantity,
                price=price
            )

# -------------------------------
# Logging Configuration
# -------------------------------
def setup_logger():
    logging.basicConfig(
        filename="trading_bot.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger("trading_bot")

# -------------------------------
# Input Validation
# -------------------------------
def validate_order(args):
    if not args.symbol.isupper():
        raise ValueError("Symbol must be uppercase, e.g., BTCUSDT")

    if args.side not in ["BUY", "SELL"]:
        raise ValueError("Side must be BUY or SELL")

    if args.type not in ["MARKET", "LIMIT"]:
        raise ValueError("Order type must be MARKET or LIMIT")

    if args.quantity <= 0:
        raise ValueError("Quantity must be greater than 0")

    if args.type == "LIMIT" and args.price is None:
        raise ValueError("Price must be provided for LIMIT orders")

# -------------------------------
# Main CLI Logic
# -------------------------------
def main():
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot CLI")
    parser.add_argument("--symbol", required=True, help="Trading pair symbol, e.g., BTCUSDT")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"], help="Order side")
    parser.add_argument("--type", required=True, choices=["MARKET", "LIMIT"], help="Order type")
    parser.add_argument("--quantity", required=True, type=float, help="Order quantity")
    parser.add_argument("--price", type=float, help="Order price (required for LIMIT orders)")
    args = parser.parse_args()

    logger = setup_logger()
    validate_order(args)

    # Dummy keys for interview project
    api_key = "demo_key"
    api_secret = "demo_secret"

    client = BinanceClient(api_key, api_secret, testnet=True)
    try:
        response = client.place_order(args.symbol, args.side, args.type, args.quantity, args.price)
        logger.info(f"Order placed: {response}")
        print("✅ Order placed successfully!")
        print(response)
    except Exception as e:
        logger.error(f"Error placing order: {e}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
2026-07-01 21:47:31,274 - ERROR - Error placing order: APIError(code=-2014): API-key format invalid.
2026-07-01 22:00:58,140 - ERROR - Error placing order: APIError(code=-2015): Invalid API-key, IP, or permissions for action
2026-07-01 22:04:08,070 - INFO - Order placed: {'symbol': 'BTCUSDT', 'side': 'BUY', 'type': 'MARKET', 'quantity': 0.01, 'price': None, 'status': 'FILLED (mock)'}
