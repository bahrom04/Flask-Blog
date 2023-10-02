from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from webapp.models import Accounts

class RegistrationForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = Accounts.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')
        

    username = StringField(label='Username', validators=[Length(min=4, max=25), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create account')


class LoginForm(FlaskForm):
    username = StringField(label='Username',validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Login')




    
    