import numpy as np

def ivnd_testcard():
    frame_r = np.full((64, 64), False, dtype=np.bool)
    frame_r[1, 1:63] = True
    frame_r[62, 1:63] = True
    frame_r[1:63, 1] = True
    frame_r[1:63, 62] = True

    frame_g = np.full((64, 64), False, dtype=np.bool)
    for i in range(1, 63):
        frame_g[i, i] = True
        frame_g[i, 63-i] = True

    frame_b = np.full((64, 64), False, dtype=np.bool)
    frame_b[31:33, 1:63] = True
    frame_b[1:63, 31:33] = True

    return frame_r, frame_g, frame_b

__valid_numbers = [str(i) for i in range(10)]
def __single_number(num):
    frame = np.zeros((32, 64), dtype=np.bool)

    if num not in __valid_numbers:
        frame[8:28, 8:57] = True
        return frame

    if num not in ["0", "1", "7"]:
        # mid h stroke
        frame[9:27, 31:33] = True
        frame[10:26, 30:34] = True

    if num not in ["1", "2", "3", "7"]:
        # left top v stroke
        frame[8:10, 9:32] = True
        frame[7:11, 10:31] = True

    if num in ["0", "2", "6", "8"]:
        # left bottom v stroke
        frame[8:10, 32:55] = True
        frame[7:11, 33:54] = True

    if num not in ["1", "4", "7"]:
        # bot h stroke
        frame[9:27, 54:56] = True
        frame[10:26, 53:57] = True

    if num != "2":
        # right bottom v stroke
        frame[26:28, 32:55] = True
        frame[25:29, 33:54] = True

    if num not in ["5", "6"]:
        # right top v stroke
        frame[26:28, 9:32] = True
        frame[25:29, 10:31] = True

    if num not in ["1", "4"]:
        # top h stroke
        frame[9:27, 8:10] = True
        frame[10:26, 7:11] = True

    return frame
def ivnd_number(num1, num2):
    frame = np.full((64, 64), False, dtype=np.bool)

    num1_fr = __single_number(num1)
    frame[:32, :] = num1_fr
    num2_fr = __single_number(num2)
    frame[32:-4, :] = num2_fr[4:, :]

    return frame

def __micro_number(num):
    frame = np.zeros((3, 5), dtype=np.bool)

    if num not in __valid_numbers:
        frame[:, :] = True
        return frame

    # mid h stroke
    frame[0:3, 2] |= num not in ["0", "1", "7"]
    # left top v stroke
    frame[0, 0:2] |= num not in ["1", "2", "3", "7"]
    # left bottom v stroke
    frame[0, 2:5] |= num in ["0", "2", "6", "8"]
    # bot h stroke
    frame[0:3, 4] |= num not in ["1", "4", "7"]
    # right bottom v stroke
    frame[2, 2:5] |= num != "2"
    # right top v stroke
    frame[2, 0:2] |= num not in ["5", "6"]
    # top h stroke
    frame[0:3, 0] |= num not in ["1", "4"]

    return frame
def ivnd_embed_number(value, frame_a, frame_n):
    frame_a[1:13, 1:7] = True
    frame_n[4, 1:6] = True
    frame_n[8, 1:6] = True
    frame_n[1:13, 6] = True
    frame_n[12, 1:6] = True

    val_string = f"{value:003}"
    num1 = __micro_number(val_string[0])
    frame_n[1:4, 1:6] = np.invert(num1)
    num2 = __micro_number(val_string[1])
    frame_n[5:8, 1:6] = np.invert(num2)
    num3 = __micro_number(val_string[2])
    frame_n[9:12, 1:6] = np.invert(num3)

__sign_mtp = np.array([
    [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1],
    [1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
    [1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
], dtype=np.bool).transpose()
__sign_c = np.array([
    [1, 1, 1],
    [1, 0, 0],
    [1, 0, 0],
    [1, 0, 0],
    [1, 1, 1]
], dtype=np.bool).transpose()
__sign_arrow = np.array([
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 1, 1, 1],
    [0, 0, 0, 1, 0],
    [0, 0, 1, 0, 0]
], dtype=np.bool).transpose()
def ivnd_ask_mtp(sel, values):
    base = np.zeros((64, 64), dtype=np.bool)
    select = np.zeros((64, 64), dtype=np.bool)
    static = np.zeros((64, 64), dtype=np.bool)

    static[1:12, 1:6] = __sign_mtp
    static[25:28, 1:6] = __sign_c

    nums = [__micro_number(v) for v in values]
    if sel != 1:
        base[13:16, 1:6] = nums[0]
    else:
        select[13:16, 1:6] = nums[0]
    if sel != 2:
        base[17:20, 1:6] = nums[1]
    else:
        select[17:20, 1:6] = nums[1]
    if sel != 3:
        base[21:24, 1:6] = nums[2]
    else:
        select[21:24, 1:6] = nums[2]
    if sel != 4:
        base[29:32, 1:6] = nums[3]
    else:
        select[29:32, 1:6] = nums[3]
    if sel != 5:
        base[33:36, 1:6] = nums[4]
    else:
        select[33:36, 1:6] = nums[4]

    i = 0
    if len(nums) > 5:
        # dash
        static[37:40, 5] = True

        for i in range(len(nums) - 5):
            static[41+(4*i):44+(4*i), 1:6] = nums[i+5]
        i += 2
    if sel != 0:
        base[37 + (4 * i):42 + (4 * i), 1:6] = __sign_arrow
    else:
        select[37 + (4 * i):42 + (4 * i), 1:6] = __sign_arrow
    return base, select, static
