from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, DataTable, Footer

class LibraryScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield DataTable(id="song-table", cursor_type="row")
        yield Footer()

    def on_mount(self) -> None:
        tbl = self.query_one(DataTable)
        tbl.add_columns("Title", "Artist", "Duration")

        for i, s in enumerate(self.app.songs):
            tbl.add_row(
                s['title'],
                s['artist'],
                s['duration'],
                key=str(i)
            )

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        from screens.player import PlayerScreen
        idx = int(event.row_key.value)
        self.app.play_song(idx)
        self.app.switch_screen("player")