# terminal play





### For source code building

>pyinstaller --onefile --console 
--exclude-module PyQt5 --exclude-module PySide6 
--collect-submodules textual 
--collect-submodules pyfiglet
--add-data "style.tcss;." 
--add-data "C:\Users\Swift G0 14\AppData\Local\Programs\Python\Python313\Lib\site-packages\pyfiglet\fonts;pyfiglet/fonts"
main.py
