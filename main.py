import tkinter as tk
from tkinter import ttk
from gui import build_tabs


def main():
    root = tk.Tk()
    root.title("VPN Manager")
    root.geometry("600x500")
    root.resizable(False, False)

    build_tabs(root)

    root.mainloop()


if __name__ == "__main__":
    main()
