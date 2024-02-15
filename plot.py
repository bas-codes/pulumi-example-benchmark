from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt
from pint import UnitRegistry

ureg = UnitRegistry()
ureg.define("MBps = 1 * megabyte / second")
ureg.define("KBps = 1 * kilobyte / second")


def graph_fio(FIO_RESULTS):
    with plt.xkcd():
        fig, ax = plt.subplots()
        ax.set_title(f"FIO report")
        ax.set_xlabel("RW Speed [MBps]")
        y_values = np.arange(len(FIO_RESULTS))
        ax.set_yticks(y_values + 0.2)
        ax.set_yticklabels(FIO_RESULTS.keys())

        n = len(FIO_RESULTS)

        ax.barh(
            y_values - 0.2 * 2,
            [fio[0].magnitude for fio in FIO_RESULTS.values()],
            height=0.2,
            label="0",
        )
        ax.barh(
            y_values - 0.2 * 1,
            [fio[1].magnitude for fio in FIO_RESULTS.values()],
            height=0.2,
            label="1",
        )
        ax.barh(
            y_values + 0.2 * 0,
            [fio[2].magnitude for fio in FIO_RESULTS.values()],
            height=0.2,
            label="2",
        )
        ax.barh(
            y_values + 0.2 * 1,
            [fio[3].magnitude for fio in FIO_RESULTS.values()],
            height=0.2,
            label="3",
        )

        ax.grid(False, axis="x")
        legend = ax.legend()
        plt.tight_layout()

        plt.show()

        return fig, ax


def show_plots(DATA):
    FIO_RESULTS = OrderedDict()
    for contestant, data in DATA.items():
        fios = data["fio"]
        fios_rw = [
            ureg(f'{fio["speed_rw"]} {fio["speed_units"]}').to("MBps") for fio in fios
        ]
        FIO_RESULTS[contestant] = fios_rw
    fig, ax = graph_fio(FIO_RESULTS)
    return fig, ax
