from flask import Flask, request
from app.schemas import Role, UserLogin, User, UserWithPassword
import hashlib
import os
from flask_pydantic import validate

salt = os.urandom(32)  # Remember this


def hash_password(password: str) -> str:
    return hashlib.pbkdf2_hmac(
        "sha256",  # The hash digest algorithm for HMAC
        password.encode("utf-8"),  # Convert the password to bytes
        salt,  # Provide the salt
        100000,  # It is recommended to use at least 100,000 iterations of SHA-256
    )


# this is the temp db...
users = [
    UserWithPassword(
        id="001",
        name="admin",
        email="admin@tom.com",
        password=hash_password("admin"),
        roles=[Role(name="the_admin")],
    ),
    UserWithPassword(
        id="002",
        name="user",
        email="user@tom.com",
        password=hash_password("user"),
        roles=[],
    ),
]

app = Flask(__name__)


@app.route("/login", methods=["POST"])
@validate()
def login(user_login: UserLogin):
    # user_login = request.body_params
    for u in users:
        if u.email == user_login.email and u.password == user_login.password:
            return 0
    return 1


@app.route("/internal/get_public_key", methods=["GET"])
def get_public_key():
    return ""
