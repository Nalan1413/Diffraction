# No Truce With The Furies
import numpy as np
import matplotlib.pyplot as plt


def single_slit(theta, wavelength, b, I0):
    A = I0 ** (1 / 2)
    displacement_x = np.linspace(-b / 2, b / 2, 1000)
    result_intensity = np.array([])
    for angle in theta:
        path_difference = displacement_x * np.sin(angle)
        phase_difference = 2 * np.pi / wavelength * path_difference
        A_f = np.sum(A * np.cos(phase_difference)) / len(displacement_x)
        I_f = A_f ** 2
        result_intensity = np.append(result_intensity, I_f)
    return result_intensity


def grading(theta, wavelength, b, I0, d, n):
    A = I0 ** (1 / 2)
    displacement_x = np.linspace(-b / 2, b / 2, 1000)
    result_intensity = np.zeros(len(theta))
    for a, angle in enumerate(theta):
        A_f = 0
        for k in range(0, n):
            path_difference = (k * d + displacement_x) * np.sin(angle)
            phase_difference = 2 * np.pi / wavelength * path_difference
            A_f_single = np.sum(A * np.cos(phase_difference)) / len(displacement_x)
            A_f += A_f_single
        I_f = (A_f / n) ** 2
        result_intensity[a] = I_f
    return result_intensity


def wavelength_to_rgb(wavelength):
    if 380 * 1e-9 <= wavelength < 440 * 1e-9:  # Violet to blue
        r = -(wavelength - 440 * 1e-9) / (440 * 1e-9 - 380 * 1e-9)
        g = 0.0
        b = 1.0
    elif 440 * 1e-9 <= wavelength < 490 * 1e-9:  # Blue to cyan
        r = 0.0
        g = (wavelength - 440 * 1e-9) / (490 * 1e-9 - 440 * 1e-9)
        b = 1.0
    elif 490 * 1e-9 <= wavelength < 510 * 1e-9:  # Cyan to green
        r = 0.0
        g = 1.0
        b = -(wavelength - 510 * 1e-9) / (510 * 1e-9 - 490 * 1e-9)
    elif 510 * 1e-9 <= wavelength < 580 * 1e-9:  # Green to yellow
        r = (wavelength - 510 * 1e-9) / (580 * 1e-9 - 510 * 1e-9)
        g = 1.0
        b = 0.0
    elif 580 * 1e-9 <= wavelength < 645 * 1e-9:  # Yellow to red
        r = 1.0
        g = -(wavelength - 645 * 1e-9) / (645 * 1e-9 - 580 * 1e-9)
        b = 0.0
    elif 645 * 1e-9 <= wavelength <= 780 * 1e-9:  # Red
        r = 1.0
        g = 0.0
        b = 0.0
    else:
        r = g = b = 0.0  # Wavelength outside visible range

    # Intensity adjustment for wavelengths outside 700-780 nm
    if wavelength > 700 * 1e-9:
        fac = 0.3 + 0.7 * (780 * 1e-9 - wavelength) / (780 * 1e-9 - 700 * 1e-9)
    elif wavelength < 420 * 1e-9:
        fac = 0.3 + 0.7 * (wavelength - 380 * 1e-9) / (420 * 1e-9 - 380 * 1e-9)
    else:
        fac = 1.0

    return r * fac, g * fac, b * fac


factor = 200
angle_min_lim = -0.001 * factor
angle_max_lim = 0.001 * factor
resolution = 100 * factor + 1
theta_angle = np.linspace(angle_max_lim, angle_min_lim, resolution)
screen_height = 1
image = np.zeros((screen_height, resolution, 3))
slit_width = 10 * 1e-6
intensity = 0.5
distance = 50 * 1e-6


light_dictionary = {
    'red': 650 * 1e-9,
    'orange': 600 * 1e-9,
    'yellow': 580 * 1e-9,
    'green': 550 * 1e-9,
    'cyan': 500 * 1e-9,
    'blue': 450 * 1e-9,
    'violet': 400 * 1e-9
}

plt.figure(figsize=(10, 6))
plt.title('Single-Slit Diffraction Pattern')
plt.xlabel(r'$\theta$ (radians)')
plt.ylabel('Intensity(W/m^2)')
plt.xlim([angle_min_lim, angle_max_lim])
plt.grid()

for j, (color, light_wave_length) in enumerate(light_dictionary.items()):
    if j != -1:
        Intensity = grading(theta_angle, light_wave_length, slit_width, intensity, distance, 50)
        plt.plot(theta_angle, Intensity, label=color, color=color)
        rgb_color = np.array(wavelength_to_rgb(light_wave_length))
        for i, I in enumerate(Intensity):
            image[:, i, :] += I * rgb_color

plt.legend()
image = image**0.5

plt.figure(figsize=(48, 6))
plt.imshow(image, extent=[angle_min_lim, angle_max_lim, 0, 1], aspect='auto')
plt.title("Single-Slit Diffraction on screen")
plt.xlabel(r"$\theta$ (radians)")
plt.ylabel("Screen Position (arbitrary)")

plt.show()
