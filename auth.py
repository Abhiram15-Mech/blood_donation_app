import hashlib
import hmac
import secrets
from bottle import request, redirect

def hash_password(password):
    # Beginner-friendly hashing. For production, use a dedicated password
    # hashing algorithm such as Argon2/bcrypt.
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt.encode(), 120000
    ).hex()
    return f"{salt}${digest}"

def verify_password(password, stored):
    try:
        salt, expected = stored.split("$", 1)
        actual = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), salt.encode(), 120000
        ).hex()
        return hmac.compare_digest(actual, expected)
    except ValueError:
        # Supports old sample SHA-256 seed passwords if needed.
        return hmac.compare_digest(
            hashlib.sha256(password.encode()).hexdigest(), stored
        )

def login_user(user):
    request.environ["lifedrop.user_id"] = user["id"]
    request.environ["lifedrop.user_name"] = user["full_name"]

def logout_user():
    request.environ.pop("lifedrop.user_id", None)
    request.environ.pop("lifedrop.user_name", None)

def current_user_id():
    return request.environ.get("lifedrop.user_id")

def require_login():
    if not current_user_id():
        redirect("/login")
    return current_user_id()
