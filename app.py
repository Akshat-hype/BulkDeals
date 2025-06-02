from flask import Flask, request, jsonify
import pandas as pd
from datetime import datetime, timedelta
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})


bulk_deals_df = pd.read_csv("bulk_deals.csv")
bulk_deals_df.columns = bulk_deals_df.columns.str.strip()  

shares_df = pd.read_csv("outstanding_shares.csv")
shares_df.columns = shares_df.columns.str.strip()
shares_dict = dict(zip(shares_df['symbol'], shares_df['outstanding_shares']))


def is_hft(deal_row):
    volume = deal_row['deal_volume']
    time_diff = deal_row.get('time_diff_minutes', 0)
    return time_diff < 5 or volume < 50000


@app.route("/bulk-deals", methods=["GET"])
@cache.cached(timeout=300)
def get_bulk_deals():
    
    min_pct_volume = float(request.args.get("min_volume", 1.0))

    
    bulk_deals_df['deal_date'] = pd.to_datetime(bulk_deals_df['DATE'], errors='coerce')
    cutoff = datetime.now() - timedelta(days=30)
    recent_deals = bulk_deals_df[bulk_deals_df['deal_date'] >= cutoff]

    results = []

    for _, row in recent_deals.iterrows():
        symbol = row['symbol']
        deal_volume = row['deal_volume']

        if symbol not in shares_dict:
            continue  

        outstanding = shares_dict[symbol]
        volume_pct = (deal_volume / outstanding) * 100

        if volume_pct <= min_pct_volume:
            continue  

        result = {
            "symbol": symbol,
            "deal_date": row['deal_date'].strftime('%Y-%m-%d'),
            "deal_volume": deal_volume,
            "volume_percentage": round(volume_pct, 2),
            "buyer": row.get("buyer", "N/A"),
            "is_hft_filtered": is_hft(row),
            "position": row.get("position", "BUY")
        }
        results.append(result)

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
