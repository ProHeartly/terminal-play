from textual.app import ComposeResult, RenderResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Button, Static, Label, Switch, DataTable
from textual_slider import Slider
from textual.containers import Vertical, Horizontal, Middle
import random
from rich.text import Text
from rich.console import RenderableType
from frames_data import FRAMES # Don't change frames_data to fun -_-

# Verse 1: I had fun making this.. I experimented with different style, color combination and came to like the current one.. (IT WILL HAVE UPDATE IN FUTURE)
# Tryna make something new :D  and this could break the system so making new file
# Verse 2: I made something better UI........ I'M SOOOOO HAPPYYY TO SEE THISSS UI WORKKK

class PlayerScreen(Screen):
    def compose(self) -> ComposeResult:
        with Vertical(id="player-container"):
            with Horizontal(id="top-nav"):
                yield Button("←", id="go-back")
                yield Label("PLAYLIST", id="playlist-name-title")
                yield Button("☰", id="menu-btn")
            with Horizontal(id="middle-content"):
                with Vertical(id="left-pane"):
                    with Horizontal(id="art-container"):
                        yield Static("", id="big-art") # I wanted to add like some media inside of this.. I will add in some future update ;-;

                    with Vertical(id="info-container"):
                        yield Static("Song Title Loading...", id="song-title")
                        yield Static("Song Artist Loading...", id="song-artist")

                with Vertical(id="right-pane"):
                    with Horizontal(id="visualiser-container"):
                        yield AsciiCinema(frames=FRAMES, fps=10, id="visualiser") # ANIMATIONNNNNn

            with Vertical(id="timeline-wrapper"):
                with Horizontal(id="timeline-info"):
                    yield Label("00:00", id="start-time")
                    yield CircleSlider(min=0, max=100, step=1, value=0, id="timeline-slider")
                    yield Label("00:00", id="end-time")
                
            with Horizontal(id="button-row"):
                with Horizontal(id="vol-section"):
                    yield Slider(min=0, max=100, step=5, value=70, id="vol-slider")
                    yield Label("🔊")
                    
                with Horizontal(id="controls-section"):
                    yield Button("⏮ ", id="prev")
                    yield Button("||", id="pause", variant="warning")
                    yield Button(">", id="resume", variant="success") # > cuz why not :p
                    yield Button("⏭ ", id="next")
                    
                with Horizontal(id="next-section"):
                    yield Label("Auto-Play Next", id="auto-play")
                    yield Switch(value=True, id="auto-play-switch")

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
            self.query_one("#song-artist").update(s.get('artist', 'Unknown Artist'))
            self.query_one("#big-art").update("(Music Playing)")
            self.refresh_timeline()
        
    def poll_status(self) -> None:
        if self.query_one("#auto-play-switch").value:
            if self.app.audio.finished():
                self.app.next_song()
                self.update_ui()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        visualiser = self.query_one("#visualiser", AsciiCinema)
        if event.button.id == "pause":
            self.app.audio.pause()
            self.query_one("#pause").display = False
            self.query_one("#resume").display = True
            visualiser.playing = False

        elif event.button.id == "resume":
            self.app.audio.resume()
            self.query_one("#pause").display = True
            self.query_one("#resume").display = False
            visualiser.playing = True

        elif event.button.id == "next":
            self.app.next_song()
            self.update_ui()

        elif event.button.id == "prev":
            self.app.prev_song()
            self.update_ui()

        elif event.button.id == "go-back":
            self.app.switch_screen("home")

    def on_slider_changed(self, event: Slider.Changed) -> None:
        if event.slider.id == "vol-slider":
            self.app.audio.set_volume(event.value / 100)

        elif event.slider.id == "timeline-slider":
            _, total, _ = self.app.audio.progress()
            target = (event.value / 100) * total

            self.query_one("#start-time").update(self.to_mmss(target))

            if event.slider.has_focus:
                self.app.audio.seek(target)

    def on_screen_resume(self) -> None:
        self.update_ui()
        self.query_one("#visualiser", AsciiCinema).playing = True
        self.query_one("#pause").display = True
        self.query_one("#resume").display = False

    def on_screen_suspend(self) -> None:
        self.query_one("#visualiser", AsciiCinema).playing = False # saves resource when screen is not active

# Let's have some fun with ANIMATIONNNN
class AsciiCinema(Static):
    def __init__(self, frames, fps=12, **kwargs):
        super().__init__("", **kwargs)
        self.frames = frames
        self.frame_index = 0
        self.interval = 1.0 / fps # interval = time it takes to change between frames
        self.playing = True

    def on_mount(self) -> None:
        self.set_interval(self.interval, self.next_frame)
    
    def next_frame(self) -> None:
        if self.frames and self.playing:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.refresh()
    
    def render(self) -> RenderResult:
        if not self.frames:
            return Text("No Animation Data", style="red")
        
        if not self.playing:
            return Text(self.frames[self.frame_index], style="#008888")
        
        return Text(self.frames[self.frame_index], style="#00ffff")


"""
        Don't mind me... copy paste gemini code.. I wanted some cool circular slider ;-;
        and I'm not smart enough to make thisssss..
        I do know the process now thoooo so no AI from next time >.<
"""

class CircleSlider(Slider):
    def render(self) -> RenderableType:
        # 1. Safety check for width
        width = max(1, self.content_size.width)
        
        # 2. Calculate handle position
        pos_ratio = self._slider_position / 100
        handle_index = min(int(pos_ratio * width), width - 1)
        
        # 3. Define Colors (Hex is safer and looks better)
        # Using a nice gold/amber hex code
        GOLD_HEX = "#FFD700" 
        DIM_HEX = "#444444" 
        
        # 4. Build the bar segments
        track_char = "─"
        circle_char = "●"
        
        bar = Text()
        
        # Left side: The "filled" progress
        bar.append(track_char * handle_index, style=GOLD_HEX)
        
        # The Handle: The "Circle"
        bar.append(circle_char, style=f"bold {GOLD_HEX}")
        
        # Right side: The remaining track
        remaining = width - handle_index - 1
        if remaining > 0:
            bar.append(track_char * remaining, style=DIM_HEX)
        
        return bar

# WAIT!! did u acctually read all the code?? and what are you even doing here?