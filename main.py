from datetime import datetime
import os
from flask import Flask, abort, render_template, request , url_for, redirect, flash
from flask_bootstrap import Bootstrap5
from flask_gravatar import Gravatar
from forms import CommentForm, ContactForm, LoginForm, PostForm, RegisterForm , ckeditor
from utils import send_mail 
from models import db, BlogPost , User , Comment
import dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, login_required, current_user, logout_user

dotenv.load_dotenv()

# Load environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
PASSWORD = os.getenv("PASSWORD")
RECIVER_EMAIL = os.getenv("RECIVER_EMAIL")
DB_URI = os.getenv("DB_URI")

# Initialize Flask app and extensions
app = Flask(__name__) # Create Flask application instance
app.config['SECRET_KEY'] = SECRET_KEY # Set secret key for session management
Bootstrap5(app) # Initialize Bootstrap5 for styling
ckeditor.init_app(app) # Initialize CKEditor for rich text editing
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI # Configure database URI
db.init_app(app) # Initialize SQLAlchemy with the Flask app
login_manager = LoginManager() # Create LoginManager instance
login_manager.init_app(app) # Initialize LoginManager with the Flask app
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None) # Initialize Gravatar for user avatars

@login_manager.user_loader
def load_user(user_id):
    '''Given user_id, return the associated User object.'''
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

def admin_only(f):
    '''Decorator to restrict access to admin users only.'''
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    '''Render the home page with the latest 5 blog posts.'''
    posts = BlogPost.query.order_by(BlogPost.id.desc()).limit(5).all()
    return render_template("index.html" , posts=posts)

@app.route('/about')
@login_required
def about():
    '''Render the about page.'''
    return render_template("about.html")

@app.route('/contact', methods=["GET", "POST"])
@login_required
def contact():
    '''Render the contact page and handle contact form submissions.'''
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

################### CRUD ROUTES #####################

@app.route('/new-post', methods=["GET", "POST"])
@login_required
@admin_only
def make_post():
    '''Render the new post page and handle new blog post submissions.'''
    form = PostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            author_user=current_user,
            body=form.body.data,
            img_url=form.img_url.data,
            date=datetime.now().strftime("%B %d, %Y") 
        )
        db.session.add(new_post)
        db.session.commit()
        return home()
    return render_template("make-post.html", form=form , is_edit=False)

@app.route('/edit-post/<int:post_id>', methods=["GET", "POST"])
@login_required
@admin_only
def edit_post(post_id):
    '''Render the edit post page and handle blog post updates.'''
    post = BlogPost.query.get(post_id)
    form = PostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        body=post.body
    )
    if form.validate_on_submit():
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.author_user = current_user
        post.img_url = form.img_url.data
        post.body = form.body.data
        db.session.commit()
        return home()
    return render_template("make-post.html", form=form, is_edit=True)

@app.route('/delete/<int:post_id>' , methods=["POST"])
@login_required
@admin_only
def delete_post(post_id):
    '''Handle blog post deletion.'''
    post = BlogPost.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return home()

@app.route('/post/<int:post_id>' , methods=["GET" , "POST"])
@login_required
def show_post(post_id):
    '''Render a specific blog post and handle comment submissions.'''
    comment_form = CommentForm()
    requested_post = BlogPost.query.get(post_id)
    if comment_form.validate_on_submit():
        new_comment = Comment(
            text=comment_form.comment_text.data,
            author_user=current_user,
            post=requested_post
        )
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('show_post' , post_id=post_id))
    comments = Comment.query.filter_by(post_id=post_id).all()
    
    return render_template("post.html", post=requested_post, form=comment_form , comments=comments , gravatar=gravatar)

@app.route('/posts' , methods=["GET"])
@login_required
def post_list():
    '''Render the page with a list of all blog posts.'''
    posts = BlogPost.query.all()
    return render_template("posts.html", posts=posts)

################################ AUTHENTICATION ROUTES #####################

@app.route('/register', methods=["GET", "POST"])
def register():
    '''Render the registration page and handle new user registrations.'''
    form = RegisterForm()
    if form.validate_on_submit():
        
        if User.query.filter_by(username=form.username.data).first():
            flash("Username already exists. Please choose a different one.")
            return render_template("register.html", form=form)
        
        if User.query.filter_by(email=form.email.data).first():
            flash("Email already registered. Please log in instead.") 
            login_form = LoginForm()
            return render_template("login.html", form=login_form)
        
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)
        
        new_user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
            phone=form.phone.data,
            password=hashed_password,
            created_at=datetime.now()
        )
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        return redirect(url_for("home"))
    return render_template("register.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    '''Render the login page and handle user authentication.'''
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password. Please try again.")
            return render_template("login.html", form=form)
    return render_template("login.html", form=form)

@app.route('/logout')
@login_required
def logout():
    '''Log out the current user and redirect to the home page.'''
    logout_user()
    return redirect(url_for('home'))


if __name__ == "__main__":
    '''Run the Flask application.'''
    app.run(debug=False)
