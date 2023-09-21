from time import time
import flet as ft
from client_utils import new_snackbar, request, username_tf, password_tf
from shared import SaveData, Upgrades, User, hash_password


async def app(page: ft.Page):
    page.title = "CommandIncremental V2"

    async def route_change(route: ft.RouteChangeEvent):
        page.views.clear()

        async def login(_):
            resp = request("load", username=username_tf.value)
            await page.show_snack_bar_async(
                new_snackbar(
                    f'Login successful.{f" Text: {resp.text}. Status: {resp.status_code}" if resp else ""}'
                )
            )

        async def to_signup(_):
            await page.go_async("/signup")

        page.views.append(
            ft.View(
                "/",
                [
                    username_tf,
                    password_tf,
                    ft.Row(
                        [ft.FilledTonalButton("Login", expand=True, on_click=login)],
                    ),
                ],
                ft.AppBar(
                    title=ft.Text("Login"),
                    center_title=True,
                    actions=[
                        ft.IconButton(
                            ft.icons.PERSON_ADD, tooltip="Signup", on_click=to_signup
                        )
                    ],
                ),
            )
        )
        if route.route == "/signup":

            async def signup(_):
                request(
                    "save",
                    User(
                        name=username_tf.value if username_tf.value else "<unknown>",
                        password=hash_password(password_tf.value),
                        created=time(),
                        data=SaveData(
                            silicon=0,
                            money=0,
                            upgrades=Upgrades(max_silicon=100, max_money=100),
                        ),
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
        # if page.route == "/store":
        #     page.views.append(
        #         ft.View(
        #             "/store",
        #             [
        #                 ft.AppBar(
        #                     title=ft.Text("Store"), bgcolor=ft.colors.SURFACE_VARIANT
        #                 ),
        #                 ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
        #             ],
        #         )
        #     )
        await page.update_async()

    async def view_pop(view: ft.ViewPopEvent):
        page.views.pop()
        top_view = page.views[-1]
        await page.go_async(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    await page.go_async(page.route)


if __name__ == "__main__":
    ft.app(app, "CI V2", None, 7993)
