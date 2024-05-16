from flask import Blueprint, render_template, session, redirect, url_for
from services.sql.product import Product
from services.sql.cart import Cart
from services.sql.order import Order

blueprint = Blueprint("display", __name__)


@blueprint.route("/")
def index():
    try:
        return render_template("pages/index.html")
    except Exception as e:
        print(e)
        return redirect(url_for("display.generic_error"))


@blueprint.route("/products")
def products():
    try:
        products = Product.get_products()
        if "type" in session and session["type"] == "customer":
            cart_mapping = Cart.get_cart_products(session["id"])
            cart_mapping = {product["id"]: product["quantity"] for product in cart_mapping}
        else:
            cart_mapping = None
        return render_template("pages/products.html", products=products, cart_mapping=cart_mapping)
    except Exception as e:
        print(e)
        return redirect(url_for("display.generic_error"))
    

@blueprint.route("/orders/<int:oid>")
def order(oid):
    try:
        order = Order.get_order(oid)
        products = Order.get_order_products(oid)
        return render_template("pages/order.html", products=products, order=order)
    except Exception as e:
        print(e)
        return redirect(url_for("display.generic_error"))


@blueprint.route("/generic_error")
def generic_error():
    try:
        return render_template("pages/error.html", image="error.jpg")
    except Exception as e:
        print(e)
        return redirect(url_for("display.generic_error"))
