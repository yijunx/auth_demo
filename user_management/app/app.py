from flask import Flask, request
from app.schemas import Role, UserLogin, User, UserWithPassword, UserWithoutRole
from app.util.requests_util import create_response
import hashlib
import os
from flask_pydantic import validate
from app.jwt_processor import generate_token, get_user_info_from_request
from flask_cors import CORS

salt = os.urandom(32)  # Remember this


def hash_password(password: str) -> str:
    p = hashlib.pbkdf2_hmac(
        "sha256",  # The hash digest algorithm for HMAC
        password.encode("utf-8"),  # Convert the password to bytes
        salt,  # Provide the salt
        100000,  # It is recommended to use at least 100,000 iterations of SHA-256
    )
    return p


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
        roles=[Role(name="user")],
    ),
]

app = Flask(__name__)
CORS(app=app)


@app.route("/login", methods=["POST"])
@validate()
def login(body: UserLogin):
    # user_login = request.body_params
    for u in users:
        if u.email == body.email and u.password == hash_password(body.password):
            return create_response(
                response=generate_token(user=UserWithoutRole(**u.dict()))
            )
    return create_response(success=False, message="Username or password is not correct")


@app.route("/authenticate", methods=["POST"])
def authenticate():
    user = get_user_info_from_request(request=request)
    for u in users:
        if u.email == user.email:
            roles = ",".join([r.name for r in u.roles])
            return create_response(headers={"X-Roles": roles})
    return create_response(success=False, message="not a good user..")


@app.route("/internal/get_public_key", methods=["GET"])
def get_public_key():
    return ""
