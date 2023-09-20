import tkinter as tk
from tkinter import ttk

def on_select(event):
    selected_item = tree.selection()[0]
    item_text = tree.item(selected_item)['text']
    print(item_text)

root = tk.Tk()

tree = ttk.Treeview(root)
tree.insert("", "0", "item1", text="Item 1")
tree.insert("item1", "0", "subitem1", text="Subitem 1")
tree.bind("<<TreeviewSelect>>", on_select)
tree.pack()

root.mainloop()