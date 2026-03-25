# Compatibilidad retroactiva: usar utils/datetime.py
from utils.datetime import ensure_utc, utc_now

__all__ = ["utc_now", "ensure_utc"]
