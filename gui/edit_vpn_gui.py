import tkinter as tk
from tkinter import ttk, messagebox
from utils.config import get_profile_names, get_profile, selected_profile
from utils.vpn_controller import get_all_vpn_names, update_vpn_credentials
from utils import theme_config


def apply_theme(root):
    theme = theme_config.themes.get(theme_config.active_theme)
    if not theme:
        return
    bg = theme_config.to_hex(theme["bg"])
    fg = theme_config.to_hex(theme["fg"])
    panel_bg = theme_config.to_hex(theme.get("panel_bg", theme["bg"]))
    button_bg = theme_config.to_hex(theme.get("button_bg", theme["bg"]))
    dropdown_bg = theme_config.to_hex(theme.get("dropdown_bg", panel_bg))
    dropdown_fg = theme_config.to_hex(theme.get("dropdown_fg", fg))

    style = ttk.Style()
    style.configure("TFrame", background=panel_bg)
    style.configure("TLabel", background=panel_bg, foreground=fg)
    style.configure("TButton", background=button_bg, foreground=fg)
    style.configure(
        "TCombobox",
        fieldbackground=dropdown_bg,
        background=dropdown_bg,
        foreground=dropdown_fg,
        selectbackground=dropdown_bg,
        selectforeground=dropdown_fg,
    )
    style.map(
        "TCombobox",
        fieldbackground=[("readonly", dropdown_bg)],
        selectbackground=[("readonly", dropdown_bg)],
        selectforeground=[("readonly", dropdown_fg)],
        background=[("readonly", dropdown_bg)],
        foreground=[("readonly", dropdown_fg)],
    )
    root.configure(bg=bg)

    def recurse(w):
        for child in w.winfo_children():
            if isinstance(child, tk.Frame):
                child.configure(bg=panel_bg)
            elif isinstance(child, tk.Label):
                child.configure(bg=panel_bg, fg=fg)
            elif isinstance(child, tk.Button):
                child.configure(bg=button_bg, fg=fg, activebackground=button_bg)
            elif isinstance(child, tk.Entry) and not isinstance(child, ttk.Entry):
                child.configure(bg=panel_bg, fg=fg, insertbackground=fg)
            recurse(child)

    recurse(root)


def open_edit_vpn_window(parent=None, vpn_name=None):
    win = tk.Toplevel(parent) if parent else tk.Toplevel()
    win.title("Edit VPN")
    win.geometry("400x300")
    win.resizable(False, False)
    button_width = 12 

    vpn_var = tk.StringVar(value=vpn_name if vpn_name else "")
    if vpn_name:
        tk.Label(win, text=f"VPN: {vpn_name}").pack(pady=(10, 2))
    else:
        tk.Label(win, text="Select VPN:").pack(pady=(10, 2))
        vpn_dropdown = ttk.Combobox(win, state="readonly", values=get_all_vpn_names(), textvariable=vpn_var)
        vpn_dropdown.pack(pady=2)

    tk.Label(win, text="Profile:").pack(pady=(10, 2))
    profile_var = tk.StringVar(value=selected_profile if selected_profile else "")
    profile_dropdown = ttk.Combobox(win, state="readonly", values=get_profile_names(), textvariable=profile_var)
    profile_dropdown.pack(pady=2)

    tk.Label(win, text="Username:").pack(pady=(10, 2))
    user_entry = tk.Entry(win)
    user_entry.pack(pady=2)

    tk.Label(win, text="Password:").pack(pady=(10, 2))
    pass_entry = tk.Entry(win)
    pass_entry.pack(pady=2)

    def load_profile(event=None):
        prof = get_profile(profile_var.get())
        if prof:
            user_entry.delete(0, tk.END)
            user_entry.insert(0, prof["username"])
            pass_entry.delete(0, tk.END)
            pass_entry.insert(0, prof["password"])

    profile_dropdown.bind("<<ComboboxSelected>>", load_profile)
    if selected_profile:
        load_profile()

    def save():
        name = vpn_var.get()
        if not name:
            messagebox.showwarning("Input Error", "Please select a VPN")
            return
        username = user_entry.get()
        password = pass_entry.get()
        if not username or not password:
            messagebox.showwarning("Input Error", "Username and password required")
            return
        update_vpn_credentials(name, username, password)
        messagebox.showinfo("Saved", f"Updated VPN '{name}'.")
        win.destroy()

    btn_frame = tk.Frame(win)
    btn_frame.pack(pady=10)
    cancel_btn = tk.Button(btn_frame, text="Cancel", command=win.destroy, width=button_width)
    cancel_btn.pack(side="left", padx=5)
    save_btn = tk.Button(btn_frame, text="Save", command=save, width=button_width)
    save_btn.pack(side="left", padx=5)

    apply_theme(win)
    win.grab_set()
    win.transient(parent)
    win.wait_window()

