from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, DataTable, Static
from textual.containers import Vertical, Horizontal

class HomeScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="home-container"):
            yield Static("[bold gold] TERMINAL PLAY [/]", id="home-title")
            