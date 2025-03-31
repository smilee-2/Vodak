from typing import Any, List

from matplotlib import pyplot as plt
import numpy as np



def polynomial_model(wavelength: int, a: float, b: float, c: float) -> float:
    #N=A+B/λ²+C/λ^4
    return a + (b / wavelength ** 2) + (c / wavelength ** 4)


def plot_graph(data_pol_in_file:list, data_calc: list, wavelengths_int: list, wavelengths: list, name:str):
    fig, axs = plt.subplots(1, 1)
    axs.scatter(wavelengths, data_pol_in_file, label='Исходные данные', color='blue', s=150)
    axs.scatter(wavelengths_int, data_calc, label='Апроксимация полинома', color='red')
    axs.set_xlabel('Длина волны (angstroms)')
    axs.set_ylabel('Фазовый сдвиг')
    axs.set_title(f'{name}\nПолиномиальная апроксимация')
    axs.legend()
    axs.grid(True)
    fig.tight_layout()
    return fig


def calculate_sums_from_file(file):
    sum_l = 0
    sum_l_2 = 0
    sum_l_3 = 0
    sum_l_4 = 0
    sum_l_2_n = 0
    sum_l_n = 0
    n_sum = 0
    wavelengths = []
    with open(f'{file}', 'r', encoding='utf-8') as file:
        for line in file:
            if line == '\n':
                continue
            data: List[Any] = line.split()

            data[1] = data[1].replace(',', '.')
            data[0] = int(data[0])
            data[1] = float(data[1])

            wavelengths.append(data[0])

            sum_l += 1 / (data[0] ** 2)
            sum_l_2 += (1 / (data[0] ** 2)) ** 2
            sum_l_3 += (1 / (data[0] ** 2)) ** 3
            sum_l_4 += (1 / (data[0] ** 2)) ** 4

            temp_1 = (1 / (data[0] ** 2)) ** 2
            temp_2 = 1 / (data[0] ** 2)

            sum_l_2_n += data[1] * temp_1
            sum_l_n += data[1] * temp_2
            n_sum += data[1]

    temp_arr = np.array([sum_l_2_n, sum_l_n, n_sum])

    return [
            [sum_l_4, sum_l_3, sum_l_2],
            [sum_l_3, sum_l_2, sum_l],
            [sum_l_2, sum_l, 8]
        ], temp_arr, wavelengths

def calculated_interpolation(file, final_mat, start, stop, step):

    with open(file, 'r') as f:
        data_pol_in_file = []
        for wave in f:
            wavelength = int(wave.split()[0])
            data_pol_in_file.append(polynomial_model(wavelength, final_mat[2], final_mat[1], final_mat[0]))

    with open('N-интерполяция.txt', 'w') as f:
        int_l = start
        data_interp = []
        wave_range = []
        while int_l <= stop:
            val = polynomial_model(int_l, final_mat[2], final_mat[1], final_mat[0])
            data_interp.append(val)
            f.writelines(f'{int_l}\t{val}\n')
            wave_range.append(int_l)
            int_l += step

    return data_pol_in_file, data_interp, wave_range

def approximation(file, name, start, stop, step):

        matrix, temp_arr, wavelengths = calculate_sums_from_file(file)

        result = np.linalg.inv(matrix)
        final_mat = np.dot(result, temp_arr)
        data_pol_in_file, data_interp, wave_range = calculated_interpolation(file,final_mat, start, stop, step)


        fig = plot_graph(data_pol_in_file, data_interp, wave_range, wavelengths, name)
        return fig
