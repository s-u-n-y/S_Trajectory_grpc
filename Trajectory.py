import numpy as np
import matplotlib.pyplot as plt
from S_Position import S_position
from S_Jerk import S_jerk
from S_Velocity import S_velocity
from S_Acceleration import S_acceleration
from STrajectoryPara import STrajectoryPara
import os

# Boundary conditions


def Trajectory(q0, q1, v0, v1, vmax, amax, jmax, path='./', name='trajectory.jpg'):
    q0 = q0
    q1 = q1
    v0 = v0
    v1 = v1
    vmax = vmax
    amax = amax
    jmax = jmax

    sigma = np.sign(q1 - q0)

    # Obtain planning parameters Ta, Tv, Td, Tj1, Tj2, q0, q1, v0, v1, vlim, amax, amin, alima, alimd, jmax, jmin
    para = STrajectoryPara(q0, q1, v0, v1, vmax, amax, jmax)

    T = para[0] + para[1] + para[2]
    time = []
    q = []
    qd = []
    qdd = []
    qddd = []

    for t in np.arange(0, T, 0.001):
        time.append(t)
        q.append(S_position(t, *para))
        qd.append(S_velocity(t, *para))
        qdd.append(S_acceleration(t, *para))
        qddd.append(S_jerk(t, *para))

    q = [i * sigma for i in q]
    qd = [i * sigma for i in qd]
    qdd = [i * sigma for i in qdd]
    qddd = [i * sigma for i in qddd]

    os.makedirs(path, exist_ok=True)
    full_path = os.path.join(path, name)


    # Plotting
    fig, axs = plt.subplots(4, 1)
    axs[0].plot(time, q, 'r', linewidth=1.5)
    axs[1].plot(time, qd, 'b', linewidth=1.5)
    axs[2].plot(time, qdd, 'g', linewidth=1.5)
    axs[3].plot(time, qddd, linewidth=1.5)

    for ax in axs:
        ax.grid()

    plt.tight_layout()
    plt.savefig(full_path)
    plt.close(fig)

    return {"plot_name": full_path}

