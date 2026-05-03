from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static
from rich.text import Text

# Verse 1: I'm proud of myself after making this effect :D btw don't listen to startup.mov. PLEASE DON'T. I laughed at that thing for 1 hours straight.

# Verse 2: I'm tryna update the animation to something like glitchy effect.. let's have some funnnnn, SHALLL WEEE

# Verse 3: The previous animation didn't go as planned so I'm thinking of making first normal cursor effect then when everything loads, some glitching effect..

# Verse 4: YOOOOOOO I updated the animation by drasticc.... I made custom welcome screen in davinci and then used one script to convert .mov into ascii animations


try:
    from assets.ascii.welcome_ani import FRAMES
except ImportError:
    FRAMES = []

class WelcomeScreen(Screen):
    # when I tried to keep this in our main style.tcss.. it didnt work and made text disappear so I just put it here
    CSS = """
    WelcomeScreen {
        background: #000000;
        align: center middle;
    }

    #welcome-video {
        width: 100%;
        height: 100%;
        content-align: center middle;
        text-align: center;
        color: #FFB86C;
    }

    #skip-hint {
        dock: bottom;
        text-align: center;
        color: #444444;
        padding: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Static("", id="welcome-video", markup=False)
        yield Static("press esc to skip", id="skip-hint")

    def on_mount(self) -> None:
        self.app.audio.play_sfx("assets/sfx/welcome.wav")
        self.current_frame = 0
        self.total_frames = len(FRAMES)

        if self.total_frames > 0:
            self.timer = self.set_interval(0.08, self.next_frame)
        else:
            self.query_one("#welcome-video").update("Welcome to the Revolution!") # Backup
            self.set_timer(2, self.navigate)

    def next_frame(self) -> None:
        if self.current_frame < self.total_frames:
            content = FRAMES[self.current_frame]
            self.query_one("#welcome-video").update(content)
            
            self.current_frame += 1
        else:
            self.timer.stop()
            self.set_timer(0.5, self.navigate)

    def navigate(self) -> None:
        self.app.startup()

    def on_key(self, event) -> None:
        if event.key == "escape":
            try:
                self.timer.stop()
            except:
                pass
            self.app.startup()