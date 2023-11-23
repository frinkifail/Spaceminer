from hashlib import md5
from typing import Literal, TypeVar, TypedDict


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


T = TypeVar("T")
W = TypeVar("W")


def list_to_dict(keys: T, values: W) -> dict[T, W]:
    """
    Create a dictionary from two lists.

    Args:
      keys: A list of keys.
      values: A list of values.

    Returns:
      A dictionary mapping keys to values.
    """
    result = {}
    for i, key in enumerate(keys):  # type: ignore
        result[key] = values[i]  # type: ignore
    return result


class _Upgrades(TypedDict):
    max_materials: dict[str, float]
    max_money: float


class _Quantux(TypedDict):
    minerals: dict[str, float]
    upgrades: _Upgrades


_EzNewQuantux_Materials = TypedDict(
    "_EzNewQuantux_Materials", {"materials": list[str], "upgrades": list[float]}
)


def _eznewquantux(materials: _EzNewQuantux_Materials) -> _Quantux | Literal[False]:
    if len(materials["materials"]) != len(materials["upgrades"]):
        print("> blud, the lists arent even equal :skull:")
        return False
    new = list_to_dict(materials["materials"], materials["upgrades"])
    return {  # type: ignore
        "minerals": {i: 0 for i in materials["materials"]},
        "ore_amount": 0,
        "upgrades": {"max_materials": new, "max_money": 200},
    }


QUANTUXES = {  # ahem, totally not generated by an ai
    "Cosmic Lattice": _eznewquantux(
        {"materials": ["hydrogen", "helium"], "upgrades": [40, 42]}
    )
}


class _SaveData(TypedDict):
    money: float
    quantux: _Quantux


#                                                Basically "this works" ↓            ↓
DEFAULT_SAVE = _SaveData(money=0, quantux=QUANTUXES["Cosmic Lattice"].copy())  # type: ignore


class User(TypedDict):
    name: str
    created: float
    data: _SaveData
    password: str
