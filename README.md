# Terminal Play
![terminal play](screenshot/one.png)

**A music player for your terminal.** Build with python with textual library for those beautiful UI and pygame for playing the actual audio.

## NOTE: For non-window users, you won't be able to use compiled form so, you can clone repo then run 
```
pip install -r requirements.txt
```
## Then
```
python main.py
```

## Custom Features
* **Custom loading animation:** I made that animation in davinci then used .mov to ascii script to convert it into that beautiful animation.

* **Beautiful TUI:** I think the TUI (Terminal User Interface) looks beautiful (I'm not a good designer thooo), feel free for suggestions.

* **Animations:** I added some animations like in when songs are playing, right side of the screen will play a dancing character animation.

#
### Some more screenshots
![2](screenshot/two.png)
![3](screenshot/three.png)


#### First time writing README so idk what to write.. I will learn gradually (trust me)

### For source code building
1) Make sure you install the requrements first
```
pip install -r requirements.txt
```
2) Then u can run:
```
 pyinstaller --noconfirm --onefile --console --exclude-module PyQt5 --exclude-module PySide6 --collect-all textual --collect-all pyfiglet --add-data "assets;assets" main.py
 ```


 ### AI declaration:
 * Logical Errors: Sometimes when I was stuck at some logical errors, I used gemini to guide me.. but I tried to understand the fix too.

 * Repetitive work: I did most of the work but sometimes when the work was just tooo basic and repetitive like: Writing A to Z in list, I again used gemini but when I used for this purpose, I have clearly mentioned in comments.