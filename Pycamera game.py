# coding: utf-8

import cv2 
import numpy as np
import random
import math
#Pygameは別途インストールが必要かも
import pygame.mixer

#距離
def get_distance(x1, y1, x2, y2):
    d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return d

#初期条件
arrayx=[400]
arrayy=[215]
arrayframe=[0]

cnt=0
framecnt=0
pygame.mixer.init()
pygame.init()
score=0
score1=0
vx=random.randint(5,20)
vy=random.randint(5,20)
red=random.randint(0,255)
green=random.randint(0,255)
blue=random.randint(0,255)

if __name__ == "__main__":
    # 内蔵カメラを起動
    cap = cv2.VideoCapture(0)

    #目についてのxmlファイル
    cascade_path = "/Users/cocoa/opencvEnv/lib/python3.7/site-packages/cv2/data/haarcascade_eye.xml"

    #手についてのxmlフアイル
    # cascade_path = "/Users/cocoa/Desktop/proj/Hand.Cascade.1.xml"

    # カスケード分類器の特徴量を取得する
    cascade = cv2.CascadeClassifier(cascade_path)
    
    # 顔に表示される枠の色を指定（白色）
    color = (255,255,255)

    while True:
        # 内蔵カメラから読み込んだキャプチャデータを取得
        ret, frame = cap.read()

        # 顔認識の実行
        facerect = cascade.detectMultiScale(frame, scaleFactor=1.2, minNeighbors=2, minSize=(10,10))

        #跳ね返りについての条件式

        if arrayy[cnt]>470:
            vy=-random.randint(5,20)
        
        if arrayy[cnt]<0:
            vy=random.randint(5,20)

        if arrayx[cnt]>830:
            vx=-random.randint(5,20)
        
        if arrayx[cnt]<0:
            vx=random.randint(5,20)

        #速度を足していき、x座標とy座標を更新
        arrayx[cnt]+=vx
        arrayy[cnt]+=vy

        cv2.circle(frame,(arrayx[cnt],arrayy[cnt]), 40, (blue,green,red), -1)

        #得点について表示
        cv2.putText(frame,"Score:"+str(score),(10,40), cv2.FONT_HERSHEY_SIMPLEX,1.5,(255,255,255),2,cv2.LINE_AA)
        if cnt>0:
            if score1==0:
                cv2.putText(frame,"+"+str(score1)+"  Miss",(10,80), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2,cv2.LINE_AA)
            if 0<score1<40:
                cv2.putText(frame,"+"+str(score1)+"  Good",(10,80), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2,cv2.LINE_AA)
            if 40<=score1<80:
                cv2.putText(frame,"+"+str(score1)+"  Great",(10,80), cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)
            if 80<=score1<=100:
                cv2.putText(frame,"+"+str(score1)+"  Excellent",(10,80), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv2.LINE_AA)
        framecnt+=1
        # cv2.putText(frame,str(framecnt),(10,400), cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),2,cv2.LINE_AA)

        if len(facerect) > 0:
            for rect in facerect:
                pressed_keys = pygame.key.get_pressed()

                # 顔が見つかったらcv2.rectangleで顔に白枠を表示する
                cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2]+rect[2:4]), color, thickness=2)

                # 四角形の真ん中の座標を計算
                xx=int((tuple(rect[0:2])[0]+tuple(rect[0:2]+rect[2:4])[0])/2)
                yy=int((tuple(rect[0:2])[1]+tuple(rect[0:2]+rect[2:4])[1])/2)

                #距離を測る
                d = get_distance(arrayx[cnt],arrayy[cnt], xx, yy)

                if pressed_keys[pygame.K_RIGHT]== 1:
                    print("Key Z is pressed")

                #目の位置と動いてる円の位置との距離が近かったら...
                if d < 50:
                    # 次の円の位置を決める
                    arrayframe.append(framecnt)
                    x=random.randint(0, 800)
                    y=random.randint(0, 430)
                    arrayx.append(x)
                    arrayy.append(y)
                    cnt+=1
                    #次の色を決めている
                    red=random.randint(0,255)
                    green=random.randint(0,255)
                    blue=random.randint(0,255)

                    #得点をきめている
                    score1=max(0,100-(arrayframe[cnt]-arrayframe[cnt-1]))
                    score+=score1

                    #音を鳴らす
                    if score1==0:
                        pygame.mixer.music.load("/Users/cocoa/Desktop/proj/music/manuke.mp3")
                    if 0<score1<40:
                        pygame.mixer.music.load("/Users/cocoa/Desktop/proj/music/crrect_answer1.mp3")
                    if 40<=score1<80:
                        pygame.mixer.music.load("/Users/cocoa/Desktop/proj/music/crrect_answer2.mp3")
                    if 80<=score1<=100:
                        pygame.mixer.music.load("/Users/cocoa/Desktop/proj/music/crrect_answer3.mp3")
                    
                    pygame.mixer.music.play(1)

        # 表示
        cv2.imshow("frame", frame)

        # qキーを押すとループ終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 内蔵カメラを終了
    cap.release()
    cv2.destroyAllWindows()
