import sqlite3
import alpaca_trade_api as tradeapi
from config import ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_PAPER_BASE_URL

connection = sqlite3.connect('app.db')
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute("""
    SELECT id, symbol, name FROM stock
""")

rows = cursor.fetchall()

symbols = []
stock_dict = {}

for row in rows:
    symbol = row['symbol']
    symbols.append(symbol)
    stock_dict[symbol] = row['id']


api = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, base_url=ALPACA_PAPER_BASE_URL)

chunk_size = 200
for i in range(0, len(symbols), chunk_size):
    symbol_chunk = symbols[i:i+chunk_size]
    barsets = api.get_barset(symbol_chunk, 'day')
    for symbol in barsets:
        print(f"processing symbol {symbol}")
        for bar in barsets[symbol]:
            stock_id = stock_dict[symbol]
            cursor.execute("""
                INSERT INTO stock_price (stock_id, date, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (stock_id, bar.t.date(), bar.o, bar.h, bar.l, bar.c, bar.v))
            
connection.commit()