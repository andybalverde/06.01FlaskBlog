"""You first import the sqlite3 module and then open a connection to a database file named database.db," 
which will be created once you run the Python file. """
import sqlite3

connection = sqlite3.connect('database.db')

""" 
Then you use the open() function to open the schema.sql file. Next you execute its contents using the executescript() 
method that executes multiple SQL statements at once, which will create the posts table. 
"""
with open('schema.sql') as f:
    connection.executescript(f.read())
"""
You create a Cursor object that allows you to use its execute() method to execute two INSERT SQL statements to add two blog 
posts to your posts table. Finally, you commit the changes and close the connection.
"""
cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('First Post', 'Content for the first post')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Second Post', 'Content for the second post')
            )

connection.commit()
connection.close()