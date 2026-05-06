from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from flask import jsonify
from decimal import Decimal
import os
from urllib.parse import urlparse
app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = "A126109a@@"

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
    return round(float(price_jod) * float(rate))

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

def get_db_connection():
    mysql_url = os.getenv("MYSQL_PUBLIC_URL")

    if mysql_url:
        parsed = urlparse(mysql_url)

        return mysql.connector.connect(
            host=parsed.hostname,
            user=parsed.username,
            password=parsed.password,
            database=parsed.path.lstrip("/"),
            port=parsed.port,
            connection_timeout=10,
            use_pure=True
        )

    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="A126109a@@",
        database="flower_shop",
        connection_timeout=5,
        use_pure=True
    )
def clear_coupon():
    session.pop("discount", None)
    session.pop("coupon_code", None)
    session.pop("coupon_message", None)
    session.pop("coupon_used", None)

print("starting app...")
print("app started")
# --------------------------------
# الصفحة الرئيسية

@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route('/index')
def index():
    currency = session.get('currency', 'JOD')
    lang = session.get('lang', 'en')

    db = get_db_connection()
    cursor = db.cursor(dictionary=True, buffered=True)

    cursor.execute("SELECT * FROM products WHERE category_id = 1")
    flower_products = cursor.fetchall()

    cursor.execute("SELECT * FROM products WHERE category_id = 2")
    chocolate_products = cursor.fetchall()

    cursor.execute("SELECT * FROM products WHERE category_id = 3")
    perfume_products = cursor.fetchall()

    # ✅ جيب المنتجات المفضلة للمستخدم
    favorite_ids = []
    if "user_id" in session:
        cursor.execute(
            "SELECT product_id FROM favorites WHERE user_id = %s",
            (session["user_id"],)
        )
        favorite_ids = [row["product_id"] for row in cursor.fetchall()]

    cursor.close()
    db.close()

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
        favorite_ids=favorite_ids,
        currency=currency,
        lang=lang
    )

@app.route("/signup")
def signup():
    return render_template("signup.html")
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
    db = get_db_connection()
    cursor = db.cursor(dictionary=True, buffered=True)

    cursor.execute("SELECT * FROM products WHERE category_id = 1")
    flower_products = cursor.fetchall()

    cursor.execute("SELECT * FROM products WHERE category_id = 2")
    chocolate_products = cursor.fetchall()

    cursor.execute("SELECT * FROM products WHERE category_id = 3")
    perfume_products = cursor.fetchall()

    cursor.close()
    db.close()

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

    db = get_db_connection()
    cursor = db.cursor(dictionary=True, buffered=True)

    query = "SELECT * FROM products WHERE name LIKE %s"
    cursor.execute(query, ("%" + keyword + "%",))
    products = cursor.fetchall()

    cursor.close()
    db.close()

    currency = session.get("currency", "JOD")

    for product in products:
        product["converted_price"] = convert_price(product["price"], currency)

    return render_template(
        "search_results.html",
        products=products,
        keyword=keyword,
        currency=currency
    )

@app.route('/add_order', methods=['POST'])
def add_order():
    user_id = session.get('user_id')

    name = request.form.get("name")
    price = request.form.get("price")
    phone = request.form.get("phone") or ""
    address = request.form.get("address") or ""
    payment = request.form.get("payment_method") or "cash"

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO orders 
        (user_id, total, Recipient_name, phone, address, payment_method, status)
        VALUES (%s, %s, %s, %s, %s, %s, 'Pending')
    """, (user_id, price, name, phone, address, payment))

    db.commit()   # 🔥 مهم
    cursor.close()
    db.close()    # 🔥 مهم

    return redirect(url_for('profile'))

@app.route('/delete_order/<int:order_id>')
def delete_order(order_id):
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('login'))

    db = get_db_connection()
    cursor = db.cursor()

    # أولاً احذف المنتجات/العناصر المرتبطة بهذا الطلب
    cursor.execute(
        "DELETE FROM order_items WHERE order_id=%s",
        (order_id,)
    )

    # بعدين احذف الطلب نفسه
    cursor.execute(
        "DELETE FROM orders WHERE id=%s AND user_id=%s",
        (order_id, user_id)
    )

    db.commit()

    cursor.close()
    db.close()

    return redirect(url_for('profile'))


@app.route('/add_address', methods=['POST'])
def add_address():
    user_id = session.get('user_id')

    label = request.form.get("label")
    details = request.form.get("details")

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO addresses (user_id, label, details)
        VALUES (%s, %s, %s)
    """, (user_id, label, details))

    db.commit()

    cursor.close()
    db.close()

    return redirect(url_for('profile'))

@app.route('/delete_address/<int:addr_id>')
def delete_address(addr_id):
    user_id = session.get('user_id')

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("DELETE FROM addresses WHERE id=%s AND user_id=%s", (addr_id, user_id))
    db.commit()

    cursor.close()
    db.close()

    return redirect(url_for('profile'))
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

    # الخصم يشتغل فقط إذا في coupon_code
    coupon_code = session.get("coupon_code")

    if coupon_code:
        discount = session.get("discount", 0)
    else:
        discount = 0

    discount_amount = converted_total * (discount / 100)
    final_total = converted_total - discount_amount

    return render_template(
        "cart.html",
        cart_items=cart_items,
        converted_total=round(converted_total, 2),
        discount=discount,
        discount_amount=round(discount_amount, 2),
        final_total=round(final_total, 2),
        coupon_code=coupon_code,
        currency=currency
    )

@app.route("/apply_coupon", methods=["POST"])
def apply_coupon():
    code = request.form.get("coupon", "").strip().lower()

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM coupons WHERE LOWER(code) = %s", (code,))
    coupon = cursor.fetchone()

    cursor.close()
    db.close()

    if coupon:
        session["discount"] = coupon["discount"]
        session["coupon_code"] = code
        session["coupon_used"] = True
        session["coupon_message"] = f"{coupon['discount']}% discount applied"
    else:
        session["discount"] = 0
        session.pop("coupon_code", None)
        session.pop("coupon_used", None)
        session["coupon_message"] = "Invalid coupon"

    return redirect(url_for("cart"))

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
    clear_coupon()
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

@app.route("/admin/update-order-status/<int:order_id>", methods=["POST"])
def update_order_status(order_id):
    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    status = request.form.get("status")

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("UPDATE orders SET status=%s WHERE id=%s", (status, order_id))
    db.commit()

    cursor.close()
    db.close()

    return redirect(url_for("admin_orders"))

@app.route('/update_profile', methods=['POST'])
def update_profile():
    user_id = session.get('user_id')

    db = get_db_connection()
    cursor = db.cursor()

    if request.form.get("name") or request.form.get("email") or request.form.get("phone"):
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")

        cursor.execute("""
            UPDATE users 
            SET name=%s, email=%s, Phone=%s 
            WHERE id=%s
        """, (name, email, phone, user_id))

    else:
        field = request.form.get("field")
        value = request.form.get("value")

        if field == "name":
            query = "UPDATE users SET name=%s WHERE id=%s"
        elif field == "email":
            query = "UPDATE users SET email=%s WHERE id=%s"
        elif field == "phone":
            query = "UPDATE users SET Phone=%s WHERE id=%s"
        elif field == "country":
            query = "UPDATE users SET country=%s WHERE id=%s"
        else:
            cursor.close()
            db.close()
            return "Invalid field"

        cursor.execute(query, (value, user_id))

    db.commit()
    cursor.close()
    db.close()

    return redirect(url_for('profile'))
# --------------------------------
# حذف منتج من السلة
# --------------------------------
@app.route("/remove_from_cart", methods=["POST"])
def remove_from_cart():
    name = request.form.get("name")

    if "cart" in session:
        session["cart"] = [item for item in session["cart"] if item["name"] != name]
        session.modified = True

    clear_coupon()
    return redirect(url_for("cart"))


# --------------------------------
# صفحة معلومات التوصيل
# --------------------------------
@app.route("/delivery")
def delivery():
    cart_items = session.get("cart", [])
    if not cart_items:
        return redirect(url_for("index"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True, buffered=True)

    cursor.execute("SELECT * FROM countries")
    countries = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("delivery.html", countries=countries)


# --------------------------------
# الانتقال من التوصيل إلى الدفع
# --------------------------------
@app.route("/checkout", methods=["GET", "POST"])
def checkout():

    # إذا جاي من صفحة delivery (POST)
    if request.method == "POST":
        session["Recipient_name"] = request.form.get("Recipient_name") or ""
        session["country"] = request.form.get("country") or ""
        session["country_name"] = request.form.get("country_name") or ""

        # 🔥 المهم هون (ما نخرب العملة)
        session["currency"] = request.form.get("currency") or session.get("currency", "JOD")

        session["phone"] = request.form.get("phone") or ""
        session["address"] = request.form.get("address") or ""
        session["card_message"] = request.form.get("card_message") or ""
        session["gift"] = request.form.get("gift") or "0"
        session["anonymous"] = request.form.get("anonymous") or "0"
        session["notify"] = request.form.get("notify") or "0"

    # السلة
    cart_items = session.get("cart", [])

    if not cart_items:
        return redirect(url_for("index"))

    # العملة
    currency = session.get("currency", "JOD")

    converted_total = 0

    # حساب الأسعار
    for item in cart_items:
        price = float(item["price"])
        quantity = int(item["quantity"])

        item["converted_price"] = convert_price(price, currency)
        item["converted_subtotal"] = round(item["converted_price"] * quantity, 2)

        converted_total += item["converted_subtotal"]

    # 🔥 الخصم (مربوط بالكوبون)
    coupon_code = session.get("coupon_code")

    if coupon_code:
        discount = session.get("discount", 0)
    else:
        discount = 0

    discount_amount = converted_total * (discount / 100)
    final_total = converted_total - discount_amount

    return render_template(
        "checkout.html",
        cart_items=cart_items,
        total=round(converted_total, 2),
        discount=discount,
        discount_amount=round(discount_amount, 2),
        final_total=round(final_total, 2),
        currency=currency
    )

@app.route('/change_password', methods=['POST'])
def change_password():
    user_id = session.get('user_id')

    current = request.form.get("current_password")
    new = request.form.get("new_password")

    db = get_db_connection()
    cursor = db.cursor(dictionary=True, buffered=True)

    cursor.execute("SELECT password FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    if user and user['password'] == current:
        cursor.execute("UPDATE users SET password=%s WHERE id=%s", (new, user_id))
        db.commit()

    cursor.close()
    db.close()

    return redirect(url_for('profile'))

@app.route('/delete_account')
def delete_account():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('login'))

    db = get_db_connection()
    cursor = db.cursor()

    # أولاً احذف عناصر الطلبات التابعة لطلبات هذا المستخدم
    cursor.execute("""
        DELETE FROM order_items
        WHERE order_id IN (
            SELECT id FROM orders WHERE user_id = %s
        )
    """, (user_id,))

    # بعدين احذف الطلبات
    cursor.execute("DELETE FROM orders WHERE user_id=%s", (user_id,))

    # بعدين باقي الأشياء المرتبطة بالمستخدم
    cursor.execute("DELETE FROM favorites WHERE user_id=%s", (user_id,))
    cursor.execute("DELETE FROM addresses WHERE user_id=%s", (user_id,))

    # آخر شيء احذف المستخدم نفسه
    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))

    db.commit()

    cursor.close()
    db.close()

    session.clear()

    return redirect(url_for('home'))

# --------------------------------
# تنفيذ الدفع
# --------------------------------



@app.route("/process_payment", methods=["POST"])
def process_payment():
    payment_method = request.form.get("payment_method")
    cart_items = session.get("cart", [])

    if "user_id" not in session:
        return redirect(url_for("login"))

    if not cart_items:
        return redirect(url_for("cart"))

    total = sum(float(item["price"]) * int(item["quantity"]) for item in cart_items)

    user_id = session["user_id"]

    Recipient_name = request.form.get("Recipient_name") or session.get("Recipient_name","")
    phone = request.form.get("phone") or session.get("phone","")
    address = request.form.get("address") or session.get("address","")
    phone_code = request.form.get("phone_code") or session.get("phone_code","")

    country = request.form.get("country") 
    country_phone_codes={
    "Jordan": "+962",
    "Saudi Arabia": "+966",
    "UAE": "+971",
    "Egypt": "+20",
    "Kuwait": "+965",
    "Lebanon": "+961"
    }
    phone_code = country_phone_codes.get(country,"")
    country_name = request.form.get("country_name")
    card_message = request.form.get("card_message")
    gift = request.form.get("gift")
    anonymous = request.form.get("anonymous")
    notify = request.form.get("notify")
    currency = request.form.get("currency")

    session["Recipient_name"] = Recipient_name
    session["phone"] = phone
    session["address"] = address
    session["country"] = country
    session["country_name"] = country_name
    session["card_message"] = card_message
    session["gift"] = gift
    session["anonymous"] = anonymous
    session["notify"] = notify
    session["currency"] = currency or session.get("currency", "JOD")

    db = get_db_connection()
    cursor = db.cursor(buffered=True)

    cursor.execute("""
        INSERT INTO orders (
            user_id,
            Recipient_name,
            phone,
            address,
            payment_method,
            total,
            card_messag,
            status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) """, (
        user_id,
        Recipient_name,
        phone,
        address,
        payment_method,
        total,
        card_message,
        "Pending"
    ))

    order_id = cursor.lastrowid

    for item in cart_items:
        cursor.execute("SELECT id FROM products WHERE name=%s LIMIT 1", (item["name"],))
        product = cursor.fetchone()

        if product:
            product_id = product[0]

            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, quantity)
                VALUES (%s, %s, %s)
            """, (order_id, product_id, item["quantity"]))

    db.commit()
    cursor.close()
    db.close()

    session.pop("cart", None)
    session.modified = True

    return redirect(url_for("payment_success", order_id=order_id))

@app.route("/payment_success/<int:order_id>")
def payment_success(order_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    currency = session.get("currency", "JOD")
    discount = session.get("discount", 0)

    db = get_db_connection()
    cursor = db.cursor(dictionary=True, buffered=True)

    cursor.execute("""
        SELECT orders.*, users.name, users.email
        FROM orders
        LEFT JOIN users ON orders.user_id = users.id
        WHERE orders.id = %s AND orders.user_id = %s
    """, (order_id, session["user_id"]))
    order = cursor.fetchone()

    if not order:
        cursor.close()
        db.close()
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
    db.close()

    total = 0
    for item in order_items:
        item_price = convert_price(float(item["price"]), currency)
        item["converted_price"] = item_price
        item["converted_subtotal"] = round(item_price * int(item["quantity"]), 2)
        total += item["converted_subtotal"]

    discount_amount = total * (discount / 100)
    final_total = total - discount_amount

    return render_template(
        "payment_success.html",
        order_id=order_id,
        order=order,
        order_items=order_items,
        total=round(total, 2),
        discount=discount,
        discount_amount=round(discount_amount, 2),
        final_total=round(final_total, 2),
        currency=currency
    )
@app.route("/order-status/<int:order_id>")
def order_status(order_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    currency = session.get("currency", "JOD")
    discount = session.get("discount", 0)

    db = get_db_connection()
    cursor = db.cursor(dictionary=True, buffered=True)

    cursor.execute("""
        SELECT orders.*, users.name, users.email
        FROM orders
        LEFT JOIN users ON orders.user_id = users.id
        WHERE orders.id = %s AND orders.user_id = %s
    """, (order_id, session["user_id"]))
    order = cursor.fetchone()

    if not order:
        cursor.close()
        db.close()
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
    db.close()

    total = 0
    for item in order_items:
        item_price = convert_price(float(item["price"]), currency)
        item["converted_price"] = item_price
        item["converted_subtotal"] = round(item_price * int(item["quantity"]), 2)
        total += item["converted_subtotal"]

    discount_amount = total * (discount / 100)
    final_total = total - discount_amount

    return render_template(
        "order_status.html",
        order=order,
        order_items=order_items,
        total=round(total, 2),
        discount=discount,
        discount_amount=round(discount_amount, 2),
        final_total=round(final_total, 2),
        currency=currency
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

    user_id = session["user_id"]
    lang = session.get("lang", "en")

    db = get_db_connection()
    cursor = db.cursor(dictionary=True, buffered=True)

    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    cursor.execute("""
        SELECT id, Recipient_name, total, status, created_at
        FROM orders
        WHERE user_id = %s
    """, (user_id,))
    orders = cursor.fetchall()

    cursor.execute("""
        SELECT p.id, p.name, p.price, p.image
        FROM favorites f
        JOIN products p ON f.product_id = p.id
        WHERE f.user_id = %s
    """, (user_id,))
    favorites = cursor.fetchall()

    cursor.execute("SELECT id, label, details FROM addresses WHERE user_id = %s", (user_id,))
    addresses = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "profile.html",
        user=user,
        orders=orders,
        favorites=favorites,
        addresses=addresses,
        lang=lang
    )

@app.route("/orders")
def orders():
    if "user_id" not in session:
        return redirect(url_for("login"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True, buffered=True)

    query = "SELECT * FROM orders WHERE user_id = %s ORDER BY created_at DESC"
    cursor.execute(query, (session["user_id"],))
    user_orders = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("orders.html", orders=user_orders)

# --------------------------------
# صفحات أخرى
# --------------------------------
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        db = get_db_connection()
        cursor = db.cursor(dictionary=True, buffered=True)

        query = "SELECT * FROM admins WHERE email=%s AND password=%s"
        cursor.execute(query, (email, password))
        admin = cursor.fetchone()

        cursor.close()
        db.close()

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

    db = get_db_connection()
    cursor = db.cursor(dictionary=True, buffered=True)

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
    db.close()

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

    db = get_db_connection()
    cursor = db.cursor(dictionary=True, buffered=True)

    cursor.execute("""
        SELECT products.*, categories.name AS category_name
        FROM products
        LEFT JOIN categories ON products.category_id = categories.id
        ORDER BY products.id DESC
    """)
    products = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("admin_products.html", products=products)


@app.route("/admin/add-product", methods=["GET", "POST"])
def admin_add_product():
    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True, buffered=True)

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
        db.close()

        return redirect(url_for("admin_products"))

    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("admin_add_product.html", categories=categories)

@app.route("/admin/delete-product/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
    db.commit()

    cursor.close()
    db.close()

    return redirect(url_for("admin_products"))

@app.route("/admin/orders")
def admin_orders():
    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True, buffered=True)

    cursor.execute("""
        SELECT 
            orders.*,
            users.name AS customer_name,
            users.email AS customer_email
        FROM orders
        LEFT JOIN users ON orders.user_id = users.id
        ORDER BY orders.id DESC
    """)
    orders = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("admin_orders.html", orders=orders)




@app.route("/admin/users")
def admin_users():
    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True, buffered=True)

    cursor.execute("""
        SELECT users.*,
               (SELECT COUNT(*) FROM orders WHERE orders.user_id = users.id) AS orders_count
        FROM users
        ORDER BY users.id DESC
    """)
    users = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("admin_users.html", users=users)


@app.route("/admin/delete-user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    db.commit()

    cursor.close()
    db.close()

    return redirect(url_for("admin_users"))

@app.route("/admin/messages")
def admin_messages():
    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True, buffered=True)

    cursor.execute("SELECT * FROM messages ORDER BY id DESC")
    messages = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("admin_messages.html", messages=messages)

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

    email = (request.form.get("email") or "").strip()
    password = (request.form.get("password") or "").strip()

    db = get_db_connection()
    cursor = db.cursor(dictionary=True, buffered=True)

    cursor.execute(
        "SELECT * FROM users WHERE LOWER(email)=LOWER(%s) AND password=%s",
        (email, password)
    )

    user = cursor.fetchone()

    cursor.close()
    db.close()

    if user:
        session["user_id"] = user["id"]
        session["user_name"] = user["name"]

        return redirect(url_for("index"))

    else:
        return render_template("login.html", error="Email or password is incorrect")


# --------------------------------
# إنشاء مستخدم جديد
# --------------------------------
@app.route("/create_user", methods=["POST"])
def create_user():

    first_name = (request.form.get("firstName") or "").strip()
    last_name = (request.form.get("lastName") or "").strip()

    name = first_name + " " + last_name

    email = (request.form.get("email") or "").strip()
    Phone = (request.form.get("Phone") or "").strip()
    password = (request.form.get("password") or "").strip()

    db = get_db_connection()
    cursor = db.cursor(dictionary=True, buffered=True)

    # check existing email
    cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        cursor.close()
        db.close()
        return redirect(url_for("signup", error="email_exists"))

    query = """
        INSERT INTO users (name, email, password, Phone)
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(query, (name, email, password, Phone))

    db.commit()

    cursor.close()
    db.close()

    return redirect(url_for("login"))


@app.route("/contact")
def contact():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True, buffered=True)
    
    cursor.execute("SELECT * FROM messages")
    messages = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("contact.html", messages=messages)
#روت لصفحه المسجات
@app.route("/send_message", methods=["POST"])
def send_message():
    name = request.form.get("name")
    email = request.form.get("email")
    subject= request.form.get("subject") 
    message = request.form.get("message")

    db = get_db_connection()
    cursor = db.cursor()

    query = "INSERT INTO messages (name, email,subject, message) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, email, subject, message))
    db.commit()

    cursor.close()
    db.close()

    return render_template("message_sent.html", name=name)

@app.route("/forgot-pass", methods=["GET", "POST"])
def forgot_pass():
    if request.method == "POST":
        email = request.form.get("email")
        return f"Reset link would be sent to: {email}"

    return render_template("forgot-pass.html")

@app.route("/invoice/<int:order_id>")
def invoice(order_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    currency = session.get("currency", "JOD")
    discount = session.get("discount", 0)

    db = get_db_connection()
    cursor = db.cursor(dictionary=True, buffered=True)

    cursor.execute("""
        SELECT orders.*, users.name, users.email
        FROM orders
        LEFT JOIN users ON orders.user_id = users.id
        WHERE orders.id = %s AND orders.user_id = %s
    """, (order_id, session["user_id"]))
    order = cursor.fetchone()

    if not order:
        cursor.close()
        db.close()
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
    db.close()

    total = 0
    for item in order_items:
        item_price = convert_price(float(item["price"]), currency)
        item["converted_price"] = item_price
        item["converted_subtotal"] = round(item_price * int(item["quantity"]), 2)
        total += item["converted_subtotal"]

    discount_amount = total * (discount / 100)
    final_total = total - discount_amount

    return render_template(
        "invoice.html",
        order=order,
        order_items=order_items,
        total=round(total, 2),
        discount=discount,
        discount_amount=round(discount_amount, 2),
        final_total=round(final_total, 2),
        currency=currency
    )

@app.route("/toggle_favorite/<int:product_id>", methods=["POST"])
def toggle_favorite(product_id):
    if "user_id" not in session:
        return {"success": False, "message": "Please login first"}

    user_id = session["user_id"]

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM favorites WHERE user_id=%s AND product_id=%s",
        (user_id, product_id)
    )
    fav = cursor.fetchone()

    if fav:
        cursor.execute(
            "DELETE FROM favorites WHERE user_id=%s AND product_id=%s",
            (user_id, product_id)
        )
        is_favorite = False

    else:
        cursor.execute(
            "SELECT name, price, image FROM products WHERE id=%s",
            (product_id,)
        )
        product = cursor.fetchone()

        if not product:
            cursor.close()
            db.close()
            return {"success": False, "message": "Product not found"}

        cursor.execute(
            """
            INSERT INTO favorites (user_id, product_id, name, price, image)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                user_id,
                product_id,
                product["name"],
                product["price"],
                product["image"]
            )
        )
        is_favorite = True

    db.commit()
    cursor.close()
    db.close()

    return {"success": True, "is_favorite": is_favorite}

@app.route("/delete_favorite/<int:product_id>", methods=["POST"])
def delete_favorite(product_id):
    if "user_id" not in session:
        return {"success": False, "message": "Please login first"}

    user_id = session["user_id"]

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM favorites WHERE user_id=%s AND product_id=%s",
        (user_id, product_id)
    )

    db.commit()
    cursor.close()
    db.close()

    return {"success": True}

@app.route("/add_favorite_to_cart/<int:product_id>", methods=["POST"])
def add_favorite_to_cart(product_id):
    if "user_id" not in session:
        return {"success": False, "message": "Please login first"}

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT name, price, image FROM products WHERE id=%s", (product_id,))
    product = cursor.fetchone()

    cursor.close()
    db.close()

    if not product:
        return {"success": False, "message": "Product not found"}

    cart = session.get("cart", [])

    cart.append({
        "name": product["name"],
        "price": float(product["price"]),
        "image": product["image"],
        "quantity": 1
    })

    session["cart"] = cart
    session.modified = True

    return {"success": True, "cart_count": len(cart)}
#الكوبونات
@app.route("/admin/coupons")
def admin_coupons():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM coupons")
    coupons = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("admin_coupons.html", coupons=coupons)

@app.route("/admin/coupons/add", methods=["POST"])
def add_coupon():
    code = request.form.get("code")
    discount = request.form.get("discount")

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO coupons (code, discount) VALUES (%s, %s)",
        (code, discount)
    )

    db.commit()
    cursor.close()
    db.close()

    return redirect(url_for("admin_coupons"))

@app.route("/admin/coupons/delete/<int:id>")
def delete_coupon(id):
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("DELETE FROM coupons WHERE id = %s", (id,))
    db.commit()

    cursor.close()
    db.close()

    return redirect(url_for("admin_coupons"))
#الكوبونات
# --------------------------------
# تشغيل السيرفر
# --------------------------------
print("app started")

if __name__ == "__main__":
    app.run(debug=True)

