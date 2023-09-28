from flask_wtf import (
    FlaskForm, 
    StringField, 
    SubmitField, 
    PasswordField, 
    validators
    )

class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=20)])
    password = PasswordField('Password', 
                             [validators.DataRequired(),
                             validators.EqualTo('confirm', message='Passwords must match')
                             ])
    
    