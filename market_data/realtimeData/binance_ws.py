import websocket
import json
import pandas as pd

symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
timeframes = ["1m", "5m", "15m", "30m", "1h", "4h", "1d"]

def on_message(ws, message):
    data = json.loads(message)
    
 
    if "k" not in data or "s" not in data:
        print(f"ℹ  message: {data}")  
        return

    kline = data["k"]
    market_data = {
        "symbol": data["s"],
        "interval": kline["i"],
        "datetime": pd.to_datetime(kline["t"], unit="ms"),
        "open": float(kline["o"]),
        "high": float(kline["h"]),
        "low": float(kline["l"]),
        "close": float(kline["c"]),
        "volume": float(kline["v"]),
        "trade_count": int(kline["n"]),
        "vwap": (float(kline["q"]) / float(kline["v"])) if float(kline["v"]) > 0 else None  
    }

    print(f"{market_data}")

def on_error(ws, error):
    print(f"{error}")

def on_close(ws, close_status_code, close_msg):
    print("")

def on_open(ws):
    params = {
        "method": "SUBSCRIBE",
        "params": [f"{symbol.lower()}@kline_{tf}" for symbol in symbols for tf in timeframes], 
        "id": 1
    }
    ws.send(json.dumps(params))

ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws",
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)

ws.on_open = on_open
ws.run_forever()
