import matplotlib.pyplot as plt
import numpy as np

import socket1a as sk

x = [100]
y = [10]

i = 0

udp = sk.UDP_Recv("172.16.7.244", 44444)

buffer = [0]

angle = 0

current_direction = "m"
current_level = 0

plt.ion()
plt.figure(num=1, figsize=(6, 6))

while True:
    plt.clf()
    buffer = udp.recv()
    direction = buffer[0]
    level = float(buffer[1])

    if current_direction == direction:
        if current_level >= level:
            pass
        else:
            current_level = level
    else:
        if current_direction == "l":
            angle = angle - 16. * current_level
        elif current_level == "r":
            angle = angle + 16. * current_level

    if direction == "m":
        x.append(x[-1] + np.sin(angle * np.pi / 180))
        y.append(y[-1] + np.cos(angle * np.pi / 180))
        print(x, y)

    current_direction = direction
    current_level = level

    plt.plot(x, y, color="red", markersize=6)
    plt.pause(0.01)





