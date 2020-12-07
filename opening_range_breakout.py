import sqlite3
from config import *
import alpaca_trade_api as tradeapi
import datetime as date


connection = sqlite3.connect('app.db')
connection.row_factory = sqlite3.Row

cursor = connection.cursor()


cursor.execute("""
               SELECT id from strategy where name = 'opening_range_breakout'
               """)

strategy_id = cursor.fetchone()['id']

print(strategy_id)


cursor.execute("""
               SELECT symbol, name from stock 
               join stock_strategy on stock_strategy.stock_id = stock.id
               where stock_strategy.strategy_id = ?
               """, (strategy_id,))


stocks = cursor.fetchall()
symbols = [stock['symbol'] for stock in stocks]

api = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, base_url=ALPACA_PAPER_BASE_URL)

current_date = date.today().isoformat()
# start_minute_bar = f"{current_date} 09:30:00-4:00"
# end_minute_bar = f"{current_date} 09:45:00-4:00"

start_minute_bar = "2020-10-29 09:30:00-4:00"
end_minute_bar = "2020-10-29 09:45:00-4:00"

for symbol in symbols:
    minute_bars = api.polygon.historic_agg_v2(symbol, 1, 'minute', _from='2020-10-29', to='2020-10-29').df
    print(symbol)
    print(minute_bars)