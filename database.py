import sqlite3
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "blood_donation.db"

BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        password_hash TEXT NOT NULL,
        gender TEXT,
        date_of_birth TEXT,
        city TEXT,
        state TEXT,
        created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS donors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        blood_group TEXT NOT NULL,
        gender TEXT,
        date_of_birth TEXT,
        phone TEXT,
        email TEXT,
        city TEXT,
        state TEXT,
        address TEXT,
        last_donation_date TEXT,
        availability_status TEXT DEFAULT 'Available',
        created_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE SET NULL
    );

    CREATE TABLE IF NOT EXISTS blood_banks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        registration_number TEXT,
        contact_person TEXT,
        phone TEXT,
        email TEXT,
        address TEXT,
        city TEXT,
        state TEXT,
        pincode TEXT,
        created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS blood_inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        blood_bank_id INTEGER NOT NULL,
        blood_group TEXT NOT NULL,
        units INTEGER DEFAULT 0,
        last_updated TEXT NOT NULL,
        UNIQUE(blood_bank_id, blood_group),
        FOREIGN KEY(blood_bank_id) REFERENCES blood_banks(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS blood_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        patient_name TEXT NOT NULL,
        blood_group TEXT NOT NULL,
        units_required INTEGER NOT NULL,
        hospital_name TEXT,
        hospital_address TEXT,
        city TEXT,
        state TEXT,
        contact_number TEXT,
        required_date TEXT,
        emergency_level TEXT DEFAULT 'Normal',
        additional_information TEXT,
        status TEXT DEFAULT 'Pending',
        created_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE SET NULL
    );

    CREATE TABLE IF NOT EXISTS donations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        donor_id INTEGER NOT NULL,
        blood_bank_id INTEGER NOT NULL,
        donation_date TEXT NOT NULL,
        blood_group TEXT NOT NULL,
        units_donated INTEGER NOT NULL,
        status TEXT DEFAULT 'Completed',
        FOREIGN KEY(donor_id) REFERENCES donors(id) ON DELETE CASCADE,
        FOREIGN KEY(blood_bank_id) REFERENCES blood_banks(id) ON DELETE CASCADE
    );
    """)
    conn.commit()
    conn.close()

def seed_sample_data():
    conn = get_connection()
    cur = conn.cursor()
    now = datetime.now().isoformat(timespec="seconds")

    # Admin/user sample account: admin@lifedrop.local / admin123
    cur.execute("SELECT id FROM users WHERE email = ?", ("admin@lifedrop.local",))
    admin = cur.fetchone()
    if not admin:
        import hashlib
        password_hash = hashlib.sha256("admin123".encode()).hexdigest()
        cur.execute("""
            INSERT INTO users
            (full_name,email,phone,password_hash,gender,date_of_birth,city,state,created_at)
            VALUES (?,?,?,?,?,?,?,?,?)
        """, ("LifeDrop Admin", "admin@lifedrop.local", "9000000000",
              password_hash, "Other", "1995-01-01", "Visakhapatnam",
              "Andhra Pradesh", now))

    sample_users = [
        ("Arun Kumar", "arun@example.local", "9000000001", "Male", "2000-04-12", "Visakhapatnam", "Andhra Pradesh"),
        ("Priya Rao", "priya@example.local", "9000000002", "Female", "1999-08-20", "Vijayawada", "Andhra Pradesh"),
    ]
    import hashlib
    for name,email,phone,gender,dob,city,state in sample_users:
        cur.execute("SELECT id FROM users WHERE email=?", (email,))
        if not cur.fetchone():
            cur.execute("""
                INSERT INTO users
                (full_name,email,phone,password_hash,gender,date_of_birth,city,state,created_at)
                VALUES (?,?,?,?,?,?,?,?,?)
            """, (name,email,phone,hashlib.sha256("password123".encode()).hexdigest(),
                  gender,dob,city,state,now))

    banks = [
        ("City Care Blood Bank", "BB-VSK-001", "Dr. S. Rao", "9000000010",
         "citycare@example.local", "12 Health Avenue", "Visakhapatnam", "Andhra Pradesh", "530016"),
        ("Helping Hands Blood Centre", "BB-VJA-002", "Dr. P. Devi", "9000000020",
         "helpinghands@example.local", "45 Care Road", "Vijayawada", "Andhra Pradesh", "520010"),
    ]
    for bank in banks:
        cur.execute("SELECT id FROM blood_banks WHERE registration_number=?", (bank[1],))
        if not cur.fetchone():
            cur.execute("""
                INSERT INTO blood_banks
                (name,registration_number,contact_person,phone,email,address,city,state,pincode,created_at)
                VALUES (?,?,?,?,?,?,?,?,?,?)
            """, (*bank, now))

    cur.execute("SELECT id FROM blood_banks WHERE registration_number='BB-VSK-001'")
    vsk = cur.fetchone()["id"]
    cur.execute("SELECT id FROM blood_banks WHERE registration_number='BB-VJA-002'")
    vja = cur.fetchone()["id"]

    inventory = {
        vsk: {"A+":10,"A-":5,"B+":8,"B-":3,"AB+":4,"AB-":2,"O+":15,"O-":6},
        vja: {"A+":6,"A-":2,"B+":12,"B-":4,"AB+":3,"AB-":1,"O+":9,"O-":3}
    }
    for bank_id, groups in inventory.items():
        for group, units in groups.items():
            cur.execute("""
                INSERT INTO blood_inventory
                (blood_bank_id,blood_group,units,last_updated)
                VALUES (?,?,?,?)
                ON CONFLICT(blood_bank_id,blood_group)
                DO UPDATE SET units=excluded.units,last_updated=excluded.last_updated
            """, (bank_id, group, units, now))

    # Sample donors
    cur.execute("SELECT id FROM users WHERE email='arun@example.local'")
    arun_id = cur.fetchone()["id"]
    cur.execute("SELECT id FROM users WHERE email='priya@example.local'")
    priya_id = cur.fetchone()["id"]

    donors = [
        (arun_id,"O+","Male","2000-04-12","9000000001","arun@example.local",
         "Visakhapatnam","Andhra Pradesh","Demo Street 1","2026-06-10","Available"),
        (priya_id,"A+","Female","1999-08-20","9000000002","priya@example.local",
         "Vijayawada","Andhra Pradesh","Demo Street 2","2026-05-15","Available")
    ]
    for d in donors:
        cur.execute("SELECT id FROM donors WHERE user_id=?", (d[0],))
        if not cur.fetchone():
            cur.execute("""
                INSERT INTO donors
                (user_id,blood_group,gender,date_of_birth,phone,email,city,state,address,
                 last_donation_date,availability_status,created_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            """, (*d, now))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    seed_sample_data()
    print(f"Database ready: {DB_PATH}")
