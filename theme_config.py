import configparser
import os

THEMES_FILE = "themes.ini"

DEFAULT_THEMES = {
    "light": {"bg": "255,255,255", "fg": "0,0,0"},
    "dark": {"bg": "45,45,45", "fg": "220,220,220"},
}

themes = {}
active_theme = "light"

def _rgb_to_tuple(s):
    return tuple(int(x) for x in s.split(','))

def _tuple_to_rgb(t):
    return ','.join(str(x) for x in t)

def _write_default():
    config = configparser.ConfigParser()
    config["DEFAULT"] = {"active_theme": "light"}
    for name, vals in DEFAULT_THEMES.items():
        config[name] = vals
    with open(THEMES_FILE, "w", encoding="utf-8") as f:
        config.write(f)

def load_themes():
    global themes, active_theme
    if not os.path.exists(THEMES_FILE):
        _write_default()
    cfg = configparser.ConfigParser()
    cfg.read(THEMES_FILE)
    active_theme = cfg["DEFAULT"].get("active_theme", "light")
    themes = {}
    for section in cfg.sections():
        if section == "DEFAULT":
            continue
        bg = _rgb_to_tuple(cfg[section].get("bg", "255,255,255"))
        fg = _rgb_to_tuple(cfg[section].get("fg", "0,0,0"))
        themes[section] = {"bg": bg, "fg": fg}

def save_themes():
    cfg = configparser.ConfigParser()
    cfg["DEFAULT"] = {"active_theme": active_theme}
    for name, vals in themes.items():
        cfg[name] = {k: _tuple_to_rgb(v) for k, v in vals.items()}
    with open(THEMES_FILE, "w", encoding="utf-8") as f:
        cfg.write(f)

def set_active_theme(name):
    global active_theme
    if name in themes:
        active_theme = name
        save_themes()

def to_hex(rgb_tuple):
    return "#%02x%02x%02x" % rgb_tuple

# load at import
load_themes()
