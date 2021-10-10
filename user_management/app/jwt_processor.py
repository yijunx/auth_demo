import jwt
import os
from app.schemas import User, UserWithToken, UserWithoutRole
from flask import Request, abort
from datetime import datetime, timedelta, timezone
from typing import List

# mapped as specified from .devcontainer/docker-compose.yml
CERTS_FOLDER = "/opt/yijunx/etc/certs"
DOMAIN_NAME = "auth-test.freedynamicdns.net"
PRIVATE_KEY_LOCATION = os.path.join(CERTS_FOLDER, DOMAIN_NAME, "privkey1.pem")
PUBLIC_KEY_LOCATION = os.path.join(CERTS_FOLDER, DOMAIN_NAME, "pubkey.pem")


def _read_pem(file_location: str = None):
    file_location = file_location or PUBLIC_KEY_LOCATION
    with open(file_location, "rb") as f:
        key = f.read()
    return key


def get_priv_key():
    return _read_pem(file_location=PRIVATE_KEY_LOCATION)


def get_publ_key():
    return _read_pem(file_location=PUBLIC_KEY_LOCATION)


def generate_token(user: User) -> UserWithToken:
    # assuming the token expires 8 hours
    # we can add issuer also, these things should come from envvar
    additional_token_payload = {
        "exp": datetime.now(timezone.utc) + timedelta(seconds=60 * 60 * 8),
        "iat": datetime.now(timezone.utc),
    }
    payload = user.dict()
    payload.update(additional_token_payload)
    encoded = jwt.encode(
        payload=payload,
        key=_read_pem(file_location=PRIVATE_KEY_LOCATION),
        algorithm="RS256",
    )
    return UserWithToken(**user.dict(), access_token=encoded)


def decode_token(token: str):
    pub = _read_pem(file_location=PUBLIC_KEY_LOCATION)
    data = jwt.decode(jwt=token, key=pub, algorithms=["RS256"])
    return data


def get_user_info_from_request(request: Request) -> UserWithoutRole:
    cookie = request.headers.get("Cookie", None)
    raisins: List[str]=cookie.split("; ")
    token = None
    for r in raisins:
        if r.startswith("token="):
            token = r.split("=")[1]
    if token is None:
        abort(status=401)
    else:
        user = UserWithoutRole(**decode_token(token=token))
        return user


if __name__ == "__main__":
    key = _read_pem()
    print(key)
    token = generate_token(user=User(id="123", name="x", email="aa", roles=[]))
    print(f"token is : {token}, type is {type(token)}")
    data = decode_token(token)
    print(f"data is : {data}")
