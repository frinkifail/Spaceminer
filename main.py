from asyncio import sleep
from subprocess import check_output
from time import time
import flet as ft
from client_utils import new_snackbar, request, username_tf, password_tf, logged_in_user
from shared import User, hash_password, DEFAULT_SAVE
from requests.exceptions import JSONDecodeError


async def app(page: ft.Page):
    page.title = "Spaceminer"
    current_commit_version = (
        check_output(["git", "describe", "--always"]).strip().decode()
    )

    async def route_change(route: ft.RouteChangeEvent):
        page.views.clear()

        if route.route == "/":

            async def _(_):
                await page.go_async("/login")

            page.views.append(
                ft.View(
                    "/",
                    [
                        ft.Row(
                            [
                                ft.Image(
                                    "Spaceminer.png",
                                    width=512,
                                    height=512,
                                    border_radius=ft.border_radius.all(2000),
                                ),
                                ft.Text(
                                    "Spaceminer", style=ft.TextThemeStyle.DISPLAY_SMALL
                                ),
                                ft.FilledTonalButton("Play", on_click=_),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            expand=True,
                        )
                    ],
                )
            )
        elif route.route == "/login":

            async def login(_):
                resp = request("load", username=username_tf.value)
                if resp is not None:
                    try:
                        logged_in_user.set(resp.json())
                    except JSONDecodeError:
                        await page.show_snack_bar_async(
                            new_snackbar("Couldn't login properly.")
                        )
                    await page.show_snack_bar_async(new_snackbar(f"Login successful."))
                    await page.go_async("/game")
                else:
                    await page.show_snack_bar_async(
                        new_snackbar("Couldn't login properly.")
                    )

            async def to_signup(_):
                await page.go_async("/signup")

            page.views.append(
                ft.View(
                    "/login",
                    [
                        username_tf,
                        password_tf,
                        ft.Row(
                            [
                                ft.FilledTonalButton(
                                    "Login", expand=True, on_click=login
                                )
                            ],
                        ),
                    ],
                    ft.AppBar(
                        title=ft.Text("Login"),
                        center_title=True,
                        actions=[
                            ft.IconButton(
                                ft.icons.PERSON_ADD,
                                tooltip="Signup",
                                on_click=to_signup,
                            )
                        ],
                    ),
                )
            )
        elif route.route == "/signup":

            async def signup(_):
                request(
                    "save",
                    User(
                        name=username_tf.value if username_tf.value else "<unknown>",
                        password=hash_password(password_tf.value),
                        created=time(),
                        data=DEFAULT_SAVE,
                    ),
                )
                await page.go_async("/")
                await page.show_snack_bar_async(
                    # ft.SnackBar(ft.Text("Signup successful"), open=True)
                    new_snackbar("Signup successful")
                )

            page.views.append(
                ft.View(
                    "/signup",
                    [
                        username_tf,
                        password_tf,
                        ft.Row(
                            [
                                ft.FilledTonalButton(
                                    "Signup", expand=True, on_click=signup
                                )
                            ],
                        ),
                    ],
                    ft.AppBar(title=ft.Text("Signup"), center_title=True),
                )
            )

        elif route.route == "/game":
            page.views.clear()
            usr = logged_in_user.get()
            if usr == None:
                await page.show_snack_bar_async(new_snackbar("failed to load user"))
                await sleep(2)
                await page.go_async("/")
                return
            plr = usr["data"]
            page.views.append(
                ft.View(
                    "/game",
                    [],
                    ft.AppBar(
                        title=ft.Text(f"Spaceminer v{current_commit_version}"),
                        center_title=True,
                    ),
                )
            )
        await page.update_async()

    async def view_pop(view: ft.ViewPopEvent):
        page.views.pop()
        top_view = page.views[-1]
        await page.go_async(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    await page.go_async(page.route)


if __name__ == "__main__":
    ft.app(app, "CI V2", None, 7993, assets_dir="assets")
