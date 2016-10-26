"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Rating, Movie


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    
    return render_template("homepage.html")


@app.route('/users')
def user_list():
    """Show a list of users"""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route('/register')
def register_form():
    """Show a registration form"""

    return render_template('register_form.html')


@app.route('/register', methods=['POST'])
def register_process():
    """Validates SignUp"""

    user_email = request.form.get("email_address")
    password = request.form.get("password")

    if (User.query.filter(User.email == user_email).first()):
        print 'sorry that email exists in db'
    else:
        new_user = User(email=user_email,
                        password=password)
        db.session.add(new_user)
        db.session.commit()


    return redirect('/')


@app.route('/login')
def login_form():
    """Show a login form"""

    return render_template('login_form.html')


@app.route('/login', methods=["POST"])
def login():
    """Handels Login"""

    user_email = request.form.get("email_address")
    password = request.form.get("password")

    current_user = User.query.filter(User.email == user_email, User.password == password).first()

    if current_user:
        flash("Welcome, Willkommen, Bienvenidos - You are now logged in!")
        session["user_id"] = current_user.user_id

        # log user in
        return redirect('/')
    else:
        flash("email and password didn't match any of our records") 
        return redirect('/login')

    

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run()
