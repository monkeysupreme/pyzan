import json


class Serializable:
    def to_dict(self) -> dict:
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def serialize(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def deserialize(cls, json_str):
        data = json.loads(json_str)
        return cls.from_dict(data)