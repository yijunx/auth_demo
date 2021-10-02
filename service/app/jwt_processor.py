import jwt
import os
from app.schemas import User
from flask import Request, abort

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
    token = request.headers.get("Authorization", None)
    if token is None:
        abort(status=401)
    else:
        user = User(**decode_token(token=token.split(" ")[1]))
        return user
