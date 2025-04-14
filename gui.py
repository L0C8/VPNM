import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from vpn_controller import *
from config import profiles, selected_profile, add_profile, get_profile_names, get_profile, profile_selector_widget

# tab for displaying vpns
def add_vpn_tab(notebook):
    vpn_tab = tk.Frame(notebook)
    notebook.add(vpn_tab, text="Manage VPNs")

    # Create left and right panels
    left_frame = tk.Frame(vpn_tab)
    left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

    right_frame = tk.Frame(vpn_tab, bg="#f0f0f0")
    right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

    # Left side: Treeview
    label = tk.Label(left_frame, text="Current VPN Configurations:")
    label.pack(pady=10)

    tree = ttk.Treeview(left_frame, columns=("Name",), show="headings")
    tree.heading("Name", text="VPN Name")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    def refresh_tree():
        tree.delete(*tree.get_children())
        for name in get_all_vpn_names():
            tree.insert("", "end", values=(name,))

    refresh_tree()

    # profile selector dropdown
    profile_label = tk.Label(right_frame, text="Active Profile")
    profile_label.pack(pady=(10, 2))

    profile_selector = ttk.Combobox(right_frame, state="readonly", values=get_profile_names())
    profile_selector.pack(pady=2)

    def update_selected_profile(event):
        global selected_profile
        selected_profile = profile_selector.get()

    profile_selector.bind("<<ComboboxSelected>>", update_selected_profile)

    # store reference to dropdown in config
    import config
    config.profile_selector_widget = profile_selector

    # Right side: action panel
    def import_vpn_action():
        file_path = filedialog.askopenfilename(filetypes=[("OVPN files", "*.ovpn")])
        if not file_path:
            return
        profile = get_profile(selected_profile)
        username = profile["username"] if profile else ""
        password = profile["password"] if profile else ""
        name = import_vpn(file_path, username, password)
        messagebox.showinfo("Import Success", f"Imported VPN: {name}")
        refresh_tree()

    def bulk_import_action():
        folder_path = filedialog.askdirectory()
        if not folder_path:
            return
        profile = get_profile(selected_profile)
        username = profile["username"] if profile else ""
        password = profile["password"] if profile else ""
        imported = []
        for filename in os.listdir(folder_path):
            if filename.endswith(".ovpn"):
                path = os.path.join(folder_path, filename)
                name = import_vpn(path, username, password)
                imported.append(name)
        messagebox.showinfo("Bulk Import", f"Imported {len(imported)} VPN(s):\n" + "\n".join(imported))
        refresh_tree()

    def delete_all_action():
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete ALL VPN configurations?")
        if confirm:
            delete_all_vpns()
            refresh_tree()

    tk.Button(right_frame, text="Import VPN", command=import_vpn_action).pack(pady=10)
    tk.Button(right_frame, text="Bulk Import Folder", command=bulk_import_action).pack(pady=10)
    tk.Button(right_frame, text="Delete Selected VPN", command=lambda: delete_selected(tree, refresh_tree)).pack(pady=10)
    tk.Button(right_frame, text="Delete ALL VPNs", command=delete_all_action).pack(pady=10)
    tk.Button(right_frame, text="Refresh List", command=refresh_tree).pack(pady=10)

def delete_selected(tree, refresh_func):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a VPN to delete.")
        return
    for item in selected:
        name = tree.item(item, "values")[0]
        delete_vpn(name)
    refresh_func()

# tab for user data
def add_profile_tab(notebook):
    profile_tab = tk.Frame(notebook)
    notebook.add(profile_tab, text="Manage Profile")

    selected_profile_var = tk.StringVar()

    def save_profile():
        name = name_entry.get()
        user = user_entry.get()
        pwd = pass_entry.get()
        if not name:
            messagebox.showwarning("Input Error", "Profile name is required.")
            return
        add_profile(name, user, pwd)
        selected_profile_var.set(name)
        refresh_profile_dropdown()
        messagebox.showinfo("Saved", f"Profile '{name}' saved successfully.")

    def refresh_profile_dropdown():
        menu = profile_menu["menu"]
        menu.delete(0, "end")
        for name in get_profile_names():
            menu.add_command(label=name, command=tk._setit(selected_profile_var, name))

    tk.Label(profile_tab, text="Select Profile:").pack(pady=5)
    profile_menu = tk.OptionMenu(profile_tab, selected_profile_var, "")
    profile_menu.pack(pady=5)

    tk.Label(profile_tab, text="Profile Name:").pack(pady=2)
    name_entry = tk.Entry(profile_tab)
    name_entry.pack(pady=2)

    tk.Label(profile_tab, text="Username:").pack(pady=2)
    user_entry = tk.Entry(profile_tab)
    user_entry.pack(pady=2)

    tk.Label(profile_tab, text="Password:").pack(pady=2)
    pass_entry = tk.Entry(profile_tab, show="*")
    pass_entry.pack(pady=2)

    tk.Button(profile_tab, text="Save Profile", command=save_profile).pack(pady=10)

# tab for system settings
def add_settings_tab(notebook):
    settings_tab = tk.Frame(notebook)
    notebook.add(settings_tab, text="System Settings")
    tk.Label(settings_tab, text="This is the Settings tab").pack(pady=20)

def build_tabs(root):
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    add_vpn_tab(notebook)
    add_profile_tab(notebook)
    add_settings_tab(notebook)
