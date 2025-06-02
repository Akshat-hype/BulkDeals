import yfinance as yf
import csv

def get_estimated_outstanding_shares(symbol):
    ticker = yf.Ticker(symbol + ".NS")
    info = ticker.info
    try:
        market_cap = info['marketCap']
        price = info['previousClose']
        shares = int(market_cap / price)
        return shares
    except Exception as e:
        print(f"Failed for {symbol}: {e}")
        return None

# Input symbols (you can expand this list)
symbols = ['TATAMOTORS', 'RELIANCE', 'TCS']

# Save to CSV
with open('outstanding_shares.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['symbol', 'outstanding_shares'])

    for s in symbols:
        shares = get_estimated_outstanding_shares(s)
        if shares:
            writer.writerow([s, shares])
