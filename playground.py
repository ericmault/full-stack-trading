import sqlite3, os


connection = sqlite3.connect(os.path.abspath('app.db'))
# connection.row_factory = sqlite3.Row

cursor = connection.cursor()
print(os.path.abspath('app.db'))
cursor.execute("""
    SELECT symbol, name FROM stock
""")

rows = cursor.fetchall()
# symbols = [row['symbol'] for row in rows]
print(rows[0:10])