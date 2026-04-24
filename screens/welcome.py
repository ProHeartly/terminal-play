from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static
from textual.containers import Center, Middle
import pyfiglet
import random

# Verse 1: I'm proud of myself after making this effect :D btw don't listen to startup.mov. PLEASE DON'T. I laughed at that thing for 1 hours straight.

# Verse 2: I'm tryna update the animation to something like glitchy effect.. let's have some funnnnn, SHALLL WEEE

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
        
    # this was the only solution that I could think of, for delayed animation start up.. Please don't judge meee

    def start_ani(self) -> None:
        self.timer = self.set_interval(0.1, self.tick)

    def tick(self) -> None:
        if self.idx <= self.max_w:
            rows = []
            is_glitch = random.random() < 0.2 # Uhhh I wanted to make the glitch look random so I'm experimenting with this.. lets see- if i like this

            for line in self.lines:
                base_part = line[:self.idx]

                if is_glitch:
                    glitch_chars = "".join(random.choice("@#$%&§?Ø") for _ in range(3))
                    rows.append(base_part[:-3] + glitch_chars)
                else:
                    rows.append(base_part + "█")

            self.query_one("#welcome-text").update("\n".join(rows))
            self.idx += 3
        else:
            self.timer.stop()
            self.query_one("#welcome-text").update("\n".join(self.lines)) # FOR removal of cursor btw.. if u are wondering about this part
            self.set_timer(1.5, self.done)


    def done(self) -> None:
        self.set_timer(2, self.navigate)
    
    def navigate(self) -> None:
        self.app.startup()