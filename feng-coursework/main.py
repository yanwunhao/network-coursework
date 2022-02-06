from asyncio import run
import time

import cv2
import numpy as np

import socket1a as sk
import keyin

from motor5a import Lmotor, Rmotor


udp = sk.UDP_Send("172.16.7.244", 44444)

motorL = Lmotor(17)
motorR = Rmotor(18)

run_state = 0
red_state = 0
green_state = 0

camera_dev = "/dev/video0"

cap = cv2.VideoCapture(camera_dev, cv2.CAP_V4L2)
if cap.isOpened():
	OUT_FILE = "test.mp4"

	cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
	cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("Y", "U", "Y", "V"))
	cap.set(cv2.CAP_PROP_BUFFERSIZE, 4)
	cap.set(cv2.CAP_PROP_FPS, 18)

	fmt = cv2.VideoWriter_fourcc(*"MPEG")
	size = (640, 360)
	vw = cv2.VideoWriter(OUT_FILE, fmt, 18, size)
	
	key = keyin.Keyboard()
	ch = "c"
	ch_im = cv2.waitKey(1)

	while not(ch=="q" or ch_im==ord("q") or ch=="Q" or ch_im==ord("Q")):
		ret, frame = cap.read()

		# frame_grayscale = np.dot(np.array(frame), rgb_weight) / 255.

		recognize_area = frame[170:190,310:330]

		sumOfLines = np.sum(recognize_area, axis=0, keepdims=True)
		sumOfColumns = np.sum(sumOfLines, axis=1)
		sumOfRa = sumOfColumns / 400.
		
		sumOfRa = sumOfRa[0]/255.
		
		print(sumOfRa)
		
		value_b = sumOfRa[0]
		value_g = sumOfRa[1]
		value_r = sumOfRa[2]

		if value_r > 0.4 and value_r - (value_b + value_g) > 0:
			print("stop")
			run_state = 0
			red_state = 1
			motorL.move(0)
			motorR.move(0)
		else:
			red_state = 0
		if value_g > 0.4 and value_g - (value_b + value_r) > 0:
			print("move")
			run_state = 1
			green_state = 1
			motorL.run(20)
			motorR.run(20)
		else:
			green_state = 0

		state_code = str(run_state) + str(red_state) + str(green_state)
		udp.send(state_code.encode())

		cv2.imshow("nmsl", recognize_area)
		ch_im = cv2.waitKey(1)
		ch = key.read()
		vw.write(frame)

	motorL.stop()
	motorR.stop()	
	vw.release()
	cap.release()		
else:
	print("camera not work")
