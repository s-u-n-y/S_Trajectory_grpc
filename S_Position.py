def S_position(t, Ta, Tv, Td, Tj1, Tj2, q0, q1, v0, v1, vlim, amax, amin, alima, alimd, jmax, jmin):
    T = Ta + Tv + Td
    # Acceleration phase
    if 0 <= t < Tj1:
        q = q0 + v0*t + jmax*(t**3)/6
    elif Tj1 <= t < Ta - Tj1:
        q = q0 + v0*t +(alima/6)*(3*(t**2) - 3*Tj1*t + Tj1**2)
    elif Ta - Tj1 <= t < Ta:
        q = q0 + (vlim + v0)*(Ta/2)- vlim*(Ta - t) - jmin*((Ta - t)**3/6)
    # Uniform speed phase
    elif Ta <= t < Ta + Tv:
        q = q0 + (vlim + v0)*(Ta/2) + vlim*(t - Ta)
    # Deceleration phase
    elif Ta + Tv <= t < T - Td + Tj2:
        q = q1 - (vlim + v1)*(Td/2) + vlim*(t - T + Td) - jmax*((t - T + Td)**3/6)
    elif T - Td + Tj2 <= t < T - Tj2:
        q = q1 - (vlim + v1)*(Td/2) + vlim*(t - T + Td) + (alimd/6)*(3*((t - T + Td)**2) - 3*Tj2*(t - T + Td) + Tj2**2)
    elif T - Tj2 <= t <= T:
        q = q1 - v1*(T - t) - jmax*((T - t)**3/6)

    return q