import serial
import serial.tools.list_ports
import time
import cv2
import numpy as np
from PIL import Image
import matplotlib

ports = serial.tools.list_ports.comports()

i = 0

for p in ports:
    print(str(i) + ". " + str(p.device))
    i = i + 1
print(len(ports), 'ports found')

port = input("Select a port: ")
ser = serial.Serial(ports[int(port)].device, timeout=0.015)
print("Connected to: " + ser.name)
while True:
    data = ser.read(768 * 4)
    if (len(data) < 768 * 4):
        continue
    datafloat = np.frombuffer(data, np.float32)
    dataavg = np.average(datafloat)
    datamax = np.amax(datafloat)
    datamin = np.amin(datafloat)

    datafloat = datafloat - dataavg
    datascale = 255 / (datamax - datamin)
    datafloat = datafloat * datascale
    datafloat = datafloat + 127
    datafloat = np.clip(datafloat, 0, 255)

    dataint = datafloat.astype(np.uint8)
    dataint = np.reshape(dataint, (24,32))

    resized = cv2.resize(dataint, (320,240), interpolation=cv2.INTER_LINEAR)
    #pic.save('img.png')

    cv2.imshow("Cam",resized)
    cv2.waitKey(15)
    #resized.save('imgResized.png')
    #print("img saved")
