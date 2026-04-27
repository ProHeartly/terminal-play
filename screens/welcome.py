from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static
from textual.containers import Center, Middle
import pyfiglet
import random

# Verse 1: I'm proud of myself after making this effect :D btw don't listen to startup.mov. PLEASE DON'T. I laughed at that thing for 1 hours straight.

# Verse 2: I'm tryna update the animation to something like glitchy effect.. let's have some funnnnn, SHALLL WEEE

# Verse 3: The previous animation didn't go as planned so I'm thinking of making first normal cursor effect then when everything loads, some glitching effect..

class WelcomeScreen(Screen):

    def compose(self) -> ComposeResult:
        with Center():
            with Middle():
                yield Static("", id="welcome-text")

    def on_mount(self) -> None:
        #self.app.audio.play_sfx("assets/startup.mp3")
        fig = pyfiglet.Figlet(font='epic', width=100)
        self.text_1 = fig.renderText("HELLO, USER..").splitlines()
        self.text_2 = fig.renderText("HAVE     FUN").splitlines()

        self.lines = self.text_1
        self.max_w = max(len(l) for l in self.text_1)
        self.idx = 0
        self.glitch_count = 0

        self.set_timer(0.5, self.start_ani)
        
    # this was the only solution that I could think of, for delayed animation start up.. Please don't judge meee

    def start_ani(self) -> None:
        self.timer = self.set_interval(0.01, self.tick)

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
            self.set_timer(1.5, self.done_1)

    def done_1(self) -> None:
        self.set_timer(2, self.start_ani_1)

    def start_ani_1(self) -> None:
        self.timer.stop()
        self.timer = self.set_interval(0.08, self.glitch_morph)

    def glitch_morph(self) -> None:
        self.glitch_count += 1

        if self.glitch_count < 12:
            rows = []
            for line in self.text_1:
                glitched = "".join(
                    c if random.random() > 0.3 else random.choice("@#$%&§?Ø")
                    for c in line
                )
                rows.append(glitched)
            self.query_one("#welcome-text").update("\n".join(rows))
        elif self.glitch_count < 20:
            self.lines = self.text_1 if random.random() > 0.5 else self.text_2
            self.query_one("#welcome-text").update("\n".join(self.lines))
        else:
            self.timer.stop()
            self.query_one("#welcome-text").update("\n".join(self.text_2))
            self.set_timer(1, self.navigate)
    
    def navigate(self) -> None:
        self.app.startup()