def get_token(token_path, password: str) -> str:
    if not password or not token_path:
        raise OSError("Без пароля токен не расшифровать")
        return
    with open(token_path, "r") as f:
        token = f.read()
    return token