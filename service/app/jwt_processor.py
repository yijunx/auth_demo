import jwt
import os
from app.schemas import User
from flask import Request, abort
from app.schemas import Role

# mapped as specified from .devcontainer/docker-compose.yml
CERTS_FOLDER = "/opt/yijunx/etc/certs"
DOMAIN_NAME = "auth-test.freedynamicdns.net"
PUBLIC_KEY_LOCATION = os.path.join(CERTS_FOLDER, DOMAIN_NAME, "pubkey.pem")


def _read_pem(file_location: str = None):
    file_location = file_location or PUBLIC_KEY_LOCATION
    with open(file_location, "rb") as f:
        key = f.read()
    return key


def decode_token(token: str):
    pub = _read_pem(file_location=PUBLIC_KEY_LOCATION)
    data = jwt.decode(jwt=token, key=pub, algorithms=["RS256"])
    return data


def get_user_info_from_request(request: Request) -> User:
    print(request.headers)
    token = request.headers.get("Cookie", None)
    roles = request.headers.get("X-Roles", "")
    roles = roles.split(",")
    if token is None:
        abort(status=401)
    else:
        user_dict = decode_token(token=token.split("=")[1])
        user_dict["roles"] = [Role(name=x) for x in roles]
        user = User(
            **user_dict,
        )
        print(f"user is {user}")
        return user
