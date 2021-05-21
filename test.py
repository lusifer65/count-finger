
import time
import mediapipe as mp
import cv2


def draw(img,cx,cy):
    cv2.circle(img,(cx,cy),5,(255,0,0),4)

def finger(image,flist):
    s=0
    if flist[8][2]<flist[6][2]:
        s+=1
    if flist[4][2]>flist[6][2] and flist[4][1]<flist[5][1]:
        s+=1
    if flist[12][2]<flist[11][2]:
        s+=1
    if flist[16][2]<flist[15][2]:
        s+=1
    if flist[20][2]<flist[19][2]:
        s+=1
    # time.sleep(0.05)
    # press(s)
    return s
mp_drawing = mp.solutions.drawing_utils
mp_hands=mp.solutions.hands
hands=mp_hands.Hands(max_num_hands=1,min_tracking_confidence=0.5)

cap=cv2.VideoCapture(0)
# cap = cv2.VideoCapture("https://192.168.153.26:8080/video")


ct=0
pt=0


while cap.isOpened():
    success, frame = cap.read()
    frame = cv2.resize(frame, (720, 600), interpolation=cv2.INTER_AREA)
    x1, y1, x2, y2 = 10, 100, 300, 400
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
    image = frame[y1:y2, x1:x2]


    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    whichHands=""
#left or right
    if results.multi_handedness:
        whichHands=list(str(results.multi_handedness[0]).split("\n"))[3].split(' "')[-1][:-1]

    coordinatae=[]
    if results.multi_hand_landmarks and whichHands=='Right':
      for hand_landmarks in results.multi_hand_landmarks:
        # print(hand_landmarks)
        for id , lm in enumerate(hand_landmarks.landmark):
            h,w,c=image.shape
            cx,cy=int(lm.x* w),int(lm.y * h)
            coordinatae.append([id, cx, cy,lm.z])
            if len(coordinatae)!=0:

                try:
                    s=finger(image,coordinatae)
                    cv2.putText(frame, str(s), (100, 100), cv2.FONT_HERSHEY_PLAIN,5, (0, 0, 0), 5)
                    draw(image,coordinatae[2][1],coordinatae[2][2])
                except Exception as e:
                    pass
            if id%4==0:
                draw(image,cx,cy)
            # coordinate of the hand for futher use
        # print(coordinatae)

        mp_drawing.draw_landmarks(image, hand_landmarks,mp_hands.HAND_CONNECTIONS)


    image = cv2.resize(image, (500, 600), interpolation=cv2.INTER_AREA)

#FPS
    ct=time.time()
    fps=int(1/(ct-pt))
    pt=ct

#text on image
    cv2.putText(frame,f"{fps}",(20,40),cv2.FONT_HERSHEY_PLAIN,3,(0,0,200),3)
    cv2.putText(frame,f"{whichHands}",(100,40),cv2.FONT_HERSHEY_PLAIN,3,(0,0,0),3)


    cv2.imshow('Hands', image)
    cv2.imshow('Main screen', frame)


    if cv2.waitKey(5) & 0xFF == 27:  #press Esc to exit
      break
cap.release()