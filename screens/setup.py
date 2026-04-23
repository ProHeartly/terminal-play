from textual.app import ComposeResult
from textual.widgets import Header, Footer, Input, Button, Label, ListItem, ListView, Static, DirectoryTree
from textual.screen import Screen
from textual.containers import Vertical, Horizontal, Center, Container

#last time I used AI for reference but I think I can cook with my own thingy..

class SetupScreen(Screen):
    def __init__(self):
        super().__init__()
        self.pending_paths = []

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical(id="browser-side"): # dont mind about the name ;-; I alr told you I don't really know what to name../
                yield Label(" [b]1. BROWSE FOLDERS[/]", classes="setup-title") # using class instead of ID feels weird but my web dev friend suggest me to use cuz i can stack the css effect to different TITLEs
                yield DirectoryTree("./", id="dir-tree")
                yield Static("Double-click or Enter to select", id="tree-hint")

            with Vertical(id="queue-side"):
                yield Label(" [b]2. SELECETED PATHS [/]", classes="setup-title")
                yield ListView(id="queue-list")

                with Horizontal(id="setup-actions"):
                    yield Button("Clear ALL", variant="error", id="btn-clear")
                    yield Button("Start SYNC", variant="success", id="btn-sync")
        yield Footer()

    def on_directory_tree_seleceted(self, event: DirectoryTree.DirectorySelected) -> None:
        path_str = str(event.path)

        if path_str not in self.pending_paths:
            self.pending_paths.append(path_str)
            self.query_one("queue-list").append(ListItem(Static(f"📁 {path_str}"))) # I hope this looks good :D (if u are reading this, this acctually looks good)
            self.app.notify(f"Added {event.path.name}")
        else:
            self.app.notify("Folder already in queue! ;-;", severity="warning")

    def on_button_presss(self, event: Button.press) -> None:
        if event.button.id == "btn-clear":
            self.pending_paths = []
            self.query_one("#queue-list").clear()
        elif event.button.id == "btn-sync":
            if not self.pending_paths:
                self.app.notify("Choose atleast one folder baka!!", severity="error")
                return
            
            self.app.notify("Brewing the holy poition of songs ;-;") # Someone suggest some good meme pleaseeeee
            self.app.songs = self.app.lib.build(self.pending_paths)
            self.app.resolve_startup()
            

