from fastapi import FastAPI
import requests, time

app = FastAPI()
FINNHUB_API_KEY = "cvmrlv9r01ql90pvrht0cvmrlv9r01ql90pvrhtg"  # Replace this with your actual key

@app.get("/get_price")
def get_price(symbol: str = "NVDA"):
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}"
    r = requests.get(url).json()
    return {"symbol": symbol, "price": r.get("c"), "high": r.get("h"), "low": r.get("l"), "previous_close": r.get("pc")}

@app.get("/get_candles")
def get_candles(symbol: str = "NVDA", resolution: str = "1", count: int = 20):
    now = int(time.time())
    seconds = {"1":60, "5":300, "15":900, "D":86400}
    start = now - count * seconds.get(resolution, 60)
    url = f"https://finnhub.io/api/v1/stock/candle?symbol={symbol}&resolution={resolution}&from={start}&to={now}&token={FINNHUB_API_KEY}"
    r = requests.get(url).json()
    if r.get("s") != "ok":
        return {"error": r}
    return {"symbol": symbol, "resolution": resolution, "count": len(r["t"]),
            "candles": [{"time": t, "open": o, "high": h, "low": l, "close": c, "volume": v}
                        for t, o, h, l, c, v in zip(r["t"], r["o"], r["h"], r["l"], r["c"], r["v"])]}
