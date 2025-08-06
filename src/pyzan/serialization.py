import json
from enum import Enum
from typing import get_type_hints, Type, Any


class Serializable:
    __exclude__ = ["state_db", "opened_file", "opened_files"]

    def to_dict(self) -> dict:
        result = {}
        for key, value in self.__dict__.items():
            if key in self.__exclude__:
                continue
            result[key] = self._serialize_value(value)
        return result

    @classmethod
    def from_dict(cls, data: dict):
        obj = cls.__new__(cls)
        hints = get_type_hints(cls)

        for key, value in data.items():
            expected_type = hints.get(key, None)
            setattr(obj, key, cls._deserialize_value(value, expected_type))

        return obj

    def serialize(self) -> str:
        return json.dumps(self.to_dict(), indent=4)

    @classmethod
    def deserialize(cls, json_str: str):
        data = json.loads(json_str)
        return cls.from_dict(data)

    @staticmethod
    def _serialize_value(value: Any):
        if isinstance(value, Serializable):
            return value.to_dict()
        elif isinstance(value, Enum):
            return value.name
        elif isinstance(value, list):
            return [Serializable._serialize_value(v) for v in value]
        else:
            return value

    @staticmethod
    def _deserialize_value(value: Any, expected_type: Type):
        if expected_type is None:
            return value

        origin = getattr(expected_type, '__origin__', None)

        if origin == list:
            inner_type = expected_type.__args__[0]
            return [Serializable._deserialize_value(v, inner_type) for v in value]

        if isinstance(value, dict) and issubclass(expected_type, Serializable):
            return expected_type.from_dict(value)

        if isinstance(value, str) and isinstance(expected_type, type) and issubclass(expected_type, Enum):
            return expected_type[value]

        return value