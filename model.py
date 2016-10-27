"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy
import correlation

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        return "User id={} email={} password={} zipcode={}".format(
        self.user_id, self.email, self.password, self.zipcode)

    def calculate_pearson(self, user2):
        """Calculates pearson similarity between two users"""

        user_ratings = {}

        paired_ratings = []

        for r in self.ratings:
            user_ratings[r.movie_id] = r.score

        for r2 in user2.ratings:
            user_score = user_ratings.get(r2.movie_id)

            if user_score is not None:
                paired_ratings.append((user_score, r2.score))

        return correlation.pearson(paired_ratings)



# Put your Movie and Rating model classes here.

class Movie(db.Model):
    """ Movie details for ratings website"""

    __tablename__ = "movies"

    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    released_at = db.Column(db.DateTime, nullable=True)
    imdb_url = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return "Movie-ID={} Title={}".format(
        self.movie_id, self.title)


class Rating(db.Model):
    """ Rating details about movies from the ratings websie """

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_id = db.Column(db.ForeignKey("movies.movie_id"))
    user_id = db.Column(db.ForeignKey("users.user_id"))
    score = db.Column(db.Integer, nullable=False)

    user = db.relationship("User", backref=db.backref("ratings", order_by=rating_id))

    movie = db.relationship("Movie", backref=db.backref("ratings", order_by=rating_id))

    def __repr__(self):
        return "Rating id={} movie_id={} user_id={} score={}".format(
        self.rating_id, self.movie_id, self.user_id, self.score)




##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
