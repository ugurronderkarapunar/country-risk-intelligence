import bcrypt

# bcrypt en fazla 72 byte şifre kabul eder (UTF-8)
_MAX = 72


def hash_password(password: str) -> str:
    raw = password.encode("utf-8")[:_MAX]
    return bcrypt.hashpw(raw, bcrypt.gensalt(rounds=12)).decode("ascii")


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8")[:_MAX], hashed.encode("ascii"))
    except (ValueError, TypeError):
        return False
