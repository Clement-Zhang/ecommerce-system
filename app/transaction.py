from flask import Blueprint, render_template, request, url_for, redirect, session
from services.sql.cart import Cart
from services.sql.interactive import Interactive
from services.sql.order import Order

blueprint = Blueprint("transaction", __name__)


@blueprint.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    try:
        product_ids = request.form.getlist("product_ids", type=int)
        quantities = request.form.getlist("quantities", type=int)
        mapping = list(zip(product_ids, quantities))
        Cart.update_cart(session["id"], mapping)
        return redirect(url_for("transaction.cart"))
    except Exception as e:
        print(e)
        return redirect(url_for("display.generic_error"))


@blueprint.route("/cart", methods=["GET", "POST"])
def cart():
    try:
        if request.method == "POST":
            removed = request.form.getlist("remove", type=int)
            Cart.remove_from_cart(session["id"], removed)
        products = Cart.get_cart_products(session["id"])
        total = Cart.get_cart_total(session["id"])
        return render_template("pages/cart.html", products=products, total=total)
    except Exception as e:
        print(e)
        return redirect(url_for("display.generic_error"))


@blueprint.route("/checkout")
def checkout():
    try:
        Interactive.checkout(session["id"])
        return redirect(url_for("transaction.orders"))
    except Exception as e:
        print(e)
        return redirect(url_for("display.generic_error"))


@blueprint.route("/orders", methods=["GET", "POST"])
def orders():
    try:
        if request.method == "POST":
            removed = request.form.getlist("remove", type=int)
            Order.cancel_orders(removed)
        orders = Order.get_orders(session["id"])
        return render_template("pages/orders.html", orders=orders)
    except Exception as e:
        print(e)
        return redirect(url_for("display.generic_error"))
