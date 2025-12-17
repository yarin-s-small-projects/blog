from datetime import datetime
import os
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
import requests
from forms import ContactForm, PostForm , ckeditor
from utils import send_mail 
from models import db, BlogPost
import dotenv

dotenv.load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
PASSWORD = os.getenv("PASSWORD")
RECIVER_EMAIL = os.getenv("RECIVER_EMAIL")
DB_URI = os.getenv("DB_URI")

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
Bootstrap5(app)
ckeditor.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
db.init_app(app)

with app.app_context():
    db.create_all()



@app.route('/')
def home():
    posts = BlogPost.query.all()
    return render_template("index.html" , posts=posts)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact', methods=["GET", "POST"])
def contact():  
    form  = ContactForm()
    posts = BlogPost.query.all()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        message = form.message.data
        seccess = send_mail(SENDER_EMAIL, PASSWORD, RECIVER_EMAIL, f"New message from {name}", f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}")
        if seccess:
            msg = "Message sent successfully!"
        else:
            msg = "Failed to send message."
        return render_template("index.html" , posts=posts , msg=msg)
    return render_template("contact.html", form=form)

@app.route('/new-post', methods=["GET", "POST"])
def make_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            author=form.author.data,
            body=form.body.data,
            img_url=form.img_url.data,
            date=datetime.now().strftime("%B %d, %Y") 

        )
        db.session.add(new_post)
        db.session.commit()
        return home()
    return render_template("make-post.html", form=form , is_edit=False)

@app.route('/edit-post/<int:post_id>', methods=["GET", "POST"])
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    form = PostForm(
        title=post.title,
        subtitle=post.subtitle,
        author=post.author,
        img_url=post.img_url,
        body=post.body
    )
    if form.validate_on_submit():
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.author = form.author.data
        post.img_url = form.img_url.data
        post.body = form.body.data
        db.session.commit()
        return home()
    return render_template("make-post.html", form=form, is_edit=True)

@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    post = BlogPost.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return home()

@app.route('/post/<int:post_id>')
def show_post(post_id):
    requested_post = BlogPost.query.get(post_id)
    return render_template("post.html", post=requested_post)

if __name__ == "__main__":
    app.run(debug=True)
