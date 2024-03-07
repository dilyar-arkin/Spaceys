import numpy as np

#sensor data
temperature_readings = [20.1, 22.5, 19.8, 21.2, 20.0] 
pressure_readings = [1001.2, 1003.5, 1000.8, 1002.1, 1001.0]

#reference measurements
reference_temperature = [19.8, 21.0, 19.5, 20.8, 19.7]
reference_pressure = [1000.5, 1002.0, 1000.0, 1001.8, 1000.7]

#calibration parameters
temperature_correction = np.mean(reference_temperature) - np.mean(temperature_readings)
pressure_correction = np.mean(reference_pressure) - np.mean(pressure_readings)

calibrated_temperature = [temp + temperature_correction for temp in temperature_readings]
calibrated_pressure = [pressure + pressure_correction for pressure in pressure_readings]

print("Temperature Correction:", temperature_correction, "°C")
print("Pressure Correction:", pressure_correction, "hPa")

#post- flight analysis
temperature_error = np.mean(np.abs(calibrated_temperature - reference_temperature))
pressure_error = np.mean(np.abs(calibrated_pressure - reference_pressure))

print("Temperature Error:", temperature_error, "°C")
print("Pressure Error:", pressure_error, "hPa")