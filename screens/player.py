from textual.app import ComposeResult, RenderResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Button, Static, Label, Switch, DataTable
from textual_slider import Slider
from textual.containers import Vertical, Horizontal, Middle
import random
from rich.text import Text
from rich.console import RenderableType
from assets.ascii.visual_ani import FRAMES # Don't change frames_data to fun -_-

from custom.slider import TimelineSlider, VolumeSlider # I made this so that I could add this in other files too
#from custom.button import CircularButton
# Verse 1: I had fun making this.. I experimented with different style, color combination and came to like the current one.. (IT WILL HAVE UPDATE IN FUTURE)
# Tryna make something new :D  and this could break the system so making new file
# Verse 2: I made something better UI........ I'M SOOOOO HAPPYYY TO SEE THISSS UI WORKKK
# Verse 3: I'm revamping auto-play next button into something modern

class PlayerScreen(Screen):
    def __init__(self):
        self.loop_one = False
        super().__init__()
    
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
                        yield AsciiCinema(frames=FRAMES, fps=20, id="visualiser") # ANIMATIONNNNNn

            with Vertical(id="timeline-wrapper"):
                with Horizontal(id="timeline-info"):
                    yield Label("00:00", id="start-time")
                    yield TimelineSlider(min=0, max=100, step=1, value=0, id="timeline-slider")
                    yield Label("00:00", id="end-time")
                
            with Horizontal(id="button-row"):
                with Horizontal(id="vol-section"):
                    yield VolumeSlider(min=0, max=100, step=5, value=70, id="vol-slider") # I made my own custom sliderrrr for voluee
                    yield Label("70%🔊", id="vol-label")
                    
                with Horizontal(id="controls-section"):
                    yield Button("<", id="prev")
                    yield Button("||", id="pause")
                    yield Button(":▶", id="resume")
                    yield Button(">", id="next")
                    
                with Horizontal(id="next-section"):
                    yield Button(Text("[auto-next]"), id="loop-mode") # Oops I discovered u can JUST CHANGE LABEL OF button ;-;
                    # {{{{{{{{if u are wondering why [[ ]], cuz appearently [ ] is used for styling so it wont render single ones}}}}}}}}
                    # NVMMMM ABOUT upper line.. i think i found the fix when i was tryna fix song-title in mini_player.py

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
        if self.app.audio.finished():
            if self.loop_one:
                self.app.audio.load(self.app.cur_song['path']) 
                self.app.audio.play()
            else:
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

        elif event.button.id == "loop-mode":
            if self.loop_one:
                self.loop_one = False
                event.button.label = Text("[auto-next]") # YAHHH I fixed "[[]]" issue with Text() *.* :D immm sooo smartttt
            else:
                self.loop_one = True
                event.button.label = Text("[loop]")

    def on_slider_changed(self, event: Slider.Changed) -> None:
        if event.slider.id == "vol-slider":
            self.app.audio.set_volume(event.value / 100)
            if event.value > 70:
                self.query_one("#vol-label").update(f"{event.value}%🔊")
            elif event.value > 40:
                self.query_one("#vol-label").update(f"{event.value}%🔉")
            elif event.value != 0:
                self.query_one("#vol-label").update(f"{event.value}%🔈")
            else:
                self.query_one("#vol-label").update(f"{event.value}%🔇")

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
            return Text(self.frames[self.frame_index], style="#732323")
        
        return Text(self.frames[self.frame_index], style="#C11313")

# WAIT!! did u acctually read all the code?? and what are you even doing here?