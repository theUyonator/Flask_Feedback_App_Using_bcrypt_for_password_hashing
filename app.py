from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterUserForm, LoginUserForm, AddFeedbackForm, EditFeedbackForm
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///flask_feedback_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "feedbackloop"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)

toolbar = DebugToolbarExtension(app)

@app.route("/")
def homepage():
    """This route redirects to the '/register' route"""
    if "username" not in session:
        flash("Please register first!", "danger")
        return redirect("/register")
    flash("Welcome to flask feedback, here are all feedbacks!", "primary")
    return redirect("/feedbacks")

@app.route("/register", methods=["GET", "POST"])
def register_new_user():
    """This view function renders the register form on the GET request and registers a new user on the post request"""

    form=RegisterUserForm()
    # Check that the form data is available and validated through Flask WT-forms and add this new user to the db
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        email=form.email.data
        first_name=form.first_name.data
        last_name=form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
    # To avoid a trying to register with an existing username and our code breaking, we except the IntegrityError
    # imported from sqlalchemy on commit. This way the user is notified to pick a new username and is redirected 
    #back to the register form
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append("Username is already taken, pick another")
            return render_template("register.html", form=form)
    #To make sure that a user stays logged in after registering, the username is added to the session   
        session["username"] = new_user.username
        flash("Welcome, your account has succesffully been created", "success")
        return redirect(f"/user/{new_user.username}")

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_user():
    """This view function renders the login form on the GET request and authenticates an 
    existing user on teh post request"""

    form=LoginUserForm()
    #Check that the form data is available and has been validated on submit
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data

        user = User.authenticate(username,password)

        if user:
            flash(f"Welcome back {user.username}!", "primary")
            # Add username to the session to stay logged in
            session["username"] = user.username
            return redirect(f"/users/{session['username']}")
        else:
            # If authentication returns false, we add an error to the form to alert the user
            form.username.errors=["Invalid Username/Password"]

    return render_template("login.html", form=form)

@app.route("/users/<username>")
def user(username):
    """This renders the user.html file"""
    if "username" not in session or username != session["username"]:
        raise Unauthorized()
    else:
        user = User.query.get_or_404(username)
        return render_template("user.html", user=user)

@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):
    """This view function renders and submits a form to add user feedback"""

    if "username" not in session or username != session["username"]:
        raise Unauthorized()
    
    form=AddFeedbackForm()
    # user= User.query.get_or_404(username)

    if form.validate_on_submit():
        title=form.title.data
        content=form.content.data
        username=username

        new_feedback = Feedback(title=title, content=content, username=username)

        db.session.add(new_feedback)
        db.session.commit()

        return redirect(f"/users/{username}")

    return render_template("add_feedback.html", form=form)

@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def edit_feedback(feedback_id):
    """This view function renders and submits a form to edit user feedback"""

    feedback = Feedback.query.get_or_404(feedback_id)

    if "username" not in session or feedback.user.username != session["username"]:
        raise Unauthorized()

    form=EditFeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template("edit_feedback.html", form=form, feedback=feedback)

@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """This view function deletes feedback from the flask feedback db"""

    feedback = Feedback.query.get_or_404(feedback_id)
    if "username" not in session or feedback.user.username != session["username"]:
        raise Unauthorized()

    db.session.delete(feedback)
    db.session.commit()

    return redirect(f"/users/{feedback.user.username}")

@app.route("/feedbacks")
def show_feedbacks():
    """This view function shows all feedbacks for all users"""

    if "username" not in session:
        return redirect("/login")
    feedbacks = Feedback.query.all()

    return render_template("feedbacks.html", feedbacks=feedbacks)

@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """This view function deletes user from the db"""

    user = User.query.get_or_404(username)

    if "username" not in session or username != session["username"]:
        raise Unauthorized()

    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect(f"/register")


@app.route("/logout")
def logout_user():
    """This view function logs a user out of the app and removes the username from the session"""

    session.pop("username")
    flash("Goodbye", "info")
    return redirect("/login")