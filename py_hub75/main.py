import random
import numpy as np
from ivnd_display import IVNDDisplay
from ivnd_rotary import IVNDRotary
from ivnd_patterns import *
from ivnd_fun import *
import time

rot = IVNDRotary()
mat = IVNDDisplay()
mat.clear()
mat.set_brightness(0x0F)

# mat.render_static()
# ivnd_badapple(mat)

val = 1
last_val = 0
task = 0
phase = 0
while True:
    for a in rot.read():
        if a == 1:
            if val < 999:
                val += 1
        if a == 2:
            if val > 1:
                val -= 1
        if a == 3:
            if phase != 1:
                phase += 1

    if phase > 0:
        if phase == 1:
            print(f"Pressed at framerate {last_val}, expecting {task}")
            phase = 2
            val = 0
            mat.render_static()

        if val > 99:
            val = 99
        ent_num = f"{val:02}"
        buf = ivnd_number(ent_num[0], ent_num[1])
        mat.write(image_b=buf)

        if phase == 4:
            print(f"Received {val}, expecting {task}")
            phase = 0
            val = last_val
            last_val = 0
            mat.clear()
            continue
        phase = 2

    elif val != last_val:
        last_val = val
        mat.render_strobe(val)
        task = f"{random.randint(1, 99):02}"
        buf = ivnd_number(task[0], task[1])

        neg = np.zeros((64, 64), dtype=np.bool)
        alw = np.zeros((64, 64), dtype=np.bool)
        ivnd_embed_number(val, alw, neg)

        mat.write(image_r = alw, image_g = neg, image_b = buf)
    time.sleep(0.5)