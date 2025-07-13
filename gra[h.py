import serial
import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
ser = serial.Serial('COM5', 9600)

def graph():
    temperature_data = []
    sound_data = []
    time_data = []
    fig, (ax1, ax2) = plt.subplots(2, 1)
    line1, = ax1.plot(time_data, temperature_data, label='Temperature')
    line2, = ax2.plot(time_data, sound_data, label='Sound Level')

    ax1.set_xlabel('Time')
    ax1.set_ylabel('Temperature')
    ax1.set_title('Temperature vs. Time')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Sound Level')
    ax2.set_title('Sound Level vs. Time')
    def update_plots(frame):
        now = datetime.datetime.now()
        time_data.append(now)

        line = ser.readline().decode().strip()
        data = line.split(', ')
        if len(data) == 2:
            temperature, sound_level = data
            temperature_data.append(float(temperature))
            sound_data.append(float(sound_level))
            line1.set_data(time_data, temperature_data)
            line2.set_data(time_data, sound_data)
        ax1.relim()
        ax1.autoscale_view()
        ax2.relim()
        ax2.autoscale_view()
    ani = FuncAnimation(fig, update_plots, interval=1000, cache_frame_data=False)
     # Update every 1 second (adjust as needed)

    # Start the animation
    plt.show()

    # Rest of your code remains unchanged...
graph()
