from flask import Flask, session, redirect, url_for, request, render_template
from model.account import Account as AccountModel
from services.crypto import Crypto
from services.sql.account import Account 
from app.all import blueprints


class App():
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = "dasdsahdkjsadhasjkhjkdhsajkd"
        self.account = None
        for blueprint in blueprints:
            self.app.register_blueprint(blueprint)
        self.special_routes()

    def special_routes(self):
        """Set up routes that need special handling"""
        # special handling: manipulate instance variable(s)
        self.app.add_url_rule(
            "/logout_backend", "logout_backend", self.logout_backend)
        self.app.add_url_rule("/login_backend", "login_backend",
                              self.login_backend, methods=["POST"])

    def logout_backend(self):
        try:
            account_type = session["type"]
            session.clear()
            self.account = None
            return redirect(url_for("display.index"))
        except Exception as e:
            print(e)
            return redirect(url_for("display.generic_error"))

    def login_backend(self):
        try:
            username = request.form.get("username")
            password = request.form.get("password")
            hashed_password = Crypto.hash_password(password)
            if Account.validate_user(username, hashed_password):
                account = Account.get_user_by_username_password(username, hashed_password)
                session["id"] = account["id"]
                session["username"] = username
                session["type"] = account["type"]
                self.account = AccountModel(session["id"], session["username"])
                return redirect(url_for("display.index"))
            else:
                return render_template("pages/user_entry.html", title="Login", to="/login_backend", message="Invalid username or password.")
        except Exception as e:
            print(e)
            return redirect(url_for("display.generic_error"))


if __name__ == "__main__":
    app = App()
    app.app.run(debug=True)