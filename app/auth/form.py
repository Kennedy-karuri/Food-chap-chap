from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import Required,Email,Length,EqualTo
from ..models import User
from  wtforms import ValidationError,TextAreaField

class LoginForm(FlaskForm):
    email = StringField('Your Email Address',validators=[Required(),Email()])
    password = PasswordField('Password',validators =[Required()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    email = StringField('Your Email Address',validators=[Required(),Email()])
    username = StringField('Enter your username',validators = [Required()])
    password = PasswordField('Password',validators = [Required(),
    EqualTo('password2',message = 'Passwords must match')])
    password2 = PasswordField('Confirm Passwords',validators = [Required()])
    submit = SubmitField('Sign Up')


    def validate_email(self,data_field):
        if User.query.filter_by(email =data_field.data).first():
            raise ValidationError('Account  already exist')

    def validate_username(self,data_field):
        if User.query.filter_by(username = data_field.data).first():
            raise ValidationError('Username already exist')
class ContactForm(FlaskForm):
  name = TextAreaField("Name")
  email = TextAreaField("Email")
  subject = TextAreaField("Subject")
  message = TextAreaField("Message")
  submit = SubmitField("Send")       
