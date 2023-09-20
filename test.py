from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,filedialog,END,ttk,Variable,messagebox
from tkinter.filedialog import askopenfilename
from pathlib import Path
# Create a window object
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/")
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()
window.title("Crawler")
window.geometry("800x500")
window.configure(bg = "#202020")
canvas = Canvas(
    window,
    bg = "#202020",
    height = 500,
    width = 800,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
canvas.place(x = 0, y = 0)

canvas.create_text(
    200.0,
    50.0,
    anchor="nw",
    text="IP address",
    fill="#FFFFFF",
    font=("Roboto Medium", 14 * -1)
)
canvas.create_text(
    350.0,
    50.0,
    anchor="nw",
    text="PORT",
    fill="#FFFFFF",
    font=("Roboto Medium", 14 * -1)
)
canvas.create_text(
    480.0,
    50.0,
    anchor="nw",
    text="USERNAME",
    fill="#FFFFFF",
    font=("Roboto Medium", 14 * -1)
)
canvas.create_text(
    660.0,
    50.0,
    anchor="nw",
    text="PASSWORD",
    fill="#FFFFFF",
    font=("Roboto Medium", 14 * -1)
)

IP_address1_entry = Entry(
    bd=0,
    bg="#2D2D2D",
    fg="#FFFFFF",
    highlightthickness=0
)

IP_address1_entry.place(
    x=145.0,
    y=100,
    width=170.0,
    height=30.0
)

PORT1_entry = Entry(
    bd=0,
    bg="#2D2D2D",
    fg="#FFFFFF",
    highlightthickness=0
)
PORT1_entry.place(
    x=325.0,
    y=100,
    width=100.0,
    height=30.0
)

USERNAME1_entry = Entry(
    bd=0,
    bg="#2D2D2D",
    fg="#FFFFFF",
    highlightthickness=0
)
USERNAME1_entry.place(
    x=435.0,
    y=100,
    width=170.0,
    height=30.0
)

PASSWORD1_entry = Entry(
    bd=0,
    bg="#2D2D2D",
    fg="#FFFFFF",
    highlightthickness=0
)
PASSWORD1_entry.place(
    x=615.0,
    y=100,
    width=170.0,
    height=30.0
)

canvas.create_text(
    50.0,
    107.0,
    anchor="nw",
    text="Proxy 1",
    fill="#FFFFFF",
    font=("Roboto Medium", 14 * -1)
)

IP_address2_entry = Entry(
    bd=0,
    bg="#2D2D2D",
    fg="#FFFFFF",
    highlightthickness=0
)

IP_address2_entry.place(
    x=145.0,
    y=155,
    width=170.0,
    height=30.0
)

PORT2_entry = Entry(
    bd=0,
    bg="#2D2D2D",
    fg="#FFFFFF",
    highlightthickness=0
)
PORT2_entry.place(
    x=325.0,
    y=155,
    width=100.0,
    height=30.0
)

USERNAME2_entry = Entry(
    bd=0,
    bg="#2D2D2D",
    fg="#FFFFFF",
    highlightthickness=0
)
USERNAME2_entry.place(
    x=435.0,
    y=155,
    width=170.0,
    height=30.0
)

PASSWORD2_entry = Entry(
    bd=0,
    bg="#2D2D2D",
    fg="#FFFFFF",
    highlightthickness=0
)
PASSWORD2_entry.place(
    x=615.0,
    y=155,
    width=170.0,
    height=30.0
)

canvas.create_text(
    50.0,
    162.0,
    anchor="nw",
    text="Proxy 2",
    fill="#FFFFFF",
    font=("Roboto Medium", 14 * -1)
)

IP_address3_entry = Entry(
    bd=0,
    bg="#2D2D2D",
    fg="#FFFFFF",
    highlightthickness=0
)

IP_address3_entry.place(
    x=145.0,
    y=210,
    width=170.0,
    height=30.0
)

PORT3_entry = Entry(
    bd=0,
    bg="#2D2D2D",
    fg="#FFFFFF",
    highlightthickness=0
)
PORT3_entry.place(
    x=325.0,
    y=210,
    width=100.0,
    height=30.0
)

USERNAME3_entry = Entry(
    bd=0,
    bg="#2D2D2D",
    fg="#FFFFFF",
    highlightthickness=0
)
USERNAME3_entry.place(
    x=435.0,
    y=210,
    width=170.0,
    height=30.0
)

PASSWORD3_entry = Entry(
    bd=0,
    bg="#2D2D2D",
    fg="#FFFFFF",
    highlightthickness=0
)
PASSWORD3_entry.place(
    x=615.0,
    y=210,
    width=170.0,
    height=30.0
)

canvas.create_text(
    50.0,
    217.0,
    anchor="nw",
    text="Proxy 3",
    fill="#FFFFFF",
    font=("Roboto Medium", 14 * -1)
)

canvas.create_text(
    23.0,
    300.0,
    anchor="nw",
    text="Category Name",
    fill="#FFFFFF",
    font=("Roboto Medium", 14 * -1)
)


category_entry = Entry(
    bd=0,
    bg="#2D2D2D",
    fg="#FFFFFF",
    highlightthickness=0
)

category_entry.place(
    x=145.0,
    y=295,
    width=380.0,
    height=30.0
)

canvas.create_text(
    30.0,
    350.0,
    anchor="nw",
    text="Console Log",
    fill="#FFFFFF",
    font=("Roboto Medium", 14 * -1)
)

console_entry = Entry(
    bd=0,
    bg="#2D2D2D",
    fg="#FFFFFF",
    highlightthickness=0
)

console_entry.place(
    x=145.0,
    y=345,
    width=380.0,
    height=30.0
)


start_img = PhotoImage(file=relative_to_assets("start.png"))
# start_btn = Button(
#     image=start_img, borderwidth=0, highlightthickness=0, relief="flat", command=lambda : handle_btn_press("start"),activebackground= "#202020")
start_btn = Button(
    image=start_img, borderwidth=0, highlightthickness=0, relief="flat",activebackground= "#202020")
start_btn.place(x=50, y=420, width=100, height=47)

stop_img = PhotoImage(file=relative_to_assets("stop.png"))
# stop_btn = Button(image=stop_img, borderwidth=0, highlightthickness=0, relief="flat", command=lambda : handle_btn_press("stop"),activebackground= "#202020", state="disabled")
stop_btn = Button(image=stop_img, borderwidth=0, highlightthickness=0, relief="flat",activebackground= "#202020")
stop_btn.place(x=250, y=420, width=100, height=47)

Display_img = PhotoImage(file=relative_to_assets("result.png"))
# Display_btn = Button(image=Display_img, borderwidth=0, highlightthickness=0, relief="flat", command=lambda : handle_btn_press("stop"),activebackground= "#202020", state="disabled")
Display_btn = Button(image=Display_img, borderwidth=0, highlightthickness=0, relief="flat",activebackground= "#202020")
Display_btn.place(x=450, y=420, width=100, height=47)

Import_img = PhotoImage(file=relative_to_assets("import.png"))
# stop_btn = Button(image=Import_img, borderwidth=0, highlightthickness=0, relief="flat", command=lambda : handle_btn_press("stop"),activebackground= "#202020", state="disabled")
Import_btn = Button(image=Import_img, borderwidth=0, highlightthickness=0, relief="flat",activebackground= "#202020")
Import_btn.place(x=650, y=420, width=100, height=47)

# IP_address1_entry.insert(0, "1632 Scholar Dr")
# PORT1_entry.insert(0, "Lawrenceville")
# USERNAME1_entry.insert(0, "GA")
# PASSWORD1_entry.insert(0, "202-337-1412")

# IP_address2_entry.insert(0, "605 Saint Lawrence Blvd")
# PORT2_entry.insert(0, "Eastlake")
# USERNAME2_entry.insert(0, "OH")
# PASSWORD2_entry.insert(0, "202-337-1412")

# IP_address3_entry.insert(0, "203 Magnolia St")
# PORT3_entry.insert(0, "Siloam Springs")
# USERNAME3_entry.insert(0, "AR")
# PASSWORD3_entry.insert(0, "202-337-1412")

window.resizable(False, False)
# Run the main event loop to display the window
window.mainloop()