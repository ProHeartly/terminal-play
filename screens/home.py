from textual.app import ComposeResult
from textual.screen import Screen, ModalScreen
from textual.widgets import Header, Footer, Button, Static, Label, DataTable, ListItem, ListView, TabbedContent, TabPane, Input, SelectionList
from textual.containers import Vertical, Horizontal, ScrollableContainer, Center, HorizontalScroll, Container
from textual.widgets.selection_list import Selection

from screens.mini_player import MiniPlayer
from screens.library import LibraryScreen
from screens.setup import SetupScreen
import time
# VERSE 1: gonna make something like yt music or spotify buttt later I'm gonna touch my typa creativity.
# VERSE 2: I'm tryna improve the ui.. hope it looks good before I spend 10 hours on it T-T
# Quote of the file: "Make it before you perfect it" - ME
# Verse 3: Making playlist tab beautiful anddd workingg

class HomeScreen(Screen):
    def compose(self) -> ComposeResult: # the main screen's UI is damn complex.. I hope my future self would be able to read this ;-;
        yield Header()
        with Vertical(id="main-app-shell"):
            with TabbedContent(id="home-tabs"):
                with TabPane("🎵 Library", id="tab-library"):
                    yield DataTable(id="all-songs-table", cursor_type="row")

                with TabPane("📁 Playlists", id="tab-playlists"):
                    with ScrollableContainer(id="playlist-tab-container"):
                        with Horizontal(classes="playlist-header-row"):
                            yield Label("AUTO GENERATED", classes="section-label")
                            yield Button("🔄 Regenerate", id="btn-regenerate")
                        
                        with HorizontalScroll(id="auto-playlists"):
                            pass
                        
                        with Horizontal(classes="playlist-header-row"):
                            yield Label("YOUR PLAYLISTS", classes="section-label")
                            yield Button("➕ Create", id="btn-create-playlist")
                        
                        with HorizontalScroll(id="user-playlists"):
                            pass

                with TabPane("⚙ Settings", id="tab-settings"):
                    with ScrollableContainer(id="settings-scroll"):
                        yield Label("Music Directories", classes="section-label")
                        yield ListView(id="dir-list")
                        with Horizontal(id="settings-actions"):
                            yield Button("Add Directory", id="btn-add-dir")
                            yield Button("Remove Selected", id="btn-remove-dir")
                            yield Button("Re-Sync Library", id="btn-resync")
        
        yield MiniPlayer(id="mini-player-bar")

    def on_mount(self) -> None:
        self.app.lib.refresh_random_playlists()
        self.load_library() # Loads the library (list of all of your songs)
        self.load_playlists() # Loads the auto generated playlist and user's playlist
        self.load_setting() # Loads the settings >.<

    def load_library(self) -> None:
        tbl = self.query_one("#all-songs-table", DataTable)
        tbl.add_columns("Title", "Artist", "Duration")
        for i, s in enumerate(self.app.songs):
            tbl.add_row(s["title"], s["artist"], s["duration"], key=str(i))

    def load_playlists(self) -> None:
        playlists = self.app.lib.get_playlists()

        auto_container = self.query_one("#auto-playlists")
        user_container = self.query_one("#user-playlists")

        auto_container.remove_children()
        user_container.remove_children()
        
        stamp = int(time.time())
        for pl in playlists:
            btn = Button(
                f"  {pl['name']} \n({len(pl['songs'])} songs)",
                id=f"pl-{pl['id']}-{stamp}",
                classes="playlist-btn"
            ) # Making playlist as button ;-; I'm SMART.. aren't I??
            if pl["type"] == "auto":
                auto_container.mount(btn)
            else:
                user_container.mount(btn)
    
    def load_setting(self) -> None:
        data = self.app.lib.readlib()
        if not data:
            return
        dir_list = self.query_one("#dir-list", ListView)
        dir_list.clear()
        for d in data.get("directories", []):
            item_label = Static(f"📁 {d}", name=str(d)) # Fix for remove button previously not working
            dir_list.append(ListItem(item_label))

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        if event.data_table.id == "all-songs-table":
            idx = int(event.row_key.value)
            self.app.songs = self.app.lib.readlib().get("songs", [])
            self.app.play_song(idx)
            self.app.push_screen("player")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id.startswith("pl-"): # this filter outs all the crappy or mistakely clicked button issue
            raw = event.button.id[3:] # Starts with "pl-" so lets skip it
            pl_id = raw.rsplit("-", 1)[0] # removes the timestamp part >.<
            playlists = self.app.lib.get_playlists()

            for pl in playlists:
                if pl["id"] == pl_id:
                    self.app.push_screen(LibraryScreen(pl["songs"], pl["name"], pl["id"])) # Opens NEW AND CHANGEd library screen
                    break
        
        elif event.button.id == "btn-add-dir":
            self.app.push_screen(SetupScreen())

        elif event.button.id == "btn-remove-dir": # Finally this button works ;-) . I gave alpha testing to my friend and he said this wasn't working and raised error "AttributeError: 'Static' object has no attribute 'renderable'" but now.. I realised my big mistake. And its fixed now no worriess
            dir_list = self.query_one("#dir-list", ListView)
            if dir_list.highlighted_child:
                selected = dir_list.highlighted_child
                path = selected.query_one(Static).name
                data = self.app.lib.readlib()
                if data:
                    data["directories"] = [d for d in data["directories"] if d != path]
                    self.app.lib._writelib(data)
                    selected.remove()
                    self.app.notify(f"Removed {path}")

        elif event.button.id == "btn-resync":
            data = self.app.lib.readlib()
            if data:
                self.app.notify("Re-syncing library...")
                self.app.songs = self.app.lib.build(data["directories"])
                self.app.notify("Done! Restart to see changes.", severity="information")
        
        elif event.button.id == "btn-regenerate":
            self.app.lib.refresh_random_playlists()
            # Uhhh, regenerate cuzzz why not
            auto_container = self.query_one("#auto-playlists")
            auto_container.remove_children()
            playlists = self.app.lib.get_playlists()
            stamp = int(time.time()) # Time stamp for making unique id effortlessly
            for pl in playlists:
                if pl["type"] == "auto":
                    auto_container.mount(Button(
                        f"  {pl['name']}  \n({len(pl['songs'])} songs)",
                        id=f"pl-{pl['id']}-{stamp}",
                        classes="playlist-btn"
                    ))
            self.app.notify("Playlists regenerated")

        elif event.button.id == "btn-create-playlist":
            self.app.push_screen(CreatePlaylistScreen())


# creating playlist screen :D
class CreatePlaylistScreen(ModalScreen):
    def compose(self) -> ComposeResult:
        with Vertical(id="create-playlist-container"):
            yield Input(placeholder="Playlist Name..", id="pl-name-input")
            yield SelectionList(id="song-selection")

        with Horizontal(id="create-pl-action"):
            yield Button("Save", id="btn-save-pl")
            yield Button("Cancel", id="btn-cancel-pl")

    def on_mount(self) -> None:
        selector = self.query_one("#song-selection", SelectionList)
        for i, song in enumerate(self.app.songs):
            selector.add_option(Selection(
                f"{song['title']} - {song['artist']}",
                i,
                False
            ))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-cancel-pl":
            self.app.pop_screen()

        elif event.button.id == "btn-save-pl":
            name = self.query_one("#pl-name-input").value
            selected_indices = self.query_one("#song-selection").selected

            if not name or not selected_indices:
                self.app.notify("Need a name and some songs!", severity="error")

            selected_songs = [self.app.songs[i] for i in selected_indices]
            self.app.lib.save_playlists(name, selected_songs)
            self.app.notify(f"Playlist: '{name}' created!!", severity="information")
            self.app.get_screen("home").load_playlists()
            self.app.pop_screen()
    