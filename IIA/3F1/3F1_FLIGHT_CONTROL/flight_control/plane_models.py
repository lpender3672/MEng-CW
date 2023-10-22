from scipy.signal import TransferFunction

F4E_FIGHTER_AIRCRAFT = {
    "operating_point_1": TransferFunction([185.3521, 163.8444], [1, 15.8408, 22.0034, -52.7495, 0]),
    "operating_point_2": TransferFunction([507.7712, 789.0659], [1, 17.12, 34.93, -122.5005, 0]),
    "operating_point_3": TransferFunction([158.3182, 101.8049], [1, 15.3257, 17.514, -14.6419, 0]),
    "operating_point_4": TransferFunction([304.2262, 251.4097], [1.0, 15.7412, 43.6008, 269.1355, 0.0]),
}

F4E_FIGHTER_AIRCRAFT_DESCRIPTIONS = {
    "operating_point_1": "Altitude: 5000ft. Mach 0.5",
    "operating_point_2": "Altitude: 5000ft. Mach 0.85",
    "operating_point_3": "Altitude: 35000ft. Mach 0.9",
    "operating_point_4": "Altitude: 35000ft. Mach 1.5",
}
