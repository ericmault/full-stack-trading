import sqlite3
connection = sqlite3.connect('app.db')
cursor = connection.cursor()

# Delete Data
cursor.execute("DELETE FROM stock")
connection.commit()

# Drop table
cursor.execute("DROP TABLE stock")
connection.commit()


# Drop table
cursor.execute("DROP TABLE stock_price")
connection.commit()

# Drop table
cursor.execute("DROP TABLE strategy")
connection.commit()

# Drop table
cursor.execute("DROP TABLE stock_strategy")
connection.commit()

