def S_jerk(t, Ta, Tv, Td, Tj1, Tj2, q0, q1, v0, v1, vlim, amax, amin, alima, alimd, jmax, jmin):
    T = Ta + Tv + Td
    if 0 <= t < Tj1:
        qddd = jmax
    elif Tj1 <= t < Ta - Tj1:
        qddd = 0
    elif Ta - Tj1 <= t < Ta:
        qddd = -jmin
    # Uniform speed phase
    elif Ta <= t < Ta + Tv:
        qddd = 0
    # Deceleration phase
    elif Ta + Tv <= t < T - Td + Tj2:
        qddd = -jmax
    elif T - Td + Tj2 <= t < T - Tj2:
        qddd = 0
    elif T - Tj2 <= t <= T:
        qddd = jmax

    return qddd