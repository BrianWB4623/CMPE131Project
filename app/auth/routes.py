from flask import render_template, flash, request, redirect, url_for
from flask_login import login_user, logout_user, current_user
from . import auth_bp
from ..forms import LoginForm
from ..models import User

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or user.password_hash != form.password.data:
                flash("Invalid username or password", "error")
                return redirect(url_for("auth.login"))
            login_user(user, remember=form.remember_me.data)
            flash(f"Welcome back, {user.username}!", "success")
            return redirect(url_for("main.index"))
        else:
            flash("Please fix the errors below and try again.", "warning")
    return render_template("auth/login.html", form=form)

@auth_bp.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.index"))