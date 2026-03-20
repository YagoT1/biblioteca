from __future__ import annotations

import re
from datetime import datetime

from utils.datetime import ensure_utc, utc_now
from utils.errors import ApiError

ISBN_PATTERN = re.compile(r"^(?:\d{9}[\dXx]|\d{13})$")


def require_json_object(payload):
    if not isinstance(payload, dict):
        raise ApiError("El cuerpo de la solicitud debe ser un objeto JSON", 400)


def validate_allowed_fields(payload: dict, allowed_fields: set[str]):
    unknown_fields = set(payload.keys()) - allowed_fields
    if unknown_fields:
        raise ApiError(
            f"Campos no permitidos: {', '.join(sorted(unknown_fields))}",
            400,
        )


def sanitize_string(value: str | None, field_name: str, max_length: int, *, required: bool = False) -> str | None:
    if value is None:
        if required:
            raise ApiError(f"{field_name} es obligatorio", 400)
        return None

    if not isinstance(value, str):
        raise ApiError(f"{field_name} debe ser texto", 400)

    cleaned = value.strip()
    if required and not cleaned:
        raise ApiError(f"{field_name} no puede ser vacío", 400)
    if cleaned and len(cleaned) > max_length:
        raise ApiError(f"{field_name} supera longitud máxima de {max_length}", 400)
    return cleaned or None


def parse_datetime(value, field_name: str) -> datetime:
    if not isinstance(value, str):
        raise ApiError(f"{field_name} debe ser string ISO-8601", 400)

    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ApiError(f"{field_name} debe estar en formato ISO-8601 válido", 400) from exc

    return ensure_utc(parsed)


def validate_future_due_date(fecha_vencimiento: datetime, fecha_salida: datetime | None = None) -> datetime:
    due = ensure_utc(fecha_vencimiento)
    salida = ensure_utc(fecha_salida or utc_now())

    if due <= utc_now():
        raise ApiError("fecha_vencimiento debe ser mayor a la fecha actual UTC", 400)
    if due <= salida:
        raise ApiError("fecha_vencimiento debe ser mayor a fecha_salida", 400)

    return due


def validate_positive_int(value, field_name: str) -> int:
    if not isinstance(value, int) or value <= 0:
        raise ApiError(f"{field_name} debe ser un entero positivo", 400)
    return value


def validate_isbn(value: str | None) -> str | None:
    if value is None:
        return None

    normalized = value.replace("-", "").replace(" ", "")
    if not ISBN_PATTERN.match(normalized):
        raise ApiError("isbn debe tener formato ISBN-10 o ISBN-13 válido", 400)
    return normalized
