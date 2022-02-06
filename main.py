import time

import cv2
import numpy as np

import socket1a as sk
import keyin

from motor5a import Lmotor, Rmotor


udp = sk.UDP_Send("172.16.7.244", 44444)

motorL = Lmotor(17)
motorR = Rmotor(18)

camera_dev = "/dev/video0"

rgb_weight = [0.114, 0.587, 0.229]

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

		frame_grayscale = np.dot(np.array(frame), rgb_weight) / 255.

		recognize_area = frame_grayscale[340:,210:430]

		compressed_ra =np.mean(recognize_area, axis=0)

		directions = []

		if len(compressed_ra) == 220:
			for i in range(11):
				directions.append(1. - np.mean(compressed_ra[i * 20 : (i + 1) * 20]))
		
		right_direction = np.argmax(directions)

		if right_direction == 5:
			udp.send("m0".encode())
			motorL.run(20)
			motorR.run(20)
		elif right_direction < 5:
			udp.send(("l"+str(abs(right_direction-5))).encode())
			motorL.run(-12)
			motorR.run(12)
		elif right_direction > 5:
			udp.send(("r"+str(abs(right_direction-5))).encode())
			motorL.run(12)
			motorR.run(-12)
		else:
			print("There is something wrong")
			break

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
