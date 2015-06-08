# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session, \
    flash
from functools import wraps

# create the application object
app = Flask(__name__)

app.secret_key = "my precious key"


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

# use decorators to link the function to a url
@app.route('/')
@login_required
def home():
    #return "Hello, world!"  # return a string
    return render_template("index.html")  # render a template


@app.route('/welcome')
def welcome():
    return render_template("welcome.html")  # render a template


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' \
                or request.form['password'] != 'admin':
            error = 'Invalid credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You were just logged in!')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were just logged out!')
    return redirect(url_for('welcome'))


# state the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
