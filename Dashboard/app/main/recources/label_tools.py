def get_colors():
    return {
        "background": "#FFFFFF",  # white background
        "text": "#000000",  # black text for visibility
        "Risk Label": {
            "Info": "#45B6FE",  # blue
            "Low": "#FFD700",  # gold
            "Medium": "#FF8C00",  # darkorange
            "High": "#FF4500",  # orangered
            "Attack": "#DC143C",  # crimson
            "Suspicious": "#800080",  # purple
            "Unlabeled": "#808080",  # grey
            "Custom": "#808080"  # grey
        }
    }


def choose_risk(weight):
    # TODO: change it to accept a different format than 0-10
    if weight <= 0:
        return "Unlabeled"
    elif weight <= 1:
        return "Info"
    elif weight <= 3:
        return "Low"
    elif weight <= 5:
        return "Medium"
    elif weight <= 7:
        return "High"
    else:
        return "Attack"
