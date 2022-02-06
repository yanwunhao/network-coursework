import matplotlib.pyplot as plt
import numpy as np

import socket1a as sk

x = []
run_state = []
red_state = []
green_state = []

i = 0

udp = sk.UDP_Recv("172.16.7.244", 44444)

buffer = []

plt.ion()
plt.figure(num=1, figsize=(6, 6))

while True:
    plt.clf()

    buffer = udp.recv()

    state_list = buffer.split(",")
    state_list = np.array(state_list, dtype=float)

    decoded_state_list = []

    for state in state_list:
        if state == 97.:
            decoded_state_list.append(0)
        else:
            decoded_state_list.append(1)

    x.append(i)
    i = i + 1

    run_state.append(decoded_state_list[0])
    red_state.append(decoded_state_list[1])
    green_state.append(decoded_state_list[2])

    plt.plot(x, run_state, color="black", markersize=6)
    plt.plot(x, red_state, color="red", markersize=6)
    plt.plot(x, green_state, color="green", markersize=6)
    plt.pause(0.01)





