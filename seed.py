"""Seed file to make sample data for the flask_feedback_db db"""

from models import db, User, Feedback
from app import app

# Create all tables

db.drop_all()
db.create_all()

# If table isn't empty, empty it 
User.query.delete()
Feedback.query.delete()


# Add users 

pete = User.register("peted9v3007", "hack9sh9q", "petedavidson@yahoo.com", "Pete", "Davidson")

Mahomes =  User.register("Mahomeboi", "TBd9g09t", "patrickmahomes@nfl.com", "Patrick", "Mahomes")


#Now we add the objects to seession, so they'll persist

db.session.add(pete)
db.session.add(Mahomes)


# To save these in the db we commit 
db.session.commit()

#Add feedbacks

petes_first = Feedback(title="Flask is really a tedious framework",
                       content="I believe flask is a very tedious framework that wants you to do everything, I don't appreciate that.",
                       username=pete.username)

petes_second = Feedback(title="Flask vs Django",
                        content="Django seems like a much better framework to use that Flask in my opinion.",
                        username=pete.username)

Mahomes_first = Feedback(title="Flask and Jinja, is there something better ?",
                         content="I heard Node.js uses another template library, I'd like to try that",
                         username=Mahomes.username)

db.session.add(petes_first)
db.session.add(petes_second)
db.session.add(Mahomes_first)

db.session.commit()



