from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path

import matplotlib
import flet as ft
from flet.matplotlib_chart import MatplotlibChart

from core import approximation, count_files_in_dir

matplotlib.use("svg")
BASE_PATH = Path(__file__).parent

def main(page: ft.Page):
    page.title = "Approximation"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width = 600
    page.window.height = 800
    page.window.min_width = 600
    page.window.min_height = 800
    page.theme_mode = 'light'

    def open_file(e):
        filepath = filedialog.askopenfilename()
        try:
            int(start.value), int(stop.value), int(step.value)
        except Exception as e:
            messagebox.showinfo('Внимание!', 'Не правильно введены данные')
            return
        if thickness.value == '':
            thickness.value = 0
        if material.value != '' and filepath != '':
            fig, fig_mu = approximation(
                filepath,
                material.value,
                int(start.value),
                int(stop.value),
                int(step.value),
                int(thickness.value)
            )
            page.add(MatplotlibChart(fig, expand=True))
            count_files = count_files_in_dir(BASE_PATH / 'image_graph/')
            if fig_mu is not None:
                page.add(MatplotlibChart(fig_mu, expand=True))
                fig_mu.savefig(BASE_PATH / f'image_graph/graph-2light-{count_files + 1}.png')
            fig.savefig(BASE_PATH / f'image_graph/graph-approx-{count_files + 1}.png')
        elif filepath == '':
            messagebox.showinfo('Внимание!','Не выбран файл')
            return
        else:
            messagebox.showinfo('Внимание!', 'Полле ввода пустое')
            return

    def clear_graphs(e):
        page.clean()
        page.update()
        page.add(
        btn_open_file,
        btn_clear,
        material,
        start,
        stop,
        step,
        thickness,
        )

    material = ft.TextField(label='Название материала')
    start = ft.TextField(label='От начала значения длины волн')
    stop = ft.TextField(label='До конца значения длины волны')
    step = ft.TextField(label='Шаг')
    thickness = ft.TextField(label='Толщина пластинки')

    btn_clear = ft.ElevatedButton(content=ft.Column(
                    [ft.Icon(name=ft.Icons.DELETE)],
                    alignment=ft.MainAxisAlignment.CENTER),
                    on_click=clear_graphs, width=100, height=50)
    btn_open_file = ft.ElevatedButton(text="Открыть файл", on_click=open_file, width=250, height=250,)

    page.add(
        btn_open_file,
        btn_clear,
        material,
        start,
        stop,
        step,
        thickness,
    )

if __name__ == '__main__':
    ft.app(main)