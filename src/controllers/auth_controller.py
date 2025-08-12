from flask import Blueprint
from flask import request
from flask import jsonify
from flask_jwt_extended import create_access_token
from ..models import User
from pydantic import ValidationError
from src.schemas import LoginInput, LoginOutput


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    User Login (JWT Auth)
    ---
    summary: Obtain a JWT token with username and password.
    tags:
      - Auth
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              example: testuser
            password:
              type: string
              example: testuser
    responses:
      200:
        description: JWT token issued successfully
        schema:
          type: object
          properties:
            access_token:
              type: string
              description: JWT access token
              example: "eyJ0eXAiOiJKV1QiLCJh..."
      400:
        description: Missing username or password
        schema:
          type: object
          properties:
            msg:
              type: string
              example: "Missing username or password"
      401:
        description: Invalid username or password
        schema:
          type: object
          properties:
            msg:
              type: string
              example: "Bad username or password"
    """
    try:
        data = LoginInput.model_validate(request.get_json())
    except ValidationError as e:
        return {"msg": "Invalid input", "errors": e.errors()}, 400

    user = User.query.filter_by(username=data.username).first()
    if not user or not user.check_password(data.password):
        return {"msg": "Bad username or password"}, 401

    token = create_access_token(identity=data.username)
    # Use Pydantic for output serialization, but keep old format
    return LoginOutput(access_token=token).model_dump(), 200
