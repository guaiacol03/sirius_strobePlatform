import numpy as np

def find_dividers(target):
    n1_range = np.arange(1, 65535)
    perf_n2 = np.full(n1_range.shape, 8000000) / (n1_range * target)

    round_n2 = np.clip(np.array([np.floor(perf_n2), np.ceil(perf_n2)]), 1, 65535)
    round_err = np.abs(round_n2 - target)
    min_err = np.unravel_index(np.argmin(round_err), round_err.shape)

    min_vals = [n1_range[min_err[1]].item(), round_n2[min_err].item()]
    return min_vals, (round_err[min_err] / 8000000)

def form_bytes(values):
        return list(reversed(np.array([values[0]], dtype=np.uint16).tobytes())) + \
    list(reversed(np.array([values[1]], dtype=np.uint16).tobytes()))