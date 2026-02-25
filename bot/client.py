import os
from binance.um_futures import UMFutures
from dotenv import load_dotenv

load_dotenv()

class BinanceClient:
    def __init__(self):
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.api_secret = os.getenv("BINANCE_API_SECRET")
        self.client = UMFutures(
            key=self.api_key, 
            secret=self.api_secret, 
            base_url="https://testnet.binancefuture.com"
        )

    def place_order(self, symbol, side, order_type, quantity, price=None):
        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": order_type.upper(),
            "quantity": float(quantity),
        }
        if params["type"] == "LIMIT":
            params["price"] = str(price)
            params["timeInForce"] = "GTC"
        return self.client.new_order(**params)

    # BONUS: OCO Implementation (TP/SL Pair)
    def place_oco_order(self, symbol, side, quantity, price, stop_price):
        """
        Simulates OCO by placing a Limit Order (Take Profit) and 
        a Stop Market Order (Stop Loss).
        """
        # 1. Take Profit (Limit Order)
        tp_side = "SELL" if side == "BUY" else "BUY"
        tp_order = self.place_order(symbol, tp_side, "LIMIT", quantity, price)
        
        # 2. Stop Loss (Stop Market)
        sl_params = {
            "symbol": symbol.upper(),
            "side": tp_side,
            "type": "STOP_MARKET",
            "quantity": float(quantity),
            "stopPrice": str(stop_price),
            "reduceOnly": "True" # Ensures it only closes positions
        }
        sl_order = self.client.new_order(**sl_params)
        
        return {"tp": tp_order, "sl": sl_order}
