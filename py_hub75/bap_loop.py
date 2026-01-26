import os
import random
from bap_platform import BAPPlatform
from bap_patterns import *
import time

class BAPProgram:
    def __init__(self):
        self.device = BAPPlatform()
        self.filename = "default"
        self.logfile = None
        self.brightness = 32

    def ask_id(self):
        self.device.clear()
        self.device.set_brightness(self.brightness)
        self.device.render_static()

        sel = 0
        values = [0, 0, 0, 0, 0, 0, self.brightness]
        presses = 0

        while True:
            for a in self.device.read_rotary():
                if a == 1:
                    values[sel] += 1
                    if sel != 6:
                        if values[sel] > 9:
                            values[sel] = 0
                    else:
                        if values[sel] > 255:
                            values[sel] = 255
                if a == 2:
                    values[sel] -= 1
                    if sel != 6:
                        if values[sel] < 0:
                            values[sel] = 9
                    else:
                        if values[sel] < 0:
                            values[sel] = 0
                if a == 3:
                    presses += 1

            if presses > 0:
                presses = 0
                sel += 1
                if sel > 6:
                    sel = 0

                values[0] = 0

            nums = [f"{a:1}" for a in values[1:-1]]
            f_name_init = f"MTP{"".join(nums[:3])}C{"".join(nums[3:5])}.csv"
            f_name_adj = f_name_init
            adj = ""
            if os.path.isfile("logs/" + f_name_init):
                adj = 1
                while adj < 999:
                    f_name_adj = f"MTP{"".join(nums[:3])}C{"".join(nums[3:5])}_{str(adj)}.csv"
                    if not os.path.isfile("logs/" + f_name_adj):
                        break
                    adj += 1
                else:
                    values = [0, 0, 0, 0, 0]

            if 3 <= values[0] <= 7:
                return f_name_adj, values[-1]

            b_base, b_select, b_static = bap_ask_mtp(sel, nums + [l for l in f"{values[-1]:003}"] + [a for a in str(adj)])
            self.device.write(image_b=b_static, image_g=b_select, image_r=b_base)
            self.device.set_brightness(values[-1])
            self.device.render_static()
            time.sleep(0.5)

    def log_write(self, log_line):
        print(log_line)
        if self.logfile is not None:
            self.logfile.writelines([log_line + "\n"])

    def main_loop(self):
        self.device.clear()
        self.device.set_brightness(self.brightness)
        self.device.render_static()

        val = 1
        last_val = 0
        task = 0
        presses = 0
        phase = 0
        log_index = 0
        log_line = ""
        log_insp = 0.0
        while True:
            tx = self.device.read_rotary()
            for a in tx:
                if a == 1:
                    val += 1
                if a == 2:
                    val -= 1
                if a == 3:
                    presses += 1
            if presses >= 1.5:
                presses = 0
                self.device.clear()
                if phase <= 0:
                    log_line = f"{self.filename},{log_index},{last_val},{task},"
                    phase = 1
                    val = 1
                    self.device.render_static()
                else:
                    log_line += f"{val:02},{log_insp:.2f}"
                    self.log_write(log_line)
                    log_index += 1

                    if val == 0:
                        break

                    phase = 0
                    val = last_val
                    last_val = 0

            presses = max(0, presses-(0.5/5))

            if phase > 0:
                if val > 99:
                    val = val - 100
                elif val < 0:
                    val = 100 + val

                ent_num = f"{val:02}"
                buf = bap_number(ent_num[0], ent_num[1])
                self.device.write(image_b=buf)
            else:
                log_insp += 0.1
                if val != last_val:
                    log_insp = 0.0
                    if val > 999:
                        val = 999
                    elif val < 1:
                        val = 1

                    last_val = val
                    self.device.render_strobe(val)
                    task = f"{random.randint(1, 99):02}"
                    buf = bap_number(task[0], task[1])

                    neg = np.zeros((64, 64), dtype=np.bool)
                    alw = np.zeros((64, 64), dtype=np.bool)
                    bap_embed_number(val, alw, neg)

                    self.device.write(image_r = alw, image_g = neg, image_b = buf)
                time.sleep(0.1)

    def run(self):
        self.filename, self.brightness = self.ask_id()
        print(f"Started {self.filename}, brt {self.brightness}")
        self.logfile = open("logs/" + self.filename, "w")
        self.logfile.writelines(["filename,trial,fps,task,answer,inspect_time\n"])
        self.main_loop()
        print(f"Ended {self.filename}")
        self.logfile.close()