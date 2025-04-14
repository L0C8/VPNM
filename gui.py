import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from vpn_controller import *

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

    # Right side: action panel
    def import_vpn_action():
        file_path = filedialog.askopenfilename(filetypes=[("OVPN files", "*.ovpn")])
        if not file_path:
            return
        # For now, use test credentials (you can hook into profile later)
        username = "testuser"
        password = "testpass"
        name = import_vpn(file_path, username, password)
        messagebox.showinfo("Import Success", f"Imported VPN: {name}")
        refresh_tree()

    import_button = tk.Button(right_frame, text="Import VPN", command=import_vpn_action)
    import_button.pack(pady=10)

    delete_button = tk.Button(right_frame, text="Delete Selected VPN", command=lambda: delete_selected(tree, refresh_tree))
    delete_button.pack(pady=10)

    refresh_button = tk.Button(right_frame, text="Refresh List", command=refresh_tree)
    refresh_button.pack(pady=10)

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
    tk.Label(profile_tab, text="This is the Profile tab").pack(pady=20)

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
