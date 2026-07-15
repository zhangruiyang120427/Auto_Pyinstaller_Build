"""Auto_Pyinstaller_Build 自带示例：点击按钮累加计数。
默认按 -w 打包为 GUI 程序，无控制台窗口。
如要换成自己的程序，直接把这个 main.py 替换掉即可，保持同目录。
"""
import tkinter as tk
from tkinter import ttk


class CounterApp:
    def __init__(self, root: tk.Tk) -> None:
        self.count = 0
        root.title("Auto PyInstaller Demo")
        root.geometry("320x180")
        root.resizable(False, False)

        self.label = ttk.Label(root, text="0", font=("Segoe UI", 36))
        self.label.pack(pady=20)

        btn = ttk.Button(root, text="+1", command=self.inc)
        btn.pack(ipadx=12, ipady=4)

    def inc(self) -> None:
        self.count += 1
        self.label.config(text=str(self.count))


if __name__ == "__main__":
    root = tk.Tk()
    CounterApp(root)
    root.mainloop()
