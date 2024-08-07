import pandas as pd
import re
import plotly.express as px

# Read the file content
file_path = './logs/combined.txt'  # Change accordingly
with open(file_path, 'r') as file:
    lines = file.readlines()
    # print(lines)

# Initialize lists to store the extracted data
temperatures = []
bus_voltages = []
currents = []
timestamps = []

# Regular expressions to match each data type
temp_pattern = re.compile(r'Temperature:\s+([\d.]+)\s*C')
volt_pattern = re.compile(r'Bus Voltage:\s+([\d.]+)\s*V')
current_pattern = re.compile(r'Current:\s+(-?[\d.]+)\s*(mA|A)')

# Extract the data
for i in range(0, len(lines), 4):  # Step by 4 lines
    if i < len(lines)-3:
        temp_match = temp_pattern.search(lines[i])
        volt_match = volt_pattern.search(lines[i + 1])
        current_match = current_pattern.search(lines[i + 2])
    
    if temp_match and volt_match and current_match:
        temperatures.append(float(temp_match.group(1)))
        bus_voltages.append(float(volt_match.group(1)))
        current_value = float(current_match.group(1))
        if current_match.group(2) == 'A':
            current_value *= 1000  # Convert A to mA if needed
        currents.append(current_value)
        timestamps.append(i // 4)  # Using block number as a proxy for time (since every block = 1s gone)

# Create a DataFrame
df = pd.DataFrame({
    'Time (s)': timestamps,
    'Temperature (C)': temperatures,
    'Bus Voltage (V)': bus_voltages,
    'Current (mA)': currents
})

# This groups the time into 1-minute intervals by dividing the time in seconds by 60 and converting the result to integers.
df['Time (1min interval)'] = (df['Time (s)'] // 60).astype(int)

# Filter out extreme values for temperature and current
temperature_filtered = df[(df['Temperature (C)'] < df['Temperature (C)'].quantile(0.99)) &
                          (df['Temperature (C)'] > df['Temperature (C)'].quantile(0.01))]

current_filtered = df[(df['Current (mA)'] < df['Current (mA)'].quantile(0.99)) &
                      (df['Current (mA)'] > df['Current (mA)'].quantile(0.01))]


# Create the scatter plots with 1-minute intervals
fig_temp_filtered = px.scatter(temperature_filtered, x='Time (1min interval)', y='Temperature (C)', title='Filtered Temperature over Time (1min intervals)')
fig_temp_filtered.update_yaxes(range=[0,30])

fig_current_filtered = px.scatter(current_filtered, x='Time (1min interval)', y='Current (mA)', title='Filtered Current over Time (1min intervals)')
fig_current_filtered.update_yaxes(range=[current_filtered['Current (mA)'].min() - 100, current_filtered['Current (mA)'].max() + 100])

fig_volt = px.scatter(df, x='Time (1min interval)', y='Bus Voltage (V)', title='Bus Voltage over Time (1min intervals)')
fig_volt.update_yaxes(range=[3.3,4.5])

# Save the plots as HTML files
fig_temp_filtered.write_html("./plots/temperature_plot_1min_filtered.html")
fig_current_filtered.write_html("./plots/current_plot_1min_filtered.html")
fig_volt.write_html("./plots/bus_voltage_plot_1min.html")

# Provide the paths for download
temp_plot_1min_filtered_path = "./plots/temperature_plot_1min_filtered.html"
current_plot_1min_filtered_path = "./plots/current_plot_1min_filtered.html"
volt_plot_1min_path = "./plots/bus_voltage_plot_1min.html"

temp_plot_1min_filtered_path, current_plot_1min_filtered_path, volt_plot_1min_path
