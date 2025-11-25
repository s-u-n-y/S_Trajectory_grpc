def S_acceleration(t, Ta, Tv, Td, Tj1, Tj2, q0, q1, v0, v1, vlim, amax, amin, alima, alimd, jmax, jmin):
    T = Ta + Tv + Td
    if 0 <= t < Tj1:
        qdd = jmax*t
    elif Tj1 <= t < Ta - Tj1:
        qdd = alima
    elif Ta - Tj1 <= t < Ta:
        qdd = -jmin*(Ta - t)
    # Uniform speed phase
    elif Ta <= t < Ta + Tv:
        qdd = 0
    # Deceleration phase
    elif Ta + Tv <= t < T - Td + Tj2:
        qdd = -jmax*(t - T + Td)
    elif T - Td + Tj2 <= t < T - Tj2:
        qdd = alimd
    elif T - Tj2 <= t <= T:
        qdd = -jmax*(T - t)

    return qdd