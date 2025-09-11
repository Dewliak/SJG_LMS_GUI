from nicegui import ui


def create_header():
    with ui.header().classes("bg-primary text-white"):
        ui.label("My App")
        ui.button("Home", on_click=lambda: ui.navigate.to("/"))
        ui.button("CRUD", on_click=lambda: ui.navigate.to("/crud"))
        ui.button("Add book", on_click=lambda: ui.navigate.to("/add_book"))
