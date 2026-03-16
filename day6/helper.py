import requests

from model import InputGuardrailError, OutputGuardrailError

RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


def validate_input(text: str) -> str:
    if not text or text.strip() == "":
        raise InputGuardrailError("Input cannot be empty")
    elif len(text) > 2000:
        raise InputGuardrailError("Input too long (max 2 000 characters).")
    else:
        prompt_injection_markers = [
            "ignore previous instructions",
            "disregard your system prompt",
            "you are now",
        ]
        for marker in prompt_injection_markers:
            if text.lower().count(marker) > 0:
                raise InputGuardrailError("Input contains disallowed patterns.")
        return text.strip()


def validate_output(text: str) -> str:
    if not text or text.strip() == "":
        raise OutputGuardrailError("Empty response from model.")
    if len(text.strip()) < 3:
        raise OutputGuardrailError("Response too short to be valid.")

    else:
        return text.strip()


def is_retryable_error(exc: Exception) -> bool:
    if isinstance(exc, requests.ConnectionError):
        return True
    if isinstance(exc, requests.Timeout):
        return True
    if isinstance(exc, requests.HTTPError):
        status = exc.response.status_code if exc.response is not None else None
        return status in RETRYABLE_STATUS_CODES
    return False
