from flask import Blueprint, render_template, request, redirect, url_for, session
from services.sql.account import Account
from services.crypto import Crypto

blueprint = Blueprint("account", __name__)


@blueprint.route("/register", methods=["GET", "POST"])
def register():
    try:
        if request.method == "GET":
            return render_template("pages/user_entry.html", title="Register", to="/register")
        else:
            account = request.form.to_dict()
            account["password"] = Crypto.hash_password(account["password"])
            if Account.add_customer(**account):
                account = Account.get_user_by_username_password(account["username"], account["password"])
                session["id"] = account["id"]
                session["username"] = account["username"]
                session["type"] = account["type"]
                return redirect(url_for("display.index"))
            else:
                return render_template("pages/user_entry.html", title="Register", to="/register_backend", message="Account already exists.")
    except Exception as e:
        print(e)
        return redirect(url_for("display.generic_error"))


@blueprint.route("/account")
def account():
    try:
        account = Account.get_user_by_id(session["id"])
        return render_template("pages/account.html", account=account)
    except Exception as e:
        print(e)
        return redirect(url_for("display.generic_error"))


@blueprint.route("/change_password", methods=["POST"])
def change_password():
    try:
        uid = session["id"]
        password = request.form.get("password")
        hashed_password = Crypto.hash_password(password)
        Account.change_password(uid, hashed_password)
        return redirect(url_for("account.account"))
    except Exception as e:
        print(e)
        return redirect(url_for("display.generic_error"))


@blueprint.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    try:
        if request.method == "GET":
            return render_template("pages/user_entry.html", title="Reset Password", to="/reset_password")
        else:
            username = request.form.get("username")
            email = request.form.get("email")
            if not Account.existing_user(username, email):
                return render_template("pages/user_entry.html", title="Reset Password", to="/reset_password", message="Username or password is incorrect. Please give the correct credentials or make a new account.")
            password = request.form.get("password")
            hashed_password = Crypto.hash_password(password)
            Account.change_password(Account.get_user_by_username_email(
                username, email)["id"], hashed_password)
            account = Account.get_user_by_username_password(username, hashed_password)
            session["id"] = account["id"]
            session["username"] = account["username"]
            return redirect(url_for("display.index"))
    except Exception as e:
        print(e)
        return redirect(url_for("display.generic_error"))


@blueprint.route("/change_fname", methods=["POST"])
def change_fname():
    try:
        uid = session["id"]
        fname = request.form.get("fname")
        Account.update_fname(uid, fname)
        return redirect(url_for("account.account"))
    except Exception as e:
        print(e)
        return redirect(url_for("display.generic_error"))


@blueprint.route("/change_lname", methods=["POST"])
def change_lname():
    try:
        uid = session["id"]
        lname = request.form.get("lname")
        Account.update_lname(uid, lname)
        return redirect(url_for("account.account"))
    except Exception as e:
        print(e)
        return redirect(url_for("display.generic_error"))


@blueprint.route("/change_email", methods=["POST"])
def change_email():
    try:
        uid = session["id"]
        email = request.form.get("email")
        Account.update_email(uid, email)
        return redirect(url_for("account.account"))
    except Exception as e:
        print(e)
        return redirect(url_for("display.generic_error"))


@blueprint.route("/change_phone", methods=["POST"])
def change_phone():
    try:
        uid = session["id"]
        phone = request.form.get("phone")
        Account.update_phone(uid, phone)
        return redirect(url_for("account.account"))
    except Exception as e:
        print(e)
        return redirect(url_for("display.generic_error"))
