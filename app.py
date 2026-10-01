from bottle import Bottle, request, response, template, redirect, static_file
from datetime import datetime
import json
import re

from database import get_connection, create_tables, seed_sample_data, BLOOD_GROUPS
from auth import hash_password, verify_password, login_user, logout_user, current_user_id, require_login

app = Bottle()

BASE_DIR = __import__("pathlib").Path(__file__).resolve().parent

def render(page, **kwargs):
    # Bottle looks for .tpl files in this directory.
    import bottle
    old_path = bottle.TEMPLATE_PATH[:]
    bottle.TEMPLATE_PATH.insert(0, str(BASE_DIR / "views"))
    try:
        return template(page, **kwargs)
    finally:
        bottle.TEMPLATE_PATH[:] = old_path

def valid_email(email):
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email or ""))

def form_value(name):
    return request.forms.get(name, "").strip()

def common_context():
    # Authentication for this demo uses a secure-ish HttpOnly cookie.
    # Read it here so the navigation bar knows whether the visitor is logged in.
    uid = request.get_cookie("lifedrop_user_id")
    try:
        uid = int(uid) if uid else None
    except ValueError:
        uid = None
    return {
        "user_id": uid,
        "blood_groups": BLOOD_GROUPS,
    }

@app.route("/static/<filepath:path>")
def server_static(filepath):
    return static_file(filepath, root=str(BASE_DIR / "static"))

@app.get("/")
def home():
    conn = get_connection()
    stats = {
        "donors": conn.execute("SELECT COUNT(*) FROM donors").fetchone()[0],
        "banks": conn.execute("SELECT COUNT(*) FROM blood_banks").fetchone()[0],
        "units": conn.execute("SELECT COALESCE(SUM(units),0) FROM blood_inventory").fetchone()[0],
        "donations": conn.execute("SELECT COUNT(*) FROM donations WHERE status='Completed'").fetchone()[0],
    }
    conn.close()
    return render("index", **common_context(), stats=stats)

@app.get("/register")
def register_page():
    return render("register", **common_context(), error=None)

@app.post("/register")
def register():
    name = form_value("full_name")
    email = form_value("email").lower()
    phone = form_value("phone")
    password = request.forms.get("password", "")
    confirm = request.forms.get("confirm_password", "")
    gender = form_value("gender")
    dob = form_value("date_of_birth")
    city = form_value("city")
    state = form_value("state")

    if not all([name, email, password, confirm, city, state]):
        return render("register", **common_context(), error="Please fill all required fields.")
    if not valid_email(email):
        return render("register", **common_context(), error="Please enter a valid email.")
    if password != confirm:
        return render("register", **common_context(), error="Passwords do not match.")
    if len(password) < 6:
        return render("register", **common_context(), error="Password must contain at least 6 characters.")

    conn = get_connection()
    try:
        conn.execute("""
            INSERT INTO users
            (full_name,email,phone,password_hash,gender,date_of_birth,city,state,created_at)
            VALUES (?,?,?,?,?,?,?,?,?)
        """, (name,email,phone,hash_password(password),gender,dob,city,state,
              datetime.now().isoformat(timespec="seconds")))
        conn.commit()
    except Exception as exc:
        conn.close()
        if "UNIQUE constraint failed" in str(exc):
            return render("register", **common_context(), error="Email already registered.")
        return render("register", **common_context(), error="Could not create account.")
    conn.close()
    redirect("/login?registered=1")

@app.get("/login")
def login_page():
    message = "Registration successful. Please log in." if request.query.registered else None
    return render("login", **common_context(), error=None, message=message)

@app.post("/login")
def login():
    email = form_value("email").lower()
    password = request.forms.get("password", "")
    conn = get_connection()
    user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
    conn.close()
    if not user or not verify_password(password, user["password_hash"]):
        return render("login", **common_context(), error="Invalid email or password.", message=None)
    # Bottle's request.environ lasts for the request only, so use a cookie for this demo.
    response.set_cookie("lifedrop_user_id", str(user["id"]), path="/", httponly=True, samesite="lax")
    redirect("/dashboard")

@app.get("/logout")
def logout():
    response.delete_cookie("lifedrop_user_id", path="/")
    redirect("/")

# Cookie-aware user helpers
def cookie_user_id():
    value = request.get_cookie("lifedrop_user_id")
    try:
        return int(value) if value else None
    except ValueError:
        return None

def logged_user():
    uid = cookie_user_id()
    if not uid:
        return None
    conn = get_connection()
    user = conn.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()
    conn.close()
    return user

@app.get("/dashboard")
def dashboard():
    user = logged_user()
    if not user:
        redirect("/login")
    conn = get_connection()
    donor = conn.execute("SELECT * FROM donors WHERE user_id=?", (user["id"],)).fetchone()
    requests = conn.execute("""
        SELECT * FROM blood_requests WHERE user_id=? ORDER BY id DESC LIMIT 5
    """, (user["id"],)).fetchall()
    conn.close()
    return render("dashboard", **common_context(), user=user, donor=donor, requests=requests)

@app.get("/donate")
def donate_page():
    user = logged_user()
    if not user:
        redirect("/login")
    return render("donor_register", **common_context(), user=user, error=None)

@app.post("/donate")
def donate():
    user = logged_user()
    if not user:
        redirect("/login")
    data = {
        "blood_group": form_value("blood_group"),
        "gender": form_value("gender"),
        "date_of_birth": form_value("date_of_birth"),
        "phone": form_value("phone"),
        "email": form_value("email"),
        "city": form_value("city"),
        "state": form_value("state"),
        "address": form_value("address"),
        "last_donation_date": form_value("last_donation_date"),
        "availability_status": form_value("availability_status"),
    }
    if data["blood_group"] not in BLOOD_GROUPS:
        return render("donor_register", **common_context(), user=user, error="Select a valid blood group.")
    conn = get_connection()
    existing = conn.execute("SELECT id FROM donors WHERE user_id=?", (user["id"],)).fetchone()
    if existing:
        conn.execute("""
            UPDATE donors SET blood_group=?,gender=?,date_of_birth=?,phone=?,email=?,
            city=?,state=?,address=?,last_donation_date=?,availability_status=?
            WHERE user_id=?
        """, (*data.values(), user["id"]))
    else:
        conn.execute("""
            INSERT INTO donors
            (user_id,blood_group,gender,date_of_birth,phone,email,city,state,address,
             last_donation_date,availability_status,created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """, (user["id"], *data.values(), datetime.now().isoformat(timespec="seconds")))
    conn.commit()
    conn.close()
    redirect("/dashboard")

@app.get("/donor-profile")
def donor_profile():
    user = logged_user()
    if not user:
        redirect("/login")
    conn = get_connection()
    donor = conn.execute("SELECT * FROM donors WHERE user_id=?", (user["id"],)).fetchone()
    conn.close()
    return render("donor_profile", **common_context(), user=user, donor=donor)

@app.get("/find-blood")
def find_blood():
    return render("find_blood", **common_context(), donors=[], searched=False)

@app.get("/find-donors")
def find_donors():
    blood_group = form_value("blood_group") if request.method == "POST" else request.query.blood_group.strip()
    city = request.query.city.strip()
    state = request.query.state.strip()
    sql = "SELECT * FROM donors WHERE availability_status='Available'"
    params = []
    if blood_group:
        sql += " AND blood_group=?"
        params.append(blood_group)
    if city:
        sql += " AND LOWER(city)=LOWER(?)"
        params.append(city)
    if state:
        sql += " AND LOWER(state)=LOWER(?)"
        params.append(state)
    sql += " ORDER BY city, full_name" if False else " ORDER BY city, name"
    # donors has no name column; join users for donor name.
    sql = """SELECT donors.*, users.full_name FROM donors
             LEFT JOIN users ON users.id=donors.user_id
             WHERE donors.availability_status='Available'"""
    params = []
    if blood_group:
        sql += " AND donors.blood_group=?"; params.append(blood_group)
    if city:
        sql += " AND LOWER(donors.city)=LOWER(?)"; params.append(city)
    if state:
        sql += " AND LOWER(donors.state)=LOWER(?)"; params.append(state)
    sql += " ORDER BY donors.city, users.full_name"
    conn = get_connection()
    donors = conn.execute(sql, params).fetchall()
    conn.close()
    return render("find_blood", **common_context(), donors=donors, searched=True)

@app.get("/blood-banks")
def blood_banks():
    city = request.query.city.strip()
    state = request.query.state.strip()
    group = request.query.blood_group.strip()
    conn = get_connection()
    sql = """
        SELECT b.*, COALESCE(SUM(CASE WHEN i.blood_group=? THEN i.units ELSE 0 END),0) AS requested_group_units,
               COALESCE(SUM(i.units),0) AS total_units
        FROM blood_banks b LEFT JOIN blood_inventory i ON b.id=i.blood_bank_id
        WHERE 1=1
    """
    params = [group]
    if city:
        sql += " AND LOWER(b.city)=LOWER(?)"; params.append(city)
    if state:
        sql += " AND LOWER(b.state)=LOWER(?)"; params.append(state)
    sql += " GROUP BY b.id ORDER BY b.city,b.name"
    banks = conn.execute(sql, params).fetchall()
    conn.close()
    return render("blood_banks", **common_context(), banks=banks, searched=bool(city or state or group), selected_group=group)

@app.get("/blood-availability")
def blood_availability():
    conn = get_connection()
    rows = conn.execute("""
        SELECT blood_group, SUM(units) AS units
        FROM blood_inventory GROUP BY blood_group
    """).fetchall()
    availability = {r["blood_group"]: r["units"] for r in rows}
    conn.close()
    return render("blood_availability", **common_context(), availability=availability)

@app.get("/request-blood")
def request_blood_page():
    user = logged_user()
    if not user:
        redirect("/login")
    return render("request_blood", **common_context(), user=user, error=None, success=None)

@app.post("/request-blood")
def request_blood():
    user = logged_user()
    if not user:
        redirect("/login")
    data = (
        form_value("patient_name"), form_value("blood_group"),
        request.forms.get("units_required","0"), form_value("hospital_name"),
        form_value("hospital_address"), form_value("city"), form_value("state"),
        form_value("contact_number"), form_value("required_date"),
        form_value("emergency_level"), form_value("additional_information")
    )
    try:
        units = int(data[2])
    except ValueError:
        units = 0
    if not data[0] or data[1] not in BLOOD_GROUPS or units <= 0:
        return render("request_blood", **common_context(), user=user, error="Enter valid patient, blood group, and units.", success=None)
    conn = get_connection()
    conn.execute("""
        INSERT INTO blood_requests
        (user_id,patient_name,blood_group,units_required,hospital_name,hospital_address,
         city,state,contact_number,required_date,emergency_level,additional_information,
         status,created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (user["id"], data[0], data[1], units, *data[3:],
          "Pending", datetime.now().isoformat(timespec="seconds")))
    conn.commit()
    conn.close()
    return render("request_blood", **common_context(), user=user, error=None,
                  success="Blood request submitted successfully.")

@app.get("/donation-history")
def donation_history():
    user = logged_user()
    if not user:
        redirect("/login")
    conn = get_connection()
    rows = conn.execute("""
        SELECT d.*, b.name AS bank_name
        FROM donations d JOIN donors dn ON dn.id=d.donor_id
        JOIN blood_banks b ON b.id=d.blood_bank_id
        WHERE dn.user_id=? ORDER BY d.donation_date DESC
    """, (user["id"],)).fetchall()
    conn.close()
    return render("donation_history", **common_context(), user=user, donations=rows)

def admin_required():
    user = logged_user()
    if not user or user["email"] != "admin@lifedrop.local":
        redirect("/login")
    return user

@app.get("/admin")
def admin():
    admin_required()
    conn = get_connection()
    stats = {
        "users": conn.execute("SELECT COUNT(*) FROM users").fetchone()[0],
        "donors": conn.execute("SELECT COUNT(*) FROM donors").fetchone()[0],
        "banks": conn.execute("SELECT COUNT(*) FROM blood_banks").fetchone()[0],
        "requests": conn.execute("SELECT COUNT(*) FROM blood_requests").fetchone()[0],
        "donations": conn.execute("SELECT COUNT(*) FROM donations WHERE status='Completed'").fetchone()[0],
        "units": conn.execute("SELECT COALESCE(SUM(units),0) FROM blood_inventory").fetchone()[0],
    }
    requests = conn.execute("""
        SELECT r.*, u.full_name AS requester FROM blood_requests r
        LEFT JOIN users u ON u.id=r.user_id ORDER BY r.id DESC LIMIT 20
    """).fetchall()
    conn.close()
    return render("admin", **common_context(), stats=stats, requests=requests)

@app.get("/admin/donors")
def admin_donors():
    admin_required()
    conn = get_connection()
    rows = conn.execute("""
        SELECT d.*, u.full_name FROM donors d LEFT JOIN users u ON u.id=d.user_id
        ORDER BY d.id DESC
    """).fetchall()
    conn.close()
    return render("admin_donors", **common_context(), donors=rows)

@app.get("/admin/blood-banks")
def admin_banks():
    admin_required()
    conn = get_connection()
    rows = conn.execute("SELECT * FROM blood_banks ORDER BY id DESC").fetchall()
    conn.close()
    return render("admin_banks", **common_context(), banks=rows)

@app.get("/admin/inventory")
def admin_inventory():
    admin_required()
    conn = get_connection()
    rows = conn.execute("""
        SELECT i.*, b.name AS bank_name FROM blood_inventory i
        JOIN blood_banks b ON b.id=i.blood_bank_id
        ORDER BY b.name,i.blood_group
    """).fetchall()
    banks = conn.execute("SELECT * FROM blood_banks ORDER BY name").fetchall()
    conn.close()
    return render("admin_inventory", **common_context(), inventory=rows, banks=banks)

@app.post("/admin/inventory/update")
def admin_inventory_update():
    admin_required()
    bank_id = request.forms.get("blood_bank_id")
    group = request.forms.get("blood_group")
    units = request.forms.get("units")
    try:
        bank_id = int(bank_id); units = max(0, int(units))
    except (TypeError, ValueError):
        redirect("/admin/inventory")
    conn = get_connection()
    conn.execute("""
        INSERT INTO blood_inventory(blood_bank_id,blood_group,units,last_updated)
        VALUES(?,?,?,?)
        ON CONFLICT(blood_bank_id,blood_group)
        DO UPDATE SET units=excluded.units,last_updated=excluded.last_updated
    """, (bank_id,group,units,datetime.now().isoformat(timespec="seconds")))
    conn.commit()
    conn.close()
    redirect("/admin/inventory")

@app.get("/admin/requests")
def admin_requests():
    admin_required()
    conn = get_connection()
    rows = conn.execute("""
        SELECT r.*, u.full_name AS requester FROM blood_requests r
        LEFT JOIN users u ON u.id=r.user_id ORDER BY r.id DESC
    """).fetchall()
    conn.close()
    return render("admin_requests", **common_context(), requests=rows)

@app.post("/admin/requests/status")
def admin_request_status():
    admin_required()
    rid = request.forms.get("request_id")
    status = request.forms.get("status")
    allowed = {"Pending","Approved","Fulfilled","Rejected"}
    if status in allowed:
        conn = get_connection()
        conn.execute("UPDATE blood_requests SET status=? WHERE id=?", (status,rid))
        conn.commit()
        conn.close()
    redirect("/admin/requests")

@app.get("/about")
def about():
    return render("about", **common_context())

@app.get("/contact")
def contact():
    return render("contact", **common_context())

# JSON API
@app.get("/api/blood-availability")
def api_availability():
    conn = get_connection()
    rows = conn.execute("""
        SELECT blood_group, SUM(units) AS units
        FROM blood_inventory GROUP BY blood_group ORDER BY blood_group
    """).fetchall()
    conn.close()
    response.content_type = "application/json"
    return json.dumps([dict(r) for r in rows])

@app.get("/api/donors")
def api_donors():
    group = request.query.blood_group.strip()
    city = request.query.city.strip()
    sql = """SELECT donors.id, users.full_name, donors.blood_group,
                    donors.city, donors.state, donors.availability_status
             FROM donors LEFT JOIN users ON users.id=donors.user_id
             WHERE donors.availability_status='Available'"""
    params=[]
    if group:
        sql += " AND donors.blood_group=?"; params.append(group)
    if city:
        sql += " AND LOWER(donors.city)=LOWER(?)"; params.append(city)
    conn = get_connection()
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    response.content_type = "application/json"
    return json.dumps([dict(r) for r in rows])

@app.get("/api/blood-banks")
def api_banks():
    conn = get_connection()
    rows = conn.execute("SELECT id,name,city,state,phone,email FROM blood_banks ORDER BY name").fetchall()
    conn.close()
    response.content_type = "application/json"
    return json.dumps([dict(r) for r in rows])

if __name__ == "__main__":
    create_tables()
    seed_sample_data()
    print("LifeDrop running at http://localhost:8080")
    app.run(host="localhost", port=8080, debug=True, reloader=True)
