"""
Create ICMP Heatmap Plot.

This Python file creates an ICMP heatmap plot by logging into each device and sending
pings to all the other devices.

All devices should be listed in the 'device_list.yml' file. IP addresses are FQDNs are allowed.
The plot created will use the information provided in the 'device_list.yml' file to build its
rows and columns.

"""

import sys
import napalm
import yaml
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from napalm.base.exceptions import ConnectionClosedException, ConnectionException


def main():
    """Program entry point."""
    with open(r"device_list.yml", encoding="utf8") as file:
        device_list = yaml.safe_load(file)
    # Use the appropriate network driver to connect to the device:
    driver = napalm.get_network_driver("ios")

    # Check to make sure we can connect to all devices in the device list. If unable to connect,
    # the device is removed from the list.

    # NOTE: It is not secure to put real device credentials in code. It is recommended to
    # use a password vault for production devices.

    for device in device_list:
        device_drv = driver(
            hostname=device,
            username="cisco",
            password="cisco",
            timeout=60,
            optional_args={"secret": "cisco"},
        )
        try:
            print(f"Verifying connection to {device}")
            device_drv.open()
        except ConnectionException:
            print(f"Unable to connect to {device}. Removing from list.")
            device_list.remove(device)

    print(device_list)

    grid_data = np.array([])

    for device in device_list:
        device_drv = driver(
            hostname=device,
            username="cisco",
            password="cisco",
            timeout=60,
            optional_args={"secret": "cisco", "global_delay_factor": 2},
        )

        print(f"Initiating tests from {device}")

        # connect to device
        device_drv.open()

        for device2 in device_list:
            try:
                ping_results = device_drv.ping(
                    device2, timeout=1, count=10, source_interface="Loopback0"
                )
                if "success" in ping_results:
                    avg_response = ping_results["success"]["rtt_avg"]
                    print(avg_response)
                    if avg_response == 0.0:
                        grid_data = np.append(grid_data, 9999)
                    else:
                        grid_data = np.append(grid_data, avg_response)
                else:
                    print(f"Cannot ping {device2} from {device}")
                    grid_data = np.append(grid_data, np.nan)
            except ConnectionClosedException as e:
                print(f"Error: {e}")
                print(
                    "Ping command took too long....Need to exit program to prevent data "
                    "alignment error....."
                )
                sys.exit()

    print(grid_data)
    num_devices = len(device_list)

    # reshape array by num_devices x num_devices
    grid_data = np.reshape(grid_data, (num_devices, num_devices))
    print(grid_data)

    # apply default seaborn theme
    sns.set_theme()

    # Create a dataset
    df = pd.DataFrame(grid_data, index=device_list, columns=device_list)
    print(df)

    # save pandas DF to CSV
    df.to_csv("output.csv")

    # Set up plot

    plt.figure(figsize=(35, 30), edgecolor="black")
    plt.rcParams["xtick.bottom"] = plt.rcParams["xtick.labelbottom"] = False
    plt.rcParams["xtick.top"] = plt.rcParams["xtick.labeltop"] = True

    sns.set_context("paper", font_scale=4.0)

    # cmap found here: https://matplotlib.org/stable/tutorials/colors/colormaps.html
    ax = sns.heatmap(
        df,
        annot=True,
        cmap="Blues",
        linewidths=0,
        vmin=0,
        vmax=300,
        fmt="g",
        cbar=True,
        square=True,
        annot_kws={"fontsize": 30, "color": "black", "visible": True},
    )

    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    ax.set_yticklabels(ax.get_xticklabels(), rotation=0)

    plt.savefig("output.png")
    plt.show()


if __name__ == "__main__":
    main()
