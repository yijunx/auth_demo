import jwt
import os
from app.schemas import User, Token

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


def generate_token(user: User) -> Token:
    encoded = jwt.encode(
        payload=user.dict(),
        key=_read_pem(file_location=PRIVATE_KEY_LOCATION),
        algorithm="RS256",
    )
    return Token(access_token=encoded)


def decode_token(token: Token):
    pub = _read_pem(file_location=PUBLIC_KEY_LOCATION)
    data = jwt.decode(jwt=token.access_token, key=pub, algorithms=["RS256"])
    return data


if __name__ == "__main__":
    key = _read_pem()
    print(key)
    token = generate_token(user=User(id="123", name="x", email="aa", roles=[]))
    print(f"token is : {token}, type is {type(token)}")
    data = decode_token(token)
    print(f"data is : {data}")