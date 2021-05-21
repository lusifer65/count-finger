import cv2 as vision
import time
def fun(x):
    pass
vision.namedWindow("frame")

video=vision.VideoCapture(0)
#2 for mobile
while 1:
    c,frame1=video.read()
    c2,frame2=video.read()
    frame=vision.absdiff(frame1,frame2)
    frame = vision.cvtColor(frame,vision.COLOR_BGR2GRAY)
    val, frame = vision.threshold(frame, 25, 255, vision.THRESH_BINARY)

    counture, herrarchy = vision.findContours(frame, vision.RETR_TREE, vision.CHAIN_APPROX_SIMPLE)
    for con in counture:
        a=100
        vision.createTrackbar("contourArea","frame",100,5000,fun)
        x=vision.getTrackbarPos("contourArea","frame")
        # print(x)
        if vision.contourArea(con) > x:
            (x, y, w, h) = vision.boundingRect(con)
            vision.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 4)
            vision.putText(frame1,"motion dected",(100,80),vision.FONT_HERSHEY_SIMPLEX,1,(0,30,255),4)
    vision.putText(frame1,f"ContourArea: {x}",(50,50),vision.FONT_HERSHEY_SIMPLEX,1,(245,30,35),3)
    # frame1 = vision.resize(frame1, (1000, 700), interpolation=vision.INTER_AREA)
    vision.imshow("frame",frame1)
    # time.sleep(.8)
    if vision.waitKey(1)==ord('q'):
        break
vision.destroyWindow()
