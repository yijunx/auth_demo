import jwt
import os

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


def generate_token():
    data = {"aaa": "bbb", "bbb": "ccc"}
    encoded = jwt.encode(
        payload=data,
        key=_read_pem(file_location=PRIVATE_KEY_LOCATION),
        algorithm="RS256",
    )
    return encoded


def decode_token(token: str):
    pub = _read_pem(file_location=PUBLIC_KEY_LOCATION)
    data = jwt.decode(jwt=token, key=pub, algorithms=["RS256"])
    return data


if __name__ == "__main__":
    key = _read_pem()
    print(key)
    token = generate_token()
    print(f"token is : {token}, type is {type(token)}")
    data = decode_token(token)
    print(f"data is : {data}")
