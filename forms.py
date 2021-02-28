from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email


class RegisterUserForm(FlaskForm):
    """This class handles the registration of new users"""

    username = StringField("Username",
                        validators=[InputRequired(message="Please Enter Username"), Length(min=6, max=20, message="Username not long enough")])

    password = PasswordField("Password",
                           validators=[InputRequired(message="Please Enter Password"), Length(min=6, max=25, message="Password too short")])

    email = StringField("email",
                            validators=[InputRequired(message="Please Enter Valid Email Address"), 
                                        Email(),
                                        Length(max=50)])

    first_name = StringField("First name",
                        validators=[InputRequired(message="Please Enter First Name"), Length(min=2, max=30)])

    last_name = StringField("Last Name",
                       validators=[InputRequired(message="Please Enter Last Name"), Length(min=2, max=30)])


class LoginUserForm(FlaskForm):
    """This class handles the login of an existing user"""
    
    username = StringField("Username",
                        validators=[InputRequired(message="Please Enter Username"), Length(min=6, max=20, message="Username not long enough")])

    password = PasswordField("Password",
                           validators=[InputRequired(message="Please Enter Password"), Length(min=6, max=25, message="Password too short")])



class AddFeedbackForm(FlaskForm):
    """This class handles the addition of a feedback by a user"""

    title = StringField("Title",
                        validators=[InputRequired(message="Please Enter Feedback Title"), Length(max=100)])

    content = StringField("Content",
                          validators=[InputRequired(message="Please Enter Content")])

class EditFeedbackForm(FlaskForm):
    """This class handles the editing of a feedback by a user"""

    title = StringField("Title",
                        validators=[InputRequired(message="Please Enter Feedback Title"), Length(max=100)])

    content = StringField("Content",
                          validators=[InputRequired(message="Please Enter Content")])
    
