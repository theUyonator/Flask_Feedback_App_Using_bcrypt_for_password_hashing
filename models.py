"""Models for flash feedback"""
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to the db"""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """This model holds information on the structure of the users table in the flask_feedback db"""

    __tablename__='users'

    username = db.Column(db.String(20),
                         primary_key=True)

    password = db.Column(db.String(100),
                         nullable=False)

    email = db.Column(db.String(50),
                      nullable=False,
                      unique=True)

    first_name = db.Column(db.String(30),
                           nullable=False)

    last_name = db.Column(db.String(30),
                           nullable=False)

    feedbacks = db.relationship("Feedback", backref="user", cascade="all,delete")

    
    def __repr__(self):
        """This method shows a representation of this particular instance of the User class"""
        p = self

        return f"<username = {p.username}, email = {p.email} name = {p.full_name}>"


    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """This method registers a user with hased password and returns the user"""

        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal(unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        #return instance of User class with hashed password 
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        """Validate that the user exists and the password is correct
        
        Return user if valid, else return false
        """

        u = User.query.filter_by(username=username).first()
        

        if u and bcrypt.check_password_hash(u.password, password):
            # return user instance
            return u
        else:
            return False

    @property
    def full_name(self):
        """This method returns full name of the user"""
        p = self

        return f"{p.first_name} {p.last_name}"



class Feedback(db.Model):
    """This model holds information on the structure of the feedbacks table in the flask_feedback db"""

    __tablename__="feedbacks"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.String(100),
                      nullable=False)
                      
    content = db.Column(db.Text,
                        nullable=False)

    username = db.Column(db.String(20),
                         db.ForeignKey("users.username"),
                         nullable=False)

        