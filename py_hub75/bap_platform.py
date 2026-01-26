import RPi.GPIO as GPIO
from bap_freq import find_dividers, form_bytes
import spidev
import numpy as np

class BAPPlatform:
    def __init__(self, rotary = True):
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 500000

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(25, GPIO.OUT)

        self.brightness = 0x0F

        if rotary:
            self.rotary_buffer = []

    def read_rotary(self):
        if self.rotary_buffer is None:
            return []

        while len(self.rotary_buffer) < 3 or self.rotary_buffer[-2:] != [0x00, 0x00]:
            self._write([0xAA, 0xAA])
            GPIO.output(25, True)
            self._write([0xAA, 0xAA])
            GPIO.output(25, False)

        b_buf = np.concat([np.unpackbits(e) for e in np.array(self.rotary_buffer, dtype=np.uint8)])
        t_buf = np.zeros(b_buf.shape)
        t_buf[:-4] += np.all(np.lib.stride_tricks.sliding_window_view(b_buf, 5) == np.array([0, 1, 1, 1, 0]),
                   axis=1) * 3

        t_buf[:-3] += np.all(np.lib.stride_tricks.sliding_window_view(b_buf, 4) == np.array([0, 1, 1, 0]),
                   axis=1) * 2

        t_buf[:-2] += np.all(np.lib.stride_tricks.sliding_window_view(b_buf, 3) == np.array([0, 1, 0]),
                   axis=1)
        r_buf = t_buf[np.nonzero(t_buf)]
        self.rotary_buffer = []

        return r_buf.astype(int).tolist()

    def _write(self, arr):
        if self.rotary_buffer is not None:
            self.rotary_buffer += self.spi.xfer(arr)
        else:
            self.spi.writebytes2(arr)

    def clear(self, fast=True):
        # write byte to IMAGE to reset CTRL (would not display even if transacts)
        GPIO.output(25, False)
        self._write([0xAA])

        # zero out CTRL (brightness = 0)
        GPIO.output(25, True)
        self._write([0x00 for j in range(8)])
        GPIO.output(25, False)

        if not fast:
            # zero out IMAGE
            self._write([0x00 for j in range(8*64*3)])

    def set_brightness(self, brightness):
        if brightness > 0xFF:
            brightness = 0xFF
            print("brightness clamped to 255")
        elif brightness < 0x00:
            brightness = 0x00
            print("brightness clamped to 0")

        self.brightness = brightness

    def render_static(self):
        self._write([0xAA])
        brt = list(np.array([self.brightness], dtype=np.uint8).tobytes())
        GPIO.output(25, True)
        self._write(brt + [0x00 for j in range(7)]) # 1x{brightness} - 7x{0x00}
        GPIO.output(25, False)

    def render_strobe(self, fps=None):
        if fps is None:
            self.render_static()
            return

        values, err = find_dividers(fps)
        divs = form_bytes(values)
        brt = list(np.array([self.brightness], dtype=np.uint8).tobytes())

        self._write([0xAA])
        GPIO.output(25, True)
        self._write(brt + divs + [0x00, 0x00, 0xFF])  # 1x{brightness} - 2x{div1} - 2x{div2} - 2x{0x00} - 1x{0xFF}
        GPIO.output(25, False)

    def write(self,
              image_r = np.zeros((64, 64), dtype=np.bool),
              image_g = np.zeros((64, 64), dtype=np.bool),
              image_b = np.zeros((64, 64), dtype=np.bool)):

        self._write(list(np.packbits(image_r).tobytes()) + \
                             list(np.packbits(image_g).tobytes()) + \
                             list(np.packbits(image_b).tobytes()))

    def __del__(self):
        self.spi.close()