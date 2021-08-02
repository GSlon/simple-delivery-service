import bcrypt


def hash_password(password: str) -> str:
    bpass = password.encode()
    bhash = bcrypt.hashpw(bpass, bcrypt.gensalt())
    return str(bhash)[2:-1]   # убираем 'b' и кавычки


def check_equal_pass_and_hash(password: str, shash: str):
    bpass = password.encode()
    bhash = shash.encode()
    return bcrypt.checkpw(bpass, bhash)
