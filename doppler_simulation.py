import numpy as np
import matplotlib.pyplot as plt

def calculate_received_power(target_range): 
    received_power = (Pt * antenna_gain**2 * wavelength**2 * sigma) / ((4*np.pi)**3 * target_range**4 * system_losses)
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

# L 
system_losses = 1


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
