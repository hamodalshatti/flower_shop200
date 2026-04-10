from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from flask import jsonify
from decimal import Decimal


def convert_price(price_jod, currency):
    rates = {
        "JOD": Decimal("1"),
        "SAR": Decimal("5.29"),
        "AED": Decimal("5.18"),
        "KWD": Decimal("0.43"),
        "QAR": Decimal("5.14"),
        "BHD": Decimal("0.53")
    }

    rate = rates.get(currency, 1)

    return round (float(price_jod) * float(rate))
def get_country_from_currency(currency):
    countries = {
        "JOD": "Jordan",
        "SAR": "Saudi Arabia",
        "AED": "UAE",
        "KWD": "Kuwait",
        "QAR": "Qatar",
        "BHD": "Bahrain"
    }
    return countries.get(currency, "Jordan")

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = "A126109a@@"

print("starting app...")
print("trying to connect database...")

try:
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="A126109a@@",
        database="flower_shop",
        connection_timeout=5,
        use_pure=True
    )
    print("database connected successfully")
except Exception as e:
    print("database connection error:", e)
    raise

print("app started")
def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="A126109a@@",
        database="flower_shop",
        connection_timeout=5,
        use_pure=True
    )


    # إضافة المنتجات للطلب
    order["items"] = items
    return order
# --------------------------------
# الصفحة الرئيسية

@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route('/index')
def index():
    currency = session.get('currency', 'JOD')
    lang = session.get('lang', 'en')

    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM products WHERE category_id = 1")
    flower_products = cursor.fetchall()

    cursor.execute("SELECT * FROM products WHERE category_id = 2")
    chocolate_products = cursor.fetchall()

    cursor.execute("SELECT * FROM products WHERE category_id = 3")
    perfume_products = cursor.fetchall()

    cursor.close()

    def convert(products):
        for p in products:
            p['converted_price'] = convert_price(p['price'], currency)
        return products

    flower_products = convert(flower_products)
    chocolate_products = convert(chocolate_products)
    perfume_products = convert(perfume_products)

    return render_template(
        "index.html",
        flower_products=flower_products,
        chocolate_products=chocolate_products,
        perfume_products=perfume_products,
        currency=currency,
        lang=lang
    )

# --------------------------------
# تغيير العملة
# --------------------------------
@app.route("/set_currency", methods=["POST"])
def set_currency():
    currency = request.form.get("currency")

    if not currency:
        return "Currency not provided", 400

    session["currency"] = currency
    session["country_name"] = get_country_from_currency(currency)

    return redirect(request.referrer or url_for("index"))

#products
@app.route("/products")
def products():
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM products WHERE category_id = 1")
    flower_products = cursor.fetchall()

    cursor.execute("SELECT * FROM products WHERE category_id = 2")
    chocolate_products = cursor.fetchall()

    cursor.execute("SELECT * FROM products WHERE category_id = 3")
    perfume_products = cursor.fetchall()

    cursor.close()

    currency = session.get("currency", "JOD")

    return render_template(
        "products.html",
        flower_products=flower_products,
        chocolate_products=chocolate_products,
        perfume_products=perfume_products,
        currency=currency
    )



# --------------------------------
#@app.route("/search")
#def search():
#
#   keyword = request.args.get("q")
#  cursor = db.cursor(dictionary=True)
# query = "SELECT * FROM products WHERE name LIKE %s"
#cursor.execute(query, ("%" + keyword + "%",))
#results = cursor.fetchall()
#cursor.close()
 #return render_template("search_results.html", products=results, keyword=keyword)


@app.route("/search")
def search():
    keyword = request.args.get("q", "").strip()

    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM products WHERE name LIKE %s"
    cursor.execute(query, ("%" + keyword + "%",))
    products = cursor.fetchall()
    cursor.close()

    currency = session.get("currency", "JOD")

    for product in products:
        product["converted_price"] = convert_price(product["price"], currency)

    return render_template(
        "search_results.html",
        products=products,
        keyword=keyword,
        currency=currency
    )


# --------------------------------
# صفحة السلة
# --------------------------------
@app.route("/cart")
def cart():
    cart_items = session.get("cart", [])
    currency = session.get("currency", "JOD")

    converted_total = 0

    for item in cart_items:
        price = float(item["price"])
        quantity = int(item["quantity"])

        item["converted_price"] = convert_price(price, currency)
        item["converted_subtotal"] = round(item["converted_price"] * quantity, 2)

        converted_total += item["converted_subtotal"]

    return render_template(
        "cart.html",
        cart_items=cart_items,
        converted_total=round(converted_total, 2),
        currency=currency
    )

# --------------------------------
# إضافة منتج للسلة

@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    name = request.form.get("name")
    price = request.form.get("price")
    quantity = request.form.get("quantity", 1)
    image = request.form.get("image", "")

    try:
        price = float(price)
        quantity = int(quantity)
    except ValueError:
        price = 0
        quantity = 1

    if "cart" not in session:
        session["cart"] = []

    for item in session["cart"]:
        if item["name"] == name:
            item["quantity"] += quantity
            break
    else:
        session["cart"].append({
            "name": name,
            "price": price,
            "quantity": quantity,
            "image": image
        })

    session.modified = True
    return redirect(url_for("cart"))
# --------------------------------تعديل على الكارت عشان تزيد وتنقص
@app.route("/update_cart_quantity", methods=["POST"])
def update_cart_quantity():
    name = request.form.get("name")
    action = request.form.get("action")

    if "cart" in session:
        for item in session["cart"]:
            if item["name"] == name:
                if action == "increase":
                    item["quantity"] += 1
                elif action == "decrease":
                    item["quantity"] -= 1

                if item["quantity"] <= 0:
                    session["cart"] = [cart_item for cart_item in session["cart"] if cart_item["name"] != name]

                session.modified = True
                break

    return redirect(url_for("cart"))
# --------------------------------
# حذف منتج من السلة
# --------------------------------
@app.route("/remove_from_cart", methods=["POST"])
def remove_from_cart():
    name = request.form.get("name")

    if "cart" in session:
        session["cart"] = [item for item in session["cart"] if item["name"] != name]
        session.modified = True

    return redirect(url_for("cart"))


# --------------------------------
# صفحة معلومات التوصيل
# --------------------------------
@app.route("/delivery")
def delivery():
    cart_items = session.get("cart", [])
    if not cart_items:
        return redirect(url_for("index"))

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM countries")
    countries = cursor.fetchall()
    cursor.close()

    return render_template("delivery.html", countries=countries)


# --------------------------------
# الانتقال من التوصيل إلى الدفع
# --------------------------------
@app.route("/checkout", methods=["GET", "POST"])
def checkout():

    # إذا جاي من صفحة delivery (POST)
    if request.method == "POST":
        session["Recipient_name"] = request.form.get("Recipient_name")
        session["country_name"] = request.form.get("country_name")
        session["phone_code"] = request.form.get("phone_code")
        session["currency"] = request.form.get("currency")
        session["phone"] = request.form.get("phone")
        session["address"] = request.form.get("address")
        session["message"] = request.form.get("message")
        session["gift"] = "gift" in request.form
        session["anonymous"] = "anonymous" in request.form

    # دايماً نجيب الكارت
    cart_items = session.get("cart", [])

    # إذا السلة فاضية
    if not cart_items:
        return redirect(url_for("index"))

    currency = session.get("currency", "JOD")

    converted_total = 0

    for item in cart_items:
        price = float(item["price"])
        quantity = int(item["quantity"])

        item["converted_price"] = convert_price(price, currency)
        item["converted_subtotal"] = round(item["converted_price"] * quantity, 2)

        converted_total += item["converted_subtotal"]

    return render_template(
        "checkout.html",
        cart_items=cart_items,
        total=round(converted_total, 2),
        currency=currency
    )


# --------------------------------
# تنفيذ الدفع
# --------------------------------



@app.route("/process_payment", methods=["POST"])
def process_payment():

    #  نوع الدفع
    payment_method = request.form.get("payment_method")

    #  السلة
    cart_items = session.get("cart", [])

    #  حماية
    if "user_id" not in session:
        return redirect(url_for("login"))

    if not cart_items:
        return redirect(url_for("cart"))

    #  الحساب
    total = sum(item["price"] * item["quantity"] for item in cart_items)

    #  بيانات
    user_id = session["user_id"]
    Recipient_name = session.get("Recipient_name")
    phone = session.get("phone")
    address = session.get("address")

    cursor = db.cursor()

    #  إنشاء order
    cursor.execute("""
        INSERT INTO orders (
            user_id,
            Recipient_name,
            phone,
            address,
            payment_method,
            total,
            status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        user_id,
        Recipient_name,
        phone,
        address,
        payment_method,
        total,
        "Pending"
    ))

    #  رقم الطلب
    order_id = cursor.lastrowid

    #  إدخال المنتجات
    for item in cart_items:

        cursor.execute("SELECT id FROM products WHERE name=%s LIMIT 1", (item["name"],))
        product = cursor.fetchone()

        if product:
            product_id = product[0]

            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, quantity)
                VALUES (%s, %s, %s)
            """, (order_id, product_id, item["quantity"]))

    #  حفظ
    db.commit()
    cursor.close()

    #  حذف السلة
    session.pop("cart", None)

    # 1 تحويل
    return redirect(url_for("payment_success", order_id=order_id))
@app.route("/payment_success/<int:order_id>")
def payment_success(order_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    currency = session.get("currency", "JOD")

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT orders.*, users.name, users.email
        FROM orders
        LEFT JOIN users ON orders.user_id = users.id
        WHERE orders.id = %s AND orders.user_id = %s
    """, (order_id, session["user_id"]))
    order = cursor.fetchone()

    if not order:
        cursor.close()
        return "Order not found"

    cursor.execute("""
        SELECT order_items.quantity,
               products.name,
               products.price,
               products.image
        FROM order_items
        JOIN products ON order_items.product_id = products.id
        WHERE order_items.order_id = %s
    """, (order_id,))
    order_items = cursor.fetchall()

    cursor.close()

    total = 0
    for item in order_items:
        total += float(item["price"]) * int(item["quantity"])

    return render_template(
        "payment_success.html",
        order_id=order_id,
        order=order,
        order_items=order_items,
        total=round(total, 2),
        currency=currency
    )
@app.route("/order-status/<int:order_id>")
def order_status(order_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT orders.*, users.name, users.email
        FROM orders
        LEFT JOIN users ON orders.user_id = users.id
        WHERE orders.id = %s AND orders.user_id = %s
    """, (order_id, session["user_id"]))
    order = cursor.fetchone()

    if not order:
        cursor.close()
        return "Order not found"

    cursor.execute("""
        SELECT order_items.quantity,
               products.name,
               products.price,
               products.image
        FROM order_items
        JOIN products ON order_items.product_id = products.id
        WHERE order_items.order_id = %s
    """, (order_id,))
    order_items = cursor.fetchall()

    cursor.close()

    return render_template(
        "order_status.html",
        order=order,
        order_items=order_items
    )

 


@app.route('/set_lang', methods=['POST'])
def set_lang():
    lang = request.form.get('lang', 'en')
    session['lang'] = lang
    return redirect(request.referrer or url_for('index'))


@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))

    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE id = %s"
    cursor.execute(query, (session["user_id"],))
    user = cursor.fetchone()
    cursor.close()

    return render_template("profile.html", user=user)



@app.route("/orders")
def orders():
    if "user_id" not in session:
        return redirect(url_for("login"))

    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM orders WHERE user_id = %s ORDER BY created_at DESC"
    cursor.execute(query, (session["user_id"],))
    user_orders = cursor.fetchall()
    cursor.close()

    return render_template("orders.html", orders=user_orders)

# --------------------------------
# صفحات أخرى
# --------------------------------
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM admins WHERE email=%s AND password=%s"
        cursor.execute(query, (email, password))
        admin = cursor.fetchone()
        cursor.close()

        if admin:
            session["admin_id"] = admin["id"]
            session["admin_email"] = admin["email"]
            return redirect(url_for("admin_dashboard"))
        else:
            return "Wrong admin email or password"

    return render_template("admin_login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_id", None)
    session.pop("admin_email", None)
    return redirect(url_for("admin_login"))


@app.route("/admin/dashboard")
def admin_dashboard():
    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total_products FROM products")
    total_products = cursor.fetchone()["total_products"]

    cursor.execute("SELECT COUNT(*) AS total_orders FROM orders")
    total_orders = cursor.fetchone()["total_orders"]

    cursor.execute("SELECT COUNT(*) AS total_users FROM users")
    total_users = cursor.fetchone()["total_users"]

    cursor.execute("SELECT COUNT(*) AS new_orders FROM orders WHERE status = 'Pending'")
    new_orders = cursor.fetchone()["new_orders"]

    cursor.execute("""
        SELECT orders.id, orders.total, orders.status, users.name
        FROM orders
        LEFT JOIN users ON orders.user_id = users.id
        ORDER BY orders.id DESC
        LIMIT 5
    """)
    recent_orders = cursor.fetchall()

    cursor.close()

    return render_template(
        "admin_dashboard.html",
        total_products=total_products,
        total_orders=total_orders,
        total_users=total_users,
        new_orders=new_orders,
        recent_orders=recent_orders
    )



@app.route("/admin/products")
def admin_products():
    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT products.*, categories.name AS category_name
        FROM products
        LEFT JOIN categories ON products.category_id = categories.id
        ORDER BY products.id DESC
    """)
    products = cursor.fetchall()
    cursor.close()

    return render_template("admin_products.html", products=products)


@app.route("/admin/add-product", methods=["GET", "POST"])
def admin_add_product():
    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        name = request.form.get("name")
        price = request.form.get("price")
        image = request.form.get("image")
        description = request.form.get("description")
        stock = request.form.get("stock")
        category_id = request.form.get("category_id")

        query = """
            INSERT INTO products (name, price, image, description, stock, category_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, price, image, description, stock, category_id))
        db.commit()
        cursor.close()

        return redirect(url_for("admin_products"))

    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()
    cursor.close()

    return render_template("admin_add_product.html", categories=categories)

@app.route("/admin/delete-product/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
    db.commit()
    cursor.close()
    return redirect(url_for("admin_products"))

@app.route("/admin/orders")
def admin_orders():
    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT orders.*, users.name
        FROM orders
        LEFT JOIN users ON orders.user_id = users.id
        ORDER BY orders.id DESC
    """)
    orders = cursor.fetchall()
    cursor.close()

    return render_template("admin_orders.html", orders=orders)

    return redirect(request.referrer or url_for('index'))




@app.route("/admin/users")
def admin_users():
    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT users.*,
               (SELECT COUNT(*) FROM orders WHERE orders.user_id = users.id) AS orders_count
        FROM users
        ORDER BY users.id DESC
    """)
    users = cursor.fetchall()
    cursor.close()

    return render_template("admin_users.html", users=users)


@app.route("/admin/delete-user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    db.commit()
    cursor.close()
    return redirect(url_for("admin_users"))



@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/login")
def login():
    return render_template("login.html")

# --------------------------------
# التحقق من تسجيل الدخول
# --------------------------------
@app.route("/check_login", methods=["POST"])
def check_login():

    email = request.form.get("email")
    password = request.form.get("password")

    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users WHERE email=%s AND password=%s",
        (email, password)
    )

    user = cursor.fetchone()
    cursor.close()

    if user:
        session["user_id"] = user["id"]
        return redirect(url_for("index"))

    else:
        return "Wrong email or password"

@app.route("/signup")
def signup():
    return render_template("signup.html")


# --------------------------------
# إنشاء مستخدم جديد
# --------------------------------
@app.route("/create_user", methods=["POST"])
def create_user():

    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    cursor = db.cursor()

    query = "INSERT INTO users (name, email, password) VALUES (%s,%s,%s)"
    cursor.execute(query,(name,email,password))

    db.commit()
    cursor.close()

    return redirect(url_for("login"))


@app.route("/contact")
def contact():
    return render_template("contact.html")

#روت لصفحه المسجات
@app.route("/send_message", methods=["POST"])
def send_message():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    cursor = db.cursor()
    query = "INSERT INTO messages (name, email, message) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, email, message))
    db.commit()
    cursor.close()

    return render_template("message_sent.html", name=name)

@app.route("/forgot-pass", methods=["GET", "POST"])
def forgot_pass():
    if request.method == "POST":
        email = request.form.get("email")
        return f"Reset link would be sent to: {email}"

    return render_template("forgot-pass.html")


# --------------------------------
# تشغيل السيرفر
# --------------------------------
print("app started")

if __name__ == "__main__":
    app.run(debug=True)

