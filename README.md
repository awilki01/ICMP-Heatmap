# ICMP-Heatmap
Create ICMP Heatmap

The Python file 'create_plot.py' creates an ICMP heatmap plot by logging into each device in the 'device_list.yml' file and sending
pings to all the other devices in the file. It creates a PNG image file and CSV file of the data. The CSV file can be imported into other tools e.g. Microsoft Excel to display data.

IP addresses and FQDNs (or short names that are resolvable from the machine running the Python script) within the 'device_list.yml' file are allowed.

The plot created will use the information provided in the 'device_list.yml' file to build its rows and columns headers.

The current username/password for the devices is set to cisco/cisco within the 'create_plot.py' script. It is not recommended to hardcode username and passwords in code within production environments. Please use a secure vault to store production credentials!

The script is set to run on IOS-XE based devices, but it can be easily modified to run on any platform that the NAPALM library supports.

Please first test on non-production devices prior to using in production. Use at your own risk.
