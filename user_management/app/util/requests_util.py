from typing import Dict
from app.schemas import StandardResponse
from pydantic import BaseModel
from flask import make_response, jsonify


def create_response(
    response: BaseModel = None,
    success: bool = True,
    message: str = None,
    status: int = 200,
    headers: Dict = None,
    cookies: Dict = None,
):
    resp = make_response(
        jsonify(
            StandardResponse(success=success, response=response, message=message).dict()
        ),
        status,
    )
    if headers:
        for k, v in headers.items():
            resp.headers[k] = v
    if cookies:
        for k, v in cookies.items():
            resp.set_cookie(key=k, value=v, httponly=True, secure=True)
    return resp
