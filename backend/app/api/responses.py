def success_response(message: str, data=None):
    return {
        "status": "success",
        "message": message,
        "data": data or {},
        "errors": [],
    }


def error_response(message: str, errors=None):
    return {
        "status": "error",
        "message": message,
        "data": {},
        "errors": errors or [],
    }
