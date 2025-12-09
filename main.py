import os
from flask import Flask, render_template, request
import requests
from post import Post
from utils import send_mail
import dotenv

dotenv.load_dotenv()

app = Flask(__name__)

BLOGS_API = os.getenv("BLOGS_API")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
PASSWORD = os.getenv("PASSWORD")
RECIVER_EMAIL = os.getenv("RECIVER_EMAIL")


blog_data = requests.get(BLOGS_API)
blog_data = blog_data.json()
posts = {}
for blog in blog_data:
    id = blog["id"]
    date = blog["date"]
    title = blog["title"]
    subtitle = blog["subtitle"]
    body = blog["body"]
    img = blog["image_url"]
    post = Post(id, title, subtitle, body, img, date)
    posts[id] = post


@app.route('/')
def home():
    return render_template("index.html" , posts=posts)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact', methods=["GET", "POST"])
def contact():  
    title = "Contact Me"
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]
        seccuss = send_mail(SENDER_EMAIL, PASSWORD, RECIVER_EMAIL, f"New message from {name}", f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}")
        if seccuss:
            title = "Successfully sent your message"
    return render_template("contact.html", posts=posts, title=title)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    requested_post = posts.get(post_id)
    return render_template("post.html", post=requested_post)

if __name__ == "__main__":
    app.run(debug=True)
