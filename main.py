from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, DataTable, Static, Button
from textual.screen import Screen
from textual.containers import Vertical

from back import SongLibrary, Player

from screens.library import LibraryScreen
from screens.welcome import WelcomeScreen
from screens.setup import SetupScreen
from screens.player import PlayerScreen

# I just searched what what library I may need :D.. I guess most of them are not even needed

class TerminalPlayer(App):

    CSS_PATH = "style.tcss"

    def on_mount(self) -> None:
        self.lib = SongLibrary("library.json")
        self.audio = Player()
        self.songs = []
        self.cur_idx = 0
        self.install_screen(WelcomeScreen(), name="welcome") # FINALLY THE AI SUGGESTED SOMETHING GOOD... "ONLY USED AI FOR REFERENCE ;-;"
        self.install_screen(LibraryScreen(), name="library")
        self.install_screen(PlayerScreen(), name="player")
        self.install_screen(SetupScreen(), name="setup")
        #self.install_screen()

        self.push_screen("welcome")
        # self.indexer = SongLibrary("D:\\songs")
        # self.audio = Player()
        # self.songs = self.indexer.build([])
        # self.cur_song = None

        # self.push_screen(LibraryScreen())

    def play_song(self, idx) -> None:
        self.cur_idx = idx
        self.cur_song = self.songs[idx]

        self.audio.stop()
        if self.audio.load(self.cur_song["path"]):
            self.audio.play()

            if self.screen.name == "player":
                self.screen.update_ui()

    def next_song(self) -> None:
        if self.songs:
            next_idx = (self.cur_idx + 1) % len(self.songs)
            self.play_song(next_idx)

    def prev_song(self) -> None:
        if self.songs:
            next_idx = (self.cur_idx - 1) % len(self.songs)
            self.play_song(next_idx)

    def startup(self):
        if self.lib.exists():
            data = self.lib.readlib()
            self.songs = data.get("songs", [])
            self.switch_screen("library")
        else:
            self.notify("BAUNA GOD has summoned you..")
            self.switch_screen("setup")


if __name__ == "__main__":
    TerminalPlayer().run()