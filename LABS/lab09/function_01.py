def compute_average(grades):
    """Return the trimmed mean of six grades, with 33 representing laude."""
    import math
    from numbers import Real
    if not isinstance(grades, (list, tuple)) or len(grades) != 6:
        raise ValueError("Expected exactly six grades")
    for value in grades:
        if isinstance(value, bool):
            raise ValueError("A boolean is not a grade")
        if not isinstance(value, Real):
            raise TypeError("Expected numeric grades")
        if not math.isfinite(value) or not (18 <= value <= 30 or value == 33):
            raise ValueError("Invalid grade")
    return (sum(grades) - min(grades) - max(grades)) / 4
