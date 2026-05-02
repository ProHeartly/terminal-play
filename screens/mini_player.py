from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Label, Button, ProgressBar
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual_slider import Slider

from custom.slider import TimelineSlider

# THIS WILL BE REVOLUTIONNNNNN OF TERMINAL PLAYER...

# Uhhh, I'm jst experimenting so idk if this will work out ;)

# Let's revamp this thing into something good >.<

class MiniPlayer(Widget): # First time trying to make a widget ;-;
    def compose(self) -> ComposeResult:
        with Horizontal(id="mini-player"):
            with Vertical(id="mini-info"):
                yield Label("No song playing", id="mini-title")
                yield Label("", id="mini-artist")
            with Horizontal(id="mini-controls"):
                yield Button("<<", id="mini-prev")
                yield Button("||", id="mini-pause")
                yield Button(":▶", id="mini-resume")
                yield Button(">>", id="mini-next")
            with Vertical(id="mini-timeline-wrapper"):
                with Horizontal(id="mini-timeline-info"):
                    yield Label("00:00", id="mini-start-time")
                    yield TimelineSlider(min=0, max=100, step=1, value=0, id="mini-timeline-slider")
                    yield Label("00:00", id="mini-end-time")

    def on_mount(self) -> None:
        self.query_one("#mini-resume").display = False
        self.set_interval(0.5, self.update_ui)
        # 0.5 should be smooth enough ._.

    def update_ui(self) -> None:
        song = self.app.cur_song
        if not song:
            return
        
        self.query_one("#mini-title").update(song["title"])
        self.query_one("#mini-artist").update(song["artist"])

        curr, total, pct = self.app.audio.progress()
        slider = self.query_one("#mini-timeline-slider")
        slider.value = pct
        self.query_one("#mini-start-time").update(self.to_mmss(curr))
        self.query_one("#mini-end-time").update(self.to_mmss(total))

    def to_mmss(self, secs):
        m, s = divmod(int(secs), 60)
        return f"{m:02d}:{s:02d}"
    
    def on_slider_changed(self, event: Slider.Changed) -> None:
        if event.slider.id == "mini-timeline-slider":
                _, total, _ = self.app.audio.progress()
                target = (event.value / 100) * total

                self.query_one("#mini-start-time").update(self.to_mmss(target))

                if event.slider.has_focus:
                    self.app.audio.seek(target)
    
    def refresh_timeline(self) -> None:
        slider = self.query_one("#mini-timeline-slider")
        
        if slider.has_focus:
            self.query_one("#mini-prev").focus()
            return
        
        curr, total, pct = self.app.audio.progress()

        self.query_one("#mini-start-time").update(self.to_mmss(curr))
        self.query_one("#mini-end-time").update(self.to_mmss(total))
        slider.value = int(pct)

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
            self.update_ui()

        elif event.button.id == "mini-prev":
            self.app.prev_song()
            self.update_ui()

        event.stop()

    def on_click(self) -> None:
        self.app.push_screen("player") # I do love trying new things