import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
import json
import random
from pathlib import Path
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

class SongLibrary:
    def __init__(self, lib_file="library.json"):
        self.lib_file = lib_file
        self.exts = {".mp3", ".wav", ".ogg", ".flac"}

    def exists(self) -> bool:
        data = self.readlib()

        if (data is not None) and (len(data.get("songs", [])) > 0):
            return True
        else:
            return False
        
    def to_mmss(self, secs):
        m, s = divmod(int(secs), 60)
        return f"{m:02d}:{s:02d}"

    def readlib(self):
        if os.path.exists(self.lib_file):
            with open(self.lib_file, "r") as f:
                return json.load(f)
        return None

    def build(self, folders):
        found = []

        for folder in folders:
            p = Path(folder)
            if not p.exists():
                continue
                
            for fp in p.rglob("*"):
                if fp.suffix.lower() in self.exts:
                    try:
                        tag = MP3(fp, ID3=EasyID3)
                        name = str(tag.get("title", [fp.stem])[0])
                        who = str(tag.get("artist", ["Unknown"])[0])
                        dur = self.to_mmss(tag.info.length)
                    except Exception:
                        name = fp.stem
                        who = "Unknown"
                        dur = "??:??"

                    found.append({
                        "title": name,
                        "artist": who,
                        "duration": dur,
                        "path": str(fp.absolute())
                    })
            
        out = {
            "directories": folders,
            "songs": found
        }

        with open(self.lib_file, "w") as f:
            json.dump(out, f, indent=4)

        return found
    
    def random_picks(self, n=20):
        data = self.readlib()
        if data and data["songs"]:
            return random.sample(data["songs"], min(n, len(data["songs"])))
        return []

class Player:
    def __init__(self):
        pygame.mixer.init()
        self.loaded = None
        self.paused = False
        self.total_len = 0.0
        self.seek_offset = 0.0

    def load(self, path):
        if os.path.exists(path):
            pygame.mixer.music.load(path)
            self.loaded = path
            self.total_len = MP3(path).info.length
            return True
        return False
    
    def play(self) -> None:
        if self.loaded:
            self.seek_offset = 0.0
            pygame.mixer.music.play()
            self.paused = False
    
    def pause(self) -> None:
        pygame.mixer.music.pause()
        self.paused = True

    def resume(self, at=None) -> None:
        if at is not None:
            pygame.mixer.music.play(start=at)
            self.seek_offset = at
            self.paused = False
        else:
            pygame.mixer.music.unpause()
            self.paused = False

    def stop(self) -> None:
        pygame.mixer.music.stop()
        self.paused = False

    def set_volume(self, vol: float) -> None:
        pygame.mixer.music.set_volume(vol)

    def get_volume(self) -> float:
        return pygame.mixer.music.get_volume()
    
    def playing(self):
        return pygame.mixer.music.get_busy()
    
    def finished(self):
        return not pygame.mixer.music.get_busy() and not self.paused
    
    def progress(self):
        if not self.loaded:
            return 0, 0, 0
        
        pos = pygame.mixer.music.get_pos()
        elapsed = max(0, pos / 1000.0) + self.seek_offset
        pct = (elapsed / self.total_len) * 100
        return elapsed, self.total_len, pct
    
    def seek(self, t: float) -> None:
        if self.loaded:
            self.seek_offset = t
            pygame.mixer.music.play(start=t)

            if self.paused:
                pygame.mixer.music.pause()

    def play_sfx(self, path: str) -> None:
        if os.path.exists(path):
            effect = pygame.mixer.Sound(path)
            effect.play()


if __name__ == "__main__":
    my_folder = "D:\\songs"
    lib = SongLibrary("library.json")
    songs = lib.build([my_folder])

    print(f"Found {len(songs)} songs:\n")
    for i, s in enumerate(songs):
        print(f"{i+1}. {s['title']} - {s['artist']} [{s['duration']}]")