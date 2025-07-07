__all__ = [
    "SUPPORTED_TRUE_SYMBOLS",
    "SUPPORTED_FALSE_SYMBOLS",
    "to_boolean",
    "TSupportedTypes",
]

# I'm perhaps pushing at little bit here, but just for the sake of completness,
# I included a whole plethora of symbols that could be parsed as True of False.
SUPPORTED_TRUE_SYMBOLS = [
    True,
    "true",
    "verdadeiro",
    "wahr",
    "1",
    "1.0",
    "y",
    "yes",
    "ja",
]

SUPPORTED_FALSE_SYMBOLS = [
    False,
    "false",
    "falso",
    "falsch",
    "0",
    "0.0",
    "n",
    "no",
    "nein",
]


type TSupportedTypes = bool | str | float | int | None


def to_boolean(value: TSupportedTypes) -> bool | None:
    """Check if the incoming value is parseable as a boolean. If so, returns its parsed form."""

    value_type = type(value).__name__

    def check_inclusion(v: TSupportedTypes) -> bool | None:
        if v in SUPPORTED_TRUE_SYMBOLS:
            return True

        if v in SUPPORTED_FALSE_SYMBOLS:
            return False

    match value_type:
        case "bool":
            return value
        case "str":
            return check_inclusion(value.strip().lower())
        case "int", "float", "bigint":
            return check_inclusion(value)
        case "NoneType":
            return value
        case _:
            return None

    return None
