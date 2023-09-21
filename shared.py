from hashlib import md5
from typing import TypedDict


def hash_password(password: str | None):
    if password is not None:
        pass
    elif password is None:
        return "<unknown>"
    return md5(password.encode()).hexdigest()


def create_file(path: str, default_data: str | None = None):
    if not default_data:
        open(path, "x").close()
    else:
        f = open(path, "w+")
        f.write(default_data)
        f.close()


class Upgrades(TypedDict):
    max_silicon: int
    max_money: float


class SaveData(TypedDict):
    silicon: int
    money: float
    upgrades: Upgrades


class User(TypedDict):
    name: str
    created: float
    data: SaveData
    password: str
