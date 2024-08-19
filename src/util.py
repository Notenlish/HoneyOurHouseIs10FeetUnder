def lerp(start: float, end: float, t: float) -> float:
    """Linear interpolate on the scale given by a to b, using t as the point on that scale.
    Examples
    --------
        50 == lerp(0, 100, 0.5)
        4.2 == lerp(1, 5, 0.8)
    """
    return (1 - t) * start + t * end


def inv_lerp(start: float, end: float, v: float) -> float:
    """Inverse Linar Interpolation, get the fraction between a and b on which v resides.
    Examples
    --------
        0.5 == inv_lerp(0, 100, 50)
        0.8 == inv_lerp(1, 5, 4.2)
    """
    return (v - start) / (end - start)

def ease_in(t):
    return t * t

def ease_out(t):
    return t * (2 - t)

def ease_in_out(t):
    return t * t * (3 - 2 * t)
