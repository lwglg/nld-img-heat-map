from pydantic import ConfigDict
from pydantic.v1.fields import ModelField


class ConStr(str):
    min_length = 0
    max_length = 0

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: str, config: ConfigDict):
        if not isinstance(value, str):
            raise TypeError('This value is only str')

        if not cls.min_length <= len(value) <= cls.max_length:
            raise ValueError(f'This value length {cls.min_length} ~ {cls.max_length}')

        return value
