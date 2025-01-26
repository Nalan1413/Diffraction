import numpy as np
import scipy.signal as signal


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


def grading(theta, wavelength, b, I0, d, number_slits):
    A = I0 ** (1 / 2)
    displacement_x = np.linspace(-b / 2, b / 2, 1000)
    result_intensity = np.zeros(len(theta))
    for a, angle in enumerate(theta):
        A_f = 0
        for n in range(0, number_slits):
            path_difference = (n * d + displacement_x) * np.sin(angle)
            phase_difference = 2 * np.pi / wavelength * path_difference
            A_f_single = np.sum(A * np.cos(phase_difference)) / len(displacement_x)
            A_f += A_f_single
        I_f = (A_f / number_slits) ** 2
        result_intensity[a] = I_f
    return result_intensity


# Settings --------
factor = 50
angle_min_lim = -0.001 * factor
angle_max_lim = 0.001 * factor
resolution = 100 * factor + 1
theta_angle = np.linspace(angle_max_lim, angle_min_lim, resolution)
screen_height = 1
image = np.zeros((screen_height, resolution, 3))
slit_width = 10 * 1e-6
intensity = 0.5
distance = [50 * 1e-6, 60 * 1e-6, 70 * 1e-6, 80 * 1e-6, 90 * 1e-6]

light_dictionary = {
    'red': 650 * 1e-9,
    'orange': 600 * 1e-9,
    'yellow': 580 * 1e-9,
    'green': 550 * 1e-9,
    'cyan': 500 * 1e-9,
    'blue': 450 * 1e-9,
    'violet': 400 * 1e-9
}

# End of Settings --------

peak_dic = {
    'red': [[], [], [], []],
    'orange': [[], [], [], []],
    'yellow': [[], [], [], []],
    'green': [[], [], [], []],
    'cyan': [[], [], [], []],
    'blue': [[], [], [], []],
    'violet': [[], [], [], []]
}

for dis in distance:
    for j, (color, light_wave_length) in enumerate(light_dictionary.items()):
        Intensity = grading(theta_angle, light_wave_length, slit_width, intensity, dis, 50)
        peaks, _ = signal.find_peaks(Intensity)
        top_4_peak_indices = sorted(peaks, key=lambda x: Intensity[x], reverse=True)[:7]
        top_4_peak_indices = sorted(top_4_peak_indices, key=lambda x: theta_angle[x], reverse=True)[:4]

        for i, peak_value in enumerate(top_4_peak_indices):
            rounded_value = round(theta_angle[peak_value], 10)
            peak_dic[color][3 - i].append(rounded_value)

print(peak_dic)
