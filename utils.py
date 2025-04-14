profiles = {}

selected_profile = None

def add_profile(name, username, password):
    global profiles
    profiles[name] = {"username": username, "password": password}

def get_profile_names():
    return list(profiles.keys())

def get_profile(name):
    return profiles.get(name, None)

def delete_profile(name):
    global profiles
    if name in profiles:
        del profiles[name]

def update_profile(name, username=None, password=None):
    if name in profiles:
        if username is not None:
            profiles[name]["username"] = username
        if password is not None:
            profiles[name]["password"] = password