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


@app.route("/logout", methods=["POST"])
def logout():
    # here is how to do the backend logout
    # while the frontend just wipeout the token

    # there is an iat field in the token
    # when login, iat, user.last_logout is None or t1

    # when authenticating:
    # user management knows user.last_logout
    # if iat > last_logout, allow , else, deny

    # when user logout, update the user.last_logout to t2 (t2 will be > X)
    # now if the user try to use the same token, 
    # when authenticating:
    # iat will be < last_logout, then deny

    # this thing is better done with a proper database, so it is not coded here
    # as i want to make this a very light code to show authN/Z
    return {"hello": "world"}

@app.route("/authenticate", methods=["POST"])
def authenticate():
    # so here we need to check user.last_logout vs token's iat..
    user = get_user_info_from_request(request=request)
    for u in users:
        if u.email == user.email:
            roles = ",".join([r.name for r in u.roles])
            # so here we need to check user.last_logout vs token's iat..
            # if iat < last logout, deny the access
            return create_response(headers={"X-Roles": roles})
    return create_response(success=False, message="not a good user..", status=403)


@app.route("/internal/get_public_key", methods=["GET"])
def get_public_key():
    return ""
