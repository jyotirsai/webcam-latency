from threading import Thread
import serial
import time
import time
import cv2
from numpy import mean, subtract

ser = serial.Serial('COM4', 9600)
LEDtimes = []

def LEDLoop():
    count = 0
    time.sleep(10)
    while True:
        ser.write(b'H')
        realOnTime = time.perf_counter()
        LEDtimes.append(realOnTime)
        time.sleep(1)
        ser.write(b'L')
        time.sleep(1)
        if count >= 99:
            return LEDtimes
        else:
            count = count+ 1


captureTimes = []

def webcam():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) # 640
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) # 480

    bAverage = []
    
    count = 0
    i = 0
    while True:
        
        ret,video = cap.read()
        grayVideo = cv2.cvtColor(video, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Nexigo Webcam', grayVideo)

        bAverage.append(grayVideo.mean())
        print(grayVideo.mean())
        if bAverage[i-1]:
            if ((bAverage[i] >= 30) and (bAverage[i-1] < 30)): 
                # LED on detected
                count = count + 1
                onTime = time.perf_counter()
                captureTimes.append(onTime)

        i = i + 1

        if cv2.waitKey(1) & 0xFF == 27:
            break

    print("mean: ", mean(bAverage))
    print("count: ", count)
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    a = Thread(target = LEDLoop)
    b = Thread(target = webcam)
    a.start()
    b.start()
    a.join()
    b.join()

    print("latency: ", round(mean(subtract(captureTimes, LEDtimes)),2)*1000, " ms")