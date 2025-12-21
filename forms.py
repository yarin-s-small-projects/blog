import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField , PasswordField
from wtforms.validators import DataRequired, URL , Email , Length , EqualTo 
from flask_ckeditor import CKEditorField
from flask_ckeditor import CKEditor

ckeditor = CKEditor()

class ContactForm(FlaskForm):
    '''Contact Form for users to send messages'''
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    phone = StringField("Phone Number", validators=[DataRequired()])
    message = CKEditorField("Message", validators=[DataRequired()])
    submit = SubmitField("Send Message")


class PostForm(FlaskForm):
    '''Form for creating and editing blog posts'''
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")
    
class CommentForm(FlaskForm):
    '''Form for submitting comments on blog posts'''
    comment_text = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")
    
class RegisterForm(FlaskForm):
    '''User Registration Form'''
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone Number", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired() , Length(min=8)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField("Register")
    
class LoginForm(FlaskForm):
    '''User Login Form'''
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired() , Length(min=8)])
    submit = SubmitField("Login")