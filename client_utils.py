from typing import Callable, Literal
from flet import TextField
from requests import put
from shared import User

HOST, PORT = ('http://localhost', 7992)
structure_route: Callable[[str, int, str], str] = lambda host, port, route: f"{host}:{port}/{route}"

type TypeOfHttpRequest = Literal['save'] # Skill issue, non-Python 3.12.0rc3 64-bit'ers

def request(type_of_request: TypeOfHttpRequest, save_data: User | None = None):
    match type_of_request:
        case "save":
            if save_data is not None:
                resp = put(structure_route(HOST, PORT, 'save'), json=save_data)
                return resp
            else:
                print("[ERROR] Save data not found")
        case _:
            print("[WARNING] Invalid request type")

username_tf = TextField(label='Username')
password_tf = TextField(label='Password', password=True)
