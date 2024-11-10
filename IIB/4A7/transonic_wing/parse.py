

import re
import numpy as np
import json

def check_converged(content):

    for line in content.splitlines():
        if "ITERATIVE PROCEDURE HAS DIVERGED" in line:
            return False

    return True

def extract_single_value_variables(content):
    single_value_vars = {}

    # regex is horrible
    pattern = re.compile(r"([\w\+]+)\s*=\s*([-+]?\d*\.?\d+|\d+)")

    matches = pattern.findall(content)

    for key, value in matches:
        single_value_vars[key] = float(value) if '.' in value else int(value)

    return single_value_vars

def extract_shock_locations(content):
    upper_shock_locations = []
    lower_shock_locations = []

    upper_shock_pattern = re.compile(r"SHOCK NO\.\s+\d+\s+ON UPPER SURFACE\.\s+X\(SHOCK\)=\s*([-+]?\d*\.?\d+)")
    lower_shock_pattern = re.compile(r"SHOCK NO\.\s+\d+\s+ON LOWER SURFACE\.\s+X\(SHOCK\)=\s*([-+]?\d*\.?\d+)")

    upper_shocks = upper_shock_pattern.findall(content)
    lower_shocks = lower_shock_pattern.findall(content)

    upper_shock_locations = [float(x) for x in upper_shocks]
    lower_shock_locations = [float(x) for x in lower_shocks]

    return {
        'upper_shock_locations': upper_shock_locations,
        'lower_shock_locations': lower_shock_locations
    }


def extract_boundary_layer_data_at_x(content, x_value=1.0):
    boundary_layer_data = {}

    # terrible but it works
    x_str = f"{x_value:.5f}"

    check = False

    for line in content.splitlines():
        line = line.strip()
        if "UPPER-SURFACE BOUNDARY-LAYER DATA" in line:
            check = True
            continue
        elif "LOWER-SURFACE BOUNDARY-LAYER DATA" in line:
            check = False
            break
        if check and line.strip().startswith(x_str):
            parts = line.split()
            if len(parts) >= 5:
                boundary_layer_data = {
                    "X": float(parts[0]),
                    "HBAR": float(parts[1]),
                    "DELSTAR": float(parts[2]),
                    "THETA": float(parts[3]),
                    "CFLOC": float(parts[4])
                }
            if len(parts) >= 6:
                # "DELTA": float(parts[5])
                boundary_layer_data["DELTA"] = float(parts[5])
            break

    return boundary_layer_data


def load_surface_data(content):
    data = []

    data_pattern = re.compile(
        r"^\s*([-+]?\d*\.?\d+)\s+([-+]?\d*\.?\d+)\s+([-+]?\d*\.?\d+)\s+([-+]?\d*\.?\d+)\s+([-+]?\d*\.?\d+)\s+([-+]?\d*\.?\d+)\s*$"
    )

    for line in content.splitlines():
        line = line.strip()
        match = data_pattern.match(line)
        if match:
            data.append([float(value) for value in match.groups()])

    data_array = np.array(data)

    return data_array


if __name__ == "__main__":

    from remote_vgk import DPO_Session
    def load_password(path):

        with open(path) as f:
            secrets = json.load(f)
            shifted_pwd = secrets['password']
        pwd = ''
        for s in shifted_pwd:
            pwd += chr(ord(s) - 1)
        return pwd
    pwd = load_password('IIB/4A7/transonic_wing/secrets.json')
    sesh = DPO_Session('lwp26', pwd)

    sftp_client = sesh.teaching_client.open_sftp()
    remote_file = sftp_client.open('Airfoil-hb/Autorun.FUL')

    #file_path = 'IIB/4A7/transonic_wing/Autorun.FUL'
    with sftp_client.open('Airfoil-hb/Autorun.FUL') as remote_file:
        content = remote_file.read().decode()

    if not check_converged(content):
        print("Simulation did not converge")

    variables = extract_single_value_variables(content)
    print(variables)
    shock_locations = extract_shock_locations(content)
    print(shock_locations)
    boundary_layer_data = extract_boundary_layer_data_at_x(content, 1.0)
    print(boundary_layer_data)
    surface_data = load_surface_data(content)
    print(surface_data)


    # end sesh
    remote_file.close()
    sftp_client.close()
    sesh.end()