from json import dump, load
from os import mkdir, path
from flask import Flask, request
from flask_cors import CORS

from shared import User, create_file

def init():
    if not path.exists('data'):
        mkdir('data')
    if not path.exists('data/users.json'):
        create_file('data/users.json', '{}')

def update_data(data: User | None = None, load_all: bool = False, load_all_data: dict[str, User] | None = None):
    if data is not None and load_all is False:
        print(f'[INFO] Saving {data["name"]}')
        if path.exists('data/users.json'):
            print(f"[SUCCESS] {data['name']} save progress passed db check")
            try:
                users_file = open('data/users.json', 'w+')
                json_data: dict[str, User] = load(users_file)
                json_data.update({data['name']: data})
                dump(json_data, users_file)
                users_file.close()
            except Exception as e:
                print(f"[ERROR] Something went wrong while trying to save {data['name']}!")
                print(f"[ERROR] {e}")
        else:
            print(f"[ERROR] db file doesn't exist")
    elif data is None and load_all is True and load_all_data is not None:
        print(f'[INFO] Saving...')
        if path.exists('data/users.json'):
            print(f"[SUCCESS] Save progress passed db check")
            try:
                users_file = open('data/users.json', 'w')
                dump(load_all_data, users_file)
                users_file.close()
                # json_data.update({data['name']: data})
            except Exception as e:
                print(f"[ERROR] Something went wrong while trying to save!")
                print(f"[ERROR] {e}")
        else:
            print(f"[ERROR] db file doesn't exist")

def load_data(username: str):
    print(f'[INFO] Loading {username}...')
    if path.exists('data/users.json'):
        print(f"[SUCCESS] Load progress passed db check")
        try:
            users_file = open('data/users.json', 'w')
            json_data: dict[str, User] = load(users_file)
            users_file.close()
            return json_data.get(username)
            # json_data.update({data['name']: data})
        except Exception as e:
            print(f"[ERROR] Something went wrong while trying to load!")
            print(f"[ERROR] {e}")
    else:
        print(f"[ERROR] db file doesn't exist")

app = Flask(__name__)
CORS(app)

init()

session_data: dict[str, User] = {}

@app.route('/', methods=['GET'])
async def index():
    return '?'

@app.route('/save', methods=['PUT'])
async def save():
    data: User = request.get_json(True)
    session_data.update({data['name']: data})
    update_data(data)
    return "Success", 200

@app.route('/load', methods=[])
async def load(): ...

if __name__ == "__main__":
    app.run(None, 7992, True)
