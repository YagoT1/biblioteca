from flask import jsonify


def api_response(success: bool, data=None, error=None, status_code: int = 200):
    payload = {
        "success": success,
        "data": data if data is not None else {},
        "error": error,
    }
    return jsonify(payload), status_code
