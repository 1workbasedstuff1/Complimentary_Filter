import matplotlib.pyplot as plt
import math
import time
import random
from matplotlib.animation import FuncAnimation

def Noisy_Gyro(t):
    return math.cos(t) + random.uniform(-0.1, 0.3)

def Noisy_accel(t):
    return math.sin(t) + random.uniform(-0.4,0.4)

# Initialize lists to store the time and signal data
time_data = []
gyro_data = []
integrated_signal = []  # List to store the integrated signal data
Noisy_accel_data = []
Complimentary = []

# Set up the figure and axes
fig, ax = plt.subplots()
ax.set_xlim(0, 10)  # Initial time window
ax.set_ylim(-5, 5)  # Range of signal values
line1, = ax.plot([], [], label='Noisy Gyro Signal')
line2, = ax.plot([], [], label='Integrated Signal')
line3, = ax.plot([], [], label='Noisy Accelerometer')
line4, = ax.plot([], [], label='Complimentary Estimate')
ax.legend()

# Initialize the lines and time
start_time = time.time()
last_time = start_time
last_integral = 0  # Initial value of the integral

def init():
    line1.set_data([], [])
    line2.set_data([], [])
    line3.set_data([], [])
    line4.set_data([], [])
    return line1, line2, line3, line4


current = 0
integral = 0 #Pure gyro estimation
estimate = 0

def update(frame, currenttime=[0]):
    
    global estimate
    global integral
    global current
    current = current + 1
    alpha = 0.95

    global last_time, last_integral, Noisy_accel_data
    global Complimentary
    current_time = time.time() - start_time

    print(current_time)

    gyro_value = Noisy_Gyro(current_time)
    
    accel_value = Noisy_accel(current_time)
    
    time_data.append(current_time)

    print(time_data[-1]) #current time
    gyro_data.append(gyro_value)

    Noisy_accel_data.append(accel_value)
    
    # Compute the integrated signal using the trapezoidal rule
    if current>2:
        integral += (time_data[-1] - time_data[-2])*(Noisy_Gyro(time_data[-1]))
        integrated_signal.append(integral)
    else:
        integrated_signal.append(0)

    if current>2:
        estimate = Complimentary[-1]
        estimateNew = ( alpha * (estimate + (time_data[-1] - time_data[-2])*(Noisy_Gyro(time_data[-1])))
                     + (1 - alpha)*Noisy_accel_data[-1])
        Complimentary.append(estimateNew)
    else:
        Complimentary.append(0) #this is first angle estimate
        #wed lie drone on table to begin with



    last_integral = integrated_signal[-1]
    last_time = current_time

    # Update data in the plot
    #line1.set_data(time_data, gyro_data)
    line2.set_data(time_data, integrated_signal)
    line3.set_data(time_data, Noisy_accel_data)
    line4.set_data(time_data, Complimentary)


    # Adjust the x-axis to show the last 10 seconds
    ax.set_xlim(max(0, current_time - 10), current_time)
    return line2, line3, line4

# Create the animation
ani = FuncAnimation(fig, update, init_func=init, interval=20)

plt.show()