profiles = {}
selected_profile = None
profile_selector_widget = None

def add_profile(name, username, password):
    global profiles
    profiles[name] = {"username": username, "password": password}
    if profile_selector_widget:
        profile_selector_widget.configure(values=get_profile_names())
        profile_selector_widget.set(name)

def get_profile_names():
    return list(profiles.keys())

def get_profile(name):
    return profiles.get(name, None)

def delete_profile(name):
    global profiles
    if name in profiles:
        del profiles[name]

# Update profile credentials
def update_profile(name, username=None, password=None):
    if name in profiles:
        if username is not None:
            profiles[name]["username"] = username
        if password is not None:
            profiles[name]["password"] = password