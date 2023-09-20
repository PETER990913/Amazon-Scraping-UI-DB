import sys
import tkinter as tk
from contextlib import redirect_stdout
from io import StringIO

root = tk.Tk()

console_output = StringIO()
with redirect_stdout(console_output):
    print("Hello, world!")
    print("This is a test.")

console_text = console_output.getvalue()

console_entry = tk.Entry(
    bd=0,
    bg="#ebe6e6",
    fg="#000000",
    highlightthickness=0
)
console_entry.place(
    x=219.0,
    y=525,
    width=781.0,
    height=100.0
)

console_entry.insert(tk.END, console_text)

root.mainloop()