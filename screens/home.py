from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Button, Static, Label
from textual.containers import Vertical, Horizontal, ScrollableContainer
from screens.mini_player import MiniPlayer
from screens.library import LibraryScreen

# VERSE 1: gonna make something like yt music or spotify buttt later I'm gonna touch my typa creativity.
# Quote of the file: "Make it before you perfect it" - ME

class HomeScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="home-container"):
            yield Static("[b] TERMINAL PLAY [/]", id="home-title")
            yield Label("AUTO PLAYLISTS", classes="section-label")
            with ScrollableContainer(id="auto-playlists"):
                pass # Filled in on_mount
            yield Label("YOUR PLAYLISTS", classes="section-label")
            with ScrollableContainer(id="user-playlists"):
                pass # same as auto-playlists

        yield MiniPlayer(id="mini-player-bar")
        yield Footer()

    def on_mount(self) -> None:
        self.app.lib.refresh_random_playlists()
        self.load_playlists()

    def load_playlists(self) -> None:
        playlists = self.app.lib.get_playlists()

        auto_container = self.query_one("#auto-playlists")
        user_container = self.query_one("#user-playlists")

        for pl in playlists:
            btn = Button(
                f"  {pl['name']} ({len(pl['songs'])} songs)",
                id=f"pl-{pl['id']}",
                classes="playlist-btn"
            ) # Making playlist as button ;-; I'm SMART.. aren't I??
            if pl["type"] == "auto":
                auto_container.mount(btn)
            else:
                user_container.mount(btn)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if not event.button.id.startswith("pl-"): # this filter outs all the crappy or mistakely clicked button issue
            return
        
        pl_id = event.button.id[3:] # Starts with "pl-" so lets skip it
        playlists = self.app.lib.get_playlists()

        for pl in playlists:
            if pl["id"] == pl_id:
                self.app.push_screen(LibraryScreen(pl["songs"], pl["name"])) # Opens NEW AND CHANGEd library screen
                break