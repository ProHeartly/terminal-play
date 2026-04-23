from textual.app import ComposeResult
from textual.widgets import Header, Footer, Input, Button, Label, ListItem, ListView, Static
from textual.screen import Screen
from textual.containers import Vertical, Horizontal, Center, Container

class SetupScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical(id="nav-rail"):
                yield Static("INDEXER", classes="nav-header")
                yield Button("Add Source", variant="primary", classes="nav-item")
                yield Static("", id="nav-spacer")
                yield Static("[dim]v1.0[/]")

            with Container(id="workspace"):
                yield Label("Library Setup", classes="h1")
                yield Label("Enter the full path to your music folder:")
                
                yield Input(placeholder="e.g. D:\Music or /home/user/music", id="path-input")
                yield Button("Add to Queue", id="cmd-add")

                yield Label("Pending Folders", id="queue-label")
                with Vertical(id="path-queue-container"):
                    yield ListView(id="path-queue")
                
                with Horizontal(id="action-group"):
                    yield Button("Clear", variant="error", id="cmd-reset")
                    yield Button("Finalize & Sync", variant="success", id="cmd-sync", classes="btn-finish")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        input_widget = self.query_one("#path-input", Input)
        queue = self.query_one("#path-queue", ListView)

        if event.button.id == "cmd-add":
            path = input_widget.value.strip()
            if path:
                # Add to UI
                item = ListItem(Static(f"📂 {path}"))
                item.target_path = path
                queue.append(item)
                input_widget.value = ""
                self.app.notify(f"Added {path}")
            else:
                self.app.notify("Path cannot be empty", severity="error")

        elif event.button.id == "cmd-reset":
            queue.clear()
            self.app.notify("Queue cleared")

        elif event.button.id == "cmd-sync":
            targets = [getattr(item, "target_path") for item in queue.children]
            
            if not targets:
                self.app.notify("No folders to sync!", severity="error")
                return

            self.app.notify("Scanning metadata...")
            self.app.songs = self.app.lib.build(targets)
            
            self.app.startup()

