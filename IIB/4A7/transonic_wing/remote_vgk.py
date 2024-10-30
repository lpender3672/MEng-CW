
import json
import os
import paramiko
import pyautogui
import pygetwindow as gw
import subprocess
import time
import re
from matplotlib import pyplot as plt


absp = 'IIB/4A7/transonic_wing/'

with open(absp + '/secrets.json') as f:
    secrets = json.load(f)
    shifted_pwd = secrets['password']

pwd = ''
for s in shifted_pwd:
    pwd += chr(ord(s) - 1)

intermediate_hostname = 'gate.eng.cam.ac.uk'
teaching_hostname = 'ts-access'
username = "lwp26"

time.sleep(1)

_ = input("Setup Airfoil app to run via Putty and X11 forwarding. Press enter when window is open.")

time.sleep(1)

window = gw.getWindowsWithTitle("Airfoil")[0]

if window:
    window.activate()
    print("Window found")



intermediate_client = paramiko.SSHClient()
intermediate_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
intermediate_client.connect(intermediate_hostname, username=username, password=pwd)

intermediate_transport = intermediate_client.get_transport()
intermediate_session = intermediate_transport.open_session()
#intermediate_session.request_x11()

transport = intermediate_client.get_transport()
dest_addr = (teaching_hostname, 22)
src_addr = (intermediate_hostname, 22)
channel = transport.open_channel("direct-tcpip", dest_addr, src_addr)

teaching_client = paramiko.SSHClient()
teaching_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
teaching_client.connect(teaching_hostname, username=username, password=pwd, sock=channel)

teaching_transport = teaching_client.get_transport()
teaching_session = teaching_transport.open_session()
#teaching_session.request_x11()


class Result():
    def __init__(self, variables, upper_surface_cp, lower_surface_cp):
        self.CD2 = variables['CDV+CD2'] - variables['CDV']
        self.Cd = variables['CDV+CD2']
        self.Cl = variables['CL']
        self.Alpha = variables['ALP']
        self.Mach = variables['EM']

        self.x_upper, self.cp_upper = zip(*upper_surface_cp)
        self.x_lower, self.cp_lower = zip(*lower_surface_cp)

class AirfoilApp():

    def __init__(self, ssh_client, window):
        self.ssh_client = ssh_client
        self.ssh_client.exec_command("cd Airfoil-hb")

        self.window = window

        self.M = 0.75
        self.alpha = 2.0

        x = self.window.left
        y = self.window.top
        w = self.window.width
        h = self.window.height

        self.mach_input_loc = (x + w * 0.33 - 50, y + h * 0.7)
        self.alpha_input_loc = (x + w * 0.66 - 50, y + h * 0.7)
        self.run_loc = (x + w * 0.75, y + h * 0.9)

        

    def run(self, M, alpha):

        if M != self.M:
            self.M = M
            self.set_M(M)
        
        if alpha != self.alpha:
            self.alpha = alpha
            self.set_alpha(alpha)

        # run 
        # sleep
        # get results

    def set_M(self):
        # set in window
        
        pyautogui.click(self.mach_input_loc, duration=0.5)
        pyautogui.sleep(0.5)
        pyautogui.keyDown('backspace')
        pyautogui.sleep(0.5)
        pyautogui.keyUp('backspace')
        pyautogui.write(str(self.M), interval=0.05)
        pyautogui.sleep(0.5)
        pyautogui.press('enter')
        pyautogui.sleep(0.5)


    def set_alpha(self):
        # set in window
        
        pyautogui.click(self.alpha_input_loc, duration=0.5)
        pyautogui.sleep(0.5)
        pyautogui.keyDown('backspace')
        pyautogui.sleep(0.5)
        pyautogui.keyUp('backspace')
        pyautogui.write(str(self.alpha), interval=0.05)
        pyautogui.sleep(0.5)
        pyautogui.press('enter')
        pyautogui.sleep(0.5)


    def load_result(self):
        
        sftp_client = self.ssh_client.open_sftp()
        remote_file = sftp_client.open('Airfoil-hb/Autorun.BRF')

        variables = {}
        upper_surface_cp = []
        lower_surface_cp = []
        variable_pattern = re.compile(r"([\w+]+)\s*=\s*([-\d.]+)")
        cp_data_pattern = re.compile(r"^\s*([\d.]+)\s+([-.\d]+)")
        parsing_upper = False
        parsing_lower = False

        for line in remote_file:
            if "Upper surface CP values" in line:
                parsing_upper = True
                parsing_lower = False
                continue
            elif "Lower surface CP values" in line:
                parsing_upper = False
                parsing_lower = True
                continue

            # Parse variable if not within CP sections

            if not (parsing_upper or parsing_lower):
                matches = variable_pattern.findall(line)
                for var, val in matches:
                        variables[var] = float(val) if '.' in val else int(val)

            # Parse upper surface CP data
            if parsing_upper:
                cp_match = cp_data_pattern.match(line)
                if cp_match:
                    x, cp = map(float, cp_match.groups())
                    upper_surface_cp.append((x, cp))
                else:
                    parsing_upper = False

            # Parse lower surface CP data
            elif parsing_lower:
                cp_match = cp_data_pattern.match(line)
                if cp_match:
                    x, cp = map(float, cp_match.groups())
                    lower_surface_cp.append((x, cp))
                else:
                    parsing_lower = False

        out = Result(variables, upper_surface_cp, lower_surface_cp)

        remote_file.close()
        sftp_client.close()

        return out


# Parsing flags
App = AirfoilApp(teaching_client, window)

App.set_M()
App.set_alpha()

# Read each line and parse accordingly


teaching_client.close()
intermediate_client.close()
