from textual.app import ComposeResult
from textual.widgets import Header, Footer, Input, Button, Label, ListItem, ListView, Static, DirectoryTree, Tabs, Tab
from textual.screen import Screen
from textual.containers import Vertical, Horizontal, Center, Container
import os
from pathlib import Path


#last time I used AI for reference but I think I can cook with my own thingy..

class SetupScreen(Screen):
    def __init__(self):
        super().__init__()
        self.pending_paths = []

    def get_drive(self):
        drives = []
        uppercase_letters = ["A", "B", "C", "D", "E", "F", "G","H", "I", "J", "K", "L", "M", "N","O", "P", "Q", "R", "S", "T","U", "V", "W", "X", "Y", "Z"] # Used AI for this btw :D
        if os.name == 'nt': # I had to look up this cuz it had been a while since I used this condition.. interesting isn't it??
            for letter in uppercase_letters:
                drive = f"{letter}:\\"
                if os.path.exists(drive):
                    drives.append(drive)
        else:
            drives = ["/"] # I don't really know if it works for mac/linux.. please raise issue if it doesn't work :D

        return drives

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical(id="browser-side"): # dont mind about the name ;-; I alr told you I don't really know what to name../
                yield Label(" [b]1. BROWSE FOLDERS[/]", classes="setup-title") # using class instead of ID feels weird but my web dev friend suggest me to use cuz i can stack the css effect to different TITLEs
                yield Tabs(*[Tab(d, id=f"drive-{d[0]}") for d in self.get_drive()], id="drive-tabs")
                yield DirectoryTree("C:\\", id="dir-tree") # Starts at C: cuz why not.. I think this might raise some issue for other OS
                yield Button("SELECT", variant="primary", id="btn-add-folder")
                yield Static("Click the button to select", id="tree-hint")

            with Vertical(id="queue-side"):
                yield Label(" [b]2. SELECETED PATHS [/]", classes="setup-title")
                yield ListView(id="queue-list")

                with Horizontal(id="setup-actions"):
                    yield Button("Clear ALL", variant="error", id="btn-clear")
                    yield Button("Start SYNC", variant="success", id="btn-sync")
        yield Footer()

    def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:
        drive_path = event.tab.label.plain
        tree = self.query_one("#dir-tree", DirectoryTree)
        tree.path = drive_path

    def on_directory_tree_selected(self, event: DirectoryTree.DirectorySelected) -> None:
        self.add_folder_to_queue(event.path)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-clear":
            self.pending_paths = []
            self.query_one("#queue-list").clear()
        elif event.button.id == "btn-sync":
            if not self.pending_paths:
                self.app.notify("Choose atleast one folder baka!!", severity="error")
                return
            
            self.app.notify("Brewing the holy poition of songs ;-;") # Someone suggest some good meme pleaseeeee
            self.app.songs = self.app.lib.build(self.pending_paths)
            self.app.startup()
        elif event.button.id == "btn-add-folder":
            tree = self.query_one("#dir-tree", DirectoryTree)
            node = tree.cursor_node

            if node and node.data:
                path = node.data.path
                if path.is_dir():
                    self.add_folder_to_path(path)
                else:
                    self.app.notify("You selected file baka! Select FOLDER/DIRECTORY..", severity="warning")

    def add_folder_to_path(self, path: Path) -> None:
        path_str = str(path)
        if path_str not in self.pending_paths:
            self.pending_paths.append(path_str)
            self.query_one("#queue-list").append(ListItem(Static(f"📁 {path_str}")))
            self.app.notify(f"Added {path.name}")
        else:
            self.app.notify("Folder is already there!? WHY RAGEBAITT", severity="warning")
