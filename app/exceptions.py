from datetime import datetime, timezone

class InvalidRequestException(Exception):
    def __init__(self, status_code=400, message="Invalid request", fields=None):
        self.status_code = status_code
        self.message = message
        self.fields = fields or {}
        self.timestamp = datetime.now(timezone.utc)

    def to_dict(self):
        error_dict = {
            "status_code": self.status_code,
            "message": self.message,
            "timestamp": self.timestamp.isoformat()
        }
        if self.fields:
            error_dict["fields"] = self.fields
        return error_dict
