import sqlite3

connection = sqlite3.connect('app.db')

cursor = connection.cursor()

#create stock table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock (
        id INTEGER PRIMARY KEY, 
        symbol TEXT NOT NULL UNIQUE, 
        name TEXT NOT NULL,
        exchange TEXT NOT NULL
    )
""")

#create stock price table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_price (
        id INTEGER PRIMARY KEY, 
        stock_id INTEGER,
        date NOT NULL,
        open NOT NULL, 
        high NOT NULL, 
        low NOT NULL, 
        close NOT NULL, 
        volume NOT NULL,
        FOREIGN KEY (stock_id) REFERENCES stock (id)
    )
""")

#create strategy table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS strategy (
        id INTEGER PRIMARY KEY,  
        name NOT NULL
    )
""")

#create stock_strategy table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_strategy (
        stock_id INTEGER PRIMARY KEY,  
        strategy_id INTEGER NOT NULL,
        FOREIGN KEY (stock_id) REFERENCES stock (id),
        FOREIGN KEY (strategy_id) REFERENCES strategy (id)
    )
""")


#create records for strategy table
strategies = ['opening_range_breakout','opening_range_breakdown']

for strategy in strategies:
    cursor.execute("""
                   INSERT INTO strategy (name) VALUES (?)
                   """,(strategy,))

connection.commit()

#create crypto table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS crypto (
        id INTEGER PRIMARY KEY, 
        symbol TEXT NOT NULL UNIQUE, 
        name TEXT NOT NULL
    )
""")

#create crypto price table --- need to update schema when downloading data
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS crypto_price (
#         id INTEGER PRIMARY KEY, 
#         stock_id INTEGER,
#         date NOT NULL,
#         open NOT NULL, 
#         high NOT NULL, 
#         low NOT NULL, 
#         close NOT NULL, 
#         adjusted_close NOT NULL, 
#         volume NOT NULL,
#         FOREIGN KEY (stock_id) REFERENCES stock (id)
#     )
# """)



connection.commit()