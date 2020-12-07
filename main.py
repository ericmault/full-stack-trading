from flask import Flask, render_template, jsonify, url_for, request, redirect
import sqlite3, json, jinja2
from config import ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_PAPER_BASE_URL
from datetime import date


app = Flask('__main__')

@app.route('/')
def index():

    connection = sqlite3.connect('app.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    
    if request.args:
        filter_parameter = request.args["filter"]
    else:
        filter_parameter = 0
    
    
    # if url_for('index',filter='new_intra_day_highs') == '/?filter=new_intra_day_highs':
    if filter_parameter == 'new_closing_highs':

        cursor.execute("""SELECT * FROM (
            select symbol, name, stock_id, max(close), date
            FROM stock_price join stock on stock.id = stock_price.stock_id
            group by stock_id
            order by symbol
            ) where date = ? """, (date.today().isoformat(),))
    else:
        cursor.execute("""
            SELECT id, symbol, name FROM stock ORDER BY symbol
        """)

    rows = cursor.fetchall()
    
    return render_template('index.html',rows = rows)


@app.route('/strategy/<strategy_id>')
def strategy(strategy_id):
    
    connection = sqlite3.connect('app.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    
    
    cursor.execute("""
        SELECT id, name FROM strategy
        WHERE id = ?
        """, (strategy_id,))

    strategy = cursor.fetchone()
    
    cursor.execute("""
        SELECT symbol, name FROM stock
        JOIN stock_strategy on stock_strategy.stock_id = stock.id
        WHERE strategy_id = ?
        """, (strategy_id,))
    
    rows = cursor.fetchall()
    
    return render_template('strategy.html', rows = rows, strategy = strategy)
    
@app.route('/stock/<symbol>', methods=['POST','GET'])
def stock_detail(symbol):
    
    connection = sqlite3.connect('app.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    
    if request.method == 'POST':
        strat = request.form['strategy_id']
        stonk = request.form['stock.id']
        
        cursor.execute(""" INSERT INTO stock_strategy (stock_id, strategy_id) VALUES (?,?)
                       """, (stonk, strat))
        
        connection.commit()
        
        return redirect(url_for('strategy',strategy_id = strat, stonk_var = stonk))
    else:

        cursor.execute(""" SELECT * from strategy
                    """)

        strategies = cursor.fetchall()

        cursor.execute("""
            SELECT id, symbol, name FROM stock WHERE symbol = ?
        """, (symbol,))

        rows = cursor.fetchone()
        
        
        cursor.execute("""
            SELECT *  FROM stock_price WHERE stock_id = ? ORDER BY date DESC
        """, (rows["id"],))
        
        prices = cursor.fetchall()
        
        return render_template('stock_detail.html',rows = rows, prices=prices, strategies = strategies)




if __name__ == '__main__':
    app.run(debug=True)