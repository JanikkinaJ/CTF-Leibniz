from flask import Blueprint, render_template, request, redirect, session
from .models import User
from . import db

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/admin", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session["user_id"] = user.id
            session["role"] = user.role
            return redirect("/dashboard")
        else:
            error = "Invalid username/password"

    return render_template("admin.html", error=error)

@main.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/admin")
    return f"Welcome, {session['role']} user!"