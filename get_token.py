from distutils.log import ERROR


def get_token(token_path, password: str) -> str:
    if not password or not token_path:
        raise OSError("Без пароля токен не расшифровать")
    with open(token_path, "r") as f:
        token = f.read()
    if token == "":
        raise ERROR("С пустым токеном невозможно работать")
    return token