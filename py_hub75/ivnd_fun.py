import numpy as np
from PIL import Image, ImageSequence
import time

def ivnd_badapple(dev):
    with Image.open("badapple.gif") as im:
        im.seek(1)
        for fr in ImageSequence.Iterator(im):
            w, h = fr.size
            crop = fr.crop((16, 26, w - 17, h - 27))
            sz = crop.resize((64, round(64 * (75 / 95)))).convert('1')
            d = np.asarray(sz)

            frame = np.zeros((64, 64), dtype=np.bool)
            frame[:51, :] = d
            frame = np.transpose(frame)
            dev.write(image_b = frame)

            time.sleep(1 / 15)