from numba import jit, prange, njit
import multiprocessing
import numpy as np
ncpu = multiprocessing.cpu_count()
import parmap
import pyarrow as pa
import pyarrow.parquet as pq

@jit(nopython=True, nogil=True)
def getAngle(ping_index, x, y, z, ping_indexes, beam_indexes):
    if ping_index == 0:
        start = 0
        stop = ping_indexes[ping_index]
        shape = ping_indexes[ping_index]
        nadir_index = int(beam_indexes[ping_index][1] / 2)
    else:
        start = ping_indexes[ping_index - 1]
        stop = ping_indexes[ping_index]
        shape = ping_indexes[ping_index] - ping_indexes[ping_index - 1]
        nadir_index = int(
            np.sum(beam_indexes[0: beam_indexes[ping_index][0]][:, 1])
            + (beam_indexes[ping_index][1] / 2)
        )
    XY = np.array([(x[nadir_index], y[nadir_index])])
    pings = np.column_stack((x[start:stop], y[start:stop]))
    Zi = z[start:stop]
    a_min_b = XY - pings
    d = np.sqrt(np.sum((a_min_b) ** 2, axis=1))
    angle = np.rad2deg(np.arctan2(np.abs(Zi), d)).reshape(
        shape,
    )
    # return [start, stop, angle]
    return angle


def run_it(mb_data):
    unique, counts = np.unique(mb_data["GpsTime"], return_counts=True)
    beam_indexes = np.array([[i, v] for i, v in enumerate(list(counts))])

    ping_indexes = np.cumsum(beam_indexes[:, 1])
    input_indexes = list(range(len(ping_indexes)))

    chunksize = unique.shape[0] / ncpu
    chunksize = int(chunksize - (chunksize % ncpu))
    print('chunksize:', chunksize)
    angles = parmap.map(
        getAngle,
        input_indexes,
        mb_data["X"],
        mb_data["Y"],
        mb_data["Z"],
        ping_indexes,
        beam_indexes,
        pm_processes=ncpu,
        pm_pbar=True,
        pm_parallel=True,
        pm_chunksize=chunksize,
    )
    angle_values = [beam for ping in angles for beam in ping]
    ara_data = pa.table(
        {
            'X': mb_data["X"],
            'Y': mb_data["Y"],
            'Z': mb_data["Z"],
            'GpsTime': mb_data["GpsTime"],
            'Amplitude': mb_data["Amplitude"],
            'angle_values': angle_values,
            }
        )
    return ara_data