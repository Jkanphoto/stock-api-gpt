from fastapi import FastAPI
import requests
import time

app = FastAPI()

POLYGON_API_KEY = "TPRWamRgcZ5CH00kfkRXx163NqMvb2nl"

@app.get("/get_price")
def get_price(symbol: str = "NVDA"):
    url = f"https://api.polygon.io/v2/last/trade/stocks/{symbol}?apiKey={POLYGON_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return {
        "symbol": symbol,
        "price": data.get("results", {}).get("p"),
        "timestamp": data.get("results", {}).get("t")
    }

@app.get("/get_candles")
def get_candles(symbol: str = "NVDA", timespan: str = "minute", limit: int = 20):
    now = int(time.time())
    start = now - 60 * 60  # 1 hour ago

    url = (
        f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/{timespan}/{start*1000}/{now*1000}"
        f"?adjusted=true&sort=desc&limit={limit}&apiKey={POLYGON_API_KEY}"
    )
    response = requests.get(url)
    data = response.json()

    if "results" not in data:
        return {"error": data}

    candles = [
        {
            "time": c["t"],
            "open": c["o"],
            "high": c["h"],
            "low": c["l"],
            "close": c["c"],
            "volume": c["v"]
        } for c in data["results"]
    ]

    return {
        "symbol": symbol,
        "candles": candles
    }
