#This system detects total no. of vehicles at the time of Red signal. 
#Suppose, a signal glows for 60s in default condition for all situations.
#There are 30 vehicles to be crossed after signal turns green. For this, 60s is suitable time duration.
#Sometimes, 10-15 vehicles are to be crossed after signal turns green.
#In this case, vehicles will cross the road in 30-40s out of 60s.
#But signal will glow for that remaining time howerver there are no vehicles to cross.

#In real life, many times signal-extra-glow time duration is 10-15s.
#At the same time, the vehicles which are on Red signal side, they are waiting for Green signal.
#Many times, vehicles are ON that releases carbon emissions and increases AQI in that area.

import cv2
import numpy as np

cap = cv2.VideoCapture('assets/carsVideo.mp4')
min_width_react=80
min_height_react=80
count_line_position =550
algo=cv2.bgsegm.createBackgroundSubtractorMOG()

def center_handle(x,y,w,h):
    x1=int(w/2)
    y1=int(h/2)
    cx= x+x1
    cy = y+y1
    return cx, cy
detect = []
offset=6
counter=0
while True:
    ret,frame1=cap.read()
    grey=cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(grey,(3,3),5)
    img_sub=algo.apply(blur)
    dilat=cv2.dilate(img_sub,np.ones((5,5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    dilatada = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)
    dilatada = cv2.morphologyEx(dilatada, cv2.MORPH_CLOSE, kernel)
    counterSahpe,h = cv2.findContours(dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.line(frame1,(25,count_line_position),(1200,count_line_position),(255,127,0),3)

    for (i,c) in enumerate(counterSahpe):
        (x,y,w,h) = cv2.boundingRect(c)
        validate_counter = (w>= min_width_react) and (h >= min_height_react)
        if not validate_counter:
            continue

        cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.putText(frame1,"Vehicle Count: "+str(counter),(x,y-20),cv2.FONT_HERSHEY_TRIPLEX,1,(255,244,0),2)
        center = center_handle(x,y,w,h)
        detect.append(center)
        cv2.circle(frame1,center,4, (0,0,255),-1)

        for(x,y) in detect:
            if y<(count_line_position+offset) and y>(count_line_position-offset):
                counter+=1
            cv2.line(frame1,(25,count_line_position),(1200,count_line_position),(0,0,0),3)
            detect.remove((x,y))
            print("Count: ", counter)
    cv2.putText(frame1,"Count: "+str(counter),(450,70),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),5)
    # cv2.imshow('Detecter', dilatada)
    cv2.imshow('testVideos/carsVideo.mp4',frame1)
    if cv2.waitKey(1) == 13:
        break
cv2.destroyAllWindows()
cap.release()

#With help of this vehicle detection system, we can decrease the signal-extra-glow time
#Due to this, AQI in that area reduced at certain levels.
#In this way, we can control pollution in metro cities.