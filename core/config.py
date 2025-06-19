from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent
REFLECTIONS_FOLDER = BASE_PATH / "reflections"
META_FILE = BASE_PATH / "kai_exchange_meta.json"

WAIT_BEFORE_CAPTURE = 12

UI_CONFIGS = {
    "Kai": {
        "input_top_left": (183, 958),
        "send_button": (832, 1025),
        "read_area_top_left": (150, 206),
        "read_area_bottom_right": (873, 862),
        "safe_click": ((410, 920), (410, 920)),
        "scroll_region": (150, 206, 873, 862),
        "typing_delay": 0.05,
        "response_wait": 5,
        "scroll_sensitivity": -2
    },
    "CLAUDE": {
        "input_top_left": (1194, 976),
        "send_button": (1912, 1037),
        "read_area_top_left": (1174, 226),
        "read_area_bottom_right": (1919, 571),
        "safe_click": ((1556, 960), (1556, 960)),
        "scroll_region": (1174, 226, 1919, 571),
        "typing_delay": 0.1,
        "response_wait": 8,
        "scroll_sensitivity": -1
    },
    "Perplexity": {
        "input_top_left": (342, 999),
        "send_button": (911, 1022),
        "read_area_top_left": (190, 160),
        "read_area_bottom_right": (949, 360),
        "safe_click": ((130, 975), (130, 975)),
        "scroll_region": (190, 160, 949, 360),
        "typing_delay": 0.05,
        "response_wait": 6,
        "scroll_sensitivity": -2
    },
    "Grok": {
        "input_top_left": (1266, 969),
        "send_button": (1922, 1034),
        "read_area_top_left": (1248, 195),
        "read_area_bottom_right": (1946, 866),
        "safe_click": ((1189, 1005), (1189, 1005)),
        "scroll_region": (1248, 195, 1946, 866),
        "typing_delay": 0.05,
        "response_wait": 6,
        "scroll_sensitivity": -2
    }
}

CONVERSATION_FLOW = {
    "four_ai": [
        ("Kai", "CLAUDE"),
        ("CLAUDE", "Grok"),
        ("Grok", "Perplexity"),
        ("Perplexity", "Kai")
    ]
}
