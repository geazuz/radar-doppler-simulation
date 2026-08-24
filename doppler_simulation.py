import numpy as np
import matplotlib.pyplot as plt

plt.style.use("dark_background")

c = 3.0e8 # speed of light in m/s

carrier_f = 24.0e9 # radar carrier frequency (24 GHz)

target_velocity = 10.0 # targets radial veloicty (m/s)

wavelength = c / carrier_f # calculates wavelength 

doppler_f = (2 * target_velocity) / wavelength # calculates doppler frequency shift (radar doppler relationship)
# = fd

print(f"Radar frequency: {carrier_f / 1e9:.1f} GHz")
print(f"Wavelength: {wavelength:.4f} m")
print(f"Target velocity: {target_velocity:.1f} m/s")
print(f"Doppler shift: {doppler_f:.2f} Hz")

# singal sampling parameters
sample_rate = 20_000 # 20,000 samples/sec

duration = 0.01 # units = seconds 

# starts at 0 seconds, stops at 0.01 seconds, and creates a point every 1/20,000 seconds
time = np.arange(0, duration, 1/ sample_rate) # creates an array of time samples, 1/20,000 = 0.00005 s

# evaluates the x(t) function
doppler_signal = np.sin(2 * np.pi * doppler_f * time) # generates simulated doppler return, x(t)=sin(2pifd*t)

plt.plot(time, doppler_signal) # plots the created simulated signal

plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("Simulated Doppler Radar Return")

plt.grid()
plt.show()