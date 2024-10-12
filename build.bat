:: Pyinstaller build script
cd C:\Users\ch1ka\Desktop\Sugaku\
nuitka --standalone --output-dir=build --noinclude-default-mode=error --deployment --nofollow-import-to=unittest --windows-icon-from-ico=s.ico Sugaku.py
