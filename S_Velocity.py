def S_velocity(t, Ta, Tv, Td, Tj1, Tj2, q0, q1, v0, v1, vlim, amax, amin, alima, alimd, jmax, jmin):
    T = Ta + Tv + Td
    if 0 <= t < Tj1:
        qd = v0 + jmax*(t**2/2)
    elif Tj1 <= t < Ta - Tj1:
        qd = v0 + alima*(t - Tj1/2)
    elif Ta - Tj1 <= t < Ta:
        qd = vlim + jmin*((Ta - t)**2/2)
    # Uniform speed phase
    elif Ta <= t < Ta + Tv:
        qd = vlim
    # Deceleration phase
    elif Ta + Tv <= t < T - Td + Tj2:
        qd = vlim - jmax*((t - T + Td)**2/2)
    elif T - Td + Tj2 <= t < T - Tj2:
        qd = vlim + alimd*(t - T + Td - Tj2/2)
    elif T - Tj2 <= t <= T:
        qd = v1 + jmax*((t - T)**2/2)

    return qd