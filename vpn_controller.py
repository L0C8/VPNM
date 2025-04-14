import os
import subprocess

def populate_vpn_tree(tree):
    tree.delete(*tree.get_children())
    result = subprocess.run(["nmcli", "-t", "-f", "NAME,TYPE", "connection", "show"], capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")
    for line in lines:
        if ":vpn" in line:
            name = line.split(":")[0]
            tree.insert("", "end", values=(name,))