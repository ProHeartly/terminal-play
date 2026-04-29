from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, DataTable, Footer, Button, Label
from textual.containers import Vertical, Horizontal
from screens.mini_player import MiniPlayer

# verse 1: One of the easiest screen that I made... (FOR NOW **FORESHADOWING NEW UPDATES**)
# verse 2: I'm gonna change everything that I currently made, it will break but for better future *-*

class LibraryScreen(Screen):
    def __init__(self, playlist: list, name: str = "Playlist"):
        # TESTING NEW THINGS... hopeee this works [BABHAHAABFAKJALKjflkdsja]
        super().__init__()
        self.playlist = playlist
        self.playlist_name = name

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="playlist-container"):
            with Horizontal(id="playlist-header"):
                yield Button("← Back", id="btn-back", variant="primary")
                yield Label(f"[b]{self.playlist_name}[/b]", id="playlist-title")
            yield DataTable(id="song-table", cursor_type="row")
        yield MiniPlayer(id="mini-player-bar")
        yield Footer()

    def on_mount(self) -> None:
        tbl = self.query_one(DataTable)
        tbl.add_columns("Title", "Artist", "Duration")

        for i, s in enumerate(self.playlist):
            tbl.add_row(
                s['title'],
                s['artist'],
                s['duration'],
                key=str(i)
            )

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        idx = int(event.row_key.value)
        self.app.songs = self.playlist
        self.app.play_song(idx)
        self.app.switch_screen("player")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-back":
            self.app.pop_screen()