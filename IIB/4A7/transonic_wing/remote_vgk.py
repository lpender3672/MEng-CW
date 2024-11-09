
import json
import os
import paramiko
import pyautogui
import pygetwindow as gw
import time
import re
from matplotlib import pyplot as plt
import numpy as np
import pickle

from parse import (
    extract_single_value_variables, 
    extract_shock_locations, 
    extract_boundary_layer_data_at_x, 
    check_converged, 
    load_surface_data
    )


class Result():
    def __init__(self, variables, surface_data, boundary_layer_data, shock_locations):

        self.CD2 = variables['CDV+CD2'] - variables['CDV']
        self.Cd = variables['CDV+CD2']
        self.Cl = variables['CL']
        self.alpha = variables['ALP']
        self.M = variables['EM']
        self.Re = variables['R'] * 100

        self.x = surface_data[:, 1]
        self.z = surface_data[:, 2]
        self.cp = surface_data[:, 3]
        self.boundary_layer_data = boundary_layer_data
        self.shock_locations = shock_locations

        self.cpte = self.cp[self.x == 1.0][0]
        self.Hbar = boundary_layer_data['HBAR']

        self.buffeting = False
        self.buffet_causes = []

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

        self.mach_input_loc = (x + 90, y + h * 0.776)
        self.alpha_input_loc = (x + 190, y + h * 0.776)
        self.reynolds_input_loc = (x + 290, y + h * 0.776)
        self.run_loc = (x + w * 0.75, y + h * 0.9)

        

    def run(self, M, alpha, Re):

        if self.check_result_saved(M, alpha, Re):
            return self.load_result_local(M, alpha, Re)

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

        return self.load_result_remote()

    def set_M(self):
        # set in window
        if self.M > 0.95 or self.M < 0.05:
            raise ValueError("Mach number must be between 0.05 and 0.95")
        
        for i in range(2):

            pyautogui.click((
                self.mach_input_loc
            ), duration = 0.1)
            
            pyautogui.press(
                "backspace", presses = 5, interval = 0.1
            )

        pyautogui.typewrite(
            str(np.round(self.M * 1e5))[:5],
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
        # set in window
        if self.Re > 50 or self.Re < 1:
            raise ValueError("Reynolds number must be between 1 and 50 million")
        
        pyautogui.click((
            self.reynolds_input_loc
        ), duration = 0.1)
        
        pyautogui.press(
            "backspace", presses = 8, interval = 0.1
        )

        pyautogui.typewrite(
            str(np.round(self.Re, 5)),
            interval = 0.1
        )

    def click_run(self):

        pyautogui.click(self.run_loc, clicks=1, duration=0.1)

    def load_result_remote(self):
        
        sftp_client = self.ssh_client.open_sftp()
        remote_file = sftp_client.open('Airfoil-hb/Autorun.BRF')

        #file_path = 'IIB/4A7/transonic_wing/Autorun.FUL'
        with sftp_client.open('Airfoil-hb/Autorun.FUL') as remote_file:
            content = remote_file.read().decode()

        if check_converged(content):
            
            variables = extract_single_value_variables(content)
            #print(variables)
            shock_locations = extract_shock_locations(content)
            #print(shock_locations)
            boundary_layer_data = extract_boundary_layer_data_at_x(content, 1.0)
            #print(boundary_layer_data)
            surface_data = load_surface_data(content)
            #print(surface_data)

            out = Result(variables, surface_data, boundary_layer_data, shock_locations)

        else:
            out = None

        # end sesh
        remote_file.close()
        sftp_client.close()

        self.save_result_locally(out)

        return out
    
    def save_result_locally(self, res):

        # add data to lookup
        try:
            lookup = np.loadtxt(f'data/lookup_{self.foil}.csv', delimiter=',')
        except FileNotFoundError:
            lookup = np.empty((0,4))
        
        if res is None:
            # must have been called by a run that immidietly failed
            # can use self
            newrow = np.array([[self.M, self.alpha, self.Re, 0]])
        else:
            newrow = np.array([[res.M, res.alpha, res.Re, 1]])

        lookup = np.vstack((lookup, newrow))

        np.savetxt(f'data/lookup_{self.foil}.csv', lookup, delimiter=',')

        if res is None:
            # dont add to pickle if run failed, its already in lookup as a fail
            return

        try:
            with open(f'data/db_{self.foil}.pkl', "rb") as file:
                loaded_objects = pickle.load(file)
        except FileNotFoundError:
            loaded_objects = []

        loaded_objects.append(res)

        with open(f'data/db_{self.foil}.pkl', "wb") as file:
            pickle.dump(loaded_objects, file)

    def load_result_local(self, M, alpha, Re):
        # returns a result class
        # will load quite a big file so its best to check lookup before calling this
        # TODO load pickle file
        try:
            with open(f'data/db_{self.foil}.pkl', "rb") as file:
                loaded_objects = pickle.load(file)
        except FileNotFoundError:
            print("Warning: pickle file not found")
            return None
        
        tol = 1e-4
        for obj in loaded_objects:
            if (np.isclose(obj.M, M, atol = tol) and 
                np.isclose(obj.alpha, alpha, atol = tol) and 
                np.isclose(obj.Re, Re, atol = tol)):
                return obj
        
    def cpte_alpha(self, M, Re):
        # get a list of cp vs alpha for a given M and Re
        try:
            with open(f'data/db_{self.foil}.pkl', "rb") as file:
                loaded_objects = pickle.load(file)
        except FileNotFoundError:
            print("Warning: pickle file not found")
            return None
        
        alphas = np.empty(0)
        cps = np.empty(0)
        
        tol = 1e-4
        for obj in loaded_objects:
            if (np.isclose(obj.M, M, atol = tol) and 
                np.isclose(obj.Re, Re, atol = tol)):
                alphas = np.append(alphas, obj.alpha)
                cps = np.append(cps, obj.cpte)

        # sort by alpha
        idx = np.argsort(alphas)
        alphas = alphas[idx]
        cps = cps[idx]

        return alphas, cps

    def cpte_M(self, alpha, Re):
        # get a list of cp vs M for a given alpha and Re
        try:
            with open(f'data/db_{self.foil}.pkl', "rb") as file:
                loaded_objects = pickle.load(file)
        except FileNotFoundError:
            print("Warning: pickle file not found")
            return None
        
        Ms = np.empty(0)
        cps = np.empty(0)
        
        tol = 1e-4
        for obj in loaded_objects:
            if (np.isclose(obj.alpha, alpha, atol = tol) and 
                np.isclose(obj.Re, Re, atol = tol)):
                Ms = np.append(Ms, obj.M)
                cps = np.append(cps, obj.cpte)

        # sort by M
        idx = np.argsort(Ms)
        Ms = Ms[idx]
        cps = cps[idx]

        return Ms, cps
    
    def check_result_saved(self, M, alpha, Re):
        # returns true or false if operating point is in lookup

        try:
            lookup = np.loadtxt(f'data/lookup_{self.foil}.csv', delimiter=',', ndmin=2)
        except FileNotFoundError:
            print("Warning: lookup file not found")
            return False
        
        tol = 1e-4
        for i in range(lookup.shape[0]):
            if (np.isclose(lookup[i, 0], M, atol = tol) and 
                np.isclose(lookup[i, 1], alpha, atol = tol) and 
                np.isclose(lookup[i, 2], Re, atol = tol)):
                return True
        
        return False
    
    def delete_result(self, M, alpha, Re):
        # delete a result from the pickle
        try:
            with open(f'data/db_{self.foil}.pkl', "rb") as file:
                loaded_objects = pickle.load(file)
        except FileNotFoundError:
            print("Warning: pickle file not found")
            return None
        
        tol = 1e-4
        for i in range(len(loaded_objects)):
            if (np.isclose(loaded_objects[i].M, M, atol = tol) and 
                np.isclose(loaded_objects[i].alpha, alpha, atol = tol) and 
                np.isclose(loaded_objects[i].Re, Re, atol = tol)):
                del loaded_objects[i]
                break
        
        with open(f'data/db_{self.foil}.pkl', "wb") as file:
            pickle.dump(loaded_objects, file)

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

        plt.plot(res.x, res.cp, label=f"$\\alpha$ = {res.alpha}, M={res.M}", color=cs[i])

        i += 1

    plt.grid()
    plt.legend()
    plt.show()

    sesh.end()
    print("Session closed")
