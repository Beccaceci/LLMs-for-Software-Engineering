def computeFee(basePrice, n_passengers, n_over18, n_under15):
    from numbers import Real
    import math
    if isinstance(basePrice,bool) or not isinstance(basePrice,Real) or not math.isfinite(basePrice) or basePrice < 0:
        raise ValueError("Invalid base price")
    counts = (n_passengers,n_over18,n_under15)
    if any(isinstance(n,bool) or not isinstance(n,int) for n in counts):
        raise ValueError("Passenger counts must be integers")
    if not 1 <= n_passengers <= 5 or min(n_over18,n_under15) < 0 or n_over18+n_under15 > n_passengers:
        raise ValueError("Inconsistent group counts")
    eligible = n_passengers >= 2 and n_over18 >= 1
    return float(basePrice * (n_passengers-n_under15 if eligible else n_passengers))
