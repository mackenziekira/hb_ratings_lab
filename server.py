"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Rating, Movie

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound


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


@app.route('/users/<user_id>')
def user_info(user_id):
    """ Shows user age, zipcode, list of rated movies"""

    user = User.query.get(user_id)

    return render_template("user_info.html", user=user)

@app.route('/movies')
def show_movies():
    """Show a list of the movies"""
    
    movies = Movie.query.all()
    return render_template('movie_list.html', movies=movies)

@app.route('/movie/<movie_id>')
def show_movie_details(movie_id):
    """Show movie details"""

    movie = Movie.query.get(movie_id)
    return render_template('movie_details.html', movie=movie)

@app.route('/register')
def register_form():
    """Show a registration form"""

    return render_template('register_form.html')


@app.route('/register', methods=['POST'])
def register_process():
    """Validates SignUp"""

    user_email = request.form.get("email_address")
    password = request.form.get("password")

    try:
        User.query.filter(User.email == user_email).one()
        flash('That email address already exists. Please choose another.')
        return redirect('/register')
    except NoResultFound:
        new_user = User(email=user_email,
                        password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')
    except MultipleResultsFound:
        print "multiple email addresses found. corrupt db. investigate!"
        flash('That email address already exists. Please choose another.')
        return redirect('/register')


@app.route('/login')
def login_form():
    """Show a login form"""

    return render_template('login_form.html')


@app.route('/login', methods=["POST"])
def login():
    """Handles Login"""

    user_email = request.form.get("email_address")
    password = request.form.get("password")

    try:
        current_user = User.query.filter(User.email == user_email, User.password == password).one()
        flash("Welcome, Willkommen, Bienvenidos - You are now logged in!")
        session["user_id"] = current_user.user_id

        return redirect('/users/' + str(current_user.user_id))

    except NoResultFound:
        flash("email and password didn't match any of our records") 
        return redirect('/login')

@app.route('/logout')
def logout_handler():
    """Handles logout"""

    
    session.clear()
    flash("Goodbye, Auf Wiedersehen, Adieux. You are now logged out!")

    return redirect('/')

@app.route('/score-a-movie', methods=["POST"])
def score_a_movie():
    """Updates or enters a movie score, using a user's session id"""

    score = request.form.get('score')
    movie_id = request.form.get('movie_id')

    # try:
    #     get one row from ratings db based on user id and movie id
    #     if there, update ratings.score
    #     commit to db
    # except NoResultFound:
    #     insert new rating object and commit to db
    # db_score = Rating.query.filter()



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run()
