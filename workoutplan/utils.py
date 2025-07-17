def get_display_label(value, choices):
    return dict(choices).get(value, value)

def get_display_list(values, choices):
    return [dict(choices).get(v, v) for v in values]
