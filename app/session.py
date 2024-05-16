from flask import Blueprint, render_template, redirect, url_for

blueprint = Blueprint("session", __name__)


@blueprint.route("/login")
def login():
    try:
        return render_template("pages/user_entry.html", title="Login", to="/login_backend")
    except Exception as e:
        print(e)
        return redirect(url_for("display.generic_error"))