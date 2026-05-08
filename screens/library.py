from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, DataTable, Footer, Button, Label
from textual.containers import Vertical, Horizontal, Center
from screens.mini_player import MiniPlayer

# verse 1: One of the easiest screen that I made... (FOR NOW **FORESHADOWING NEW UPDATES**)
# verse 2: I'm gonna change everything that I currently made, it will break but for better future *-*
# Verse 3: I added some CSS and also made Delete button ;-;

class LibraryScreen(Screen):
    def __init__(self, playlist: list, name: str = "Playlist", playlist_id = None):
        # TESTING NEW THINGS... hopeee this works [BABHAHAABFAKJALKjflkdsja]
        super().__init__()
        self.playlist = playlist
        self.playlist_name = name
        self.playlist_id = playlist_id

    def compose(self) -> ComposeResult:
        with Vertical(id="playlist-container"):
            with Horizontal(id="playlist-header"):
                yield Button("← Back", id="btn-back")
                with Center():
                    yield Label(f"[b]{self.playlist_name}[/b]", id="playlist-title")
                if self.playlist_id and not self.playlist_id.startswith("mix_"):
                    yield Button("Delete", id="btn-delete-playlist")
            yield DataTable(id="song-table", cursor_type="row")
        yield MiniPlayer(id="mini-player-bar")


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
        
        elif event.button.id == "btn-delete-playlist":
            self.app.lib.delete_playlist(self.playlist_id)
            self.app.notify(f"Playlist '{self.playlist_name}' deleted. (T_T)", severity="error")
            self.app.get_screen("home").load_playlists()
            self.app.pop_screen()