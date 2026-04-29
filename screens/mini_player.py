from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Label, Button, ProgressBar
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive

# THIS WILL BE REVOLUTIONNNNNN OF TERMINAL PLAYER...

# Uhhh, I'm jst experimenting so idk if this will work out ;)

class MiniPlayer(Widget): # First time trying to make a widget ;-;
    def compose(self) -> ComposeResult:
        with Horizontal(id="mini-player"):
            with Vertical(id="mini-info"):
                yield Label("No song playing", id="mini-title")
                yield Label("", id="mini-artist")
            with Horizontal(id="mini-controls"):
                yield Button("⏮", id="mini-prev")
                yield Button("⏸", id="mini-pause")
                yield Button("▶", id="mini-resume")
                yield Button("⏭", id="mini-next")
            yield ProgressBar(total=100, show_eta=False, show_percentage=False, id="mini-progress")

    def on_mount(self) -> None:
        self.query_one("#mini-resume").display = False
        self.set_interval(0.5, self.tick)
        # 0.5 should be smooth enough ._.

    def tick(self) -> None:
        song = self.app.cur_song
        if not song:
            return
        
        self.query_one("#mini-title").update(song["title"])
        self.query_one("#mini-artist").update(song["artist"])

        curr, total, pct = self.app.audio.progress()
        self.query_one("#mini-progress").update(progress=pct)

    # Same as normal player.py but small ;-;
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "mini-pause":
            self.app.audio.pause()
            self.query_one("#mini-pause").display = False
            self.query_one("#mini-resume").display = True

        elif event.button.id == "mini-resume":
            self.app.audio.resume()
            self.query_one("#mini-pause").display = True
            self.query_one("#mini-resume").display = False

        elif event.button.id == "mini-next":
            self.app.next_song()
            self.tick()

        elif event.button.id == "mini-prev":
            self.app.prev_song()
            self.tick()

        event.stop()

    def on_click(self) -> None:
        self.app.push_screen("player") # I do love trying new things