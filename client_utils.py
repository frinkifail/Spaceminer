from typing import Callable, Literal
from flet import TextField, SnackBar, Text
from requests import get, put
from shared import User

HOST, PORT = ("http://localhost", 7992)
structure_route: Callable[
    [str, int, str], str
] = lambda host, port, route: f"{host}:{port}/{route}"

type TypeOfHttpRequest = Literal['save', 'load'] # Skill issue, non-Python 3.12.0rc3 64-bit'ers
# Fuck you black formatter doesn't support 3.12.0
class settable_object[T]:
    def __init__(self, v: T) -> None:
        self.obj: T = v
    def set(self, v: T):
        self.obj = v
    def get(self):
        return self.obj
logged_in_user: settable_object[User | None] = settable_object(None)

def new_snackbar(message: str):
    return SnackBar(Text(message), open=True)


def request(
    type_of_request: TypeOfHttpRequest,
    save_data: User | None = None,
    username: str | None = None,
):
    match type_of_request:
        case "save":
            if save_data is not None:
                resp = put(structure_route(HOST, PORT, "save"), json=save_data)
                return resp
            else:
                print("[ERROR] Save data not found")
        case "load":
            if username is not None:
                resp = get(structure_route(HOST, PORT, "load"), json=username)
                return resp
            else:
                print("[ERROR] Username not passed")
        case _:
            print("[WARNING] Invalid request type")


username_tf = TextField(label="Username")
password_tf = TextField(label="Password", password=True)
