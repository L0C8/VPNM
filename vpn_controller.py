import os
import subprocess

def get_all_vpn_names():
    result = subprocess.run(["nmcli", "-t", "-f", "NAME,TYPE", "connection", "show"], capture_output=True, text=True)
    return [line.split(":")[0] for line in result.stdout.strip().split("\n") if ":vpn" in line]

def import_vpn(file_path, username, password):
    name = os.path.splitext(os.path.basename(file_path))[0]
    subprocess.run(["nmcli", "connection", "import", "type", "openvpn", "file", file_path])
    subprocess.run(["nmcli", "connection", "modify", name, "vpn.user-name", username])
    subprocess.run(["nmcli", "connection", "modify", name, "+vpn.data", "password-flags=0"])
    subprocess.run(["nmcli", "connection", "modify", name, "vpn.secrets", f"password={password}"])
    return name

def delete_vpn(name):
    subprocess.run(["nmcli", "connection", "delete", name])

def delete_all_vpns():
    for name in get_all_vpn_names():
        delete_vpn(name)

def populate_vpn_tree(tree):
    tree.delete(*tree.get_children())
    result = subprocess.run(["nmcli", "-t", "-f", "NAME,TYPE", "connection", "show"], capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")
    for line in lines:
        if ":vpn" in line:
            name = line.split(":")[0]
            tree.insert("", "end", values=(name,))

def set_autoconnect(name, enabled=True):
    flag = "yes" if enabled else "no"
    subprocess.run(["nmcli", "connection", "modify", name, "connection.autoconnect", flag])