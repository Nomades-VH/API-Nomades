from bcrypt import checkpw, gensalt, hashpw


def hash_password(password: str) -> str:
    return hashpw(password.encode(), gensalt()).decode()


def verify_password(plain_password, hashed_password) -> bool:
    return checkpw(plain_password.encode(), hashed_password.encode())
