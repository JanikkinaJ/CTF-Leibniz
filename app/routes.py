from flask import Blueprint, render_template, request, redirect, session
from .models import User, Post
from . import db

main = Blueprint("main", __name__)

@main.route("/")
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("index.html", posts=posts)

@main.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session["user_id"] = user.id
            session["role"] = user.role
            session["username"] = user.username #for new navigation bar-->displayment
            return redirect("/")
        else:
            error = "Invalid username/password"

    return render_template("login.html", error=error)

#logout
@main.route("/logout")
def logout():
    session.clear() 
    return redirect("/")  

#create posts
@main.route("/create", methods=["GET", "POST"])
def create_post():
    if "user_id" not in session:
        return redirect("/login")

    error = None
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        if not title or not content:
            error = "Title and content are required"
        else:
            from .models import Post, User
            author = User.query.get(session["user_id"])
            new_post = Post(title=title, content=content, author=author)
            db.session.add(new_post)
            db.session.commit()
            return redirect("/")

    return render_template("create_posts.html", error=error)

#edit posts
@main.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    if "user_id" not in session:
        return redirect("/login")

    post = Post.query.get_or_404(post_id)

    # only author
    if session.get("user_id") != post.author.id:
        return redirect("/")

    error = None
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        if not title or not content:
            error = "Title and content are required"
        else:
            post.title = title
            post.content = content
            db.session.commit()
            return redirect("/")

    return render_template("edit_posts.html", post=post, error=error)

# delete posts
@main.route("/delete/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    if "user_id" not in session:
        return redirect("/login")

    post = Post.query.get_or_404(post_id)

    # only author and admin
    if session.get("user_id") != post.author.id and session.get("role") != "admin":
        return redirect("/")

    db.session.delete(post)
    db.session.commit()
    return redirect("/")


@main.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    return f"Welcome, {session['role']} user!"

#other routes
@main.route("/about")
def about():
    return render_template("about.html")

@main.route("/contact")
def contact():
    return render_template("contact.html")