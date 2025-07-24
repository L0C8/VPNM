import json
import os

PROFILES_FILE = os.path.join(os.path.dirname(__file__), "profiles.json")

profiles = {}
selected_profile = None
profile_selector_widget = None

def load_profiles():
    global profiles, selected_profile
    if os.path.exists(PROFILES_FILE):
        try:
            with open(PROFILES_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                profiles = data.get("profiles", {})
                selected_profile = data.get("selected_profile")
        except Exception:
            profiles = {}
            selected_profile = None
    else:
        profiles = {}
        selected_profile = None

def save_profiles():
    data = {
        "profiles": profiles,
        "selected_profile": selected_profile,
    }
    with open(PROFILES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)

def set_selected_profile(name):
    global selected_profile
    selected_profile = name
    save_profiles()

# Load profiles when module is imported
load_profiles()

def add_profile(name, username, password):
    global profiles
    profiles[name] = {"username": username, "password": password}
    if profile_selector_widget:
        profile_selector_widget.configure(values=get_profile_names())
        profile_selector_widget.set(name)
    save_profiles()

def get_profile_names():
    return list(profiles.keys())

def get_profile(name):
    return profiles.get(name, None)

def delete_profile(name):
    """Remove a stored profile by name."""
    global profiles, selected_profile
    if name in profiles:
        del profiles[name]
        if selected_profile == name:
            selected_profile = None
        if profile_selector_widget:
            profile_selector_widget.configure(values=get_profile_names())
            profile_selector_widget.set(selected_profile or "")
        save_profiles()

# Update profile credentials
def update_profile(name, username=None, password=None):
    if name in profiles:
        if username is not None:
            profiles[name]["username"] = username
        if password is not None:
            profiles[name]["password"] = password
        save_profiles()
