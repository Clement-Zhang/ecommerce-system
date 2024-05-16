from flask import Blueprint, redirect, url_for, session
from services.sql.account import Account
from services.sql.product import Product
from services.sql.interactive import Interactive
from services.crypto import Crypto

blueprint = Blueprint("test", __name__)


@blueprint.route("/set")
def test():
    try:
        Account.add_admin("blah", Crypto.hash_password(
            "123"), "John", "Smith", "js@yahoo.ca", "1234567890")
        # user = Account.get_user_by_username_email("blah", "js@yahoo.ca")
        # session["id"] = user["id"]
        # session["username"] = "blah"
        # session["type"] = "admin"
        Product.add_product("p1", 1.2, "p1desc", "error.jpg", 5)
        Product.add_product("p2", 1.2, "p2desc", "error.jpg", 5)
        return redirect(url_for("display.index"))
    except Exception as e:
        print(e)
        return redirect(url_for("display.generic_error"))


@blueprint.route("/reset")
def reset():
    try:
        Interactive.wipe()
        session.clear()
        return redirect(url_for("display.index"))
    except Exception as e:
        print(e)
        return redirect(url_for("display.generic_error"))
