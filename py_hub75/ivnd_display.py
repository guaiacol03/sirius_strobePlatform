import RPi.GPIO as GPIO
from ivnd_freq import find_dividers, form_bytes
import spidev
import numpy as np

class IVNDDisplay:
    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 500000

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(25, GPIO.OUT)

        self.brightness = 0x0F

    def clear(self, fast=True):
        # write byte to IMAGE to reset CTRL (would not display even if transacts)
        GPIO.output(25, False)
        self.spi.writebytes2([0xAA])

        # zero out CTRL (brightness = 0)
        GPIO.output(25, True)
        self.spi.writebytes2([0x00 for j in range(8)])
        GPIO.output(25, False)

        if not fast:
            # zero out IMAGE
            self.spi.writebytes2([0x00 for j in range(8*64*3)])

    def set_brightness(self, brightness):
        if brightness > 0xFF:
            brightness = 0xFF
            print("brightness clamped to 255")
        elif brightness < 0x00:
            brightness = 0x00
            print("brightness clamped to 0")

        self.brightness = brightness

    def render_static(self):
        brt = list(np.array([self.brightness], dtype=np.uint8).tobytes())
        GPIO.output(25, True)
        self.spi.writebytes2(brt + [0x00 for j in range(7)]) # 1x{brightness} - 7x{0x00}
        GPIO.output(25, False)

    def render_strobe(self, fps=None):
        if fps is None:
            self.render_static()
            return

        values, err = find_dividers(fps)
        divs = form_bytes(values)
        brt = list(np.array([self.brightness], dtype=np.uint8).tobytes())

        GPIO.output(25, True)
        self.spi.writebytes2(brt + divs + [0x00, 0x00, 0xFF])  # 1x{brightness} - 2x{div1} - 2x{div2} - 2x{0x00} - 1x{0xFF}
        GPIO.output(25, False)

    def write(self,
              image_r = np.zeros((64, 64), dtype=np.bool),
              image_g = np.zeros((64, 64), dtype=np.bool),
              image_b = np.zeros((64, 64), dtype=np.bool)):

        self.spi.writebytes2(list(np.packbits(image_r).tobytes()) + \
                             list(np.packbits(image_g).tobytes()) + \
                             list(np.packbits(image_b).tobytes()))

    def __del__(self):
        self.spi.close()