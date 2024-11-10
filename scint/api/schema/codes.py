def http_status_to_message(status_code: int) -> str:
    match status_code:
        case 200:
            "OK"
        case 201:
            "Created"
        case 204:
            "No Content"
        case 400:
            "Bad Request"
        case 401:
            "Unauthorized"
        case 403:
            "Forbidden"
        case 404:
            "Not Found"
        case 409:
            "Conflict"
        case 422:
            "Unprocessable Entity"
        case 429:
            "Too Many Requests"
        case 500:
            "Internal Server Error"
