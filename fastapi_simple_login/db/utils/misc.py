import re

camelcase_re = re.compile(r'([A-Z]+)(?=[a-z0-9])')


def camel_to_snake_case(name: str) -> str:
    def _join(match):
        word = match.group()
        result = f"_{word}"

        if len(word) > 1:
            result = f"_{word[:-1]}_{word[-1]}"

        return result.lower()

    return camelcase_re.sub(_join, name).lstrip("_")
