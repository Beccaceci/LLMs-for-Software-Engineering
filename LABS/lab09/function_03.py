def computeMaxTime(winner_time, avg_speed, track_type):
    import math
    from numbers import Real
    if any(isinstance(v,bool) or not isinstance(v,Real) or not math.isfinite(v) or v <= 0 for v in (winner_time,avg_speed)):
        return 0
    if track_type not in ("A","B","C"):
        return 0
    if track_type == "C":
        return winner_time * 1.5
    band = 0 if avg_speed <= 30 else 1 if avg_speed <= 35 else 2
    increment = {"A":(0.05,0.10,0.15),"B":(0.20,0.25,0.30)}[track_type][band]
    return winner_time * (1 + increment)
