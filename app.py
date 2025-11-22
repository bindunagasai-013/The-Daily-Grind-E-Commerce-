from flask import Flask, render_template, g, redirect, url_for, session
import sqlite3, os

DATABASE = os.path.join(os.path.dirname(__file__), "daily_grind.db")

app = Flask(__name__)
app.secret_key = "secret-key"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db:
        db.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/products")
def products():
    db = get_db()
    rows = db.execute("SELECT * FROM products").fetchall()
    return render_template("products.html", products=rows)


@app.route("/add-to-cart/<int:product_id>")
def add_to_cart(product_id):
    cart = session.get("cart", {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session["cart"] = cart
    return redirect(url_for("view_cart"))


@app.route("/cart")
def view_cart():
    cart = session.get("cart", {})
    items = []
    total = 0

    if cart:
        db = get_db()
        ids = list(cart.keys())
        placeholders = ",".join(["?"] * len(ids))
        rows = db.execute(f"SELECT * FROM products WHERE id IN ({placeholders})", ids).fetchall()
        price_lookup = {str(r["id"]): r for r in rows}

        for pid, qty in cart.items():
            p = price_lookup.get(pid)
            if p:
                subtotal = p["price"] * qty
                total += subtotal
                items.append({"name": p["name"], "qty": qty, "price": p["price"], "subtotal": subtotal})

    return render_template("cart.html", items=items, total=total)


@app.route("/clear-cart")
def clear_cart():
    session.pop("cart", None)
    return redirect(url_for("products"))


if __name__ == "__main__":
    app.run(debug=True)
