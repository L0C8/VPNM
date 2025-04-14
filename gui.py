import tkinter as tk
from tkinter import ttk

# tab for displaying vpns
def add_vpn_tab(notebook):
    vpn_tab = tk.Frame(notebook)
    notebook.add(vpn_tab, text="Manage VPNs")
    tk.Label(vpn_tab, text="This is the VPN tab").pack(pady=20)

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