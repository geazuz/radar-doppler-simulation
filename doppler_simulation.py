import numpy as np
import matplotlib.pyplot as plt

def calculate_atm_loss(target_range): 
    # added atmospheric attenuation to the radar-equation part of sim

    range_km = target_range / 1000 # convert target (R) to km

    to_target_and_back_distance = 2 * range_km # radar travels to target and back 

    total_atm_attenuation = attenuation_val * to_target_and_back_distance # total atmospherica loss in dB

    atm_loss_linear = 10**(total_atm_attenuation / 10) # convert dB to a linear power-loss factor = Latm
    return atm_loss_linear

def calculate_received_power(target_range, atm_loss_linear=1): 
    received_power = (Pt * antenna_gain**2 * wavelength**2 * sigma) / ((4*np.pi)**3 * target_range**4 * system_losses * atm_loss_linear)
    return received_power


plt.style.use("dark_background")

# Constants & Parameters

c = 3.0e8 # speed of light in m/s

carrier_f = 24.0e9 # radar carrier frequency (24 GHz)

target_velocity = 11.3 # targets radial veloicty (m/s)

wavelength = c / carrier_f # calculates wavelength 

doppler_f = (2 * target_velocity) / wavelength # calculates doppler frequency shift (radar doppler relationship), true doppler frequency
# = fd

# transmit power (W)
Pt = 1

# Gain (G) 
antenna_gain = 10

# Radar cross section (RCS) (m^2)
sigma = 1 

# L (system)
system_losses = 1

attenuation_val = 0.1 # dB/km


print(f"Radar frequency: {carrier_f / 1e9:.1f} GHz")
print(f"Wavelength: {wavelength:.4f} m")
print(f"Target velocity: {target_velocity:.2f} m/s")
print(f"Doppler shift: {doppler_f:.2f} Hz")

# singal sampling parameters
sample_rate = 20_000 # 20,000 samples/sec (fs)

duration = 0.1 # units = seconds (T) 

# starts at 0 seconds, stops at 0.01 seconds, and creates a point every 1/20,000 seconds
time = np.arange(0, duration, 1/ sample_rate) # creates an array of time samples, 1/20,000 = 0.00005 s

# evaluates the x(t) function
doppler_signal = np.sin(2 * np.pi * doppler_f * time) # generates simulated doppler return, x(t)=sin(2pifd*t)

# mean, standard deviation, number of values
noise = np.random.normal(0, 0.5, len(time)) 

noisy_signal = doppler_signal + noise 

# 1. computing doppler_signals FFT -- 
    # the FFT
fft_output = np.fft.rfft(noisy_signal) 

    # asks python "how many samples are actually in this signal?"
number_of_samples_N = len(noisy_signal) # tried number_of_samples_N = sample_rate * duration first = 20,000 * 0.01 = 200

    # delta_f 
frequency_resolution = sample_rate / number_of_samples_N

# 2. Creating corresponding array of frequency bins --  

    # requires N, & d = time between samples, tells us where each frequency is
frequency_bins = np.fft.rfftfreq(number_of_samples_N, d=1/sample_rate)

# 3. determining which frequency ahs the largest FFT Magnitude -- 

    # "how strong is this frequency component?" tells how strong each frequency is
FFT_magnitude = np.abs(fft_output)

    # determine which index in FFT_magnitude contains the largest values
MAX_magnitude_index = np.argmax(FFT_magnitude)

# 4. The detected doppler frequency
    #
detected_frequency = frequency_bins[MAX_magnitude_index]

# 5. Estimating target velocity 
    #  
estimated_velocity = (detected_frequency * wavelength) / 2

# 6. Prints both the known velocity and esitmated velocity 
print(number_of_samples_N)
print(frequency_resolution)
print(frequency_bins[:20])
print(f"Frequency FFT bin: {MAX_magnitude_index} ")
print(f"FFT Estimate: {detected_frequency} Hz")
print(f"Estimated Velocity: {estimated_velocity:.2f} m/s")

plt.plot(time, doppler_signal) # plots the created simulated signal
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("Simulated Doppler Radar Return")
# plt.grid()
plt.show()

# 7. Plot FFT Magnitude vs. Frequency
plt.plot(frequency_bins, FFT_magnitude)
plt.xlabel("Frequency")
plt.ylabel("FFT Magnitude")
plt.title("FFT Magnitude vs. Frequency")
plt.show()

absolute_error = abs(target_velocity - estimated_velocity)

percent_error = (absolute_error / (abs(target_velocity))) * 100 

print(f"Absolute Error = {absolute_error: .2f} m/s")
print(f"Percent Error = {percent_error: .3f}%")

# R (m)
# target_range = 100 
# received_power = (Pt * antenna_gain**2 * wavelength**2 * sigma) / ((4*np.pi)**3 * target_range**4 * system_losses)

# print(f"Received Power = {received_power: .3e} W")

received_power_100m = calculate_received_power(100)
print(f"received_power_100m = {received_power_100m: .3e} W")

# R (m)
# target_range = 200 
# received_power = (Pt * antenna_gain**2 * wavelength**2 * sigma) / ((4*np.pi)**3 * target_range**4 * system_losses)

received_power_200m = calculate_received_power(200)
print(f"received power at 200m = {received_power_200m: .3e} W")

# physics lesson here, doubling the range reduced the received power by 16x (didn't merely make the received signal a "little weaker")
ratio_of_recieved_power = received_power_100m / received_power_200m
print(f"Power Ratio = {ratio_of_recieved_power: .3e}")


target_ranges = np.arange(10, 510, 10) # (start, stop, step) can't start a zero since it would be 1/inf due to R^-4
# print(target_ranges)

multiple_received_power = calculate_received_power(target_ranges) 

# Received Power (Pr) is proportional too 1/R^4 or R^-4
plt.plot(target_ranges, multiple_received_power)
plt.xlabel("Range (m)")
plt.xscale("log")
plt.ylabel("Received Power (W)")
plt.yscale("log")
plt.title("1/R^4 Falloff Visualization")
plt.show()

atm_loss_5km = calculate_atm_loss(5000) # target range = 5km 

power_no_atm = calculate_received_power(5000, 1) # Latm = 1 (no-atmosphere case)

power_w_atm = calculate_received_power(5000, atm_loss_5km) 

P_ratio = power_no_atm / power_w_atm 

print(f"Atmopshere Loss = {atm_loss_5km: .3f}")
print(f"No Atmopshere Loss Case = {power_no_atm: .3e} W")
print(f"Received Power with Atmopshere Loss = {power_w_atm: .3e} W")
print(f"Received Power Ratio with both losses = {P_ratio: .3e}")
