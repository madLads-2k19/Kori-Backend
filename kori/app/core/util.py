import re


def camel_to_snake(s: str):
    """
    This helper can be used to convert camelCase/TitleCase to snake_case

    :param s: String in TitleCase or camelCase
    :return: String in snake_case
    """
    if s.isupper():
        return s.lower()
    else:
        return re.sub("([A-Z])", "_\\1", s).lower().lstrip("_")

