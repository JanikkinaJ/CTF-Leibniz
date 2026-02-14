from flask import Blueprint, render_template, request, redirect, session
from .models import User, Post
from . import db

main = Blueprint("main", __name__)

@main.route("/")
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("index.html", posts=posts)

@main.route("/admin", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session["user_id"] = user.id
            session["role"] = user.role
            return redirect("/dashboard")
        else:
            error = "Invalid username/password"

    return render_template("admin.html", error=error)

#create posts as admin
@main.route("/admin/create", methods=["GET", "POST"])
def create_post():
    if "user_id" not in session or session.get("role") != "admin":
        return redirect("/admin")

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


@main.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/admin")
    return f"Welcome, {session['role']} user!"