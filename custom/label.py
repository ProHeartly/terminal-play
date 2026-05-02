from textual.widgets import Static
from rich.text import Text # THIS IS DAMN important cuz in title of songs, they often use "[]" but it gets formatted and removed so we will use this to our advantage

# Marquee typa animation when the text gets overflowed..
# This animation doesn't get played normally but if the text overflows, in normal text.. it should be hidden but due to this custom Label type, it plays marquee animation to show the text.
# Also Text() is used to get rid of "[]" formatting
class MarqueeLabel(Static):
    def __init__(self, text: str = "", **kwargs):
        super().__init__(Text(str(text)), **kwargs)
        self.old_text = str(text)
        self.gap = "   |    "
        self.display_text = self.old_text + self.gap
        self.step = 0

    def update_text(self, new_text: str) -> None:
        new_text = str(new_text)
        if new_text == self.old_text:
            return
        
        self.old_text = new_text
        self.display_text = new_text + self.gap
        self.step = 0
        self.update(Text(self.old_text))

    def on_mount(self) -> None:
        self.set_interval(0.2, self.scroll)

    def scroll(self) -> None:
        width = self.content_size.width

        if width > 0 and len(self.old_text) > width:
            pool = self.display_text * 3
            cycle_lenth = len(self.display_text)
            self.step = (self.step + 1) % cycle_lenth
            renderable = pool[self.step : self.step + width]

            self.update(Text(renderable))

        else:
            if self.step != 0:
                self.step = 0
            self.update(Text(self.old_text))