import configparser
import os

THEMES_FILE = os.path.join(os.path.dirname(__file__), "themes.ini")

# Default theme definitions including additional values for tab colors
DEFAULT_THEMES = {
    "light": {
        "bg": "255,255,255",
        "fg": "0,0,0",
        "panel_bg": "240,240,240",
        "button_bg": "230,230,230",
        "tab_bg": "230,230,230",
        "tab_active_bg": "210,210,210",
        "dropdown_bg": "230,230,230",
        "dropdown_fg": "0,0,0",
        "tree_bg": "255,255,255",
        "tree_fg": "0,0,0",
        "tree_select_bg": "200,200,200",
        "tree_select_fg": "0,0,0",
        "tree_heading_bg": "230,230,230",
        "tree_heading_fg": "0,0,0",
    },
    "dark": {
        "bg": "45,45,45",
        "fg": "220,220,220",
        "panel_bg": "55,55,55",
        "button_bg": "70,70,70",
        "tab_bg": "60,60,60",
        "tab_active_bg": "75,75,75",
        "dropdown_bg": "55,55,55",
        "dropdown_fg": "220,220,220",
        "tree_bg": "45,45,45",
        "tree_fg": "220,220,220",
        "tree_select_bg": "70,70,70",
        "tree_select_fg": "220,220,220",
        "tree_heading_bg": "60,60,60",
        "tree_heading_fg": "220,220,220",
    },
    "dark-blue": {
        "bg": "10,25,55",
        "fg": "173,216,230",
        "panel_bg": "20,35,70",
        "button_bg": "30,50,90",
        "tab_bg": "25,40,80",
        "tab_active_bg": "40,55,100",
        "dropdown_bg": "20,35,70",
        "dropdown_fg": "173,216,230",
        "tree_bg": "10,25,55",
        "tree_fg": "173,216,230",
        "tree_select_bg": "40,55,100",
        "tree_select_fg": "173,216,230",
        "tree_heading_bg": "25,40,80",
        "tree_heading_fg": "173,216,230",
    },
    "dark-green": {
        "bg": "10,55,25",
        "fg": "144,238,144",
        "panel_bg": "20,70,35",
        "button_bg": "30,90,50",
        "tab_bg": "25,80,45",
        "tab_active_bg": "40,100,60",
        "dropdown_bg": "20,70,35",
        "dropdown_fg": "144,238,144",
        "tree_bg": "10,55,25",
        "tree_fg": "144,238,144",
        "tree_select_bg": "40,100,60",
        "tree_select_fg": "144,238,144",
        "tree_heading_bg": "25,80,45",
        "tree_heading_fg": "144,238,144",
    },
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
    """Load themes from the config file."""
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
        defaults = DEFAULT_THEMES.get(section, DEFAULT_THEMES["light"])
        values = {}
        for key, default in defaults.items():
            values[key] = _rgb_to_tuple(cfg[section].get(key, default))
        themes[section] = values


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

# Load themes on import
load_themes()
