"""
EIOS
Master Dossier Serializer

Converts complex Python objects into JSON-serializable
structures for storage, APIs, UI, and databases.
"""

from dataclasses import asdict, is_dataclass
from datetime import date, datetime
from enum import Enum


class MasterDossierSerializer:
    """
    Recursively converts Python objects into JSON-safe types.
    """

    @classmethod
    def serialize(cls, obj):
        # None
        if obj is None:
            return None

        # Primitive types
        if isinstance(obj, (str, int, float, bool)):
            return obj

        # Dates
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()

        # Enums
        if isinstance(obj, Enum):
            return obj.value

        # Dataclasses
        if is_dataclass(obj):
            return cls.serialize(asdict(obj))

        # Dictionaries
        if isinstance(obj, dict):
            return {
                key: cls.serialize(value)
                for key, value in obj.items()
            }

        # Lists / Tuples / Sets
        if isinstance(obj, (list, tuple, set)):
            return [
                cls.serialize(item)
                for item in obj
            ]

        # Generic objects
        if hasattr(obj, "__dict__"):
            return cls.serialize(vars(obj))

        # Fallback
        return str(obj)