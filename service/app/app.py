from flask import Flask, request
from app.jwt_processor import get_user_info_from_request
from app.util.requests_util import create_response
from app.schemas import Resource
import uuid


app = Flask(__name__)


resources = [
    Resource(id=str(uuid.uuid4()), name="one", created_by="001"),
    Resource(id=str(uuid.uuid4()), name="two", created_by="002"),
    Resource(id=str(uuid.uuid4()), name="three", created_by="003"),
    Resource(id=str(uuid.uuid4()), name="four", created_by="004"),
]


@app.route("/resources", methods=["GET"])
def get_resources():
    # need to return jwt sort of things
    user = get_user_info_from_request(request=request)
    print(user.roles)
    if [r for r in user.roles if r.name == "the_admin"]:
        return create_response(response=[x.dict() for x in resources])
    else:
        return create_response(
            response=[x.dict() for x in resources if user.id == x.created_by]
        )


@app.route("/something", methods=["GET"])
def get_something():
    return "<h1>something<h1>"
