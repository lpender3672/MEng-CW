
import json
import os
import paramiko
import pyautogui
import pygetwindow as gw
import time
import re
from matplotlib import pyplot as plt
import numpy as np



class Result():
    def __init__(self, variables, upper_surface_cp, lower_surface_cp):
        self.CD2 = variables['CDV+CD2'] - variables['CDV']
        self.Cd = variables['CDV+CD2']
        self.Cl = variables['CL']
        self.Alpha = variables['ALP']
        self.M = variables['EM']
        self.Re = 10
        # currently Re isnt in variables[] from Autorun.BRF, need Autorun.FUL or something else

        self.x_upper, self.cp_upper = zip(*upper_surface_cp)
        self.x_lower, self.cp_lower = zip(*lower_surface_cp)

class AirfoilApp():

    def __init__(self, ssh_client, window, foil):
        self.ssh_client = ssh_client
        #self.ssh_client.exec_command("cd Airfoil-hb")

        self.window = window

        self.foil = foil

        self.M = 0.75
        self.alpha = 2.0 # degrees
        self.Re = 10 # million

        x = self.window.left
        y = self.window.top
        w = self.window.width
        h = self.window.height

        self.mach_input_loc = (x + 80, y + h * 0.776)
        self.alpha_input_loc = (x + 190, y + h * 0.776)
        self.run_loc = (x + w * 0.75, y + h * 0.9)

        

    def run(self, M, alpha, Re):

        if self.check_results_saved(self, M, alpha, Re):
            return self.load_result

        self.window.activate()

        if M != self.M:
            self.M = M
            self.set_M()
        
        if alpha != self.alpha:
            self.alpha = alpha
            self.set_alpha()

        if Re != self.Re:
            self.Re = Re
            self.set_Re()

        self.click_run()

        pyautogui.sleep(2)
        # sleep
        # get results

        return self.load_result()

    def set_M(self):
        # set in window
        if self.M > 0.95 or self.M < 0.05:
            raise ValueError("Mach number must be between 0.05 and 0.95")
        
        pyautogui.click((
            self.mach_input_loc
        ), duration = 0.1)
        
        pyautogui.press(
            "backspace", presses = 7, interval = 0.1
        )

        pyautogui.typewrite(
            str(np.round(self.M, 5)),
            interval = 0.1
        )

    def set_alpha(self):
        # set in window
        
        if self.alpha > 20 or self.alpha < -10:
            raise ValueError("Angle of attack must be between -20 and 20 degrees")
        
        pyautogui.click((
            self.alpha_input_loc
        ),  duration = 0.1)
        
        pyautogui.press(
            "backspace", presses = 8, interval = 0.1
        )

        pyautogui.typewrite(
            str(np.round(self.alpha, 5)),
            interval = 0.1
            )
    
    def set_Re(self):
        # TODO
        pass

    def click_run(self):

        pyautogui.click(self.run_loc, clicks=1, duration=0.1)

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

        # test that result converges

        for line in remote_file:

            # if line empty, skip
            if not line.strip():
                continue
            if "PROCEDURE HAS DIVERGED" in line:
                out = None
                break

            if "Upper surface CP values" in line:
                parsing_upper = True
                parsing_lower = False
                continue
            elif "Lower surface CP values" in line:
                parsing_upper = False
                parsing_lower = True
                continue

            # Parse variable if not within CP sections

            matches = variable_pattern.findall(line)
            for var, val in matches:
                    variables[var] = float(val) if '.' in val else int(val)

            # Parse upper surface CP data
            if parsing_upper:
                cp_match = cp_data_pattern.match(line)
                if cp_match:
                    x, cp = map(float, cp_match.groups())
                    upper_surface_cp.append((x, cp))

            # Parse lower surface CP data
            elif parsing_lower:
                cp_match = cp_data_pattern.match(line)
                if cp_match:
                    x, cp = map(float, cp_match.groups())
                    lower_surface_cp.append((x, cp))
        else:
            out = Result(variables, upper_surface_cp, lower_surface_cp)


        remote_file.close()
        sftp_client.close()

        self.save_result_locally(res)

        return out
    
    def save_result_locally(self, res):

        # add data to lookup
        try:
            lookup = np.loadtxt(f'data/{self.foil}_lookup.csv', delimiter=',')
        except FileNotFoundError:
            lookup = np.empty((0,4))
        
        if res is None:
            # must have been called by a run that immidietly failed
            # can use self
            lookup = np.append(lookup, [self.M, self.alpha, self.Re, 0])
        else:
            lookup = np.append(lookup, [res.M, res.alpha, res.Re, 1])

        np.savetxt(f'data/{self.foil}_lookup.csv', lookup)

        # save res class using pickle
        # TODO

    def load_result_locally(self, M, alpha, Re):
        # returns a result class
        # will load quite a big file so its best to check lookup before calling this
        # TODO load pickle file
        pass
        
    def check_result_saved(self, M, alpha, Re):
        # returns true or false if operating point is in lookup

        try:
            lookup = np.loadtxt(f'data/{self.foil}_lookup.csv', delimiter=',')
        except FileNotFoundError:
            return False
        
        for i in range(lookup.shape[0]):
            if (np.isclose(lookup[i, 0], M) and 
                np.isclose(lookup[i, 1], alpha) and 
                np.isclose(lookup[i, 2], Re)):
                return True
        
        return False        

class DPO_Session():

    def __init__(self, username, pwd):

        intermediate_hostname = 'gate.eng.cam.ac.uk'
        teaching_hostname = 'ts-access'

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

        self.teaching_client = teaching_client
        self.intermediate_client = intermediate_client
    
    def end(self):
        
        if hasattr(self, 'teaching_client'):
            self.teaching_client.close()
        if hasattr(self, 'intermediate_client'):
            self.intermediate_client.close()


def load_password(path):

    with open(path) as f:
        secrets = json.load(f)
        shifted_pwd = secrets['password']
    pwd = ''
    for s in shifted_pwd:
        pwd += chr(ord(s) - 1)

    return pwd

# Parsing flags

if __name__ == "__main__":

    try:
        window = gw.getWindowsWithTitle("millenicut:19")[0]
    except IndexError:
        raise Exception("Window not found")

    time.sleep(1)

    # Setup SSH
    absp = 'IIB/4A7/transonic_wing/secrets.json'
    pwd = load_password(absp)
    sesh = DPO_Session('lwp26', pwd)

    # Create the AirfoilApp
    App = AirfoilApp(sesh.teaching_client, window)

    alphas = np.linspace(0, 3, 5)
    cs = ['r', 'g', 'b', 'y', 'k']

    plt.gca().invert_yaxis()
    i = 0

    for alpha in alphas:
        res = App.run(0.75, alpha)
        if res is None:
            continue

        plt.plot(res.x_upper, res.cp_upper, label=f"$\\alpha$ = {res.Alpha}, M={res.M}", color=cs[i])
        plt.plot(res.x_lower, res.cp_lower, color=cs[i])

        i += 1

    plt.grid()
    plt.legend()
    plt.show()

    sesh.end()
    print("Session closed")
