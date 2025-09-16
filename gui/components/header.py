from nicegui import ui


def create_header():
    with ui.header().classes("bg-primary text-white"):
        with ui.row().classes('w-full items-center'):
                ui.button("Home", on_click=lambda: ui.navigate.to("/"))
                ui.button("Books", on_click=lambda: ui.navigate.to("/crud"))
                ui.button("Return book", on_click=lambda: ui.navigate.to("/return"))
                ui.button("Add book", on_click=lambda: ui.navigate.to("/add_book"))
                ui.button("QR Codes", on_click=lambda: ui.navigate.to("/qr"))
                ui.button("Info", on_click=lambda: ui.navigate.to("/info"))
                ui.label("SJG LMS").classes('font-bold ml-auto mr-30 text-2xl')