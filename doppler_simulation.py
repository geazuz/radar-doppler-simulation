c = 3.0e8 # speed of light in m/s

carrier_f = 24.0e9 # radar carrier frequency (24 GHz)

target_velocity = 10.0 # targets radial veloicty (m/s)

wavelength = c / carrier_f # calculates wavelength 

doppler_f = (2 * target_velocity) / wavelength # calculates doppler frequency shift (radar doppler relationship)

print(f"Radar frequency: {carrier_f / 1e9:.1f} GHz")
print(f"Wavelength: {wavelength:.4f} m")
print(f"Target velocity: {target_velocity:.1f} m/s")
print(f"Doppler shift: {doppler_f:.2f} Hz")