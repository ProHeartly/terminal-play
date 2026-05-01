from textual_slider import Slider
from rich.text import Text
from rich.console import RenderableType

# I will add more custom sliders here

class TimelineSlider(Slider):
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