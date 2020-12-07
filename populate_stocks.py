import sqlite3, os
import alpaca_trade_api as tradeapi
from config import ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_PAPER_BASE_URL

connection = sqlite3.connect(os.path.abspath('app.db'))
connection.row_factory = sqlite3.Row

cursor = connection.cursor()
print(os.path.abspath('app.db'))
cursor.execute("""
    SELECT symbol, name FROM stock
""")

rows = cursor.fetchall()
symbols = [row['symbol'] for row in rows] # list comprehension
print(symbols)

api = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, base_url=ALPACA_PAPER_BASE_URL) # or use ENV Vars shown below
assets = api.list_assets()


for asset in assets:
    try:

        if asset.status == 'active' and asset.tradable and asset.symbol not in symbols:
            print(f"Added new asset {asset}")
            cursor.execute("INSERT INTO stock (symbol, name, exchange) VALUES (?, ?, ?)",(asset.symbol, asset.name, asset.exchange))
    except Exception as e:
        print(asset.symbol)
        print(e)

#sample insert
# cursor.execute("INSERT INTO stock (symbol, company) VALUES ('ADBE', 'Adobe Inc.')")

connection.commit()