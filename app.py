from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# ✅ MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",   # change this
    database="inventory_db"
)

cursor = db.cursor()

# ✅ Home Page - Show Products
@app.route("/")
def index():
    search = request.args.get("search")

    if search:
        cursor.execute("SELECT * FROM products WHERE name LIKE %s", ('%' + search + '%',))
    else:
        cursor.execute("SELECT * FROM products")

    products = cursor.fetchall()
    return render_template("index.html", products=products)

# ✅ Add Product Page
@app.route("/add", methods=["GET", "POST"])
def add_product():

    if request.method == "POST":
        name = request.form["name"]
        quantity = int(request.form["quantity"])
        price = float(request.form["price"])

        if not name or quantity < 0 or price < 0:
            return "Invalid input! Please enter valid data."

        cursor.execute(
            "INSERT INTO products (name, quantity, price) VALUES (%s, %s, %s)",
            (name, quantity, price)
        )
        db.commit()
        return redirect("/")

# ✅ Edit Product Page
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_product(id):
    if request.method == "POST":
        name = request.form["name"]
        quantity = request.form["quantity"]
        price = request.form["price"]

        cursor.execute(
            "UPDATE products SET name=%s, quantity=%s, price=%s WHERE id=%s",
            (name, quantity, price, id)
        )
        db.commit()
        return redirect("/")

    cursor.execute("SELECT * FROM products WHERE id=%s", (id,))
    product = cursor.fetchone()

    return render_template("edit.html", product=product)


# ✅ Delete Product
@app.route("/delete/<int:id>")
def delete_product(id):
    cursor.execute("DELETE FROM products WHERE id=%s", (id,))
    db.commit()
    return redirect("/")


# ✅ Run Flask App
if __name__ == "__main__":
    app.run(debug=True, port=8000)                                                                                                                                                        
