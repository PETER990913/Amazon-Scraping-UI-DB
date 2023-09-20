from tkinter import Canvas, Entry, Text,  Button, PhotoImage,filedialog,END,Variable,messagebox
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from pathlib import Path
from io import StringIO
from contextlib import redirect_stdout
console_output = StringIO()
with redirect_stdout(console_output):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path("assets/")
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = tk.Tk()
    window.title("Crawler")
    window.geometry("+500+100")
    window.geometry("1000x800")
    window.configure(bg = "#202020")
    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 800,
        width = 1000,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    canvas.place(x = 0, y = 0)
    console_entry = Entry(
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
    print('---------------------------')
    print('++++++++++++++++++++++++')
    console_text = console_output.getvalue()
    console_entry.insert(tk.END, console_text)
    window.resizable(False, False)
    # Run the main event loop to display the window
    window.mainloop()