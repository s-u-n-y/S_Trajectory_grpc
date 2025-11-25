import numpy as np


def STrajectoryPara(q0, q1, v0, v1, vmax, amax, jmax):
    sigma = np.sign(q1 - q0)
    q_0 = sigma * q0
    q_1 = sigma * q1
    v_0 = sigma * v0
    v_1 = sigma * v1
    v_max = ((sigma + 1) / 2) * vmax + ((sigma - 1) / 2) * (-vmax)
    v_min = ((sigma + 1) / 2) * (-vmax) + ((sigma - 1) / 2) * vmax
    a_max = ((sigma + 1) / 2) * amax + ((sigma - 1) / 2) * (-amax)
    a_min = ((sigma + 1) / 2) * (-amax) + ((sigma - 1) / 2) * amax
    j_max = ((sigma + 1) / 2) * jmax + ((sigma - 1) / 2) * (-jmax)
    j_min = ((sigma + 1) / 2) * (-jmax) + ((sigma - 1) / 2) * jmax

    if (v_max - v_0) * j_max < a_max ** 2:
        Tj1 = np.sqrt((v_max - v_0) / j_max)
        Ta = 2 * Tj1
        a_lima = j_max * Tj1
    else:
        Tj1 = a_max / j_max
        Ta = Tj1 + (v_max - v_0) / a_max
        a_lima = a_max
    if (v_max - v_1) * j_max < a_max ** 2:
        Tj2 = np.sqrt((v_max - v_1) / j_max)
        Td = 2 * Tj2
        a_limd = -j_max * Tj2
    else:
        Tj2 = a_max / j_max
        Td = Tj2 + (v_max - v_1) / a_max
        a_limd = -a_max

    Tv = (q_1 - q_0) / v_max - (Ta / 2) * (1 + v_0 / v_max) - (Td / 2) * (1 + v_1 / v_max)

    if Tv > 0:
        vlim = v_max
        T = Ta + Tv + Td
        return [Ta, Tv, Td, Tj1, Tj2, q_0, q_1, v_0, v_1, vlim, a_max, a_min, a_lima, a_limd, j_max, j_min]
    else:
        Tv = 0
        Tj = a_max / j_max
        Tj1 = Tj
        Tj2 = Tj
        delta = (a_max ** 4 / j_max ** 2) + 2 * (v_0 ** 2 + v_1 ** 2) + a_max * (
                    4 * (q_1 - q_0) - 2 * (a_max / j_max) * (v_0 + v_1))
        Ta = ((a_max ** 2 / j_max) - 2.0 * v_0 + np.sqrt(delta)) / (2.0 * a_max)
        Td = ((a_max ** 2 / j_max) - 2.0 * v_1 + np.sqrt(delta)) / (2.0 * a_max)
        if Ta < 0 or Td < 0:
            if Ta < 0:
                Ta = 0
                Tj1 = 0
                Td = 2 * (q_1 - q_0) / (v_0 + v_1)
                Tj2 = (j_max * (q_1 - q_0) - np.sqrt(
                    j_max * (j_max * (q_1 - q_0) ** 2 + (v_1 + v_0) ** 2 * (v_1 - v_0)))) / (j_max * (v_1 + v_0))
                a_lima = 0
                a_limd = -j_max * Tj2
                vlim = v0
                return [Ta, Tv, Td, Tj1, Tj2, q_0, q_1, v_0, v_1, vlim, a_max, a_min, a_lima, a_limd, j_max, j_min]
            elif Td < 0:
                Td = 0
                Tj2 = 0
                Ta = 2 * (q_1 - q_0) / (v_0 + v_1)
                Tj1 = (j_max * (q_1 - q_0) - np.sqrt(j_max * (j_max * (q_1 - q_0) ** 2)) - (v_1 + v_0) ** 2 * (
                            v_1 - v_0)) / (j_max * (v_1 + v_0))
                a_lima = j_max * Tj1
                a_limd = 0
                vlim = v_0 + a_lima * (Ta - Tj1)
                return [Ta, Tv, Td, Tj1, Tj2, q_0, q_1, v_0, v_1, vlim, a_max, a_min, a_lima, a_limd, j_max, j_min]
        elif Ta >= 2 * Tj and Td >= 2 * Tj:
            a_lima = a_max
            a_limd = -a_max
            vlim = v0 + a_lima * (Ta - Tj)
            return [Ta, Tv, Td, Tj1, Tj2, q_0, q_1, v_0, v_1, vlim, a_max, a_min, a_lima, a_limd, j_max, j_min]
        else:
            lambda_val = 0.99
            while Ta < 2 * Tj or Td < 2 * Tj:
                a_max = lambda_val * a_max
                Tv = 0
                Tj = a_max / j_max
                Tj1 = Tj
                Tj2 = Tj
                delta = (a_max ** 4 / j_max ** 2) + 2 * (v_0 ** 2 + v_1 ** 2) + a_max * (
                            4 * (q_1 - q_0) - 2 * (a_max / j_max) * (v_0 + v_1))
                Ta = ((a_max ** 2 / j_max) - 2.0 * v_0 + np.sqrt(delta)) / (2.0 * a_max)
                Td = ((a_max ** 2 / j_max) - 2.0 * v_1 + np.sqrt(delta)) / (2.0 * a_max)
                if Ta < 0 or Td < 0:
                    if Ta < 0:
                        Ta = 0
                        Tj1 = 0
                        Td = 2 * (q_1 - q_0) / (v_0 + v_1)
                        Tj2 = (j_max * (q_1 - q_0) - np.sqrt(
                            j_max * (j_max * (q_1 - q_0) ** 2 + (v_1 + v_0) ** 2 * (v_1 - v_0)))) / (
                                          j_max * (v_1 + v_0))
                        a_lima = 0
                        a_limd = -j_max * Tj2
                        vlim = v0
                        return [Ta, Tv, Td, Tj1, Tj2, q_0, q_1, v_0, v_1, vlim, a_max, a_min, a_lima, a_limd, j_max,
                                j_min]
                    elif Td < 0:
                        Td = 0
                        Tj2 = 0
                        Ta = 2 * (q_1 - q_0) / (v_0 + v_1)
                        Tj1 = (j_max * (q_1 - q_0) - np.sqrt(j_max * (j_max * (q_1 - q_0) ** 2)) - (v_1 + v_0) ** 2 * (
                                    v_1 - v_0)) / (j_max * (v_1 + v_0))
                        a_lima = j_max * Tj1
                        a_limd = 0
                        vlim = v_0 + a_lima * (Ta - Tj1)
                        return [Ta, Tv, Td, Tj1, Tj2, q_0, q_1, v_0, v_1, vlim, a_max, a_min, a_lima, a_limd, j_max,
                                j_min]
            return [Ta, Tv, Td, Tj1, Tj2, q_0, q_1, v_0, v_1, vlim, a_max, a_min, a_lima, a_limd, j_max, j_min]
