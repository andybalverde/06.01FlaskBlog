"You’ll use a SQLite database file to store your data because the sqlite3 module, which we will use to interact with the database, 
is readily available in the standard Python library.
You first need to create a table called posts with the necessary columns. You’ll create a .sql file that contains SQL commands to 
create the posts table with a few columns. You’ll then use this file to create the database."
DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);
"Now that you have a SQL schema in the schema.sql file, you’ll use it to create the database using a Python file that will 
generate an SQLite .db database file, create a init_db.py file inside the flask_blog directory
There you open schema.sql and execute its contents using executescript(), which creates the posts table"