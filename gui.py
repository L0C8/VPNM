import tkinter as tk
from tkinter import ttk
import subprocess

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

    populate_vpn_tree(tree)

    # Right side: test panel (with test button)
    test_button = tk.Button(right_frame, text="Test")
    test_button.pack(pady=20)

## testing, move this over to vpn_controller.py later
def populate_vpn_tree(tree):
    tree.delete(*tree.get_children())
    result = subprocess.run(["nmcli", "-t", "-f", "NAME,TYPE", "connection", "show"], capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")
    for line in lines:
        if ":vpn" in line:
            name = line.split(":")[0]
            tree.insert("", "end", values=(name,))

def populate_vpn_tree(tree):
    tree.delete(*tree.get_children())
    result = subprocess.run(["nmcli", "-t", "-f", "NAME,TYPE", "connection", "show"], capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")
    for line in lines:
        if ":vpn" in line:
            name = line.split(":")[0]
            tree.insert("", "end", values=(name,))


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