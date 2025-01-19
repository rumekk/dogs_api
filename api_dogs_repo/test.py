import tkinter as tk
from tkinter import ttk

root = tk.Tk()

label = ttk.Label(root, text="Hello!")
label.pack()
button = ttk.Button(root, text="Click Me!")
button.pack()

# label = ttk.Label(root, text="Hello!")
# label.grid(row=0, column=0)
# button = ttk.Button(root, text="Click Me!")
# button.grid(row=1, column=0)

tk.mainloop()
