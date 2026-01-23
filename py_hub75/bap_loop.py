import os
import random
from bap_display import BAPDisplay
from bap_patterns import *
from bap_rotary import BAPRotary
import time

class BAPProgram:
    def __init__(self):
        self.display = BAPDisplay()
        self.rotary = BAPRotary()
        self.filename = "default"
        self.logfile = None

    def ask_id(self):
        self.display.clear()
        self.display.set_brightness(0x0F)
        self.display.render_static()

        sel = 0
        values = [0, 0, 0, 0, 0, 0]
        presses = 0

        while True:
            for a in self.rotary.read():
                if a == 1:
                    values[sel] += 1
                    if values[sel] > 9:
                        values[sel] = 0
                if a == 2:
                    values[sel] -= 1
                    if values[sel] < 0:
                        values[sel] = 9
                if a == 3:
                    presses += 1

            if presses > 0:
                presses = 0
                sel += 1
                if sel > 5:
                    sel = 0

                values[0] = 0

            nums = [f"{a:1}" for a in values[1:]]
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
                return f_name_adj

            b_base, b_select, b_static = ivnd_ask_mtp(sel, nums + [a for a in str(adj)])
            self.display.write(image_b=b_static, image_g=b_select, image_r=b_base)
            time.sleep(0.5)

    def log_write(self, log_line):
        print(log_line)
        if self.logfile is not None:
            self.logfile.writelines([log_line + "\n"])

    def main_loop(self):
        self.display.clear()
        self.display.set_brightness(0x0F)
        self.display.render_static()

        val = 1
        last_val = 0
        task = 0
        presses = 0
        phase = 0
        log_index = 0
        log_line = ""
        while True:
            for a in self.rotary.read():
                if a == 1:
                    val += 1
                if a == 2:
                    val -= 1
                if a == 3:
                    presses += 1

            if presses >= 1.5:
                presses = 0
                self.display.clear()
                if phase <= 0:
                    log_line = f"{self.filename},{log_index},{last_val},{task},"
                    phase = 1
                    val = 1
                    self.display.render_static()
                else:
                    log_line += f"{val:02}"
                    self.log_write(log_line)
                    log_index += 1

                    if val == 0:
                        break

                    phase = 0
                    val = last_val
                    last_val = 0

            presses = max(0, presses-0.5)

            if phase > 0:
                if val > 99:
                    val = val - 100
                elif val < 0:
                    val = 100 + val

                ent_num = f"{val:02}"
                buf = bap_number(ent_num[0], ent_num[1])
                self.display.write(image_b=buf)
            elif val != last_val:
                if val > 999:
                    val = 999
                elif val < 1:
                    val = 1

                last_val = val
                self.display.render_strobe(val)
                task = f"{random.randint(1, 99):02}"
                buf = bap_number(task[0], task[1])

                neg = np.zeros((64, 64), dtype=np.bool)
                alw = np.zeros((64, 64), dtype=np.bool)
                bap_embed_number(val, alw, neg)

                self.display.write(image_r = alw, image_g = neg, image_b = buf)
            time.sleep(0.5)

    def run(self):
        self.filename = self.ask_id()
        self.logfile = open("logs/" + self.filename, "w")
        self.logfile.writelines(["filename,trial,task,answer\n"])
        self.main_loop()
        self.logfile.close()