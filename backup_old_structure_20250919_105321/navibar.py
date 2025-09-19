import flet as ft


class NaviBar(ft.Container):
    """
    Navigation bar with buttons for various actions including showing the main app, 
    fullscreen, half-screen modes, and toggling 'always on top' state.
    """

    def __init__(self, context, **kwargs):
        super().__init__(**kwargs)
        self.context = context
        self.helper = context["helper"]
        self.page = context["helper"].page
        
        self.content = ft.Row([
            ft.IconButton(
                icon=ft.Icons.VISIBILITY,
                on_click=self.check_hwp,
                tooltip="한글보이기"
            ),
            ft.IconButton(
                icon=ft.Icons.FULLSCREEN,
                on_click=self.set_fullscreen,
                tooltip="전체화면"
            ),
            ft.IconButton(
                icon=ft.Icons.FULLSCREEN_EXIT,
                on_click=self.set_halfscreen,
                tooltip="오른쪽화면"
            ),
            ft.IconButton(
                icon=ft.Icons.PUSH_PIN,
                on_click=self.toggle_always_on_top,
                tooltip="항상 위"
            ),
        ])

    def check_hwp(self, e):
        """Show the main application window."""
        self.helper.check_hwp()

    def set_fullscreen(self, e):
        """Set the application to fullscreen."""
        self.helper.set_fullscreen()

    def set_halfscreen(self, e):
        """Set the application to half-screen."""
        self.helper.set_halfscreen()

    def toggle_always_on_top(self, e):
        """Toggle the 'always on top' state of the window."""
        self.page.window_always_on_top = not self.page.window_always_on_top
        self.page.update()
