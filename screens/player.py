from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Button, Static, Label, Switch
from textual_slider import Slider
from textual.containers import Vertical, Horizontal

class PlayerScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="player-container"):
            with Horizontal(id="art-container"):
                yield Static("", id="big-art")

            yield Static("", id="song-title")

            with Vertical(id="timeline-wrapper"):
                with Horizontal(id="timeline-info"):
                    yield Label("00:00", id="start-time")
                    yield Slider(min=0, max=100, step=1, value=0, id="timeline-slider")
                    yield Label("00:00", id="end-time")
            
            with Horizontal(id="button-row"):
                with Horizontal(id="vol-section"):
                    yield Slider(min=0, max=100, step=5, value=70, id="vol-slider")
                    yield Label("🔊")
                
                with Horizontal(id="controls-section"):
                    yield Button("⏮ ", id="prev")
                    yield Button("||", id="pause", variant="warning")
                    yield Button("▶", id="resume", variant="success")
                    yield Button("⏭ ", id="next")
                
                with Horizontal(id="next-section"):
                    yield Label("Auto-Play Next")
                    yield Switch(value=True, id="auto-play-switch")

            yield Button("Back to Library", id="go-back", variant="primary")
        yield Footer()
    
    def on_mount(self) -> None:
        self.update_ui()
        self.query_one("#resume").display = False
        self.set_interval(0.5, self.refresh_timeline)
        self.set_interval(1.0, self.poll_status)

    def refresh_timeline(self) -> None:
        slider = self.query_one("#timeline-slider")
        
        if slider.has_focus:
            self.query_one("#next").focus()
            return
        
        curr, total, pct = self.app.audio.progress()

        self.query_one("#start-time").update(self.to_mmss(curr))
        self.query_one("#end-time").update(self.to_mmss(total))
        slider.value = int(pct)

    def to_mmss(self, secs):
        m, s = divmod(int(secs), 60)
        return f"{m:02d}:{s:02d}"
    
    def update_ui(self) -> None:
        s = self.app.cur_song
        if s:
            self.query_one("#song-title").update(f"[b]{s['title']}[/b]")
            self.query_one("#big-art").update("(Music Playing)")
            self.refresh_timeline()
        
    def poll_status(self) -> None:
        if self.query_one("#auto-play-switch").value:
            if self.app.audio.finished():
                self.app.next_song()
                self.update_ui()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "pause":
            self.app.audio.pause()
            self.query_one("#pause").display = False
            self.query_one("#resume").display = True

        elif event.button.id == "resume":
            self.app.audio.resume()
            self.query_one("#pause").display = True
            self.query_one("#resume").display = False

        elif event.button.id == "next":
            self.app.next_song()
            self.update_ui()

        elif event.button.id == "prev":
            self.app.prev_song()
            self.update_ui()

        elif event.button.id == "go-back":
            self.app.switch_screen("library")

    def on_slider_changed(self, event: Slider.Changed) -> None:
        if event.slider.id == "vol-slider":
            self.app.audio.set_volume(event.value / 100)

        elif event.slider.id == "timeline-slider":
            _, total, _ = self.app.audio.progress()
            target = (event.value / 100) * total

            self.query_one("#start-time").update(self.to_mmss(target))

            if event.slider.has_focus:
                self.app.audio.seek(target)