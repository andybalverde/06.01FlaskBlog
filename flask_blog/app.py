import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

"""
You’ll create a function that creates a database connection and return it. 
This get_db_connection() function opens a connection to the database.db database file, and then sets the row_factory attribute 
to sqlite3.Row so you can have name-based access to columns. This means that the database connection will return rows that behave 
like regular Python dictionaries. Lastly, the function returns the conn connection object you’ll be using to access the database.
"""
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
    
def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

'''Create a Flask application instance named app.
You pass the special variable __name__ that holds the name of the current Python module.
It’s used to tell the instance where it’s located, you need this because Flask sets up some paths behind the scenes.'''
app = Flask(__name__)
#The flash() function stores flashed messages in the client’s browser session, which requires setting a secret key. 
#This secret key is used to secure sessions, which allow Flask to remember information from one request to another, 
#such as moving from the new post page to the index page. The user can access the information stored in the session, 
#but cannot modify it unless they have the secret key, so you must never allow anyone to access your secret key. 
app.config['SECRET_KEY'] = 'your secret key'

'''
Once you create the app instance, you use it to handle incoming web requests and send responses to the user. 
@app.route is a decorator that turns a regular Python function into a Flask view function, which converts the function’s 
return value into an HTTP response to be displayed by an HTTP client, such as a web browser. 
You pass the value '/' to @app.route() to signify that this function will respond to web requests for the URL /, 
which is the main URL.
'''
@app.route('/') #this is a Decorator: converts Py function into Flask View Function (converts return value into http response to / url)
def index():
    """
    You first open a database connection using the get_db_connection() function you defined earlier
    """
    conn = get_db_connection()
    """
    You execute an SQL query to select all entries from the posts table. You implement the fetchall() method to fetch 
    all the rows of the query result, this will return a list of the posts you inserted into the database in the previous step.
    """
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    """
    You return the result of rendering the index.html template
    You also pass the posts object as an argument, which contains the results you got from the database, 
    this will allow you to access the blog posts in the index.html template.
    """
    return render_template('index.html', posts=posts)
'''
The index() view function returns the result of calling render_template() with index.html as an argument,
this tells render_template() to look for a file called index.html in the templates folder.
'''

'''
Flask provides a render_template() helper function that allows use of the Jinja template engine. 
This will make managing HTML much easier by writing your HTML code in .html files (in the /template folder) as well as 
using logic in your HTML code. You’ll use these HTML files, (templates) to build all of your application pages, 
such as the main page where you’ll display the current blog posts, page for adding new posts, page for editing, etc.
'''

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)



@app.route('/create', methods=('GET', 'POST'))
def create():
    '''
    After setting a secret key, you’ll create a view function that will render a template that displays 
    a form you can fill in to create a new blog post. Add this new function at the bottom of the file:
    '''
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')
#This creates a /create route that accepts both GET and POST requests. GET requests are accepted by default. 
#To also accept POST requests, which are sent by the browser when submitting forms, you’ll pass a tuple with 
#the accepted types of requests to the methods argument of the @app.route() decorator.
@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)
    
# ....

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))
#This view function only accepts POST requests. This means that navigating to the /ID/delete 
#route on your browser will return an error because web browsers default to GET requests.
#However you can access this route via a form that sends a POST request passing in the ID of 
#the post you want to delete. The function will receive the ID value and use it to get the post 
#from the database with the get_post() function.
#Then you open a database connection and execute a DELETE FROM SQL command to delete the post. 
#You commit the change to the database and close the connection while flashing a message to inform 
#the user that the post was successfully deleted and redirect them to the index page.
#Note that you don’t render a template file, this is because you’ll just add a Delete button to the edit page
if __name__ == '__main__':
    app.debug = True
    app.run()