from flask import Blueprint
from werkzeug.exceptions import HTTPException
from datetime import datetime, timezone
from ..exceptions import InvalidRequestException

error_bp = Blueprint('error_handlers', __name__)

@error_bp.app_errorhandler(HTTPException)
def handle_http_exception(e):
    return {
        "status_code": e.code,
        "message": e.name,
        "timestamp": datetime.now(timezone.utc)
    }

@error_bp.app_errorhandler(InvalidRequestException)
def handle_400(e):
    return {
        "status_code": 400,
        "message": "Invalid request",
        "fields": e.messages,
        "timestamp": datetime.now(timezone.utc)
    }