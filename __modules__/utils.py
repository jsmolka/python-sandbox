def remap(value, low1, high1, low2, high2):
    """Re-maps a number from one range to another"""
    return float(value - low1) / (high1 - low1) * (high2 - low2) + low2
