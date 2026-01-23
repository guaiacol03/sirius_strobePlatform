import RPi.GPIO as GPIO

class BAPRotary:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        act_buffer = [0]
        def __act_A(ch):
            if act_buffer[-1] == -2:
                act_buffer[-1] = 1
                act_buffer.append(0)
            else:
                act_buffer[-1] = -1

        def __act_B(ch):
            if act_buffer[-1] == -1:
                act_buffer[-1] = 2
                act_buffer.append(0)
            else:
                act_buffer[-1] = -2

        def __act_S(ch):
            act_buffer.insert(-1, 3)

        GPIO.add_event_detect(22, GPIO.FALLING, callback=__act_S)
        GPIO.add_event_detect(23, GPIO.FALLING, callback=__act_A)
        GPIO.add_event_detect(24, GPIO.FALLING, callback=__act_B)

        self.buffer = act_buffer

    def __del__(self):
        GPIO.remove_event_detect(22)
        GPIO.remove_event_detect(23)
        GPIO.remove_event_detect(24)

    def read(self):
        if len(self.buffer) < 2:
            return []

        ret = self.buffer[:-1]
        self.buffer[0] = self.buffer[-1]
        del self.buffer[:-1]

        return ret