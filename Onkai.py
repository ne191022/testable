# coding: utf-8
import random
import cv2 
#pygameは別途インストールしないといけないかも
import pygame.mixer

pygame.mixer.init()
pygame.init()

array=[]
for i in range(9):
    array.append(int(58.75*i))

if __name__ == "__main__":
    
    # 内蔵カメラを起動
    cap = cv2.VideoCapture(0)

    # OpenCVに用意されている顔認識するためのxmlファイルのパス
    cascade_path = "/Users/cocoa/opencvEnv/lib/python3.7/site-packages/cv2/data/haarcascade_eye.xml"
    # カスケード分類器の特徴量を取得する
    cascade = cv2.CascadeClassifier(cascade_path)
    
    # 顔に表示される枠の色を指定（白色）
    color = (255,255,255)

    while True:
        # 内蔵カメラから読み込んだキャプチャデータを取得
        ret, frame = cap.read()
    
        # 顔認識の実行
        facerect = cascade.detectMultiScale(frame, scaleFactor=1.2, minNeighbors=2, minSize=(10,10))

        for i in range(9):
            red=random.randint(0,255)
            green=random.randint(0,255)
            blue=random.randint(0,255)
            cv2.line(frame,(0,array[i]),(850,array[i]),(blue,green,red),5)

        # 顔が見つかったらcv2.rectangleで顔に白枠を表示する
        if len(facerect) > 0:
            for rect in facerect:
                cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2]+rect[2:4]), color, thickness=2)

                yy=int((tuple(rect[0:2])[1]+tuple(rect[0:2]+rect[2:4])[1])/2)

                for i in range(7):
                    if array[i]<=yy<=array[i+1]:
                        pygame.mixer.music.load("/Users/cocoa/Desktop/proj/music/piano"+str(i)+".mp3")
                
                pygame.mixer.music.play(1)
    
        # 表示
        cv2.imshow("frame", frame)

        # qキーを押すとループ終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 内蔵カメラを終了
    cap.release()
    cv2.destroyAllWindows()
