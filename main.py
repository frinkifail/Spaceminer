import flet as ft
from client_utils import request, username_tf, password_tf


async def app(page: ft.Page):
    page.title = "CommandIncremental V2"

    async def route_change(route: ft.RouteChangeEvent):
        page.views.clear()
        async def login(_):
            request()
        page.views.append(
            ft.View(
                "/",
                [
                    username_tf,
                    password_tf
                ],
                ft.AppBar(title=ft.Text("Login"), center_title=True),
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
