from flask import Blueprint
from flask import abort
from ..services import pow_service
from ..services import fib_service
from ..services import fact_service
from flask_jwt_extended import jwt_required
from flask import request
from pydantic import ValidationError
from src.schemas import PowInput
from src.schemas import NInput, ResultOutput

math_bp = Blueprint("math", __name__, url_prefix="/api/math")


def _parse_int_arg(arg_name: str):
    """Helper to get and validate an integer query param."""
    val = request.args.get(arg_name)
    if val is None or not val.isdigit():
        abort(400, description=f"Missing or invalid '{arg_name}' parameter")
    return int(val)


@math_bp.route("/pow", methods=["GET"])
@jwt_required()
def pow_route():
    """
    Calculate Power
    ---
    summary: Calculate base raised to the exp power.
    tags:
      - Math
    parameters:
      - name: base
        in: query
        type: integer
        required: true
        description: Base number (integer)
        example: 2
      - name: exp
        in: query
        type: integer
        required: true
        description: Exponent (integer)
        example: 8
    security:
      - Bearer: []
    responses:
      200:
        description: Success
        schema:
          type: object
          properties:
            result:
              type: integer
              example: 256
      400:
        description: Missing or invalid parameters
        schema:
          type: object
          properties:
            msg:
              type: string
              example: "Missing or invalid 'base' or 'exp'"
      401:
        description: Unauthorized
    """
    try:
        # Convert args to dict, filter only fields PowInput expects
        query_args = {k: request.args.get(k) for k in ["base", "exp"]}
        # Pydantic validates types; will raise if missing/invalid
        data = PowInput(**{k: int(v) for k, v in query_args.items() if v is not None})
    except (ValidationError, ValueError, TypeError):
        return {"msg": "Missing or invalid 'base' or 'exp'"}, 400

    result = pow_service(data.base, data.exp)
    return ResultOutput(result=result).model_dump(), 200


@math_bp.route("/fib", methods=["GET"])
@jwt_required()
def fib_route():
    """
    Calculate Fibonacci Number
    ---
    summary: Returns the N-th Fibonacci number.
    tags:
      - Math
    parameters:
      - name: n
        in: query
        type: integer
        required: true
        description: The index (n >= 0)
        example: 10
    security:
      - Bearer: []
    responses:
      200:
        description: Success
        schema:
          type: object
          properties:
            result:
              type: integer
              example: 55
      400:
        description: Missing or invalid parameter
        schema:
          type: object
          properties:
            msg:
              type: string
              example: "Missing or invalid 'n'"
      401:
        description: Unauthorized
    """
    try:
        query_args = {k: request.args.get(k) for k in ["n"]}
        data = NInput(**{k: int(v) for k, v in query_args.items() if v is not None})
    except (ValidationError, ValueError, TypeError):
        return {"msg": "Missing or invalid 'n'"}, 400

    result = fib_service(data.n)
    return ResultOutput(result=result).model_dump(), 200


@math_bp.route("/factorial", methods=["GET"])
@jwt_required()
def fact_route():
    """
    Calculate Factorial
    ---
    summary: Returns the factorial of n.
    tags:
      - Math
    parameters:
      - name: n
        in: query
        type: integer
        required: true
        description: The input integer (n >= 0)
        example: 5
    security:
      - Bearer: []
    responses:
      200:
        description: Success
        schema:
          type: object
          properties:
            result:
              type: integer
              example: 120
      400:
        description: Missing or invalid parameter
        schema:
          type: object
          properties:
            msg:
              type: string
              example: "Missing or invalid 'n'"
      401:
        description: Unauthorized
    """
    try:
        query_args = {k: request.args.get(k) for k in ["n"]}
        data = NInput(**{k: int(v) for k, v in query_args.items() if v is not None})
    except (ValidationError, ValueError, TypeError):
        return {"msg": "Missing or invalid 'n'"}, 400

    result = fact_service(data.n)
    return ResultOutput(result=result).model_dump(), 200
