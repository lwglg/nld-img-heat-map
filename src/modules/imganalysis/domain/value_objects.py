from src.core.pydantic import ConStr


class Object(ConStr):
    min_length = 10
    max_length = 20


class Region(ConStr):
    min_length = 10
    max_length = 50
