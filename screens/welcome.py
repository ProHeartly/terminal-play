from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static
from textual.containers import Center, Middle
import pyfiglet
from time import sleep

class WelcomeScreen(Screen):

    def compose(self) -> ComposeResult:
        with Center():
            with Middle():
                yield Static("", id="welcome-text")

    def on_mount(self) -> None:
        self.app.audio.play_sfx("assets/startup.mp3")
        fig = pyfiglet.Figlet(font='epic', width=100)
        self.ascii_art = fig.renderText("HELLO, USER..")

        self.lines = self.ascii_art.splitlines()
        self.max_w = max(len(l) for l in self.lines)
        self.idx = 0

        self.set_timer(1, self.start_ani)
        
    
    def start_ani(self) -> None:
        self.timer = self.set_interval(0.08, self.tick)

    def tick(self) -> None:
        if self.idx <= self.max_w:
            rows = []
            for line in self.lines:
                rows.append(line[:self.idx] + "█")
            
            self.query_one("#welcome-text").update("\n".join(rows))
            self.idx += 2
        else:
            self.timer.stop()
            self.query_one("#welcome-text").update("\n".join(self.lines))
            self.set_timer(1.5, self.done)
        
    def done(self) -> None:
        self.set_timer(2, self.navigate)
    
    def navigate(self) -> None:
        self.app.startup()